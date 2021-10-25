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
    prefix = '/Users/akumar1/Software/build/uccf12/H2O/dz-f12-cabs/'
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

def construct_B(spaces):
    slice_ia = slice(0, spaces[0] + spaces[1])
    slice_x = slice(spaces[2], spaces[3])
    print('slice_ia: ', slice_ia)
    print('slice_x: ', slice_x)
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
    tmp = np.einsum('pqPm,PR,rsRm->pqrs', B_left[:,:,:,slice_ia], B_middle, B_right[:,:,:,slice_ia], optimize=True)
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
    tmp = 2.0 * np.einsum('pqmx,mP,rsPx->pqrs', B_left[:,:,slice_ia,:], B_middle[slice_ia,:], B_right, optimize=True)
    B -= tmp.copy()
    B -= tmp.swapaxes(0,1).swapaxes(2,3)
    # Term 6
    filename = 'B_left_6.csv'
    B_left = read_from_file(filename, False, False) 
    filename = 'B_middle_6.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_6.csv'
    B_right = read_from_file(filename, False, False) 
    #tmp = np.einsum('pqta,tu,rsua->pqrs', B_left, B_middle, B_right, optimize=True)
    tmp = np.einsum('pqta,tu,rsua->pqrs', B_left[:,:,:,slice_x], B_middle, B_right[:,:,:,slice_x], optimize=True)
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
    tmp = np.einsum('pqmx,mn,rsnx->pqrs', B_left[:,:,slice_ia,:], B_middle[slice_ia,slice_ia], B_right[:,:,slice_ia,:], optimize=True)
    B += tmp.copy()
    B += tmp.swapaxes(0,1).swapaxes(2,3)
    # Term 8
    filename = 'B_left_8.csv'
    B_left = read_from_file(filename, False, False) 
    filename = 'B_middle_8.csv'
    B_middle = read_from_file(filename, False, False) 
    filename = 'B_right_8.csv'
    B_right = read_from_file(filename, False, False) 
    #tmp = 2.0 * np.einsum('pqta,tx,rsxa->pqrs', B_left, B_middle, B_right, optimize=True)
    tmp = 2.0 * np.einsum('pqta,tx,rsxa->pqrs', B_left[:,:,:,slice_x], B_middle, B_right[:,:,:,slice_x], optimize=True)
    B -= tmp.copy()
    B -= tmp.swapaxes(0,1).swapaxes(2,3)
    return B

def construct_VX(VX, spaces):
    slice_ia = slice(0, spaces[0] + spaces[1])
    print('slice_ia: ', slice_ia)
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
    tmp = np.einsum('pqmx,rsmx->pqrs', left[:,:,slice_ia,:], right[:,:,slice_ia,:], optimize=True)
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


# Definition of Spaces
# for water in minimal basis, 
# lets take LUMO+1 as external virtual!
# HOMO and LUMO as active space!
# HOMO-1 ... HOMO-4 as occupied space!
# so external orbitals in this case are pure CABS + (LUMO+1)
double_occ = 4
active = 2
active_vir = 1
external_vir = 1
total_vir = 2

'''
# no external virtual
double_occ = 4
active = 3
active_vir = 2
external_vir = 0
total_vir = 2
'''


spaces = [double_occ, active, active_vir, total_vir]

#b_F12_gg_gg = construct_B(spaces)
#B_F12_gg_gg =  C2_ab * b_F12_gg_gg + C2_ba * b_F12_gg_gg.swapaxes(0,1)
#print(B_F12_gg_gg[6][6])
B_F12_gg_gg = read_from_file('B_F12_gg_gg.csv')

#v_F12_gg_gg = construct_VX('V', spaces)
#V_F12_gg_gg =  C_ab * v_F12_gg_gg + C_ba * v_F12_gg_gg.swapaxes(0,1)
V_F12_gg_gg = read_from_file('V_F12_gg_gg.csv')

#x_F12_gg_gg = construct_VX('X', spaces)
#X_F12_gg_gg =  C_ab * x_F12_gg_gg + C_ba * x_F12_gg_gg.swapaxes(0,1)
X_F12_gg_gg = read_from_file('X_F12_gg_gg.csv')

# print('X_diff: ', (X_F12_gg_gg_1 - X_F12_gg_gg).max())
# print('V_diff: ', (V_F12_gg_gg_1 - V_F12_gg_gg).max())
# ----------------------------------------------------

#-------------------------------------------------------------
# Now that the intermediates are adapted to active space!
# Time to do the same to F12 amplitudes now!!
#--------------------------------------------------------------

