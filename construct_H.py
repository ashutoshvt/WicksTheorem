import numpy as np
from final_hamiltonian import construct_transcorr_H
from utils import *
from helper_scf import *
from helper_ccenergy import *


def read_from_file(filename, enuc_bool=False):
    prefix = '/Users/akumar1/ayush/f12_intermediates/H2/'
    I_file = open(prefix + filename)
    shapes = I_file.readline().split('\n')
    shapes = shapes[:-1][0].split(',')
    shapes = list(map(int, shapes))
    print('shapes: {}'.format(shapes))
    my_tensor = np.zeros((1, 1))
    if len(shapes) == 4:
        my_tensor = np.zeros((shapes[0], shapes[1], shapes[2], shapes[3])) 
    if len(shapes) == 2:
        my_tensor = np.zeros((shapes[0], shapes[1])) 
    tmp = I_file.readline().split()[0].split(',')
    nocc_ = int(tmp[0])
    aocc_ = int(tmp[1])
    frozen_occ_ = nocc_ - aocc_
    e_nuc_ = float(I_file.readline().split()[0])
    if len(shapes) == 2:
        for i in range(shapes[0]*shapes[1]):
            tmp = I_file.readline().split(',')
            p_ = int(tmp[0])
            q_ = int(tmp[1])
            my_tensor[p_][q_] = float(tmp[2])
    if len(shapes) == 4:
        for i in range(shapes[0]*shapes[1]*shapes[2]*shapes[3]):
            tmp = I_file.readline().split(',')
            p_ = int(tmp[0])
            q_ = int(tmp[1])
            r_ = int(tmp[2])
            s_ = int(tmp[3])
            my_tensor[p_][q_][r_][s_] = float(tmp[4])
    if enuc_bool:
        return my_tensor, e_nuc_
    else:
        return my_tensor


# One body operators
H1_gg = read_from_file('h1_gg.csv')
H1_gc = read_from_file('h1_gc.csv')
F1_gg = read_from_file('F1_gg.csv')
F1_gc = read_from_file('F1_gc.csv')
F1_cc, e_nuc = read_from_file('F1_cc.csv', True)

# Two body operators
V2_gg_gg = read_from_file('V2_gg_gg.csv')
V2_gg_gc = read_from_file('V2_gg_gc.csv')
R2_oo_vc = read_from_file('R2_oo_vc.csv')
V_F12_oo_gg = read_from_file('V_F12_oo_gg.csv')
X_F12_oo_oo = read_from_file('X_F12_oo_oo.csv')
B_F12_oo_oo = read_from_file('B_F12_oo_oo.csv')

# dimensions
ngen  = H1_gg.shape[0]
nocc  = R2_oo_vc.shape[0]
nvir  = R2_oo_vc.shape[2]
ncabs = R2_oo_vc.shape[3]

# put all the info needed in a list
info = [ngen, nocc, nvir, H1_gg, H1_gc, F1_gg, F1_gc, F1_cc, V2_gg_gg, V2_gg_gc, R2_oo_vc, V_F12_oo_gg, X_F12_oo_oo, B_F12_oo_oo]

# Pertubed Hamiltonian using transcorrelated approach
Pert_H_1body = np.zeros((ngen, ngen))
Pert_H_2body = np.zeros((ngen, ngen, ngen, ngen))
construct_transcorr_H(Pert_H_1body, Pert_H_2body, info)

print('Pert_H_1body: ', Pert_H_1body)
print('Pertr_H_2body: ', Pert_H_2body)

# Final Hamiltonian
H_1body = H1_gg
H_1body += 0.5 * (Pert_H_1body + Pert_H_1body.T)
H_2body = V2_gg_gg
# 4-fold symmetry for now (could experiment with eight-fold symmetry later!)
for p in range(ngen):
    for q in range(ngen):
        for r in range(ngen):
            for s in range(ngen):
                H_2body[p][q][r][s] +=  0.25 * Pert_H_2body[p][q][r][s]
                H_2body[p][q][r][s] +=  0.25 * Pert_H_2body[q][p][s][r]
                H_2body[p][q][r][s] +=  0.25 * Pert_H_2body[r][s][p][q]
                H_2body[p][q][r][s] +=  0.25 * Pert_H_2body[s][r][q][p]

# Need to do SCF and CC with the final Hamiltonian!
 scf = HelperSCF(ngen, nocc, H_1body, H_2body, e_nuc, memory=2)
scf.compute_energy(e_conv=1e-13)
SCF_E = scf.SCF_E
print('\nSCF energy:          {}'.format(SCF_E))
# No frozen occ for now!
frozen_occ = 0
 ccsd = HelperCCEnergy(ngen, nocc, frozen_occ, scf.H, scf.MO, scf.F, memory=2)
ccsd.compute_energy(e_conv=1e-13, r_conv=1e-13)
CCSDcorr_E = ccsd.ccsd_corr_e
print('\nCCSD correlation energy:          {}'.format(CCSDcorr_E))
print('\nTotal energy:          {}'.format(CCSDcorr_E + SCF_E))
