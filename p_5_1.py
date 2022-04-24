# Реализация алгоритма поиска ассоциативных правил (APRIORI)

from typing import Counter

# Метод инициализации списка всех элементов из датасета
def init_lst_from_ds(ds):
	t = []
	for lst in ds:
		t += lst
	return t

# Метод создания списка из ключей начального словаря для заданного уровня поддержки
def make_lst_from_init_dict(dict, SUPPORT):
	lst = []
	for key, value in dict.items():
		if value >= SUPPORT:
			lst.append(key)
	return lst

# Метод создания списка из ключей словаря для заданного уровня поддержки
def make_lst_from_dict(dict):
	lst = []
	for key in dict.keys():
		lst.append(key)
	return lst

# Метод проверки возможности составления нового набора из двух
def check_make_pair(text1, text2):
	common = [] # Список общих букв
	for i in range(len(text1)): # Фиксируем букву из первого набора
		for j in range(len(text2)): # Перебираем буквы из второго набора
			if text1[i] == text2[j]: # Если буквы совпадают
				common.append(text1[i]) # То добавляем букву в список общих
				break
	return len(common) == len(text1) - 1

# Метод составления нового набора из двух
def make_pair(text1, text2):
	return ''.join(sorted(list(set(text1) | set(text2))))

# Метод составления всевозможных комбинаций из списка
def make_comb(lst):
	t = []
	for i in range(len(lst)): # Фиксируем один элемент из списка
		for j in range(i, len(lst)): # Смотрим каждый другой элемент из списка
			if i != j and check_make_pair(lst[i], lst[j]): # Если из них можно составить пару
				t.append(make_pair(lst[i],lst[j])) # Составляем пару
	return t

# Метод создания нового набора для заданного уровня поддержки
def make_new_set(lst, ds, SUPPORT):
	result = []
	for elem in lst: # Для фиксированной комбинации
		test = list(elem) # Делаем из неё список из букв
		cnt = 0 # Инициализируем счетчик
		for i in range(len(ds)): # Проходим по строчкам датасета
			check = True # Инициализируем проверку принадлежности комбинации строке
			for t in test: # Для каждой буквы проверяем
				if t not in ds[i]: # Если хотя бы одной буквы нет в строке
					check = False # 
					break
			if check: cnt += 1 # Если все буквы комбинации были в строке, инкрементируем счетчик
		if cnt >= SUPPORT: # Если частота удовлетворяет уровню поддержки
			result.append([elem, cnt]) # Добавляем комбинацию и частоту
	return dict(result)

# Словарь продуктов
words = {
	'a': 'йогурт',
	'b': 'сыр',
	'c': 'сметана',
	'd': 'кофе',
	'e': 'хлеб',
	'f': 'молоко',
	'g': 'носки',
	'h': 'апельсины',
	'i': 'растительное масло',
	'j': 'булка',
	'k': 'гречка',
	'l': 'кефир',
	'm': 'чай',
	'n': 'конфеты',
	'o': 'печенье',
	'p': 'сок',
	'q': 'колбаса',
	'r': 'картофель'
}

# Датасет продуктов
ds = [
	['a', 'b', 'c', 'd', 'e', 'f', 'g'],
	['h', 'a', 'i', 'j', 'l'],
	['j', 'f', 'k', 'b', 'e'],
	['m', 'h', 'n', 'o', 'p'],
	['e', 'c', 'f', 'q'],
	['r', 'e', 'f', 'q', 'p'],
	['e', 'f', 'd']
]

# Уровень поддержки
SUPPORT = 2

print('Частота одноэлементных товаров:')
c = Counter(init_lst_from_ds(ds))
print(c)
print('Товары, которые мы берём в рассмотрение')
lst = make_lst_from_init_dict(c, SUPPORT)
print(lst)

cnt = 2
while True:
	t = lst
	print(f'Товары, которые мы берём в рассмотрение на шаге {cnt}')
	lst = make_new_set(make_comb(lst), ds, SUPPORT)
	print(lst)
	if len(lst) == 0:
		print('Ответ:', *t)
		print('Наборы:')
		for i in range(len(t)):
			print(f'{i+1} вариант:', end=' ')
			for el in t[i]:
				print(words[el], end=', ')
			print()
		break
	lst = make_lst_from_dict(lst)
	cnt += 1
