import sys
import numpy as np
# from final_hamiltonian import construct_transcorr_H
from test import construct_transcorr_H
from utils import *
from helper_scf import *
from helper_ccenergy import *
#from f12_intermediates import construct_B()


def read_from_file(filename, enuc_bool=False, other_info=True):
    #prefix = '/Users/akumar1/ayush/f12_intermediates/H2O/6-31g/'
    #prefix = '/Users/akumar1/ayush/f12_intermediates/H2/6-31g/'
    #prefix = '/Users/akumar1/ayush/f12_intermediates/LiH/'
    #prefix = '/Users/akumar1/ayush/f12_intermediates/BH/'
    #prefix = '/Users/akumar1/Software/build/uccf12/H2O/'
    #prefix = '/Users/akumar1/ayush/f12_intermediates/H2O/ano-rcc-min/1_5_gamma/aug_cc_pvtz_cabs/'
    prefix = '/Users/akumar1/Software/build/uccf12/H2O/'
    I_file = open(prefix + filename)
    shapes = I_file.readline().split('\n')
    shapes = shapes[:-1][0].split(',')
    shapes = list(map(int, shapes))
    my_tensor = np.zeros((1, 1))
    if len(shapes) == 4:
        my_tensor = np.zeros((shapes[0], shapes[1], shapes[2], shapes[3])) 
    if len(shapes) == 3:
        my_tensor = np.zeros((shapes[0], shapes[1], shapes[2])) 
    if len(shapes) == 2:
        my_tensor = np.zeros((shapes[0], shapes[1])) 
    if other_info:
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
    if len(shapes) == 3:
        for i in range(shapes[0]*shapes[1]*shapes[2]):
            tmp = I_file.readline().split(',')
            p_ = int(tmp[0])
            q_ = int(tmp[1])
            r_ = int(tmp[2])
            my_tensor[p_][q_][r_] = float(tmp[3])
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

def construct_B():
    nocc = 5
    ngen = 7
    slice_occ = slice(0,nocc)
    slice_vir = slice(nocc,ngen)
    # Term 1
    filename = 'B_left_1.csv'
    B_left = read_from_file(filename, False, False) 
    #print(B_left)
    filename = 'B_middle_1.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_1.csv'
    B_right = read_from_file(filename, False, False) 
    B = np.einsum('Kpq,KL,Lrs->pqrs', B_left, B_middle, B_right, optimize=True)
    # Term 2
    filename = 'B_hJ1_2.csv'
    B_hJ1 = read_from_file(filename, False, False)
    filename = 'B_left_2.csv'
    B_left = read_from_file(filename, False, False)
    tmp = np.einsum('pqPs,Pr->pqrs', B_left, B_hJ1, optimize=True)
    B += tmp.copy()
    B += tmp.swapaxes(0,1).swapaxes(2,3)
    # Term 3
    filename = 'B_left_3.csv'
    B_left = read_from_file(filename, False, False) 
    filename = 'B_middle_3.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_3.csv'
    B_right = read_from_file(filename, False, False) 
    tmp = np.einsum('pqQP,PR,rsQR->pqrs', B_left, B_middle, B_right, optimize=True)
    B -= tmp.copy()
    B -= tmp.swapaxes(0,1).swapaxes(2,3)
    # Term 4
    filename = 'B_left_4.csv'
    B_left = read_from_file(filename, False, False) 
    filename = 'B_middle_4.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_4.csv'
    B_right = read_from_file(filename, False, False) 
    #tmp = np.einsum('pqPt,PR,rsRt->pqrs', B_left, B_middle, B_right, optimize=True)
    tmp = np.einsum('pqPm,PR,rsRm->pqrs', B_left[:,:,:,slice_occ], B_middle, B_right[:,:,:,slice_occ], optimize=True)
    B -= tmp.copy()
    B -= tmp.swapaxes(0,1).swapaxes(2,3)
    # Term 5
    filename = 'B_left_5.csv'
    B_left = read_from_file(filename, False, False) 
    filename = 'B_middle_5.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_5.csv'
    B_right = read_from_file(filename, False, False) 
    #tmp = 2.0 * np.einsum('pqtx,tP,rsPx->pqrs', B_left, B_middle, B_right, optimize=True)
    tmp = 2.0 * np.einsum('pqmx,mP,rsPx->pqrs', B_left[:,:,slice_occ,:], B_middle[slice_occ,:], B_right, optimize=True)
    B -= tmp.copy()
    B -= tmp.swapaxes(0,1).swapaxes(2,3)
    # Term 6
    filename = 'B_left_6.csv'
    B_left = read_from_file(filename, False, False) 
    filename = 'B_middle_6.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_6.csv'
    B_right = read_from_file(filename, False, False) 
    tmp = np.einsum('pqta,tu,rsua->pqrs', B_left, B_middle, B_right, optimize=True)
    B -= tmp.copy()
    B -= tmp.swapaxes(0,1).swapaxes(2,3)
    # Term 7
    filename = 'B_left_7.csv'
    B_left = read_from_file(filename, False, False) 
    filename = 'B_middle_7.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_7.csv'
    B_right = read_from_file(filename, False, False) 
    #tmp = np.einsum('pqtx,tu,rsux->pqrs', B_left, B_middle, B_right, optimize=True)
    tmp = np.einsum('pqmx,mn,rsnx->pqrs', B_left[:,:,slice_occ,:], B_middle[slice_occ,slice_occ], B_right[:,:,slice_occ,:], optimize=True)
    B += tmp.copy()
    B += tmp.swapaxes(0,1).swapaxes(2,3)
    # Term 8
    filename = 'B_left_8.csv'
    B_left = read_from_file(filename, False, False) 
    filename = 'B_middle_8.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_8.csv'
    B_right = read_from_file(filename, False, False) 
    tmp = 2.0 * np.einsum('pqta,tx,rsxa->pqrs', B_left, B_middle, B_right, optimize=True)
    B -= tmp.copy()
    B -= tmp.swapaxes(0,1).swapaxes(2,3)
    return B

