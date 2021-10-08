import func_ewt
import operators as op
from commutator import comm
import print_terms as pt

func = func_ewt

def final_expressions(operators, name, excited_state=True):
    list_terms = []
    if len(operators) == 2:
        list_terms = comm([operators[0]], [operators[1]], 1)     
    else:
        list_terms = comm(comm([operators[0]], [operators[1]], 0), [operators[2]], 1)
    filename = 'outputs/' + name + '.txt'
    pt.print_terms(list_terms, filename)
    print('Simplification for HF ref:')
    op.simplify_for_HF(list_terms)
    list_terms = op.three_body_decompose(list_terms)
    filename = 'outputs/' + name + '_3body.txt'
    pt.print_terms(list_terms, filename)
    list_terms = op.simplify_three_body_HF(list_terms)
    if excited_state: 
        filename = 'outputs/' + name + '_3body_simplified.txt'
        pt.print_terms(list_terms, filename)
        op.excited_states_cabs_plus_to_pure_cabs(list_terms)
        op.excited_states_retain_only_one_two_cabs_amplitudes(list_terms)
        op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(list_terms)
        filename = 'outputs/' + name + '_new.txt'
        pt.print_terms(list_terms, filename)
        return list_terms
    else:
        filename = 'outputs/' + name + '_new.txt'
        pt.print_terms(list_terms, filename)
        return list_terms


# lets define all the operators here!

F1   = op.initialize_stoperator('F1', 1.0, [['p0'], ['q0']])
H1   = op.initialize_stoperator('H1', 1.0, [['p0'], ['q0']])
V2   = op.initialize_stoperator('V2', 0.5, [['p0', 'q0'], ['r0', 's0']])
# -------
R2   = op.initialize_stoperator('R2', 0.5, [['A0', 'B0'], ['i0', 'j0']])
R2D  = op.initialize_stoperator('R2D', 0.5, [['i0', 'j0'], ['A0', 'B0']])
R22  = op.initialize_stoperator('R22', 0.5, [['A1', 'B1'], ['i1', 'j1']])
R22D = op.initialize_stoperator('R22D', 0.5, [['i1', 'j1'], ['A1', 'B1']])
# excited states amplitudes
R1   = op.initialize_stoperator('R1', 1.0, [['A1'], ['p1']])
R1D  = op.initialize_stoperator('R1D', 1.0, [['p1'], ['A1']])
R11   = op.initialize_stoperator('R11', 1.0, [['B1'], ['q1']])
R11D  = op.initialize_stoperator('R11D', 1.0, [['q1'], ['B1']])
# -------
R2_abxy   = op.initialize_stoperator('R2_abxy', 0.5, [['A0', 'B0'], ['c0', 'd0']])
R2D_abxy  = op.initialize_stoperator('R2D_abxy', 0.5, [['c0', 'd0'], ['A0', 'B0']])
R22_abxy  = op.initialize_stoperator('R22_abxy', 0.5, [['A1', 'B1'], ['c1', 'd1']])
R22D_abxy = op.initialize_stoperator('R22D_abxy', 0.5, [['c1', 'd1'], ['A1', 'B1']])
# ------- would need iaxy as well, so maybe I should scale this term by 2.0 later!
R2_aixy   = op.initialize_stoperator('R2_aixy', 0.5, [['A0', 'B0'], ['c0', 'i0']])
R2D_aixy  = op.initialize_stoperator('R2D_aixy', 0.5, [['c0', 'i0'], ['A0', 'B0']])
R22_aixy  = op.initialize_stoperator('R22_aixy', 0.5, [['A1', 'B1'], ['c1', 'i1']])
R22D_aixy = op.initialize_stoperator('R22D_aixy', 0.5, [['c1', 'i1'], ['A1', 'B1']])

   
# let me try to reproduce the trans-correlated Hamiltonian
# for ground state first (used in Shiozaki's paper!)
 
# 1.  [H1, R2-R2+] == [H1, R2] - [H1,R2+]
#                       a)        b)
# a)
H1_R2  = final_expressions([H1, R2], 'H1_R2', False)
# b)
H1_R2D  = final_expressions([H1, R2D], 'H1_R2D', False)

