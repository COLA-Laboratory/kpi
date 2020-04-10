'''
this is the RA (reflex angle) algorithm of Branke et al
REFERENCES:
	Branke, J., Deb, K., Dierolf, H., Osswald, M.: Finding knees in multi-objective
optimization. In: PPSN’04: Proc. of the 8th International Conference on Parallel
Problem Solving from Nature. pp. 722-731 (2004)
'''

import numpy as np
import math
import copy

# the angle between [x_(i-1),x_i] and [x_i,x_(i+1)]
class solution(object):
	def __init__(self, m):
		self.index = -1
		self.objectives = np.zeros([1, m])
		self.angle = 0
		self.vector1 = []
		self.vector2 = []

# the angle of two vectors
def angle(v1, v2):
	dx1 = v1[2] - v1[0]
	dy1 = v1[3] - v1[1]
	dx2 = v2[2] - v2[0]
	dy2 = v2[3] - v2[1]
	angle1 = math.atan2(dy1, dx1)
	angle1 = int(angle1 * 180/math.pi)
	angle2 = math.atan2(dy2, dx2)
	angle2 = int(angle2 * 180/math.pi)

	if angle1*angle2 >= 0:
		included_angle = abs(angle1-angle2)
	else:
		included_angle = abs(angle1) + abs(angle2)
	included_angle = 360 - included_angle
	return included_angle

def main_function(data, true_knee, K):
	data = copy.copy(data)
	data_arg = data[np.lexsort(data.T)]
	num = len(data_arg)
	dim = len(data_arg[0, :])
	P = [solution(dim) for i in range(num)]

	for i in range(num):
		P[i].index = i
		P[i].objectives = data_arg[i, :]

	for i in range(num):
		#  If no neighbor to the left (right) is found, a vertical (horizontal) line is used to
		#  calculate the angle
		if i == 0:
			P[i].vector1.extend(P[i].objectives.tolist())
			P[i].vector1.append(P[i].objectives[0])
			P[i].vector1.append(P[i].objectives[1] +1)

			P[i].vector2.extend(P[i].objectives.tolist())
			P[i].vector2.extend(P[i+1].objectives.tolist())
			P[i].angle = angle(P[i].vector1, P[i].vector2)
		elif i == num-1:
			P[i].vector1.extend(P[i-1].objectives.tolist())
			P[i].vector1.extend(P[i].objectives.tolist())

			P[i].vector2.extend(P[i].objectives.tolist())
			P[i].vector2.append(P[i].objectives[0]+1)
			P[i].vector2.append(P[i].objectives[1])
			P[i].angle = angle(P[i].vector1, P[i].vector2)
			pass
		else:
			P[i].vector1.extend(P[i].objectives.tolist())
			P[i].vector1.extend(P[i-1].objectives.tolist())

			P[i].vector2.extend(P[i].objectives.tolist())
			P[i].vector2.extend(P[i+1].objectives.tolist())

			P[i].angle = angle(P[i].vector1, P[i].vector2)

	Angle = np.zeros(num)
	for i in range(num):
		Angle[i] = P[i].angle

	SK = np.argsort( -Angle )  # sort
	SK = list(SK[:K])
	knee_points = data[SK, :]
	return knee_points

if __name__ == '__main__':
	points = np.loadtxt(sys.path[0]+'/data/points1/PMOP1_M2_A2.out')
	main_function(points, 1)



