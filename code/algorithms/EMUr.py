'''
this is EMU^r (recursive computation of expected marginal utility) algorithm of Bhattacharjee et.al
REFERENCES:
    Bhattacharjee, K.S., Singh, H.K., Ryan, M., Ray, T.: Bridging the gap: Manyobjective optimization and informed decision-making. IEEE Trans. Evolutionary
Computation 21(5), 813{820 (2017)
'''

import numpy as np
import math as m
import copy
from sklearn.cluster import AffinityPropagation

class solution(object):
    def __init__(self):
        self.index = None
        self.objective = None
        self.original_objective = None
        self.type = None
        self.marginalU = 0
        self.front = 0
        self.pick = 0
        self.re_vector = None

class reference_point(object):
    def __init__(self):
        self.direction = None
        self.neighbor = []
        self.associate = []
        self.identify = None

def compute_emu(p, w):
    for i in range(len(p)):
        p[i].index = i
    obj_mat = np.asarray([i.objective for i in p]).T
    w_mat = np.asarray([i.direction for i in w])
    u_mat = np.dot(w_mat, obj_mat)
    for i in range(len(u_mat)):
        temp_index = np.argsort(u_mat[i, :])
        for j in p:
            if j.index == temp_index[0]:
                k = 1
                eta = u_mat[i, temp_index[k]] - u_mat[i, temp_index[0]]
                while eta == 0.0:
                    k = k + 1
                    if k >= len(temp_index):
                        eta = 0
                        break
                    eta = u_mat[i, temp_index[k]] - u_mat[i, temp_index[0]]
                j.marginalU += eta
            else:
                j.marginalU += 0
    return p


def Compute(p, w):
    front_current = 0
    current_array = p
    while len(current_array) > 1:
        current_array = compute_emu(current_array, w)
        front_current += 1
        next_array = []
        for i in current_array:
            if i.marginalU != 0:
                i.front = front_current
            else:
                next_array.append(i)
        current_array = next_array
    if len(current_array) == 1:
        front_current += 1
        current_array[0].front = front_current
    else:
        pass
    for i in range(front_current):
        front_now = front_current - i
        if front_now != 1:
            temp_front_array = [j.marginalU for j in p if j.front == front_now]
            temp_max_emu = max(temp_front_array)
            for k in p:
                if k.front == front_now-1:
                    k.marginalU += temp_max_emu
                else:
                    pass
        else:
            pass
    return p


def Associate(p, w):
    obj_mat = np.asarray([i.objective for i in p]).T
    w_mat = np.asarray([i.direction for i in w])
    d_mat = np.dot(w_mat, obj_mat)
    for i in range(len(w_mat)):
        d_mat[i, :] = d_mat[i, :] / np.sqrt(sum(w_mat[i, :]**2))
    for i in range(len(obj_mat[0, :])):
        length2 = sum(obj_mat[:, i]**2)
        for j in range(len(d_mat[:, i])):
            d_2 = length2-d_mat[j, i]**2
            if d_2 < 0:
                d_mat[j, i] = 0
            else:
                d_mat[j, i] = d_2
        w[np.argmin(d_mat[:, i])].associate.append(p[i])
        p[i].repoints = w[np.argmin(d_mat[:, i])]
    return p, w


def Identify(w):
    for i in w:
        if len(i.associate) >= 1:
            temp_max = -1
            for k in i.associate:
                if k.marginalU > temp_max:
                    temp_max = k.marginalU
                    i.identify = k
                    k.re_vector = i
                else:
                    pass
        else:
            pass
    return w


def Select(w):
    select_set = []
    for i in w:
        if i.identify:
            mark = 1
            for j in i.neighbor:
                if j.identify:
                    if i.identify.marginalU >= j.identify.marginalU:
                        pass
                    else:
                        mark = 0
                else:
                    pass
            if mark == 1:
                select_set.append(i.identify)
            else:
                pass
        else:
            pass
    return select_set


def Initializaiton(p, w):
    for i in p:
        i.type = None
        i.index = None
        i.marginalU = 0
        i.front = 0
        i.pick = 0
        i.re_vector = None
    for i in w:
        i.associate = []
        i.identify = None
    return p, w


