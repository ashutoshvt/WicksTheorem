import numpy as np

nocc = 5
nvir = 2
ngen = 7
ncabs = 10

# I need to have slices of V and R2!
# NEED TO WORK FURTHER ON THIS!! TODO
V2 = np.zeros((ngen, ngen, ngen, ngen))
R2 = np.zeros((nocc, nocc, ncabs, nvir))
R2D = np.zeros((nocc, nocc, ncabs, nvir))
R22 = np.zeros((nocc, nocc, ncabs, nvir))
R22D = np.zeros((nocc, nocc, ncabs, nvir))
C = np.zeros((nocc, nocc, ncabs, nvir))
F1 = np.zeros((ngen, ngen))



