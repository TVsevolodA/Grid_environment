import math
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


def generate_data_for_sending(sending_data, files, step):
    list_content_file = list()
    for f in files:
        with open(f, 'rb') as file:
            file_content = file.read()
            list_content_file.append(list(file_content))
    sending_data += f'|{step}'
    data_to_send = {
        'filename': files,
        'content': list_content_file,
        'sender_address': f'http://{HOST}:{PORT}',
        'arguments': sending_data
    }
    return data_to_send


def split_task(data, files, task_size):
    number_cells = task_size ** 2
    average_reception_time = 0.5  # сек. Время передачи подзадачи
    average_calculation_time = 3.5  # сек. Время вычисления
    average_dispatch_time = 1  # сек. Время отправки ответа

    scope_subtask = (  # Объем подзадачи (кол-во ячеек)
            number_cells
            /
            (average_reception_time + average_calculation_time + average_dispatch_time))
    scope_subtask = int(scope_subtask + 0.5)  # Округление до целого
    list_subtask = []
    curr_row = 0
    curr_cell = 0
    step = 0

    while number_cells > 0:
        last_row = curr_row
        curr_row = math.ceil((curr_cell + scope_subtask) / task_size)
        last_col = curr_cell
        curr_cell += scope_subtask - 1
        number_cells -= scope_subtask
        if number_cells < task_size:
            curr_cell += number_cells
            number_cells -= scope_subtask
        list_subtask.append(f'{last_row}-{curr_row};{last_col}-{curr_cell}')
        step += 1
        curr_cell += 1
        subtask_parameters = generate_data_for_sending(data, files, list_subtask[-1])
        requests.get('http://localhost:5001/newTask', json=subtask_parameters)
    return list_subtask


@app.route('/assign_task', methods=['GET'])
def assign_task():
    output_data.clear()
    INPUT_DATA = request.json['data']
    FILES = request.json['name_files']
    SCOPE_TASK = int(INPUT_DATA.split('|')[0])
    subtasks = split_task(INPUT_DATA, FILES, SCOPE_TASK)

    while True:
        if len(subtasks) == len(output_data):
            return output_data


@app.route('/get_solution_subtask', methods=['GET'])
def get_solution_subtask():
    output_data.append(request.json)
    return jsonify({'status': 'Решение подзадачи получено!'})


input_data = str()
output_data = list()
HOST = 'localhost'
PORT = 5000
app.run(host=HOST, port=PORT)

