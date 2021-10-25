import func_ewt
import operators as op
from commutator import comm
import print_terms as pt

func = func_ewt

def final_expressions(operators, name):
    list_terms = []
    if len(operators) == 2:
        list_terms = comm([operators[0]], [operators[1]], 1)     
    else:
        list_terms = comm(comm([operators[0]], [operators[1]], 0), [operators[2]], 1)
    filename = 'outputs/' + name + '.txt'
    pt.print_terms(list_terms, filename)
    print('Simplification for HF ref:')
    filename = 'outputs/' + name + '_HF.txt'
    op.simplify_for_HF(list_terms)
    pt.print_terms(list_terms, filename)
    list_terms = op.three_body_decompose(list_terms)
    filename = 'outputs/' + name + '_3body.txt'
    pt.print_terms(list_terms, filename)
    list_terms = op.simplify_three_body_HF(list_terms)
    filename = 'outputs/' + name + '_3body_simplified.txt'
    pt.print_terms(list_terms, filename)
    return list_terms


# lets define all the operators here!

F1   = op.initialize_stoperator('F1', 1.0, [['p0'], ['q0']])
H1   = op.initialize_stoperator('H1', 1.0, [['p0'], ['q0']])
V2   = op.initialize_stoperator('V2', 0.5, [['p0', 'q0'], ['r0', 's0']])

# ------------------------------------------------------------------------------
# Actually, I want R^A0B0_p0q0 as the F12 operator for excited states simulation!
# Just neglect R^cx_ab amplitude, include everything else!

R2   = op.initialize_stoperator('R2', 0.5, [['A0', 'B0'], ['t0', 'u0']])
R2D  = op.initialize_stoperator('R2D', 0.5, [['t0', 'u0'], ['A0', 'B0']])
R22  = op.initialize_stoperator('R22', 0.5, [['A1', 'B1'], ['t1', 'u1']])
R22D = op.initialize_stoperator('R22D', 0.5, [['t1', 'u1'], ['A1', 'B1']])

# ------------
# I am missing R^iA_pq operator where A is actually a pure cabs index!
# ------------ 
#Ri2   = op.initialize_stoperator('Ri2', 0.5, [['i0', 'B0'], ['t0', 'u0']])
#Ri2D  = op.initialize_stoperator('Ri2D', 0.5, [['t0', 'u0'], ['i0', 'B0']])
#Ri22  = op.initialize_stoperator('Ri22', 0.5, [['i1', 'B1'], ['t1', 'u1']])
#Ri22D = op.initialize_stoperator('Ri22D', 0.5, [['t1', 'u1'], ['i1', 'B1']])

# singles!
R1   = op.initialize_stoperator('R1', 1.0, [['C1'], ['p1']])
R1D  = op.initialize_stoperator('R1D', 1.0, [['p1'], ['C1']])
R11   = op.initialize_stoperator('R11', 1.0, [['D1'], ['q1']])
R11D  = op.initialize_stoperator('R11D', 1.0, [['q1'], ['D1']])

# --------------------------------------------------------------------------------
# all the terms needed!
#
# 1.  [H1, R2-R2+] == [H1, R2] - [H1,R2+]
# 2.  1/2 * [[F1, R2-R2+], R2-R2+] ==  1/2 * ([[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+])
# 3.  [V2, R2-R2+] == [V2,R2] - [V2,R2+]
# 4.  [H1, R1-R1+] == [H1, R1] - [H1,R1+]
# 5.  [V2, R1-R1+] == [V2, R1] - [V2,R1+]
# 6.  1/2 * [[F1, R1-R1+], R1-R1+] ==  1/2 * ([[F1, R1], R1] - [[F1, R1], R1+] - [[F1,R1+],R1] + [F1,R1+],R1+])
# Mixed terms R1,R2 along similar lines!  
# ------------------------------------------

# doubles: R2^AB_pq
H1_R2  = final_expressions([H1, R2], 'H1_R2')
H1_R2D  = final_expressions([H1, R2D], 'H1_R2D')
V2_R2  = final_expressions([V2, R2], 'V2_R2')
V2_R2D  = final_expressions([V2, R2D], 'V2_R2D')
F1_R2_R2 = final_expressions([F1, R2, R22], 'F1_R2_R2')
F1_R2_R2D = final_expressions([F1, R2, R22D], 'F1_R2_R2D')
F1_R2D_R2 = final_expressions([F1, R2D, R22], 'F1_R2D_R2')
F1_R2D_R2D = final_expressions([F1, R2D, R22D], 'F1_R2D_R2D')


## doubles: R2^iA_pq where A is a pure cabs index!
#H1_Ri2  = final_expressions([H1, Ri2], 'H1_Ri2')
#H1_Ri2D  = final_expressions([H1, Ri2D], 'H1_Ri2D')
#V2_Ri2  = final_expressions([V2, Ri2], 'V2_Ri2')
#V2_Ri2D  = final_expressions([V2, Ri2D], 'V2_Ri2D')
#F1_Ri2_Ri2 = final_expressions([F1, Ri2, Ri22], 'F1_Ri2_Ri2')
#F1_Ri2_Ri2D = final_expressions([F1, Ri2, Ri22D], 'F1_Ri2_Ri2D')
#F1_Ri2D_Ri2 = final_expressions([F1, Ri2D, Ri22], 'F1_Ri2D_Ri2')
#F1_Ri2D_Ri2D = final_expressions([F1, Ri2D, Ri22D], 'F1_Ri2D_Ri2D')