# 2.  1/2 * [[F1, R2-R2+], R2-R2+] ==  1/2 * ([[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+])
#                                                  a)               b)                c)              d)
# a)
F1_R2_R2 = final_expressions([F1, R2, R22], 'F1_R2_R2', False)
# b)
F1_R2_R2D = final_expressions([F1, R2, R22D], 'F1_R2_R2D', False)
# c)
F1_R2D_R2 = final_expressions([F1, R2D, R22], 'F1_R2D_R2', False)
# d)
F1_R2D_R2D = final_expressions([F1, R2D, R22D], 'F1_R2D_R2D', False)

# 3.  [V2, R2-R2+] == [V2,R2] - [V2,R2+]
#                       a)        b)
# a)
V2_R2  = final_expressions([V2, R2], 'V2_R2', False)
# b)
V2_R2D  = final_expressions([V2, R2D], 'V2_R2D', False)

# Additional terms to dress for excited states

# 4.  [H1, R1-R1+] == [H1, R1] - [H1,R1+]
#                       a)        b)
# 4 a)
H1_R1  = final_expressions([H1, R1], 'H1_R1')
# 4 b)
H1_R1D = final_expressions([H1, R1D], 'H1_R1D')

# 5.  [V2, R1-R1+] == [V2, R1] - [V2,R1+]
#                       a)        b)
# 5 a)
V2_R1 = final_expressions([V2, R1], 'V2_R1')
# 5 b)
V2_R1D = final_expressions([V2, R1D], 'V2_R1D')

# 6.  1/2 * [[F1, R1-R1+], R1-R1+] ==  1/2 * ([[F1, R1], R1] - [[F1, R1], R1+] - [[F1,R1+],R1] + [F1,R1+],R1+])
#                                                  a)               b)                c)              d)
# 6 a)
F1_R1_R1 = final_expressions([F1, R1, R11], 'F1_R1_R1')
# 6 b)
F1_R1_R1D = final_expressions([F1, R1, R11D], 'F1_R1_R1D')
# 6 c)
F1_R1D_R1 = final_expressions([F1, R1D, R11], 'F1_R1D_R1')
# 6 d)
F1_R1D_R1D = final_expressions([F1, R1D, R11D], 'F1_R1D_R1D')

# 7.  [H1, R2_abxy-R2_abxy+] == [H1, R2_abxy] - [H1,R2_abxy+]
#                                       a)        b)
# R2_abxy terms: Singles commutator
# 7 a)
H1_R2_abxy  = final_expressions([H1, R2_abxy], 'H1_R2_abxy')
# 7 b)
H1_R2D_abxy  = final_expressions([H1, R2D_abxy], 'H1_R2D_abxy')

# 8.  [V2, R2_abxy-R2_abxy+] == [V2, R2_abxy] - [V2,R2_abxy+]
#                                       a)        b)
# 8 a)
V2_R2_abxy  = final_expressions([V2, R2_abxy], 'V2_R2_abxy')
# 8 b)
V2_R2D_abxy  = final_expressions([V2, R2D_abxy], 'V2_R2D_abxy')

# R2 = R2_abxy
# 9.  1/2 * [[F1, R2-R2+], R2-R2+] ==  1/2 * ([[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+])
#                                                  a)               b)                c)              d)
# 9 a)
# R2_abxy terms: Double commutator
F1_R2_abxy_R2_abxy = final_expressions([F1, R2_abxy, R22_abxy], 'F1_R2_abxy_R2_abxy')
# 9 b)
F1_R2_abxy_R2D_abxy = final_expressions([F1, R2_abxy, R22D_abxy], 'F1_R2_abxy_R2D_abxy')
# 9 c)
F1_R2D_abxy_R2_abxy = final_expressions([F1, R2D_abxy, R22_abxy], 'F1_R2D_abxy_R2_abxy')
# 9 d)
F1_R2D_abxy_R2D_abxy = final_expressions([F1, R2D_abxy, R22D_abxy], 'F1_R2D_abxy_R2D_abxy')

# Note: 9a-9d won't contribute anything!!!

# 10.  [H1, R2_aixy-R2_aixy+] == [H1, R2_aixy] - [H1,R2_aixy+]
#                                       a)        b)
# R2_aixy terms: Singles commutator
# 10 a)
H1_R2_aixy  = final_expressions([H1, R2_abxy], 'H1_R2_abxy')
# 10 b)
H1_R2D_aixy  = final_expressions([H1, R2D_abxy], 'H1_R2D_abxy')

