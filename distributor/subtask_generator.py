import math


# def split_task(DIMENSION):
DIMENSION = 4
number_cells = DIMENSION ** 2
average_reception_time = 0.5  # сек. Время передачи подзадачи
average_calculation_time = math.e ** (DIMENSION**0.5)  # сек. Время вычисления
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
    curr_row = (curr_cell + scope_subtask) // DIMENSION#math.ceil((curr_cell + scope_subtask) / DIMENSION)
    last_col = curr_cell
    curr_cell += scope_subtask - 1
    number_cells -= scope_subtask
    if number_cells < DIMENSION:
        curr_cell += number_cells
        number_cells -= scope_subtask
    list_subtask.append(f'{last_row}-{curr_row};{last_col}-{curr_cell}')
    step += 1
    curr_cell += 1

print(len(list_subtask))
print(list_subtask)
    # return list_subtask