# singles!
H1_R1  = final_expressions([H1, R1], 'H1_R1')
H1_R1D  = final_expressions([H1, R1D], 'H1_R1D')
V2_R1  = final_expressions([V2, R1], 'V2_R1')
V2_R1D  = final_expressions([V2, R1D], 'V2_R1D')
F1_R1_R1 = final_expressions([F1, R1, R11], 'F1_R1_R1')
F1_R1_R1D = final_expressions([F1, R1, R11D], 'F1_R1_R1D')
F1_R1D_R1 = final_expressions([F1, R1D, R11], 'F1_R1D_R1')
F1_R1D_R1D = final_expressions([F1, R1D, R11D], 'F1_R1D_R1D')

# mixed singles doubles R1, R2
# R2 has A0,B0,t0,u0 and A1,B1,t1,u1
# F1 has p0q0
# R1 has p1C1, q1D1, or (p1,q1), (r1,s1)
F1_R1_R2 = final_expressions([F1, R1, R2], 'F1_R1_R2')
F1_R1_R2D = final_expressions([F1, R1, R2D], 'F1_R1_R2D')
F1_R1D_R2 = final_expressions([F1, R1D, R2], 'F1_R1D_R2')
F1_R1D_R2D = final_expressions([F1, R1D, R2D], 'F1_R1D_R2D')
# ------------------------------------------------------------
F1_R2_R1 = final_expressions([F1, R2, R1], 'F1_R2_R1')
F1_R2_R1D = final_expressions([F1, R2, R1D], 'F1_R2_R1D')
F1_R2D_R1 = final_expressions([F1, R2D, R1], 'F1_R2D_R1')
F1_R2D_R1D = final_expressions([F1, R2D, R1D], 'F1_R2D_R1D')

# mixed singles doubles R1, Ri2
# Ri2 has i0,B0,t0,u0 and i1,B1,t1,u1
# F1 has p0q0
# R1 has p1C1, q1D1
#F1_R1_Ri2 = final_expressions([F1, R1, Ri2], 'F1_R1_Ri2')
#F1_R1_Ri2D = final_expressions([F1, R1, Ri2D], 'F1_R1_Ri2D')
#F1_R1D_Ri2 = final_expressions([F1, R1D, Ri2], 'F1_R1D_Ri2')
#F1_R1D_Ri2D = final_expressions([F1, R1D, Ri2D], 'F1_R1D_Ri2D')
## ------------------------------------------------------------
#F1_Ri2_R1 = final_expressions([F1, Ri2, R1], 'F1_Ri2_R1')
#F1_Ri2_R1D = final_expressions([F1, Ri2, R1D], 'F1_Ri2_R1D')
#F1_Ri2D_R1 = final_expressions([F1, Ri2D, R1], 'F1_Ri2D_R1')
#F1_Ri2D_R1D = final_expressions([F1, Ri2D, R1D], 'F1_Ri2D_R1D')
#
## mixed doubles doubles R2, Ri2
## R2 has A0,B0,t0,u0 and A1,B1,t1,u1
## Ri2 has i0,B0,t0,u0 and i1,B1,t1,u1
## F1 has p0q0
## Need to re-define Ri2 operator to r1,s1,i1,C1
## no need for separate indices of Ri2 and Ri22 
## as these are mixed terms not pure!
#Ri2   = op.initialize_stoperator('Ri2', 0.5, [['i1', 'C1'], ['r1', 's1']])
#Ri2D  = op.initialize_stoperator('Ri2D', 0.5, [['r1', 's1'], ['i1', 'C1']])
#Ri22  = op.initialize_stoperator('Ri22', 0.5, [['i1', 'C1'], ['r1', 's1']])
#Ri22D = op.initialize_stoperator('Ri22D', 0.5, [['r1', 's1'], ['i1', 'C1']])
## ------------------------------------------------------------
#F1_R2_Ri2 = final_expressions([F1, R2, Ri22], 'F1_R2_Ri2')
#F1_R2_Ri2D = final_expressions([F1, R2, Ri22D], 'F1_R2_Ri2D')
#F1_R2D_Ri2 = final_expressions([F1, R2D, Ri22], 'F1_R2D_Ri2')
#F1_R2D_Ri2D = final_expressions([F1, R2D, Ri22D], 'F1_R2D_Ri2D')
## ------------------------------------------------------------
#F1_Ri2_R2 = final_expressions([F1, Ri2, R22], 'F1_Ri2_R2')
#F1_Ri2_R2D = final_expressions([F1, Ri2, R22D], 'F1_Ri2_R2D')
#F1_Ri2D_R2 = final_expressions([F1, Ri2D, R22], 'F1_Ri2D_R2')
#F1_Ri2D_R2D = final_expressions([F1, Ri2D, R22D], 'F1_Ri2D_R2D')