# 11.  [V2, R2_aixy-R2_aixy+] == [V2, R2_aixy] - [V2,R2_aixy+]
#                                       a)        b)
# 11 a)
V2_R2_aixy  = final_expressions([V2, R2_aixy], 'V2_R2_aixy')
# 11 b)
V2_R2D_aixy  = final_expressions([V2, R2D_aixy], 'V2_R2D_aixy')

# R2 = R2_aixy
# 12.  1/2 * [[F1, R2-R2+], R2-R2+] ==  1/2 * ([[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+])
#                                                  a)               b)                c)              d)
# 12 a)
# R2_aixy terms: Double commutator
F1_R2_aixy_R2_aixy = final_expressions([F1, R2_aixy, R22_aixy], 'F1_R2_aixy_R2_aixy')
# 12 b)
F1_R2_aixy_R2D_aixy = final_expressions([F1, R2_aixy, R22D_aixy], 'F1_R2_aixy_R2D_aixy')
# 12 c)
F1_R2D_aixy_R2_aixy = final_expressions([F1, R2D_aixy, R22_aixy], 'F1_R2D_aixy_R2_aixy')
# 12 d)
F1_R2D_aixy_R2D_aixy = final_expressions([F1, R2D_aixy, R22D_aixy], 'F1_R2D_aixy_R2D_aixy')



f = open('test.py', 'w')
f.write('import numpy as np\n')

list_list_terms = [(H1_R2, 1.0, 'H1_R2'), (H1_R2D, -1.0, 'H1_R2D'), 
                   (F1_R2_R2, 0.5, 'F1_R2_R2'), (F1_R2_R2D, -0.5, 'F1_R2_R2D'), 
                   (F1_R2D_R2, -0.5, 'F1_R2D_R2'), (F1_R2D_R2D, 0.5, 'F1_R2D_R2D'), 
                   (V2_R2, 1.0, 'V2_R2'), (V2_R2D, -1.0, 'V2_R2D'),
                   (H1_R1, 1.0, 'H1_R1'), (H1_R1D, -1.0, 'H1_R1D'),  # yes!
                   (V2_R1, 1.0, 'V2_R1'), (V2_R1D, -1.0, 'V2_R1D'),  # yes!
                   (F1_R1_R1, 0.5, 'F1_R1_R1'), 
                   (F1_R1_R1D, -0.5, 'F1_R1_R1D'),  # yes!
                   (F1_R1D_R1, -0.5, 'F1_R1D_R1'),  # yes!
                   (F1_R1D_R1D, 0.5, 'F1_R1D_R1D'),
                   (H1_R2_abxy, 1.0, 'H1_R2_abxy'), (H1_R2D_abxy, -1.0, 'H1_R2D_abxy'),
                   (V2_R2_abxy, 1.0, 'V2_R2_abxy'), (V2_R2D_abxy, -1.0, 'V2_R2D_abxy'), # yes! 
                   (F1_R2_abxy_R2_abxy, 0.5, 'F1_R2_abxy_R2_abxy'), 
                   (F1_R2_abxy_R2D_abxy, -0.5, 'F1_R2_abxy_R2D_abxy'), 
                   (F1_R2D_abxy_R2_abxy, -0.5, 'F1_R2D_abxy_R2_abxy'), 
                   (F1_R2D_abxy_R2D_abxy, 0.5, 'F1_R2D_abxy_R2D_abxy'), 
                   (H1_R2_aixy, 1.0, 'H1_R2_aixy'), (H1_R2D_aixy, -1.0, 'H1_R2D_aixy'),
                   (V2_R2_aixy, 1.0, 'V2_R2_aixy'), (V2_R2D_aixy, -1.0, 'V2_R2D_aixy'), # yes!
                   (F1_R2_aixy_R2_aixy, 0.5, 'F1_R2_aixy_R2_aixy'), 
                   (F1_R2_aixy_R2D_aixy, -0.5, 'F1_R2_aixy_R2D_aixy'), 
                   (F1_R2D_aixy_R2_aixy, -0.5, 'F1_R2D_aixy_R2_aixy'), 
                   (F1_R2D_aixy_R2D_aixy, 0.5, 'F1_R2D_aixy_R2D_aixy')]

# list_list_terms = [(V2_R2D_aixy, -1.0, 'V2_R2D_aixy')]
# list_list_terms = [(V2_R1, 1.0, 'V2_R1')]
op.einsum_expressions(list_list_terms, f)
f.close()
