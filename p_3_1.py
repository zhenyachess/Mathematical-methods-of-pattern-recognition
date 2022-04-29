# Реализация иерархической агломеративной кластеризации

from cmath import inf
import numpy as np

Points = np.array([
	[0.4,0.53],
	[0.22,0.38],
	[0.35,0.32],
	[0.26,0.19],
	[0.08,0.41],
	[0.45,0.3]
])

def dist_p(p1, p2):
	return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def init_klusters(Points):
	return [[i] for i in range(len(Points))]

def generate_matrix_dist(Points):
	matrix_dist = np.zeros([len(Points), len(Points)])
	for i in range(len(Points)):
		for j in range(len(Points)):
			if i != j: matrix_dist[i][j] = dist_p(Points[i],Points[j])
	return np.round(matrix_dist,3)

def find_min_inds_and_clusters(matrix_dist, klusters):
	_min = inf
	inds = [0, 0]
	for i in range(len(matrix_dist)):
		for j in range(i):
			if matrix_dist[i][j] < _min:
				_min = matrix_dist[i][j]
				inds = [i, j]
	inds = sorted(inds)
	kl = []
	for i in range(len(klusters)):
		if i == inds[0]:
			if len(klusters[inds[0]]) == 1:
				kl.append([klusters[inds[0]] + klusters[inds[1]]])
			else:
				kl.append([klusters[inds[0]],[klusters[inds[1]]]])
		elif i != inds[1]:
			kl.append(klusters[i])
	print(f'min is matrix_dist[{inds[1]}][{inds[0]}] = {_min}')
	print(f'connect {klusters[inds[0]]} and {klusters[inds[1]]}')
	return inds, kl

def update_matrix_dist(matrix_dist, min_inds):
	t1 = min_inds[0]
	t2 = min_inds[1]
	for j in range(len(matrix_dist)):
		if j != t1 and j != t2:
			if matrix_dist[t1][j] > matrix_dist[t2][j]:
				matrix_dist[t1][j] = matrix_dist[t2][j] 
	matrix_dist = np.delete(matrix_dist,(t2), axis = 1)
	matrix_dist = np.delete(matrix_dist,(t2), axis = 0)
	return matrix_dist

kl = init_klusters(Points)
matrix_dist = generate_matrix_dist(Points)
print(matrix_dist)
inds, kl = find_min_inds_and_clusters(matrix_dist, kl)
print(kl)

cnt = 2
while len(matrix_dist)>2:
	print(f'\nШаг {cnt}:\n')
	matrix_dist = update_matrix_dist(matrix_dist, inds)
	print(matrix_dist)
	inds, kl = find_min_inds_and_clusters(matrix_dist, kl)
	print(inds)
	print(kl)
	cnt+=1