f = open('test.py', 'w')
f.write('import numpy as np\n')
list_list_terms = [(H1_R2, 1.0, 'H1_R2'), (H1_R2D, -1.0, 'H1_R2D'), 
                   (F1_R2_R2, 0.5, 'F1_R2_R2'), (F1_R2_R2D, -0.5, 'F1_R2_R2D'), 
                   (F1_R2D_R2, -0.5, 'F1_R2D_R2'), (F1_R2D_R2D, 0.5, 'F1_R2D_R2D'), 
                   (V2_R2, 1.0, 'V2_R2'), (V2_R2D, -1.0, 'V2_R2D'),
                   (H1_R1, 1.0, 'H1_R1'), (H1_R1D, -1.0, 'H1_R1D'), 
                   (V2_R1, 1.0, 'V2_R1'), (V2_R1D, -1.0, 'V2_R1D'), 
                   (F1_R1_R1, 0.5, 'F1_R1_R1'), 
                   (F1_R1_R1D, -0.5, 'F1_R1_R1D'),  # c
                   (F1_R1D_R1, -0.5, 'F1_R1D_R1'),  # c
                   (F1_R1D_R1D, 0.5, 'F1_R1D_R1D'),
                   (F1_R1_R2, 0.5, 'F1_R1_R2'), 
                   (F1_R1_R2D, -0.5, 'F1_R1_R2D'),  # c
                   (F1_R1D_R2, -0.5, 'F1_R1D_R2'),  # c
                   (F1_R1D_R2D, 0.5, 'F1_R1D_R2D'),
                   (F1_R2_R1, 0.5, 'F1_R2_R1'), 
                   (F1_R2_R1D, -0.5, 'F1_R2_R1D'),  # c
                   (F1_R2D_R1, -0.5, 'F1_R2D_R1'),  # c
                   (F1_R2D_R1D, 0.5, 'F1_R2D_R1D')]
                   #(H1_Ri2, 2.0, 'H1_Ri2'), (H1_Ri2D, -2.0, 'H1_Ri2D'), # multiply terms containing Ri to 2
                   #(V2_Ri2, 2.0, 'V2_Ri2'), (V2_Ri2D, -2.0, 'V2_Ri2D'),
                   #(F1_Ri2_Ri2, 1.0, 'F1_Ri2_Ri2'), 
                   #(F1_Ri2_Ri2D, -1.0, 'F1_Ri2_Ri2D'), 
                   #(F1_Ri2D_Ri2, -1.0, 'F1_Ri2D_Ri2'), 
                   #(F1_Ri2D_Ri2D, 1.0, 'F1_Ri2D_Ri2D'),
                   #(F1_R1_Ri2, 1.0, 'F1_R1_Ri2'), 
                   #(F1_R1_Ri2D, -1.0, 'F1_R1_Ri2D'),  # c
                   #(F1_R1D_Ri2, -1.0, 'F1_R1D_Ri2'),  # c
                   #(F1_R1D_Ri2D, 1.0, 'F1_R1D_Ri2D'),
                   #(F1_Ri2_R1, 1.0, 'F1_Ri2_R1'), 
                   #(F1_Ri2_R1D, -1.0, 'F1_Ri2_R1D'),  # c
                   #(F1_Ri2D_R1, -1.0, 'F1_Ri2D_R1'),  # c
                   #(F1_Ri2D_R1D, 1.0, 'F1_Ri2D_R1D'),
                   #(F1_R2_Ri2, 1.0, 'F1_R2_Ri2'), 
                   #(F1_R2_Ri2D, -1.0, 'F1_R2_Ri2D'), 
                   #(F1_R2D_Ri2, -1.0, 'F1_R2D_Ri2'), 
                   #(F1_R2D_Ri2D, 1.0, 'F1_R2D_Ri2D'),
                   #(F1_Ri2_R2, 1.0, 'F1_Ri2_R2'), 
                   #(F1_Ri2_R2D, -1.0, 'F1_Ri2_R2D'), 
                   #(F1_Ri2D_R2, -1.0, 'F1_Ri2D_R2'), 
                   #(F1_Ri2D_R2D, 1.0, 'F1_Ri2D_R2D')]
#list_list_terms =  [(H1_R1, 1.0, 'H1_R1'), (H1_R1D, -1.0, 'H1_R1D'),
#                   (V2_R1, 1.0, 'V2_R1'), (V2_R1D, -1.0, 'V2_R1D'),
#                   (F1_R1_R1, 0.5, 'F1_R1_R1'),
#                   (F1_R1_R1D, -0.5, 'F1_R1_R1D'),  # c
#                   (F1_R1D_R1, -0.5, 'F1_R1D_R1'),  # c
#                   (F1_R1D_R1D, 0.5, 'F1_R1D_R1D')]
#list_list_terms =  [(H1_R1, 1.0, 'H1_R1')]
op.einsum_expressions(list_list_terms, f)
f.close()
