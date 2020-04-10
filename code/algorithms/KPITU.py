'''
this is the KPITU (Knee Point Identification Based on Trade-Off Utility) algorithm
'''

import numpy as np
import copy
import math as m

class solution(object):
    def __init__(self, m):
        self.index = -1
        self.objective = np.zeros([1, m])
        self.neighbor = []
        self.contribution = -1
        self.repoints = None
        self.left = -1

class reference_point(object):
    def __init__(self):
        self.direction = None
        self.neighbor = []
        self.associate = []

def transfer(A, B):
    if np.sum(A.objective - B.objective) > 0:
        return 1
    else:
        return 0


def select(A, B):
    return np.sum(A.objective - B.objective)


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


def main_function(data, K):
    points = copy.copy(data)
    num = len(points)
    dim = len(points[0, :])

    for i in range(dim):
        Min = min(points[:, i])
        Max = max(points[:, i])
        if Max != Min:
            points[:, i] = (points[:, i] - Min) / (Max - Min)
        else:
            points[:, i] = Min

    div = 0
    H = 0
    while H < num:
        div += 1
        H = m.factorial(div + dim - 1) / (m.factorial(div) * m.factorial(dim - 1))
    div -= 1
    if div >= 20:
        div = 20
    else:
        pass
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
    P = [solution(dim) for i in range(num)]
    for i in range(num):
        P[i].index = i
        P[i].objective = points[i, :]

    P, Repoints = Associate(P, Repoints)

    for im in range(num):
        P[im].neighbor = []
        for i1 in P[im].repoints.associate:
            if i1 is not P[im]:
                if i1 not in P[im].neighbor:
                    P[im].neighbor.append(i1)
        for i2 in P[im].repoints.neighbor:
            for i3 in i2.associate:
                if i3 not in P[im].neighbor:
                    P[im].neighbor.append(i3)

    Current = P
    Internal = []
    Peripheral = []
    Reserve = []
    for j in Current:
        for mm in j.neighbor:
            if transfer(j, mm) == 1:
                j.left = 1
            else:
                pass
        if j.left != 1:
            if min(j.repoints.direction) == 0 and dim not in [5, 8, 10]:
                Peripheral.append(j)
            else:
                Internal.append(j)
        else:
            Reserve.append(j)

    Peripheral_index = np.asarray([j.index for j in Peripheral])
    Internal_index = np.asarray([j.index for j in Internal])

    if len(Internal_index) == 0:
        if len(Peripheral_index) < K:
            if dim == 8 or dim == 10:
                add_index = []
                neighbor_num = len(Peripheral_index)
                for i in Peripheral:
                    neighbor_num += len(i.neighbor)
                    for j in i.neighbor:
                        add_index.append(j.index)
                if neighbor_num <= K:
                    Internal_index = np.hstack((Peripheral_index, np.asarray(add_index)))
                else:
                    gain_list_all = []
                    for i in Peripheral:
                        gain_value = 0
                        gain_list = []
                        for j in i.neighbor:
                            for k in i.neighbor:
                                gain_value += select(j, k)
                            gain_list.append(gain_value)
                        gain_sort = np.argsort(gain_list)
                        for j in range(len(gain_sort)):
                            gain_list[gain_sort[j]] = len(gain_sort) - j
                        gain_list_all = gain_list_all + gain_list
                    gain_sort_all = np.argsort(gain_list_all)
                    select_index = [add_index[gain_sort_all[k]] for k in range(K-len(Peripheral_index))]
                    Internal_index = np.hstack((Peripheral_index, np.asarray(select_index)))
            else:
                for i in Peripheral:
                    gain_value = 0
                    gain_list = []
                    for j in i.neighbor:
                        for k in i.neighbor:
                            gain_value += select(j, k)
                        gain_list.append(gain_value)

                    gain_list = np.asarray(gain_list)
                    SK = np.argsort(gain_list)
                    SK = list(SK[:m.ceil(K / len(Internal) - 1)])

                    for sel_index in SK:
                        Peripheral_index = np.hstack((Peripheral_index, i.neighbor[sel_index].index))
                if len(Peripheral_index) > K:
                    Internal_index = Peripheral_index[0:K]
        elif len(Peripheral_index) > K:
            gain_list = []
            for i in Peripheral:
                gain_value = 0
                for j in Peripheral:
                    gain_value += select(i, j)
                gain_list.append(gain_value)

            gain_list = np.asarray(gain_list)
            SK = np.argsort(gain_list)
            SK = list(SK[:K])
            Internal_index = Peripheral_index[SK]
        else:
            Internal_index = Peripheral_index
    elif len(Internal_index) < K:
        for i in Internal:
            gain_value = 0
            gain_list = []
            for j in i.neighbor:
                for k in i.neighbor:
                    gain_value += select(j, k)
                gain_list.append(gain_value)

            gain_list = np.asarray(gain_list)
            SK = np.argsort(gain_list)
            SK = list(SK[:m.ceil(K / len(Internal) - 1)])

            for sel_index in SK:
                Internal_index = np.hstack((Internal_index, i.neighbor[sel_index].index))
        if len(Internal_index) > K:
            Internal_index = Internal_index[0:K]
    else:
        pass

    internal_points = data[Internal_index, :]
    return internal_points

if __name__ == '__main__':
    points = np.loadtxt(sys.path[0]+'/data/points1/PMOP1_M2_A2.out')
    main_function(points, 1)