# dimensions
ngen  = H1_gg.shape[0]
nocc  = R2_oo_vc.shape[0]
nvir  = R2_oo_vc.shape[2]
ncabs = R2_oo_vc.shape[3]
slice_o = slice(0, nocc)
slice_v = slice(nocc, ngen)
slice_v1 = slice(0, nvir)

# needed for excited states!
R2_gg_oc = read_from_file('R2_gg_oc.csv')
R2_gg_vc = read_from_file('R2_gg_vc.csv')
R2_gg_vc[slice_v, slice_v, slice_v1, :] = np.zeros((nvir, nvir, nvir, ncabs))
R2_gg_cc = read_from_file('R2_gg_cc.csv')
#R2_gg_cc = np.zeros((ngen,ngen,ncabs,ncabs))

# technically, we are just extending occ to occ + active_vir for excited states simulation!
# and I am choosing 1 active_vir (LUMO) only so that I have one external virtual as well!
# But I will experiment with other choices as well, like 0 external virtual etc.     
 
# ----------------------------------------------------------------------------------------------------
# Step 1:
# R2^{LUMO, CABS}_{i+HOMO,j+HOMO} should be zero!
# R2^{CABS, LUMO}_{i+HOMO,j+HOMO} should be zero!
# since LUMO resides in active space!
# only R2^{LUMO+1, CABS}_{i+HOMO,j+HOMO} should be populated! i == doubly_occupied (4 in this example!)
# only R2^{CABS, LUMO+1}_{i+HOMO,j+HOMO} should be populated!
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Step 2:
# R2^{LUMO+1, CABS}_{i,LUMO} should be populated! 
# R2^{LUMO+1, CABS}_{LUMO,i} should be populated! 
# R2^{CABS, LUMO+1}_{i,LUMO} should be populated! 
# R2^{CABS, LUMO+1}_{LUMO,i} should be populated! 
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Step 3:
# R2^{LUMO+1, CABS}_{LUMO,LUMO} should be populated! 
# R2^{CABS, LUMO+1}_{LUMO,LUMO} should be populated! 
# R2^{LUMO, CABS}_{LUMO,LUMO} should be zero!
# R2^{CABS, LUMO}_{LUMO,LUMO} should be zero! 
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# Step 4:
# R2^{:,:}_{LUMO+1,:} should be zero!
# R2^{:,:}_{LUMO+1,:} should be zero!
# then this will have implications for the F12 intermediates as well!
# Then [V,X,B] terms involving LUMO+1 index should be zero!
# Also, the same should be true for every F12 amplitude
# technically, we just extended occ to occ + active_vir for excited states simulation!
# ----------------------------------------------------------------------------------------------------