# import ast
# import datetime
# import threading
# from queue import Queue
#
# from flask import Flask, request
# from flask_socketio import SocketIO, emit
# from subtask_generator import split_task
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
#
#
# def check_status_nodes():
#     for node, time_notification in computing_nodes.items():
#         diff = datetime.datetime.now() - time_notification
#         if not (subtasks_in_work.get(node) is None):
#             step_node = subtasks_in_work.get(node)
#             if diff.total_seconds() > 5:
#                 del computing_nodes[node]
#                 q_subtasks.put(step_node)
#                 del subtasks_in_work[node]
#         else:
#             if diff.total_seconds() > 5:
#                 del computing_nodes[node]
#
#
# def set_interval(func, sec):
#     def func_wrapper():
#         set_interval(func, sec)
#         func()
#
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#
#
# def check_combinations(NEW_NUMBER_QUEENS, COMBINATIONS):
#     global maximum_number_queens, decisions
#     if NEW_NUMBER_QUEENS > maximum_number_queens:
#         maximum_number_queens = NEW_NUMBER_QUEENS
#         decisions.clear()
#         decisions.extend(COMBINATIONS)
#     elif NEW_NUMBER_QUEENS == maximum_number_queens:
#         decisions.extend(COMBINATIONS)
#
#
# @app.route('/assign_task', methods=['POST'])
# def assign_task():
#     global dimension, positions, q_subtasks, maximum_number_queens, decisions, completed_subtasks
#     maximum_number_queens = 0
#     decisions = []
#
#     INPUT_DATA = request.json
#     dimension = INPUT_DATA['dimension']
#     positions = INPUT_DATA['positions']
#     SUBTASKS = split_task(dimension)
#
#     maximum_number_queens = len(ast.literal_eval(positions))
#
#     # Создаем очередь подзадач
#     for subtask in SUBTASKS:
#         q_subtasks.put(subtask)
#
#     # emit('echo', {'echo': 'Пришла новая задача'}, namespace='', broadcast=True)
#     for node in computing_nodes.keys():
#         if subtasks_in_work.get(node) is None:
#             submit_task(node)
#
#     # Возвращаем ответ пользователю
#     while True:
#         if q_subtasks.qsize() == 0 and len(subtasks_in_work) == 0:
#             uniq_pos = list(set(decisions))
#             result = {'quantity': maximum_number_queens, 'positions': uniq_pos}
#             return result
#
#
# @socketio.on('connect')
# def connect():
#     new_node = request.sid
#     if not (new_node in computing_nodes.keys()):
#         computing_nodes[new_node] = datetime.datetime.now()
#     print(f'Клиент {new_node} подключился к серверу')
#
#
# @socketio.on('submit_task')
# def submit_task(id_node=None):
#     if not q_subtasks.empty():
#         # Назначаем подзадачу узлу
#         node = request.sid if id_node is None else id_node
#         if not (node in computing_nodes.keys()):
#             connect()
#         step = q_subtasks.get()
#         print(f'Узел {node} получил задачу {step}')
#         subtasks_in_work[node] = {'status': 'works', 'step': step}
#         computing_nodes[node] = datetime.datetime.now()
#         with open('kernel.py', 'rb') as file:
#             file_content = file.read()
#             data_send = {
#                 'filename': 'kernel.py',
#                 'content': list(file_content),
#                 'arguments': {'dimension': dimension, 'positions': positions, 'step': step}
#             }
#             emit('my_message', data_send, namespace='', room=node)
#
#
# @socketio.on('subtask_completed')
# def subtask_completed(data):
#     # Получаем данне
#     node = request.sid
#     number_solutions = data['number_solutions']
#     combinations = data['combinations']
#
#     # Добавить решение
#     check_combinations(number_solutions, combinations)
#
#     # Обновить данные
#     computing_nodes[node] = datetime.datetime.now()
#     completed_subtasks[subtasks_in_work[node]['step']] = combinations
#     del subtasks_in_work[node]
#
#     # Отправляем новую подзадачу
#     submit_task()
#
#
# @socketio.on('getting_status')
# def getting_status():
#     node = request.sid
#     computing_nodes[node] = datetime.datetime.now()
#
#
# @socketio.on('disconnect')
# def disconnect():
#     node = request.sid
#     if not (subtasks_in_work.get(node) is None):
#         step_node = subtasks_in_work[node]['step']
#         if not (step_node in completed_subtasks.keys()):
#             q_subtasks.put(step_node)
#         del subtasks_in_work[node]
#     del computing_nodes[node]
#     print(f'Клиент {node} отключился от сервера')
#
#
# """
# Входные данные
# """
# dimension = 0  # Размер поля
# positions = []  # Начальные позиции ферзей
#
# """
# Данные для выполнения работы
# """
# computing_nodes = {}  # Словарь нод: {node: время_последнего_уведомления}
# q_subtasks = Queue()  # Подзадачи: '0-0;0-2', ...
# subtasks_in_work = {}  # Подзадачи в работе: {node: {'status': 'works', 'step': '0-0;0-2'}, ...}
# completed_subtasks = {}  # Выполненные подзадачи: {'0-0;0-2': [[0,0],...]}
#
# """
# Выходные данные
# """
# maximum_number_queens = 0
# decisions = []
#
# threading.Thread(target=set_interval, args=(check_status_nodes, 5)).start()
# socketio.run(app, host='localhost', port=5000, allow_unsafe_werkzeug=True)