def construct_VX(VX):
    nocc = 5
    ngen = 7
    slice_occ = slice(0,nocc)
    slice_vir = slice(nocc,ngen)
    prefix = ''
    if VX == 'V': 
        prefix += 'V_'
    else:
        prefix += 'X_'
    # Term 1
    filename = prefix + 'left_1.csv'
    left = read_from_file(filename, False, False) 
    filename = prefix + 'middle_1.csv'
    middle = read_from_file(filename, False, False) 
    filename = prefix + 'right_1.csv'
    right = read_from_file(filename, False, False) 
    VX = np.einsum('Kpr,KL,Lqs->pqrs', left, middle, right, optimize=True)
    # Term 2
    filename = prefix + 'left_2.csv'
    left = read_from_file(filename, False, False) 
    filename = prefix + 'right_2.csv'
    right = read_from_file(filename, False, False) 
    VX -= np.einsum('pqtu,rstu->pqrs', left, right, optimize=True)
    # Term 3
    filename = prefix + 'left_3.csv'
    left = read_from_file(filename, False, False) 
    filename = prefix + 'right_3.csv'
    right = read_from_file(filename, False, False) 
    tmp = np.einsum('pqmx,rsmx->pqrs', left, right, optimize=True)
    VX -= (tmp + tmp.swapaxes(0,1).swapaxes(2,3))
    return VX


# One body operators
H1_gg = read_from_file('h1_gg.csv')
H1_gc = read_from_file('h1_gc.csv')
F1_gg = read_from_file('F1_gg.csv')
F1_gc = read_from_file('F1_gc.csv')
F1_cc, e_nuc = read_from_file('F1_cc.csv', True)

# Two body operators
V2_gg_gg = read_from_file('V2_gg_gg.csv')
V2_gg_gc = read_from_file('V2_gg_gc.csv')
V2_gg_cc = read_from_file('V2_gg_cc.csv')
R2_oo_vc = read_from_file('R2_oo_vc.csv')
#V_F12_oo_gg = read_from_file('V_F12_oo_gg.csv')
#X_F12_oo_oo = read_from_file('X_F12_oo_oo.csv')
#B_F12_oo_oo = read_from_file('B_F12_oo_oo.csv')

## ----------------------------------------------------
# experimenting with my B intermediate!
# constants
C_0 = 1/2.0;            # (natural) singlet cusp coefficient
C_1 = 1/4.0;            # triplet cusp coefficient
C_ab = (C_0 + C_1) / 2.0;  # abab cusp coefficient = 3/8
C_ba = (C_0 - C_1) / 2.0;  # abba cusp coeffient = 1/8
C_ab_ab = C_ab * C_ab;
C_ab_ba = C_ab * C_ba;
C_ba_ab = C_ba * C_ab;
C_ba_ba = C_ba * C_ba;
C2_ab = C_ab_ab + C_ba_ba;
C2_ba = C_ab_ba + C_ba_ab;

