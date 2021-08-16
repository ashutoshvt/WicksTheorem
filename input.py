import func_ewt
func=func_ewt
import operators as op
from commutator import comm
import print_terms as pt

def initialze_stoperator(name, prefac, summ_ind, coeff_ind=None):
    opp = func_ewt.contractedobj('op', 1, 1)
    # summ and coeff would be identical!
    summ  = [item for sublist in summ_ind for item in sublist] 
    coeff=[]
    if coeff_ind:
        coeff = coeff_ind
    else:
        coeff = [item for sublist in summ_ind for item in sublist] 
    opp.upper = summ_ind[0]
    opp.lower = summ_ind[1]
    stp=[[opp]]
    co=[[1,1]]
    St_op = op.StOperator(name, prefac, summ, coeff, stp, co)
    St_op.map_org=[St_op]
    return St_op 

# let me try to reproduce the transcorrelated Hamiltonian
# for ground state first (used in Shiozaki's paper!)

# lets define all the operators here!
F1=initialze_stoperator('F1',1.0,[['p0'],['q0']])
V2=initialze_stoperator('V2',0.5,[['p0','q0'],['r0','s0']])
R2=initialze_stoperator('R2',0.5,[['A0','B0'],['i0','j0']])
R22=initialze_stoperator('R2',0.5,[['A1','B1'],['i1','j1']])
R2D=initialze_stoperator('R2',0.5,[['i0','j0'],['A0','B0']])
R22D=initialze_stoperator('R2',0.5,[['i1','j1'],['A1','B1']])

# 1.  [F1, R2-R2+] == [F1, R2] - [F1,R2+] 
#                        a)        b)

# a)

F1R2=comm([F1],[R2],1)
pt.print_terms(F1R2,'F1R2.txt')
'''
# b)

F1R2D=comm([F1],[R2D],1)
pt.print_terms(F1R2D,'F1R2D.txt')

# 2.  [[F1, R2-R2+], R2-R2+] ==  [[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+]
#                                       a)               b)               c)             d)

# a)

F1R2R2=comm(comm([F1],[R2],0),[R22],1)
pt.print_terms(F1R2R2,'F1R2R2.txt')

# b)

F1R2R2D=comm(comm([F1],[R2],0),[R22D],1)
pt.print_terms(F1R2R2D,'F1R2R2D.txt')

# c)

F1R2DR2=comm(comm([F1],[R2D],0),[R22],1)
pt.print_terms(F1R2DR2,'F1R2DR2.txt')

# d)

F1R2DR2D=comm(comm([F1],[R2D],0),[R22D],1)
pt.print_terms(F1R2DR2D,'F1R2DR2D.txt')

# 3.  [V2, R2-R2+] == [V2,R2] - [V2,R2+]
#                       a)        b)

# a)

V2R2=comm([V2],[R2],1)
pt.print_terms(V2R2,'V2R2.txt')

# b) 

V2R2D=comm([V2],[R2D],1)
pt.print_terms(V2R2D,'V2R2D.txt')
'''