'''
# Treatment of R2_gg_vc
slice_act_vir = slice(0, active_vir)
slice_act_vir_1 = slice(nocc, nocc+active_vir)
slice_ext_vir = slice(nocc + active_vir, ngen)
print('slice_ext_vir: ', slice_ext_vir)
# only amplitudes containing active indices (doubly occ + active vir) should be added!
R2_gg_vc[slice_ext_vir,slice_ext_vir,:,:] = np.zeros((external_vir,external_vir,nvir,ncabs))
R2_gg_vc[slice_ext_vir,:,:,:] = np.zeros((external_vir,ngen,nvir,ncabs))
R2_gg_vc[:,slice_ext_vir,:,:] = np.zeros((ngen,external_vir,nvir,ncabs))
# g is only (doubly occ + active vir (LUMO)) now!
# R2^{LUMO, :}_{i+HOMO,j+HOMO} should be zero! LUMO is not external!!!
# only external is allowed, rest have been projected out through the projector!
R2_gg_vc[:,:,slice_act_vir,:] = np.zeros((ngen,ngen,active_vir,ncabs))
#R2_gg_vc[slice_act_vir_1,slice_act_vir_1,slice_ext_vir,:] = np.zeros((active_vir,active_vir,external_vir,ncabs))
# v is only (LUMO+1) now!

# for zero external virtuals
#R2_gg_vc = np.zeros((ngen,ngen,total_vir,ncabs))

# Treatment of R2_gg_cc
# only amplitudes containing active indices (doubly occ + active vir) should be added!
R2_gg_cc[slice_ext_vir,slice_ext_vir,:,:] = np.zeros((external_vir,external_vir,ncabs,ncabs))
R2_gg_cc[slice_ext_vir,:,:,:] = np.zeros((external_vir,ngen,ncabs,ncabs))
R2_gg_cc[:,slice_ext_vir,:,:] = np.zeros((ngen,external_vir,ncabs,ncabs))
# g is only (doubly occ + active vir (LUMO)) now!

# Treatment of V, X and B
slice_occ_act = slice(0, nocc + active_vir)
X_F12_act_act_act_act = np.zeros((ngen, ngen, ngen, ngen))
B_F12_act_act_act_act = np.zeros((ngen, ngen, ngen, ngen))
X_F12_act_act_act_act[slice_occ_act, slice_occ_act, slice_occ_act, slice_occ_act] = X_F12_gg_gg[slice_occ_act, slice_occ_act, slice_occ_act, slice_occ_act]
B_F12_act_act_act_act[slice_occ_act, slice_occ_act, slice_occ_act, slice_occ_act] = B_F12_gg_gg[slice_occ_act, slice_occ_act, slice_occ_act, slice_occ_act]
'''
# ----------------------------------------------------------------------------------------------------
# Step 5 (Singles)
# construct R1^p_x
# R1^i_x = F1^i_x/(F1_ii - F1_xx) (same as before!)
# R1^{LUMO}_{LUMO+1} = F1^{LUMO}_{LUMO+1}/(F1^{LUMO}_{LUMO}(adjustable) - F1[LUMO+1][LUMO+1]) --> will try this later
# as I am not sure if all OBS indices (LUMO,LUMO+1) should be allowed for R1 
# I can easily say that all OBS indices are not possible in R2, but not sure in R1
# R1^{LUMO}_{CABS} = F1^{LUMO}_{CABS}/(F1^{LUMO}_{LUMO}(adjustable) - F1[CABS][CABS]) --> will try adjustments later!
# ----------------------------------------------------------------------------------------------------
########################
# Actually, R1 should have dimensions of ngen, external_vir + ncabs 
# --> nopes, since Fock is diagonal, R1 can only have ngen, ncabs dimension! 
# so, lets just consider CABS!
t1_iA = read_from_file('t_iA.csv', False, False)
R1_px = np.zeros((ngen, total_vir + ncabs))
R1_px[slice_o, 2:] = t1_iA[:,2:]
t1_ax = read_from_file('t_ax.csv', False, False)
R1_px[slice_v, 2:] = t1_ax[:,:]
'''
for p in range(nocc):
    for x in range(ncabs):
        R1_px[p][total_vir+x] = F1_gc[p][x]/(F1_gg[p][p] - F1_cc[x][x]) 
'''
'''
e_a = -1.00
for p in range(nocc, nocc+active_vir): # LUMO-CABS
    for x in range(ncabs):
        #R1_px[p][total_vir+x] = F1_gc[p][x]/(F1_gg[p][p] - F1_cc[x][x])  
        R1_px[p][total_vir+x] = F1_gc[p][x]/(e_a - F1_cc[x][x]) 
for p in range(nocc+active_vir, ngen): # LUMO+1-CABS
    for x in range(ncabs):
        R1_px[p][total_vir+x] = F1_gc[p][x]/(e_a - F1_cc[x][x]) 
        #R1_px[p][total_vir+x] = F1_gc[p][x]/(F1_gg[p][p] - F1_cc[x][x])
print('R1_px: ', R1_px)
print('ncabs: ', ncabs)
print('F1_cc max: ', np.max(F1_cc))
print('F1_cc min: ', np.min(F1_cc))
print('F1_cc diag: ', np.diag(F1_cc))


#t1_iA = read_from_file('t_iA.csv', False, False)
t1_iA_1 = t1_iA[:,2:]
R1_px_1 = R1_px[slice_o, 2:]
print('difference\n')
diff = t1_iA_1- R1_px_1
print('t1_iA: ', t1_iA_1)
print('R1_px: ', R1_px_1)
print('difference.max: ', np.max(t1_iA_1- R1_px_1))
'''
########################
'''
# Trying CABS singles amplitudes computed from MPQC!!
# severely overstimates correlation energy,
# maybe I am missing something!
#t1_iA = read_from_file('t_iA.csv', False, False)
# R1 has dimensions of ngen, total_vir + ncabs in MPQC!! 
# if couple_virtual setting is turned on (default!)
########################
R1_px = np.zeros((ngen, total_vir + ncabs))
t1_iA = read_from_file('t_iA.csv', False, False)
t1_aA = read_from_file('t_aA.csv', False, False)
# doubly occ - [CABS] 
R1_px[slice_o, 2:] = t1_iA[:, 2:]
#R1_px[nocc, 1:] = t1_aA[0, 1:] # ---> results in massive error! --> LUMO -> LUMO+1, CABS
# R1_px[nocc, 2:] = t1_aA[0, 2:] # ---> also results in massive error!!! because t_aA[0] is completely crazy!
R1_px[nocc+1, 2:] = t1_aA[1, 2:]
# LUMO - [CABS] 
#lumo = slice(nocc, nocc+1)
#lumo_vir = slice(0, 1)
#R1_px[nocc, 2:] = t1_aA[0][2:]
#R1_px[nocc+1, 2:] = t1_aA[1][2:]
#R1_px[lumo, total_vir:] = t1_aA[lumo_vir, total_vir:]
# LUMO - [LUMO+n] 
#lumo_plus_n = slice(nocc+active_vir, nocc+total_vir)
#lumo_plus_n_vir = slice(active_vir, total_vir)
#R1_px[lumo, lumo_plus_n] = t1_aA[lumo_vir, lumo_plus_n_vir]
'''
########################

