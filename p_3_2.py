# Реализация алгоритма K-Means
# Программа работает корректно, если количество кластеров от 1 до 9 и количество кластеров не превышает количества точек

import numpy as np
import random as r
import matplotlib.pyplot as plt

colors = {
	0: '#FF0000', # Красный
	1: '#FF6600', # Оранжевый
	2: '#FFFF00', # Желтый
	3: '#00FF00', # Зеленый
	4: '#80A6FF', # Голубой
	5: '#0000FF', # Синий
	6: '#8000FF', # Фиолетовый
	7: '#FFFFFF', # Белый
	8: '#000000', # Черный
}

# Метод генерации точек по количеству и границам координат
def generate_points(number_of_points, left_border, right_border):
	Points = []
	for _ in range(number_of_points):
		Points.append([r.randint(left_border, right_border), r.randint(left_border, right_border)])
	return np.array(Points)

# Метод инициализации центров из точек
def init_centres(Points, number_of_centres):
	inds = set()
	while len(inds) < number_of_centres:
		inds.add(r.randint(0,len(Points)-1))
	return np.array([Points[index] for index in inds])

# Метод нахождения расстояния между двумя точками
def dist_p(p1, p2):
	return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

# Метод заполнения кластеров 
def fill_clusters(Points, centres):
	klusters = [[] for _ in range(len(centres))] # Инициализируем список кластеров
	for i in range(len(Points)): # Проходим по точкам
		mn = [] # Инициализируем список расстояний от одной точки до центроид
		for j in range(len(centres)): # Проходим по центрам
			mn.append([dist_p(centres[j],Points[i]),Points[i],j]) # Записываем в список расстояние, точку, индекс центроиды
		kl = sorted(mn, key=lambda el: el[0]) # Сортируем список расстояний по расстояниям
		klusters[kl[0][-1]].append(kl[0][1]) # Добавляем в нужный кластер точку
	return klusters

# Метод нахождения новых центроид
def make_new_centres(kl):
	centres = [] # Инициализируем список центроид
	for i in range(len(kl)): # Проходимся по кластерам
		centres.append(sum(kl[i])/len(kl[i])) # Добавляем новые центры кластеров
	return np.array(centres)

# Точки, взятые с ПЗ
#Points = np.array([
#	[185,72],
#	[170,56],
#	[168,60],
#	[179,68],
#	[182,72],
#	[188,77]
#])

Points = generate_points(50, 150, 190)
centres = init_centres(Points, 3)
print('Инициализированные центроиды:')
print(*centres)

cnt = 1
while True:
	print(f'Шаг {cnt}:')
	check_centres = centres
	kl = fill_clusters(Points, centres)
	centres = make_new_centres(kl)
	print('Новые центроиды:', *centres)
	if np.array_equal(check_centres,centres):
		x, y, p = [], [], []
		
		for i in range(len(kl)):
			for j in range(len(kl[i])):
				x.append(kl[i][j][0])
				y.append(kl[i][j][1])
				p.append(i)

		fig = plt.figure()
		fig.patch.set_facecolor('blue')
		fig.patch.set_alpha(0.6)
		ax = fig.add_subplot(111)
		ax.patch.set_facecolor('#7673D9')
		
		for i in range(len(p)):
			plt.scatter(x[i], y[i], c=colors[p[i]])
		
		plt.show()
		break
	cnt+=1
