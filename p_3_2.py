# Будет доработано
# Реализация алгоритма K-Means

import numpy as np
import matplotlib.pyplot as plt

Points = np.array([
	[185,72],
	[170,56],
	[168,60],
	[179,68],
	[182,72],
	[188,77]
])

colors = {
	0: '#FF0000', # Красный
	1: '#00FF00', # Зеленый
	2: '#0000FF', # Синий
}

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

cnt = 1
while True:
	if cnt == 1:
		print(f'Шаг {cnt}:')
		# Инициализируем центроиды
		centres = np.array([Points[0], Points[1]])
		print('Инициализированные центроиды:')
		print(*centres)
		kl = fill_clusters(Points, centres)
		centres = make_new_centres(kl)
		check_centres = centres
		print('Кластеры:',)
		for elem in kl: print(*elem)
		print('Центроиды:', *centres)
	else:
		print(f'---\nШаг {cnt}:')
		kl = fill_clusters(Points, centres)
		centres = make_new_centres(kl)
		print('Кластеры:',)
		for elem in kl: print(*elem)
		print('Центроиды:', *centres)
		if np.array_equal(check_centres,centres):
			tcnt = 0
			x = []
			y = []
			p = []
			for i in range(len(kl)):
				for j in range(len(kl[i])):
					x.append(kl[i][j][0])
					y.append(kl[i][j][1])
					p.append(i)
			print(x)
			print(y)
			print(p)
			
			for i in range(len(p)):
				plt.scatter(x[i], y[i], c=colors[p[i]])
			plt.show()
			break
	cnt+=1