b_F12_gg_gg = construct_B()
B_F12_gg_gg =  C2_ab * b_F12_gg_gg + C2_ba * b_F12_gg_gg.swapaxes(0,1)

#B_F12_gg_gg_1 = read_from_file('B_F12_gg_gg.csv')
#b_F12_gg_gg = read_from_file('bb_F12_gg_gg.csv')
#B_F12_gg_gg_1 =  C2_ab * b_F12_gg_gg + C2_ba * b_F12_gg_gg.swapaxes(0,1)
#diff = B_F12_gg_gg - B_F12_gg_gg_1
#print('diff.max: ', diff.max())

v_F12_gg_gg = construct_VX('V')
V_F12_gg_gg =  C_ab * v_F12_gg_gg + C_ba * v_F12_gg_gg.swapaxes(0,1)
V_F12_gg_gg_1 = read_from_file('V_F12_gg_gg.csv')
x_F12_gg_gg = construct_VX('X')
X_F12_gg_gg =  C_ab * x_F12_gg_gg + C_ba * x_F12_gg_gg.swapaxes(0,1)
X_F12_gg_gg_1 = read_from_file('X_F12_gg_gg.csv')
print('X_diff: ', (X_F12_gg_gg_1 - X_F12_gg_gg).max())
print('V_diff: ', (V_F12_gg_gg_1 - V_F12_gg_gg).max())
## ----------------------------------------------------

# needed for excited states!
R2_gg_oc = read_from_file('R2_gg_oc.csv')
R2_gg_vc = read_from_file('R2_gg_vc.csv')
R2_gg_cc = read_from_file('R2_gg_cc.csv')


# dimensions
ngen  = H1_gg.shape[0]
nocc  = R2_oo_vc.shape[0]
nvir  = R2_oo_vc.shape[2]
ncabs = R2_oo_vc.shape[3]
slice_o = slice(0, nocc)
slice_v = slice(nocc, ngen)

# New observations: for water in minimal basis, no external virtuals,
# there are 2 virtuals and they should be in active space.
# only external orbitals are pure CABS
# now, it seems like semi-internal excitations are avoided?? 
# so, R^{rx}_{pq} types of terms are not included?? 
# so, R^{ax}_{ij} term should also be zero? --> maybe only for ij, it should not be zero??
# So, lets check now!

R2_gg_oc = np.zeros((ngen, ngen, nocc, ncabs))
#R2_gg_vc = np.zeros((ngen, ngen, nvir, ncabs))
R2_gg_vc[slice_v, slice_v, :, :] = np.zeros((nvir, nvir, nvir, ncabs))
#R2_gg_vc[slice_o, slice_v, :, :] = np.zeros((nocc, nvir, nvir, ncabs))
#R2_gg_vc[slice_v, slice_o, :, :] = np.zeros((nvir, nocc, nvir, ncabs))

'''
# experimentation with V, X and B:
# V(p,q,r,s) = g^{pq}_{xy} * G^{pq_xy}
# X(p,q,r,s) = G^{pq}_{xy} * G^{rs_xy}
# B(p,q,r,s) = G^{pq}_{xy} * F^{y}_{z} * G^{rs_xz}
V_F12_gg_gg =  np.einsum('pqxy,rsxy->pqrs', R2_gg_cc, V2_gg_cc)
X_F12_gg_gg =  np.einsum('pqxy,rsxy->pqrs', R2_gg_cc, R2_gg_cc)
B_F12_gg_gg =  np.einsum('pqxy,yz,rsxz->pqrs', R2_gg_cc, F1_cc, R2_gg_cc)
'''

# construct R1^p_x
# R1^i_x = F1^i_x/(F1_ii - F1_xx)
# R1^a_x = F1^a_x/(F1_aa - F1_xx)
R1_px = np.zeros((ngen, ncabs))
for p in range(nocc):
    for x in range(ncabs):
        R1_px[p][x] = F1_gc[p][x]/(F1_gg[p][p] - F1_cc[x][x]) 
for p in range(nocc, ngen):
    for x in range(ncabs):
        #R1_px[p][x] = F1_gc[p][x]/(F1_cc[x][x] - 0.2) 
        R1_px[p][x] = F1_gc[p][x]/(F1_gg[p][p] - F1_cc[x][x]) 
# print('R1_px: ', R1_px)
#print('ncabs: ', ncabs)
#print('F1_cc: ', F1_cc)


