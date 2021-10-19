"""
A Psi4 input script to compute Full Configuration Interaction from a SCF reference

Requirements:
SciPy 0.13.0+, NumPy 1.7.2+

References:
Equations from [Szabo:1996]
"""

__authors__ = "Tianyuan Zhang"
__credits__ = ["Tianyuan Zhang", "Jeffrey B. Schriber", "Daniel G. A. Smith"]

__copyright__ = "(c) 2014-2018, The Psi4NumPy Developers"
__license__ = "BSD-3-Clause"
__date__ = "2017-05-26"

import time
import numpy as np
np.set_printoptions(precision=5, linewidth=200, suppress=True)
import psi4
import sys
from helper_scf import *

# Check energy against psi4?
#compare_psi4 = True
compare_psi4 = False

# Memory for Psi4 in GB
# psi4.core.set_memory(int(2e9), False)
psi4.core.set_output_file('output.dat', False)

# Memory for numpy in GB
numpy_memory = 2

#mol = psi4.geometry("""
#O
#H 1 1.1
#H 1 1.1 2 104
#symmetry c1
#""")
#
#
#psi4.set_options({'basis': 'sto-3g',
#                  'scf_type': 'pk',
#                  'e_convergence': 1e-8,
#                  'd_convergence': 1e-8})
#
#print('\nStarting SCF and integral build...')
#t = time.time()
#
## First compute SCF energy using Psi4
#scf_e, wfn = psi4.energy('SCF', return_wfn=True)
#
## Grab data from wavfunction class
#C = wfn.Ca()
#ndocc = wfn.doccpi()[0]
#nmo = wfn.nmo()
#
## Compute size of Hamiltonian in GB
#from scipy.special import comb
#nDet = comb(nmo, ndocc)**2
#H_Size = nDet**2 * 8e-9
#print('\nSize of the Hamiltonian Matrix will be %4.2f GB.' % H_Size)
#if H_Size > numpy_memory:
#    clean()
#    raise Exception("Estimated memory utilization (%4.2f GB) exceeds numpy_memory \
#                    limit of %4.2f GB." % (H_Size, numpy_memory))
#

# Read the Hamiltonian
filename=str(sys.argv[1])
I_file = open(filename)
nmo = int(I_file.readline().split()[0])
tmp = I_file.readline().split()[0].split(',')
nocc = int(tmp[0])
aocc = int(tmp[1])
frozen_occ = nocc - aocc
e_nuc = float(I_file.readline().split()[0])
H = np.zeros((nmo,nmo))
for i in range(nmo*nmo):
    tmp = I_file.readline().split(',')
    p = int(tmp[0])
    q = int(tmp[1])
    H[p][q] = float(tmp[2])

old_MO = np.zeros((nmo, nmo, nmo, nmo))
for i in range(nmo*nmo*nmo*nmo):
    tmp = I_file.readline().split(',')
    p = int(tmp[0])
    q = int(tmp[1])
    r = int(tmp[2])
    s = int(tmp[3])
    old_MO[p][q][r][s] = float(tmp[4])

# Compute size of Hamiltonian in GB
from scipy.special import comb
nDet = comb(nmo, nocc)**2
H_Size = nDet**2 * 8e-9
print('\nSize of the Hamiltonian Matrix will be %4.2f GB.' % H_Size)
if H_Size > numpy_memory:
    clean()
    raise Exception("Estimated memory utilization (%4.2f GB) exceeds numpy_memory \
                    limit of %4.2f GB." % (H_Size, numpy_memory))


# Read the Hamiltonian
filename=str(sys.argv[1])
I_file = open(filename)
nmo = int(I_file.readline().split()[0])
tmp = I_file.readline().split()[0].split(',')
nocc = int(tmp[0])
aocc = int(tmp[1])
frozen_occ = nocc - aocc
e_nuc = float(I_file.readline().split()[0])
old_H = np.zeros((nmo,nmo))
for i in range(nmo*nmo):
    tmp = I_file.readline().split(',')
    p = int(tmp[0])
    q = int(tmp[1])
    old_H[p][q] = float(tmp[2])

