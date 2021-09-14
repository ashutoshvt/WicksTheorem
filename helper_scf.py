import numpy as np
import time

class HelperSCF(object):
    def __init__(self, nmo, nocc, H, MO, enuc, memory=2):
    
        print("Initializing SCF object....\n")
        time_init = time.time()
        self.nmo = nmo
        self.nocc = nocc 
        self.nvirt = nmo-nocc 
        self.H = H
        self.MO = MO
        self.enuc = enuc
        # Make slices
        self.slice_o = slice(0, self.nocc)
        self.slice_v = slice(self.nocc, self.nmo)
        self.slice_a = slice(0, self.nmo)
        self.slice_dict = {
            'o': self.slice_o,
            'v': self.slice_v,
            'a': self.slice_a
        }
        
    def compute_energy(self, e_conv=1e-7, d_conv=1e-7):
        self.F = np.zeros((self.nmo,self.nmo))
        D_mo = np.zeros((self.nocc,self.nocc))      
        for i in range(self.nocc):
            D_mo[i][i] = 2.0
        converged = False
        Eold = 0.0
        for SCF_ITER in range(1,100):
            self.F = self.H.copy()
            self.F += 1.0 * np.einsum('pmqn,mn->pq', self.MO[:, self.slice_o, :, self.slice_o], D_mo) 
            self.F -= 0.5 * np.einsum('pmnq,mn->pq', self.MO[:, self.slice_o, self.slice_o, :], D_mo) 
            tmp = self.H + self.F
            self.SCF_E = 0.5 * np.einsum('pq,pq->',D_mo,tmp[self.slice_o, self.slice_o]) + self.enuc

            print('SCF Iteration %3d: Energy = %4.16f   dE = % 1.5E'
            %  (SCF_ITER, self.SCF_E, (self.SCF_E - Eold)))
            if abs(self.SCF_E - Eold) < e_conv:
                converged = True
                break

            Eold = self.SCF_E
            # Diagonalize Fock matrix
            e_val, e_vec = np.linalg.eigh(self.F)      
            # modify self.H and self.MO 
            self.H = np.einsum('ap,ab,bq->pq', e_vec, self.H, e_vec) 
            self.MO = np.einsum('ap,bq,abcd,cr,ds->pqrs', e_vec, e_vec, self.MO, e_vec, e_vec, optimize=True) 