'''
# So, I need to reproduce ground state energies!
# Need to populate all these arrays accordingly!
# V_F12_gg_gg --> populate just i,j,k,l block
V_F12_gg_gg = np.zeros((ngen, ngen, ngen, ngen))
V_F12_gg_gg[slice_o, slice_o, :, :] = V_F12_oo_gg
# X_F12_gg_gg --> populate just i,j,k,l block
X_F12_gg_gg = np.zeros((ngen, ngen, ngen, ngen))
X_F12_gg_gg[slice_o, slice_o, slice_o, slice_o] = X_F12_oo_oo
# B_F12_gg_gg --> populate just i,j,k,l block
B_F12_gg_gg = np.zeros((ngen, ngen, ngen, ngen))
B_F12_gg_gg[slice_o, slice_o, slice_o, slice_o] = B_F12_oo_oo
## R2_gg_vc --> populate just i,j,v,c block
R2_gg_vc = np.zeros((ngen, ngen, nvir, ncabs))
R2_gg_vc[slice_o, slice_o, :, :] = R2_oo_vc
# R2_gg_cc --> should be zero for ground state!
R2_gg_cc = np.zeros((ngen, ngen, ncabs, ncabs))
'''

#-------------------------------------------------------------
#  let the above structure of V, X and B be like this only for excited states 
# as well, as I would need to hack MPQC!! lets revisit this later!!!
#--------------------------------------------------------------

# put all the info needed in a list
info = [ngen, nocc, nvir, H1_gg, H1_gc, F1_gg, F1_gc, F1_cc, V2_gg_gg, V2_gg_gc, R2_gg_vc, 
        R2_gg_cc, V_F12_gg_gg, X_F12_gg_gg, B_F12_gg_gg, R1_px, R2_gg_oc]

# Pertubed Hamiltonian using transcorrelated approach
Pert_H_1body = np.zeros((ngen, ngen))
Pert_H_2body = np.zeros((ngen, ngen, ngen, ngen))
construct_transcorr_H(Pert_H_1body, Pert_H_2body, info)

#print('Pert_H_1body: ', Pert_H_1body)
#print('Pert_H_2body: ', Pert_H_2body)
#print('enuc: ', e_nuc)

# Final Hamiltonian
H_1body = H1_gg
H_1body += 0.5 * (Pert_H_1body + Pert_H_1body.T)
H_2body = V2_gg_gg


# 4-fold symmetry for now (could experiment with eight-fold symmetry later!)
for p in range(ngen):
    for q in range(ngen):
        for r in range(ngen):
            for s in range(ngen):
                H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[p][q][r][s]
                H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[q][p][s][r]
                H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[r][s][p][q]
                H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[s][r][q][p]
                # ----------
                H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[r][q][p][s]
                H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[q][r][s][p]
                H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[p][s][r][q]
                H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[s][p][q][r]
              
# Need to do SCF and CC with the final Hamiltonian!
scf = HelperSCF(ngen, nocc, H_1body, H_2body, e_nuc, memory=2)
scf.compute_energy(e_conv=1e-13)
SCF_E = scf.SCF_E
print('\nSCF energy:          {}'.format(SCF_E))
# No frozen occ for now!
frozen_occ = 0
print('original Fock: ', F1_gg)
print('scf.F: ', scf.F)
ccsd = HelperCCEnergy(ngen, nocc, frozen_occ, scf.H, scf.MO, scf.F, memory=2)
ccsd.compute_energy(e_conv=1e-13, r_conv=1e-13)
CCSDcorr_E = ccsd.ccsd_corr_e
print('\nCCSD correlation energy:          {}'.format(CCSDcorr_E))
print('\nTotal energy:          {}'.format(CCSDcorr_E + SCF_E))

# write the Hamiltonian in the correct format!
filename = 'Excited_state_H.csv'
f=open(filename,'w')
f.write('{}\n'.format(ccsd.nmo))
f.write('{},{}\n'.format(ccsd.nocc, ccsd.nocc))
f.write('{}\n'.format(e_nuc))

for p in range(ccsd.nmo):
    for q in range(ccsd.nmo):
        f.write('{},{},{}\n'.format(p,q,ccsd.H[p][q]))

for p in range(ccsd.nmo):
    for q in range(ccsd.nmo):
        for r in range(ccsd.nmo):
            for s in range(ccsd.nmo):
                f.write('{},{},{},{},{}\n'.format(p,q,r,s,ccsd.MO[p][q][r][s]))

