import numpy as np
from final_hamiltonian import construct_transcorr_H

def read_from_file(filename):
    prefix = '/Users/akumar1/ayush/f12_intermediates/H2/'
    I_file = open(prefix + filename)
    shapes = I_file.readline().split('\n')
    shapes = shapes[:-1][0].split(',')
    shapes = list(map(int, shapes))
    print('shapes: {}'.format(shapes))
    my_tensor = np.zeros((1,1))
    if len(shapes) == 4:
        my_tensor = np.zeros((shapes[0], shapes[1], shapes[2], shapes[3])) 
    if len(shapes) == 2:
        my_tensor = np.zeros((shapes[0], shapes[1])) 
    tmp = I_file.readline().split()[0].split(',')
    nocc = int(tmp[0])
    aocc = int(tmp[1])
    frozen_occ = nocc - aocc
    e_nuc = float(I_file.readline().split()[0])
    if len(shapes) == 2:
        for i in range(shapes[0]*shapes[1]):
            tmp = I_file.readline().split(',')
            p = int(tmp[0])
            q = int(tmp[1])
            my_tensor[p][q] = float(tmp[2])
    if len(shapes) == 4:
        for i in range(shapes[0]*shapes[1]*shapes[2]*shapes[3]):
            tmp = I_file.readline().split(',')
            p = int(tmp[0])
            q = int(tmp[1])
            r = int(tmp[2])
            s = int(tmp[3])
            my_tensor[p][q][r][s] = float(tmp[4])
    return my_tensor

# One body operators
h1_gg = read_from_file('h1_gg.csv')
h1_gc = read_from_file('h1_gc.csv')
F1_gg = read_from_file('F1_gg.csv')
F1_gc = read_from_file('F1_gc.csv')
F1_cc = read_from_file('F1_cc.csv')

# Two body operators
V2_gg_gg = read_from_file('V2_gg_gg.csv')
V2_gg_gc = read_from_file('V2_gg_gc.csv')
R2_oo_vc = read_from_file('R2_oo_vc.csv')
V_F12_oo_gg = read_from_file('V_F12_oo_gg.csv')
X_F12_oo_oo = read_from_file('X_F12_oo_oo.csv')
B_F12_oo_oo = read_from_file('B_F12_oo_oo.csv')

# dimensions
ngen  =  h1_gg.shape[0]
nocc  =  R2_oo_vc.shape[0]
nvir  =  R2_oo_vc.shape[2]
ncabs =  R2_oo_vc.shape[3]

# put all the info needed in a list
info = [ngen, nocc, nvir, F1_gg, F1_gc, F1_cc, V2_gg_gg, V2_gg_gc, R2_oo_vc, V_F12_oo_gg, X_F12_oo_oo, B_F12_oo_oo]

# Pertubed Hamiltonian using transcorrelated approach
H_1body = np.zeros((ngen, ngen))
H_2body = np.zeros((ngen, ngen, ngen, ngen))
construct_transcorr_H(H_1body, H_2body, info)

print('H_1body: ', H_1body)
print('H_2body: ', H_2body)
