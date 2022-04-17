# Реализация генетического алгоритма

import numpy as np
import random as r
from itertools import combinations

# Диофантово уравнение
def f(a, b, c, d):
	return abs(a + 2*b + 3*c + 4*d - 30)

# Метод составления пар по индексам 
def make_pairs(mins):
	pairs = list(set([i for i in combinations(mins, 2) if i[0]!=i[1]])) # Комбинации из 3 элементов с учетом порядка
	new_pairs = [[i[0],i[1]] for i in pairs] # Комбинации в списке
	for el in list(set([0,1,2,3,4])-set(mins)): # Добавляем остальные индексы
		new_pairs.append([mins[0], el]) # Добавляем индекс к самому сильному
	for i in range(len(new_pairs)): # Проходим по всем парам
		if r.randint(0,1): new_pairs[i] = new_pairs[i][::-1] # Меняем порядок пары
	r.shuffle(new_pairs) # Меняем случайно порядок пар
	return new_pairs # Возвращаем список 5 пар

# Метод определения нужного индекса для скрещивания генов родителей на конкретном шаге
def circle_of_inds(index, number_of_elements, number_of_lists):
	cnt = 1
	lst = []
	for _ in range(number_of_lists): # Проходим по количеству списков
		if cnt < number_of_elements: lst.append(cnt) # Если счетчик меньше количества списков, то добавляем его в список
		else: 
			cnt = 1 # Иначе ставим стартовое значение счетчику 
			lst.append(cnt) # И добавляем его в список
		cnt += 1
	return lst[index] # Возвращаем нужный индекс на конкретном шаге

# Генерируем новое поколение
def generate_mutation(matrix, pairs):
	new_matrix = []
	for i in range(len(pairs)): # Проходимся по парам
		k = circle_of_inds(i, len(matrix[0]), len(matrix)) # Находим нужный индекс для среза
		new_matrix.append(np.concatenate((matrix[pairs[i][0]][:k],matrix[pairs[i][1]][k:]))) # Скрещиваем родителей и получаем нового потомка
	return np.array(new_matrix) # Возвращаем новое поколение

# Метод нахождения коэффициентов выживаемости для таблицы
def make_surv(matrix):
	surv = [[f(a,b,c,d)] for a,b,c,d in matrix]
	for i in range(len(matrix)):
		surv[i].append(i)
	return surv

# Метод нахождения тройки минимальных коэффициентов выживаемости
def make_mins(surv):
	mins = []
	for lst in sorted(surv, key=lambda el: el[0])[:3]:
		mins.append(lst[-1])
	return mins

# Метод изменения максимального коэффициента выживаемости
def change_max_descendant(new_matrix):
	surv = make_surv(new_matrix) # Находим коэффициенты выживаемости
	mx = sorted(surv, key=lambda el: el[0], reverse=True)[0] # Находим максимальный коэффициент
	while True:
		a, b, c, d = r.randint(1, 29), r.randint(1, 29), r.randint(1, 29), r.randint(1, 29) # Генерируем 4 гена
		if f(a, b, c, d) < mx[0]: # Если коэффициент стал меньше максимального
			new_matrix[mx[1]] = [a, b, c, d] # То перезаписываем гены
			break
	return new_matrix # Возвращаем матрицу генов

# По приципу Дарвина создаём новую пятерку из таблиц
def generate_matrix_min(matrix, new_matrix):
	m1 = make_surv(matrix) # Коэффициенты выживаемости родителей
	m2 = make_surv(new_matrix) # Коэффициенты выживаемости потомков
	for i in range(len(m1)): m1[i].append(0) # Добавляем номер для первой таблицы
	for i in range(len(m2)): m2[i].append(1) # Добавляем номер для второй таблицы
	m = sorted(m1 + m2, key=lambda el: el[0])[:5] # Берём пятёрку минимальных коэффициентов из двух списков
	matrix_min = []
	for i in range(5): # Заполняем результирующую таблицу
		if m[i][-1] == 0: matrix_min.append(matrix[m[i][1]]) # Добавляем список из первой матрицы
		else: matrix_min.append(new_matrix[m[i][1]]) # Добавляем список из второй матрицы
	return np.array(matrix_min)

# Инициализиурем поколение хромосом
matrix = np.array([[r.randint(1,29) for _ in range(4)] for _ in range(5)])

# Поколение хромосом, взятое из примера на ПЗ
#matrix = np.array([
#	[1,28,15,3],
#	[14,9,2,4],
#	[13,5,7,3],
#	[23,8,16,19],
#	[9,13,5,2]
#])

print('Инициализировали поколение хромосом:')
print(matrix)
print('Составляем списки коэффициентов выживаемости и лучшую тройку:')
surv = make_surv(matrix)
mins = make_mins(surv)
print(surv, mins)
print('Составляем 5 пар для получения потомков:')
print(make_pairs(mins))
print('Составляем таблицу потомков:')
new_matrix = generate_mutation(matrix,make_pairs(mins))
print(new_matrix)
print('Меняем одного потомка с максимальным коэффициентом, получим измененную таблицу потомков:')
new_matrix = change_max_descendant(new_matrix)
print(new_matrix)
print('По принципу Дарвина составляем новую таблицу сильнейших:')
result_matrix = generate_matrix_min(matrix,new_matrix)
print(result_matrix)
print('Проверяем коэффициенты выживаемости для таблицы сильнейших:')
surv = make_surv(result_matrix)
mins = make_mins(surv)
print(surv,mins)
print('Далее алгоритм идет по тому же пути, пока хотя бы один коэффициент выживаемости не будет равен 0')

cnt = 2

while True:
	print(f'Шаг {cnt}:')
	matrix = result_matrix
	surv = make_surv(matrix)
	mins = make_mins(surv)
	new_matrix = generate_mutation(matrix,make_pairs(mins))
	new_matrix = change_max_descendant(new_matrix)
	result_matrix = generate_matrix_min(matrix,new_matrix)
	surv = make_surv(result_matrix)
	mins = make_mins(surv)
	print(surv)
	if surv[0][0] == 0:
		print(result_matrix)
		break
	cnt += 1
