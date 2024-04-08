import math


def fewer_location(num_cells, N):
    return math.factorial(num_cells) / (math.factorial(N) * math.factorial(num_cells - N))


DIMENSION = 4
number_cells = DIMENSION ** 2


tmp_num_cells = number_cells
list_permutations = []
iter = 1
while tmp_num_cells >= DIMENSION:
    list_permutations.append(fewer_location(tmp_num_cells, DIMENSION))
    tmp_num_cells -= 1
# average_reception_time = 0.5  # сек. Время передачи подзадачи
# average_calculation_time = math.e * math.factorial(DIMENSION)  # сек. Время вычисления
# average_dispatch_time = 1  # сек. Время отправки ответа
#
# scope_subtask = (  # Объем подзадачи (кол-во ячеек)
#         number_cells
#         /
#         (average_reception_time + average_calculation_time + average_dispatch_time))
# scope_subtask = int(scope_subtask + 1)  # Округление до целого

list_subtask = []
curr_row = 0
curr_cell = 0
step = 0

while number_cells > 0:
    scope_subtask = 1
    if step > 0:
        last_count_combinations = list_permutations[0]
        current_count_combinations = 0
        while current_count_combinations < last_count_combinations and iter < len(list_permutations):
            current_count_combinations += list_permutations[iter]
            iter += 1
            if iter == len(list_permutations):
                iter += DIMENSION ** 2 - iter
        scope_subtask = iter - step
        step = iter
    last_row = curr_row
    curr_row = (curr_cell + scope_subtask) // DIMENSION
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
