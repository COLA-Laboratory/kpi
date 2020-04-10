import sys
import os
import numpy as np
import pandas as pd
from algorithms import EMUr, MMD, RA, KPITU, CHIM, CD

def file_name(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        files.sort()
        for file in files:
            file_list.append([os.path.join(root, file), os.path.splitext(file)[0]])
    return file_list

def KD(true_knee_points, apporixmate_points):
    if apporixmate_points.shape == (len(apporixmate_points),):
        apporixmate_points = apporixmate_points.reshape(-1, len(apporixmate_points))
    else:
        pass
    true_knee_points = true_knee_points.reshape(-1, apporixmate_points.shape[1])
    KID = 0
    for j in true_knee_points:
        min_d = 1000000
        for w in apporixmate_points:
            temp = np.sqrt(np.sum((j - w) ** 2))
            if temp < min_d:
                min_d = temp
            else:
                pass
        KID += min_d
    KID = KID / len(true_knee_points)
    return round(KID, 4)


if __name__ == '__main__':
    method = ['KPITU', 'MMD', 'EMUr', 'CHIM', 'CD']
    A = [1, 2, 26, 52]
    # A = 1 means these problems only have one global knee point.
    # A = 2 means these problems have more than one knee points.
    # A = 26 or 52 means these problems are degenerated, such as PMOP13 and PMOP14.

    # create folder for saving results
    if os.path.exists(sys.path[0] + '/results'):
        pass
    else:
        os.makedirs(sys.path[0] + '/results')

    for knee in A:
        points_files = file_name(sys.path[0] + '/data/points{}'.format(knee))
        knee_files = file_name(sys.path[0] + '/data/knee{}'.format(knee))

        if len(knee_files) == len(points_files):
            batch = len(knee_files)
            if batch != 0:
                for i in range(batch):
                    current_points = np.loadtxt(points_files[i][0])
                    current_points = np.unique(current_points, axis=0)
                    current_knee = np.loadtxt(knee_files[i][0])

                    if current_knee.shape == (len(current_knee), ):
                        current_knee = current_knee.reshape(-1, len(current_knee))
                    else:
                        pass

                    current_knee = np.unique(current_knee, axis=0)
                    results_save = [sys.path[0] + '/results/{}'.format(knee_files[i][1]), knee_files[i][1]]

                    if os.path.exists(results_save[0]):
                        pass
                    else:
                        os.makedirs(results_save[0])

                    KD_mat = {'KID': {}}
                    dim = len(current_points[0, :])
                    if knee == 1:
                        K = 1
                    elif knee == 2:
                        K = 2**(dim-1)
                    elif knee == 4:
                        K = 4**(dim-1)
                    elif knee ==  26:
                        K = 26
                    elif knee == 52:
                        K = 52
                    else:
                        K = 2**(dim-1)
                    print(results_save[0])

                    if 'KPITU' in method:
                        print('KPITU')
                        knee_temp = KPITU.main_function(current_points, K)
                        np.savetxt(results_save[0] + '/KPITU_knee.txt', knee_temp)
                        KD_mat['KID']['KPITU'] = KD(current_knee, knee_temp)

                    if 'EMUr' in method:
                        print('EMUr')
                        knee_temp = EMUr.main_function(current_points, K)
                        np.savetxt(results_save[0] + '/EMUr_knee.txt', knee_temp)
                        KD_mat['KID']['EMUr'] = KD(current_knee, knee_temp)

                    if 'MMD' in method:
                        print('MMD')
                        knee_temp = MMD.main_function(current_points, K)
                        np.savetxt(results_save[0] + '/MMD_knee.txt', knee_temp)
                        KD_mat['KID']['MMD'] = KD(current_knee, knee_temp)


                    if 'CD' in method:
                        print('CD')
                        knee_temp = CD.main_function(current_points, K)
                        np.savetxt(results_save[0] + '/CD_knee.txt', knee_temp)
                        KD_mat['KID']['CD'] = KD(current_knee, knee_temp)


                    if 'RA' in method:
                        if len(current_points[0, :]) == 2:
                            print('RA')
                            knee_temp = RA.main_function(current_points, K)
                            np.savetxt(results_save[0] + '/RA_knee.txt', knee_temp)
                            KD_mat['KID']['RA'] = KD(current_knee, knee_temp)


                    if 'CHIM' in method:
                        print('CHIM')
                        knee_temp = CHIM.main_function(current_points, K)
                        np.savetxt(results_save[0] + '/CHIM_knee.txt', knee_temp)
                        KD_mat['KID']['CHIM'] = KD(current_knee, knee_temp)


                    df = pd.DataFrame(KD_mat)
                    df.to_csv(results_save[0]+'/{}.csv'.format(results_save[1]), float_format='%.4E')
                    print('Have done: {:.1%}'.format((i+1)/batch))
            else:
                print('error: No files input!')
        else:
            print('error: The number of knee_files can not match the points_files!')