old_MO = np.zeros((nmo, nmo, nmo, nmo))
for i in range(nmo*nmo*nmo*nmo):
    tmp = I_file.readline().split(',')
    p = int(tmp[0])
    q = int(tmp[1])
    r = int(tmp[2])
    s = int(tmp[3])
    old_MO[p][q][r][s] = float(tmp[4])

scf = HelperSCF(nmo, nocc, old_H, old_MO, e_nuc, memory=2)
scf.compute_energy(e_conv=1e-13)
SCF_E = scf.SCF_E
print('\nSCF energy:          {}'.format(SCF_E))

# Integral generation from Psi4's MintsHelper
#t = time.time()
#mints = psi4.core.MintsHelper(wfn.basisset())
#H = np.asarray(mints.ao_kinetic()) + np.asarray(mints.ao_potential())
#print('\nTotal time taken for ERI integrals: %.3f seconds.\n' % (time.time() - t))

#Make spin-orbital MO
#print('Starting AO -> spin-orbital MO transformation...')
#t = time.time()
#MO = np.asarray(mints.mo_spin_eri(C, C))

# Update H, transform to MO basis and tile for alpha/beta spin
#H = np.einsum('uj,vi,uv', C, C, H)

H = scf.H
H = np.repeat(H, 2, axis=0)
H = np.repeat(H, 2, axis=1)

# Make H block diagonal
spin_ind = np.arange(H.shape[0], dtype=np.int) % 2
H *= (spin_ind.reshape(-1, 1) == spin_ind)

#print('..finished transformation in %.3f seconds.\n' % (time.time() - t))
nso = nmo * 2
MO = np.zeros((nso, nso, nso, nso))
# TODO! Mimic the function above! mo_spin_eri, look at crawford's programming projects for help!
# generate self.MO
for p in range(nso):
    for q in range(nso):
        for r in range(nso):
            for s in range(nso):
                P=int(p/2)
                Q=int(q/2)
                R=int(r/2)
                S=int(s/2)
                value1 = scf.MO[P][Q][R][S] * int((p%2==r%2)) * int((q%2==s%2))
                value2 = scf.MO[P][Q][S][R] * int((p%2==s%2)) * int((q%2==r%2))
                MO[p][q][r][s] = value1 - value2

from helper_CI import Determinant, HamiltonianGenerator
from itertools import combinations

print('Generating %d Full CI Determinants...' % (nDet))
t = time.time()
detList = []
for alpha in combinations(range(nmo), nocc):
    for beta in combinations(range(nmo), nocc):
        detList.append(Determinant(alphaObtList=alpha, betaObtList=beta))
print('..finished generating determinants in %.3f seconds.\n' % (time.time() - t))

print('Generating Hamiltonian Matrix...')

t = time.time()
Hamiltonian_generator = HamiltonianGenerator(H, MO)
Hamiltonian_matrix = Hamiltonian_generator.generateMatrix(detList)

print('..finished generating Matrix in %.3f seconds.\n' % (time.time() - t))

print('Diagonalizing Hamiltonian Matrix...')

t = time.time()

e_fci, wavefunctions = np.linalg.eigh(Hamiltonian_matrix)
print('..finished diagonalization in %.3f seconds.\n' % (time.time() - t))
fci_energies = []
excitation_energies = []
Hartree_to_eV = 27.2114
for i, vals in enumerate(e_fci):
   #fci_energies.append(vals + mol.nuclear_repulsion_energy()) 
   fci_energies.append(vals + e_nuc) 
for i in range(1, 6):
   excitation_energies.append(Hartree_to_eV * (fci_energies[i] - fci_energies[0])) 
print('fci_energies: ', fci_energies[:6])
print('excitation_energies: ', excitation_energies) 

#fci_mol_e = e_fci[0] + mol.nuclear_repulsion_energy()
fci_mol_e = e_fci[0] + e_nuc

print('# Determinants:     % 16d' % (len(detList)))

#print('SCF energy:         % 16.10f' % (scf_e))
#print('FCI correlation:    % 16.10f' % (fci_mol_e - scf_e))
print('Total FCI energy:   % 16.10f' % (fci_mol_e))

if compare_psi4:
    psi4.compare_values(psi4.energy('FCI'), fci_mol_e, 6, 'FCI Energy')
