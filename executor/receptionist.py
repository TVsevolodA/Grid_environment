import threading
from time import sleep
from dotenv import load_dotenv
import os
import socketio
import subprocess

sio = socketio.Client()


def sending_status():
    while True:
        sio.emit('getting_status')
        sleep(5)


@sio.event
def connect():
    print('Установлено новое соединение')


@sio.event
def my_message(data):
    filename = data['filename']
    file_content = data['content']
    for ind, f in enumerate(filename):
        with open(f, 'wb') as file:
            file.write(bytes(file_content[ind]))
    # file_content = bytes(data['content'])
    # with open(f'{filename}', 'wb') as file:
    #     file.write(file_content)
    arguments = data['arguments'].split('|')
    print('Файл успешно передан!')
    args = ['python', filename[0]]
    """
    Для запуска любых файлов:
    import os
    give_permission = f'chmod +x {filename[0]}'
    os.system(give_permission)
    args = [filename[0]]
    """
    for arg in arguments:
        args.append(arg)
    args = tuple(args)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    str_output = popen.stdout.read().decode()
    str_data_list = str_output.splitlines()
    sio.emit('subtask_completed', {'recipient_address': data['sender_address'], 'output': str_data_list})


@sio.event
def disconnect():
    print('Отключились от сервера')


load_dotenv()
BROKER = os.getenv('BROKER')
sio.connect(BROKER)
availability = threading.Thread(target=sending_status)
availability.start()
sio.emit('submit_task')
sio.wait()
