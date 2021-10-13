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
# amplitudes needed in excited states simulation!
R1   = op.initialize_stoperator('R1', 1.0, [['A1'], ['p1']])
R1D  = op.initialize_stoperator('R1D', 1.0, [['p1'], ['A1']])
R11   = op.initialize_stoperator('R11', 1.0, [['B1'], ['q1']])
R11D  = op.initialize_stoperator('R11D', 1.0, [['q1'], ['B1']])

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

# doubles!
H1_R2  = final_expressions([H1, R2], 'H1_R2')
H1_R2D  = final_expressions([H1, R2D], 'H1_R2D')
V2_R2  = final_expressions([V2, R2], 'V2_R2')
V2_R2D  = final_expressions([V2, R2D], 'V2_R2D')
F1_R2_R2 = final_expressions([F1, R2, R22], 'F1_R2_R2')
F1_R2_R2D = final_expressions([F1, R2, R22D], 'F1_R2_R2D')
F1_R2D_R2 = final_expressions([F1, R2D, R22], 'F1_R2D_R2')
F1_R2D_R2D = final_expressions([F1, R2D, R22D], 'F1_R2D_R2D')

# singles!
H1_R1  = final_expressions([H1, R1], 'H1_R1')
H1_R1D  = final_expressions([H1, R1D], 'H1_R1D')
V2_R1  = final_expressions([V2, R1], 'V2_R1')
V2_R1D  = final_expressions([V2, R1D], 'V2_R1D')
F1_R1_R1 = final_expressions([F1, R1, R11], 'F1_R1_R1')
F1_R1_R1D = final_expressions([F1, R1, R11D], 'F1_R1_R1D')
F1_R1D_R1 = final_expressions([F1, R1D, R11], 'F1_R1D_R1')
F1_R1D_R1D = final_expressions([F1, R1D, R11D], 'F1_R1D_R1D')

# mixed!
F1_R1_R2 = final_expressions([F1, R1, R2], 'F1_R1_R2')
F1_R1_R2D = final_expressions([F1, R1, R2D], 'F1_R1_R2D')
F1_R1D_R2 = final_expressions([F1, R1D, R2], 'F1_R1D_R2')
F1_R1D_R2D = final_expressions([F1, R1D, R2D], 'F1_R1D_R2D')
# ------------------------------------------------------------
F1_R2_R1 = final_expressions([F1, R2, R1], 'F1_R2_R1')
F1_R2_R1D = final_expressions([F1, R2, R1D], 'F1_R2_R1D')
F1_R2D_R1 = final_expressions([F1, R2D, R1], 'F1_R2D_R1')
F1_R2D_R1D = final_expressions([F1, R2D, R1D], 'F1_R2D_R1D')

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
op.einsum_expressions(list_list_terms, f)
f.close()
