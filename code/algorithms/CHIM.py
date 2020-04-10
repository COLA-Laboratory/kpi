'''
this is the convex hull of individual minima (CHIM) algorithm of Das et al.
REFERENCES:
Das, I.: On characterizing the "knee" of the Pareto curve based on
normalboundary intersection. Structural Optimization 18(2-3), 107-115 (1999)
'''

import numpy as np

class solution(object):
	def __init__(self, m):
		self.index = -1
		self.objectives = np.zeros([1, m])
		self.flag = 1

def main_function(data, K):
	num = len(data)
	dim = len(data[0, :])

	# Normalize f by each objective to get f_norm
	mat = np.zeros([num, dim])
	for i in range(dim):
		Min = min(data[:, i])
		Max = max(data[:, i])
		if Max != Min:
			mat[:, i] = (data[:, i] - Min) / (Max - Min)  # Equ 14
		else:
			mat[:, i] = Min

	# Calculate hyper_plane with its normal vector
	mat2 = np.eye(dim)
	mat3 = np.dot(np.mat(mat2).I, np.ones([dim, 1]))

	# Calculate d from each solution to hyperplane
	d = np.zeros(num)
	c = np.dot(mat2[0, :], mat3)
	L_mat3 = np.linalg.norm(mat3.T)
	for i in range(num):
		d[i] = -(np.dot((mat[i, :]), mat3) - c) / L_mat3

	SK = np.argsort(-d)
	SK = list(SK[:K])
	knee_points = data[SK, :]
	return knee_points

if __name__ == '__main__':
	points = np.loadtxt(sys.path[0]+'/data/points1/PMOP1_M2_A2.out')
	main_function(points, 1)