########################
'''
#R1_px = np.zeros((ngen, total_vir + ncabs))
#slice_cabs = slice(0, ncabs)
#R1_px[slice_o, :] = t1_iA[:,total_vir:]
#for p in range(nocc, ngen): # p is LUMO
#for p in range(nocc, nocc+active_vir): # p is LUMO
#    for x in range(ncabs):
#        R1_px[p][x] = F1_gc[p][x]/(F1_gg[p][p] - F1_cc[x][x])  # correct form!
#        #R1_px[p][x] = F1_gc[p][x]/(F1_cc[x][x] - 0.5)  # correct form!
#        #R1_px[p][x] = F1_gc[p][x]/(-0.5 - F1_cc[x][x])  # correct form!
'''
########################


'''
# old stuff!
#R2_gg_oc = np.zeros((ngen, ngen, nocc, ncabs))
#R2_gg_vc = np.zeros((ngen, ngen, nvir, ncabs))
#R2_gg_vc[slice_v, slice_v, :, :] = np.zeros((nvir, nvir, nvir, ncabs))
#R2_gg_vc[slice_o, slice_v, :, :] = np.zeros((nocc, nvir, nvir, ncabs))
#R2_gg_vc[slice_v, slice_o, :, :] = np.zeros((nvir, nocc, nvir, ncabs))
'''
########################
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
########################

#-------------------------------------------------------------
# Final form of intermediates and amplitudes now!
#--------------------------------------------------------------

# put all the info needed in a list
info = [ngen, nocc, nvir, H1_gg, H1_gc, F1_gg, F1_gc, F1_cc, V2_gg_gg, V2_gg_gc, R2_gg_vc, 
        #R2_gg_cc, V_F12_gg_gg, X_F12_act_act_act_act, B_F12_act_act_act_act, R1_px, R2_gg_oc]
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
                H_2body[p][q][r][s] +=   2.0 * 2.0 * 0.125 * Pert_H_2body[p][q][r][s]
                H_2body[p][q][r][s] +=   2.0 * 2.0 * 0.125 * Pert_H_2body[q][p][s][r]
                H_2body[p][q][r][s] +=   2.0 * 2.0 * 0.125 * Pert_H_2body[r][s][p][q]
                H_2body[p][q][r][s] +=   2.0 * 2.0 * 0.125 * Pert_H_2body[s][r][q][p]
                # ----------
                #H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[r][q][p][s]
                #H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[q][r][s][p]
                #H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[p][s][r][q]
                #H_2body[p][q][r][s] +=  2.0 * 0.125 * Pert_H_2body[s][p][q][r]

# 4-fold symmetry for now (could experiment with eight-fold symmetry later!)
tmp_H = np.zeros((ngen,ngen,ngen,ngen))
for p in range(ngen):
    for q in range(ngen):
        for r in range(ngen):
            for s in range(ngen):
                tmp = 0
                tmp +=  0.125 * H_2body[p][q][r][s]
                tmp +=  0.125 * H_2body[q][p][s][r]
                tmp +=  0.125 * H_2body[r][s][p][q]
                tmp +=  0.125 * H_2body[s][r][q][p]
                tmp +=  0.125 * H_2body[r][q][p][s]
                tmp +=  0.125 * H_2body[q][r][s][p]
                tmp +=  0.125 * H_2body[p][s][r][q]
                tmp +=  0.125 * H_2body[s][p][q][r]
                tmp_H[p][q][r][s] = tmp

#H_2body = tmp_H.copy()

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

# experimentation with V, X and B:
# V(p,q,r,s) = g^{pq}_{xy} * G^{pq_xy}
# X(p,q,r,s) = G^{pq}_{xy} * G^{rs_xy}
# B(p,q,r,s) = G^{pq}_{xy} * F^{y}_{z} * G^{rs_xz}
#V_F12_gg_gg =  np.einsum('pqxy,rsxy->pqrs', R2_gg_cc, V2_gg_cc)
#X_F12_gg_gg =  np.einsum('pqxy,rsxy->pqrs', R2_gg_cc, R2_gg_cc)
#B_F12_gg_gg =  np.einsum('pqxy,yz,rsxz->pqrs', R2_gg_cc, F1_cc, R2_gg_cc)
