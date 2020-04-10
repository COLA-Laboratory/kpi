'''
this is the CD (cone-domination) algorithm of Chiu et al.
REFERENCES:
Ram´ırez-Atencia, C., Mostaghim, S., Camacho, D.: A knee point based evolutionary multi-objective optimization for mission planning problems. In: GECCO’17:
Proc. of the Genetic and Evolutionary Computation Conference. pp. 1216-1223(2017)
'''

import numpy as np
from random import sample

def coneDominance(angle_array, individual1, individual2):
    con1 = individual1
    con2 = individual2
    Omig1 = np.dot(angle_array, con1.T)
    Omig2 = np.dot(angle_array, con2.T)
    if (np.all((Omig1 - Omig2) <= 0))  and np.any((Omig1 - Omig2)< 0):
        return 1
    else:
        return 0

def main_function(data, K):
    # 135 degree angles
    fai = 135
    del_index = []
    num = len(data)
    show_dim = len(data[0, :])

    angle_array = np.zeros([show_dim, show_dim])
    angle = np.tan((2*np.pi/360)*(fai-90)/2)
    for i in range(show_dim):
        for j in range(show_dim):
            if i != j:
                angle_array[i, j] = angle
            else:
                angle_array[i, j] = 1

    index = [i for i in range(num)]
    reserve = list(set(index).difference(set(del_index)))
    # knee_points = np.delete(data, del_index, axis=0)
    if num - len(del_index) > K:
        SK = sample(reserve, K)
        knee_points = data[SK, :]
    elif num - len(del_index) < K:
        add_list = sample(del_index, K - (num - len(del_index)))
        res_index = list(set(reserve).union(set(add_list)))
        knee_points = data[res_index, :]
    else:
        knee_points = np.delete(data, del_index, axis=0)

    return knee_points

if __name__ == '__main__':
    points = np.loadtxt(sys.path[0]+'/data/points1/PMOP1_M2_A2.out')
    main_function(points, 1)