def main_function(data, K):
    points = copy.copy(data)
    dim = len(points[0])
    popsize = len(points)
    for i in range(dim):
        temp1 = max(points[:, i])
        temp2 = min(points[:, i])
        points[:, i] = (points[:, i] - temp2) / (temp1 - temp2)

    solutions = [solution() for i in range(popsize)]

    # reference_points
    div = 0
    H = 0
    factor = 400 / 1600 * popsize
    while H <= factor:
        div += 1
        H = m.factorial(div + dim - 1) / (m.factorial(div) * m.factorial(dim - 1))
    div -= 1
    list_range = [i / div for i in range(div + 1)]
    direction = []

    def w_generator(now_dim, now_sum, now_array):
        if now_dim == 1:
            for i in list_range:
                temp_array = copy.copy(now_array)
                if round(i + now_sum - 1, 5) == 0:
                    temp_array.append(i)
                    direction.append(temp_array)
        else:
            for i in list_range:
                temp_array = copy.copy(now_array)
                if round(i + now_sum - 1, 5) <= 0:
                    temp_array.append(i)
                    w_generator(now_dim - 1, now_sum + i, temp_array)

    w_generator(dim, 0, [])
    direction = np.asarray(direction)
    Repoints = [reference_point() for i in range(len(direction))]
    for i in range(len(direction)):
        Repoints[i].direction = direction[i, :]
        distance_list = np.sum((direction - direction[i, :] * np.ones(direction.shape)) ** 2, axis = 1)
        distance_sort = np.argsort(distance_list)
        temp_min_d = distance_list[distance_sort[1]]
        current_index = 1
        while round(temp_min_d - distance_list[distance_sort[current_index]], 5) == 0:
            Repoints[i].neighbor.append(Repoints[distance_sort[current_index]])
            current_index += 1

    SOI_A = []
    SOI = []
    # initialization
    for i in range(popsize):
        SOI_A.append(solutions[i])
        solutions[i].objective = points[i, :]
        solutions[i].original_objective = data[i, :]
    # outer loop
    while len(SOI) < K:
        # inner loop
        while len(SOI_A) > 0:
            SOI_A, Repoints = Initializaiton(SOI_A, Repoints)
            SOI_A = Compute(SOI_A, Repoints)
            SOI_A, Repoints = Associate(SOI_A, Repoints)
            Repoints = Identify(Repoints)
            S = Select(Repoints)
            if len(S) <= K or len(S) == len(SOI_A):
                break
            else:
                SOI_A = S
        SOI = SOI + S
        temp = []
        for j in solutions:
            if j not in SOI:
                temp.append(j)
            else:
                pass
        SOI_A = temp
    SOI.sort(key=lambda x: x.marginalU, reverse=True)
    SOIf = []
    if len(SOI) > K:
        # classify
        minimun_value = []
        PeripheralE = []
        Peripheral = []
        Internal = []
        for i in range(dim):
            minimun_value.append(min(points[:, i]))
        for i in SOI:
            for j in range(dim):
                if i.objective[j] == minimun_value[j]:
                    i.type = 'PeripheralE'
                    PeripheralE.append(i)
                else:
                    pass
            if i.type != 'PeripheralE':
                if min(i.re_vector.direction) == 0:
                    i.type = 'Peripheral'
                    Peripheral.append(i)
                else:
                    i.type = 'Internal'
                    Internal.append(i)
            else:
                pass
        if len(Internal) > K:
            X = np.asarray([j.objective for j in Internal])
            clustering = AffinityPropagation().fit(X)
            center_points = clustering.cluster_centers_
            for j in Internal:
                for k in center_points:
                    if (j.objective == k).all():
                        if len(SOIf) < K:
                            SOIf.append(j)
                        else:
                            pass
                    else:
                        pass
            if len(SOIf) < K:
                for j in Internal:
                    if j not in SOIf:
                        SOIf.append(j)
                    else:
                        pass
                    if len(SOIf) == K:
                        break
                    else:
                        pass
        elif len(Internal) < K:
            for j in Internal:
                SOIf.append(j)
            temp_array = Peripheral + PeripheralE
            X = np.asarray([j.objective for j in temp_array])
            clustering = AffinityPropagation().fit(X)
            center_points = clustering.cluster_centers_
            for j in temp_array:
                for k in center_points:
                    if (j.objective == k).all():
                        if len(SOIf) < K:
                            SOIf.append(j)
                        else:
                            pass
                    else:
                        pass
            if len(SOIf) < K:
                for j in temp_array:
                    if j not in SOIf:
                        SOIf.append(j)
                    else:
                        pass
                    if len(SOIf) == K:
                        break
                    else:
                        pass
        else:
            SOIf = Internal
    elif len(SOI) == K:
        SOIf = SOI
    else:
        pass
    knee_points = np.asarray([j.original_objective for j in SOIf])
    return knee_points

if __name__ == '__main__':
	points = np.loadtxt(sys.path[0]+'/data/points1/PMOP1_M2_A2.out')
	main_function(points, 1)
