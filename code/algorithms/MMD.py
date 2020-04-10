'''
this is MMD (Minimum Manhattan Distance) algorithm of Chiu et.al
REFERENCES:
	Chiu, W., Yen, G.G., Juan, T.: Minimum manhattan distance approach to multiple
criteria decision making in multiobjective optimization problems. IEEE Trans.
Evolutionary Computation 20(6), 972-985 (2016)
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
			mat[:, i] = (data[:, i] - Min) / (Max - Min)  # Equ (14)
		else:
			mat[:, i] = Min

	c = np.zeros(num)
	# calculate manhattan distance (MMD) to a hyperplane formed by normalized ideal vector.
	for i in range(num):
		c[i] = sum(mat[i, :])

	SK = np.argsort(c)
	SK = list(SK[:K])
	knee_points = data[SK, :]
	return knee_points

if __name__ == '__main__':
	points = np.loadtxt(sys.path[0]+'/data/points1/PMOP1_M2_A2.out')
	main_function(points, 1)