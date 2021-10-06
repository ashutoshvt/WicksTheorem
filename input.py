import func_ewt
import operators as op
from commutator import comm
import print_terms as pt

func = func_ewt

# let me try to reproduce the trans-correlated Hamiltonian
# for ground state first (used in Shiozaki's paper!)
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



# 1.  [H1, R2-R2+] == [H1, R2] - [H1,R2+]
#                       a)        b)

# a)

H1_R2 = comm([H1], [R2], 1)
pt.print_terms(H1_R2, 'H1R2.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(H1_R2)
pt.print_terms(H1_R2, 'H1R2_new.txt')
H1_R2 = op.three_body_decompose(H1_R2)
pt.print_terms(H1_R2, 'H1_R2_3body.txt')
H1_R2 = op.simplify_three_body_HF(H1_R2)
pt.print_terms(H1_R2, 'H1_R2_3body_simplified.txt')


# b)

H1_R2D = comm([H1], [R2D], 1)
pt.print_terms(H1_R2D, 'H1R2D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(H1_R2D)
pt.print_terms(H1_R2D, 'H1R2D_new.txt')
H1_R2D = op.three_body_decompose(H1_R2D)
pt.print_terms(H1_R2D, 'H1_R2D_3body.txt')
H1_R2D = op.simplify_three_body_HF(H1_R2D)
pt.print_terms(H1_R2D, 'H1_R2D_3body_simplified.txt')


# 2.  1/2 * [[F1, R2-R2+], R2-R2+] ==  1/2 * ([[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+])
#                                                  a)               b)                c)              d)

# a)

F1_R2_R2 = comm(comm([F1], [R2], 0), [R22], 1)
pt.print_terms(F1_R2_R2, 'F1R2R2.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2_R2)
pt.print_terms(F1_R2_R2, 'F1R2R2_new.txt')
F1_R2_R2 = op.three_body_decompose(F1_R2_R2)
pt.print_terms(F1_R2_R2, 'F1_R2_R2_3body.txt')
F1_R2_R2 = op.simplify_three_body_HF(F1_R2_R2)
pt.print_terms(F1_R2_R2, 'F1_R2_R2_3body_simplified.txt')


# b)

F1_R2_R2D = comm(comm([F1], [R2], 0), [R22D], 1)
pt.print_terms(F1_R2_R2D, 'F1R2R2D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2_R2D)
pt.print_terms(F1_R2_R2D, 'F1R2R2D_new.txt')
F1_R2_R2D = op.three_body_decompose(F1_R2_R2D)
pt.print_terms(F1_R2_R2D, 'F1_R2_R2D_3body.txt')
F1_R2_R2D = op.simplify_three_body_HF(F1_R2_R2D)
pt.print_terms(F1_R2_R2D, 'F1_R2_R2D_3body_simplified.txt')


# c)

F1_R2D_R2 = comm(comm([F1], [R2D], 0), [R22], 1)
pt.print_terms(F1_R2D_R2, 'F1R2DR2.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2D_R2)
pt.print_terms(F1_R2D_R2, 'F1R2DR2_new.txt')
F1_R2D_R2 = op.three_body_decompose(F1_R2D_R2)
pt.print_terms(F1_R2D_R2, 'F1_R2D_R2_3body.txt')
F1_R2D_R2 = op.simplify_three_body_HF(F1_R2D_R2)
pt.print_terms(F1_R2D_R2, 'F1_R2D_R2_3body_simplified.txt')



# d)

F1_R2D_R2D = comm(comm([F1], [R2D], 0), [R22D], 1)
pt.print_terms(F1_R2D_R2D, 'F1R2DR2D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2D_R2D)
pt.print_terms(F1_R2D_R2D, 'F1R2DR2D_new.txt')
F1_R2D_R2D = op.three_body_decompose(F1_R2D_R2D)
pt.print_terms(F1_R2D_R2D, 'F1_R2D_R2D_3body.txt')
F1_R2D_R2D = op.simplify_three_body_HF(F1_R2D_R2D)
pt.print_terms(F1_R2D_R2D, 'F1_R2D_R2D_3body_simplified.txt')


# 3.  [V2, R2-R2+] == [V2,R2] - [V2,R2+]
#                       a)        b)

# a)

V2_R2 = comm([V2], [R2], 1)
pt.print_terms(V2_R2, 'V2R2.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2_R2)
pt.print_terms(V2_R2, 'V2R2_new.txt')
V2_R2 = op.three_body_decompose(V2_R2)
pt.print_terms(V2_R2, 'V2_R2_3body.txt')
V2_R2 = op.simplify_three_body_HF(V2_R2)
pt.print_terms(V2_R2, 'V2_R2_3body_simplified.txt')


# b)

V2_R2D = comm([V2], [R2D], 1)
pt.print_terms(V2_R2D, 'V2R2D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2_R2D)
pt.print_terms(V2_R2D, 'V2R2D_new.txt')
V2_R2D = op.three_body_decompose(V2_R2D)
pt.print_terms(V2_R2D, 'V2_R2D_3body.txt')
V2_R2D = op.simplify_three_body_HF(V2_R2D)
pt.print_terms(V2_R2D, 'V2_R2D_3body_simplified.txt')


# Write all the terms to the file in
# the einsum routine

# list_list_terms = [F1_R2_R2D]
# list_list_terms = [F1_R2_R2D, F1_R2D_R2]
# list_list_terms = [V2_R2]
# list_list_terms = [(H1_R2, 1.0)]
# list_list_terms = [(H1_R2, 1.0), (H1_R2D, -1.0)]
# list_list_terms = [(V2_R2, 1.0), (V2_R2D, -1.0)]
# list_list_terms = [(V2_R2D, -1.0)]

#f = open('final_hamiltonian.py', 'w')
#f = open('test1.py', 'w')
#f.write('import numpy as np\n')
#list_list_terms = [(H1_R2, 1.0, 'H1_R2'), (H1_R2D, -1.0, 'H1_R2D'), (F1_R2_R2, 0.5, 'F1_R2_R2'),
#                   (F1_R2_R2D, -0.5, 'F1_R2_R2D'), (F1_R2D_R2, -0.5, 'F1_R2D_R2'),
#                   (F1_R2D_R2D, 0.5, 'F1_R2D_R2D'), (V2_R2, 1.0, 'V2_R2'), (V2_R2D, -1.0, 'V2_R2D')]
#op.einsum_expressions(list_list_terms, f)
#f.close()


# Now, let me look at the extra terms that I need for excited states!
# 1.  [H1, R1-R1+] == [H1, R1] - [H1,R1+]
#                       a)        b)
# R1 terms: Singles commutator
# 1 a)
# ----------------------------
H1_R1 = comm([H1], [R1], 1)
pt.print_terms(H1_R1, 'H1R1.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(H1_R1)
op.excited_states_cabs_plus_to_pure_cabs(H1_R1)
op.excited_states_retain_only_one_two_cabs_amplitudes(H1_R1)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(H1_R1)
pt.print_terms(H1_R1, 'H1R1_new.txt')

# 1 b)
# ----------------------------
H1_R1D = comm([H1], [R1D], 1)
pt.print_terms(H1_R1D, 'H1R1D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(H1_R1D)
op.excited_states_cabs_plus_to_pure_cabs(H1_R1D)
op.excited_states_retain_only_one_two_cabs_amplitudes(H1_R1D)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(H1_R1D)
pt.print_terms(H1_R1D, 'H1R1D_new.txt')

# 2.  [V2, R1-R1+] == [V2, R1] - [V2,R1+]
#                       a)        b)
# 2 a)
# ----------------------------
V2_R1 = comm([V2], [R1], 1)
pt.print_terms(V2_R1, 'V2R1.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2_R1)
op.excited_states_cabs_plus_to_pure_cabs(V2_R1)
op.excited_states_retain_only_one_two_cabs_amplitudes(V2_R1)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(V2_R1)
pt.print_terms(V2_R1, 'V2R1_new.txt')

# 2 b)
# ----------------------------
V2_R1D = comm([V2], [R1D], 1)
pt.print_terms(V2_R1D, 'V2R1D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2_R1D)
op.excited_states_cabs_plus_to_pure_cabs(V2_R1D)
op.excited_states_retain_only_one_two_cabs_amplitudes(V2_R1D)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(V2_R1D)
pt.print_terms(V2_R1D, 'V2R1D_new.txt')

# 3.  1/2 * [[F1, R1-R1+], R1-R1+] ==  1/2 * ([[F1, R1], R1] - [[F1, R1], R1+] - [[F1,R1+],R1] + [F1,R1+],R1+])
#                                                  a)               b)                c)              d)
# 3 a)
# ----------------------------
# R1 terms: Double commutator
F1_R1_R1 = comm(comm([F1], [R1], 0), [R11], 1)
pt.print_terms(F1_R1_R1, 'F1R1R1.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R1_R1)
op.excited_states_cabs_plus_to_pure_cabs(F1_R1_R1)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R1_R1)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R1_R1)
pt.print_terms(F1_R1_R1, 'F1R1R1_new.txt')

# 3 b)
# ----------------------------
F1_R1_R1D = comm(comm([F1], [R1], 0), [R11D], 1)
pt.print_terms(F1_R1_R1D, 'F1R1R1D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R1_R1D)
op.excited_states_cabs_plus_to_pure_cabs(F1_R1_R1D)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R1_R1D)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R1_R1D)
pt.print_terms(F1_R1_R1D, 'F1R1R1D_new.txt')

# 3 c)
# ----------------------------
F1_R1D_R1 = comm(comm([F1], [R1D], 0), [R11], 1)
pt.print_terms(F1_R1D_R1, 'F1R1DR1.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R1D_R1)
op.excited_states_cabs_plus_to_pure_cabs(F1_R1D_R1)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R1D_R1)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R1D_R1)
pt.print_terms(F1_R1D_R1, 'F1R1DR1_new.txt')

# 3 d)
# ----------------------------
F1_R1D_R1D = comm(comm([F1], [R1D], 0), [R11D], 1)
pt.print_terms(F1_R1D_R1D, 'F1R1DR1D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R1D_R1D)
op.excited_states_cabs_plus_to_pure_cabs(F1_R1D_R1D)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R1D_R1D)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R1D_R1D)
pt.print_terms(F1_R1D_R1D, 'F1R1DR1D_new.txt')

# 4.  [H1, R2_abxy-R2_abxy+] == [H1, R2_abxy] - [H1,R2_abxy+]
#                       a)        b)
# R2_abxy terms: Singles commutator
# 4 a)
# ----------------------------
H1_R2_abxy = comm([H1], [R2_abxy], 1)
pt.print_terms(H1_R2_abxy, 'H1R2abxy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(H1_R2_abxy)
op.excited_states_cabs_plus_to_pure_cabs(H1_R2_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes(H1_R2_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(H1_R2_abxy)
pt.print_terms(H1_R2_abxy, 'H1R2abxy_new.txt')

# 4 b)
# ----------------------------
H1_R2D_abxy = comm([H1], [R2D_abxy], 1)
pt.print_terms(H1_R2D_abxy, 'H1R2Dabxy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(H1_R2D_abxy)
op.excited_states_cabs_plus_to_pure_cabs(H1_R2D_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes(H1_R2D_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(H1_R2D_abxy)
pt.print_terms(H1_R2D_abxy, 'H1R2Dabxy_new.txt')

# 5.  [V2, R2_abxy-R2_abxy+] == [V2, R2_abxy] - [V2,R2_abxy+]
#                                       a)        b)
# 5 a)
# ----------------------------
V2_R2_abxy = comm([V2], [R2_abxy], 1)
pt.print_terms(V2_R2_abxy, 'V2R2abxy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2_R2_abxy)
V2_R2_abxy = op.three_body_decompose(V2_R2_abxy)
pt.print_terms(V2_R2_abxy, 'V2R2abxy_3body.txt')
V2_R2_abxy = op.simplify_three_body_HF(V2_R2_abxy)
pt.print_terms(V2_R2_abxy, 'V2R2abxy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(V2_R2_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes(V2_R2_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(V2_R2_abxy)
pt.print_terms(V2_R2_abxy, 'V2R2abxy_new.txt')

# 5 b)
# ----------------------------
V2_R2D_abxy = comm([V2], [R2D_abxy], 1)
pt.print_terms(V2_R2D_abxy, 'V2R2Dabxy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2_R2D_abxy)
V2_R2D_abxy = op.three_body_decompose(V2_R2D_abxy)
pt.print_terms(V2_R2D_abxy, 'V2R2Dabxy_3body.txt')
V2_R2D_abxy = op.simplify_three_body_HF(V2_R2D_abxy)
pt.print_terms(V2_R2D_abxy, 'V2R2Dabxy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(V2_R2D_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes(V2_R2D_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(V2_R2D_abxy)
pt.print_terms(V2_R2D_abxy, 'V2R2Dabxy_new.txt')

# R2 = R2_abxy
# 6.  1/2 * [[F1, R2-R2+], R2-R2+] ==  1/2 * ([[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+])
#                                                  a)               b)                c)              d)
# 6 a)
# R2_abxy terms: Double commutator
# ----------------------------

F1_R2_abxy_R2_abxy = comm(comm([F1], [R2_abxy], 0), [R22_abxy], 1)
pt.print_terms(F1_R2_abxy_R2_abxy, 'F1R2abxyR2abxy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2_abxy_R2_abxy)
F1_R2_abxy_R2_abxy = op.three_body_decompose(F1_R2_abxy_R2_abxy)
pt.print_terms(F1_R2_abxy_R2_abxy, 'F1R2abxyR2abxy_3body.txt')
F1_R2_abxy_R2_abxy = op.simplify_three_body_HF(F1_R2_abxy_R2_abxy)
pt.print_terms(F1_R2_abxy_R2_abxy, 'F1R2abxyR2abxy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(F1_R2_abxy_R2_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R2_abxy_R2_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R2_abxy_R2_abxy)
pt.print_terms(F1_R2_abxy_R2_abxy, 'F1R2abxyR2abxy_new.txt')

# 6 b)
# ----------------------------
F1_R2_abxy_R2D_abxy = comm(comm([F1], [R2_abxy], 0), [R22D_abxy], 1)
pt.print_terms(F1_R2_abxy_R2D_abxy, 'F1R2abxyR2Dabxy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2_abxy_R2D_abxy)
F1_R2_abxy_R2D_abxy = op.three_body_decompose(F1_R2_abxy_R2D_abxy)
pt.print_terms(F1_R2_abxy_R2D_abxy, 'F1R2abxyR2Dabxy_3body.txt')
F1_R2_abxy_R2D_abxy = op.simplify_three_body_HF(F1_R2_abxy_R2D_abxy)
pt.print_terms(F1_R2_abxy_R2D_abxy, 'F1R2abxyR2Dabxy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(F1_R2_abxy_R2D_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R2_abxy_R2D_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R2_abxy_R2D_abxy)
pt.print_terms(F1_R2_abxy_R2D_abxy, 'F1R2abxyR2Dabxy_new.txt')

# 6 c)
# ----------------------------
F1_R2D_abxy_R2_abxy = comm(comm([F1], [R2D_abxy], 0), [R22_abxy], 1)
pt.print_terms(F1_R2D_abxy_R2_abxy, 'F1R2DabxyR2abxy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2D_abxy_R2_abxy)
F1_R2D_abxy_R2_abxy = op.three_body_decompose(F1_R2D_abxy_R2_abxy)
pt.print_terms(F1_R2D_abxy_R2_abxy, 'F1R2DabxyR2abxy_3body.txt')
F1_R2D_abxy_R2_abxy = op.simplify_three_body_HF(F1_R2D_abxy_R2_abxy)
pt.print_terms(F1_R2D_abxy_R2_abxy, 'F1R2DabxyR2abxy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(F1_R2D_abxy_R2_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R2D_abxy_R2_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R2D_abxy_R2_abxy)
pt.print_terms(F1_R2D_abxy_R2_abxy, 'F1R2DabxyR2abxy_new.txt')

# 6 d)
# ----------------------------
F1_R2D_abxy_R2D_abxy = comm(comm([F1], [R2D_abxy], 0), [R22D_abxy], 1)
pt.print_terms(F1_R2D_abxy_R2D_abxy, 'F1R2DabxyR2Dabxy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2D_abxy_R2D_abxy)
F1_R2D_abxy_R2D_abxy = op.three_body_decompose(F1_R2D_abxy_R2D_abxy)
pt.print_terms(F1_R2D_abxy_R2D_abxy, 'F1R2DabxyR2Dabxy_3body.txt')
F1_R2D_abxy_R2D_abxy = op.simplify_three_body_HF(F1_R2D_abxy_R2D_abxy)
pt.print_terms(F1_R2D_abxy_R2D_abxy, 'F1R2DabxyR2Dabxy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(F1_R2D_abxy_R2D_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R2D_abxy_R2D_abxy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R2D_abxy_R2D_abxy)
pt.print_terms(F1_R2D_abxy_R2D_abxy, 'F1R2DabxyR2Dabxy_new.txt')

# Note: 6a-6d won't contribute anything!!!
# The only thing left is R2_aixy now!!

# 7.  [H1, R2_aixy-R2_aixy+] == [H1, R2_aixy] - [H1,R2_aixy+]
#                                       a)        b)
# R2_aixy terms: Singles commutator
# 7 a)
# ----------------------------
H1_R2_aixy = comm([H1], [R2_aixy], 1)
pt.print_terms(H1_R2_aixy, 'H1R2aixy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(H1_R2_aixy)
op.excited_states_cabs_plus_to_pure_cabs(H1_R2_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes(H1_R2_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(H1_R2_aixy)
pt.print_terms(H1_R2_aixy, 'H1R2aixy_new.txt')

# 7 b)
# ----------------------------
H1_R2D_aixy = comm([H1], [R2D_aixy], 1)
pt.print_terms(H1_R2D_aixy, 'H1R2Daixy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(H1_R2D_aixy)
op.excited_states_cabs_plus_to_pure_cabs(H1_R2D_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes(H1_R2D_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(H1_R2D_aixy)
pt.print_terms(H1_R2D_aixy, 'H1R2Daixy_new.txt')

# 8.  [V2, R2_aixy-R2_aixy+] == [V2, R2_aixy] - [V2,R2_aixy+]
#                                       a)        b)
# 8 a)
# ----------------------------
V2_R2_aixy = comm([V2], [R2_aixy], 1)
pt.print_terms(V2_R2_aixy, 'V2R2aixy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2_R2_aixy)
V2_R2_aixy = op.three_body_decompose(V2_R2_aixy)
pt.print_terms(V2_R2_aixy, 'V2R2aixy_3body.txt')
V2_R2_aixy = op.simplify_three_body_HF(V2_R2_aixy)
pt.print_terms(V2_R2_aixy, 'V2R2aixy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(V2_R2_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes(V2_R2_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(V2_R2_aixy)
pt.print_terms(V2_R2_aixy, 'V2R2aixy_new.txt')

# 8 b)
# ----------------------------
V2_R2D_aixy = comm([V2], [R2D_aixy], 1)
pt.print_terms(V2_R2D_aixy, 'V2R2Daixy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2_R2D_aixy)
pt.print_terms(V2_R2D_aixy, 'test.txt')
V2_R2D_aixy = op.three_body_decompose(V2_R2D_aixy)
pt.print_terms(V2_R2D_aixy, 'V2R2Daixy_3body.txt')
V2_R2D_aixy = op.simplify_three_body_HF(V2_R2D_aixy)
pt.print_terms(V2_R2D_aixy, 'V2R2Daixy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(V2_R2D_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes(V2_R2D_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(V2_R2D_aixy)
pt.print_terms(V2_R2D_aixy, 'V2R2Daixy_new.txt')

# R2 = R2_aixy
# 9.  1/2 * [[F1, R2-R2+], R2-R2+] ==  1/2 * ([[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+])
#                                                  a)               b)                c)              d)
# 9 a)
# R2_aixy terms: Double commutator
# ----------------------------

F1_R2_aixy_R2_aixy = comm(comm([F1], [R2_aixy], 0), [R22_aixy], 1)
pt.print_terms(F1_R2_aixy_R2_aixy, 'F1R2aixyR2aixy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2_aixy_R2_aixy)
F1_R2_aixy_R2_aixy = op.three_body_decompose(F1_R2_aixy_R2_aixy)
pt.print_terms(F1_R2_aixy_R2_aixy, 'F1R2aixyR2aixy_3body.txt')
F1_R2_aixy_R2_aixy = op.simplify_three_body_HF(F1_R2_aixy_R2_aixy)
pt.print_terms(F1_R2_aixy_R2_aixy, 'F1R2aixyR2aixy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(F1_R2_aixy_R2_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R2_aixy_R2_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R2_aixy_R2_aixy)
pt.print_terms(F1_R2_aixy_R2_aixy, 'F1R2aixyR2aixy_new.txt')

# 9 b)
# ----------------------------
F1_R2_aixy_R2D_aixy = comm(comm([F1], [R2_aixy], 0), [R22D_aixy], 1)
pt.print_terms(F1_R2_aixy_R2D_aixy, 'F1R2aixyR2Daixy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2_aixy_R2D_aixy)
F1_R2_aixy_R2D_aixy = op.three_body_decompose(F1_R2_aixy_R2D_aixy)
pt.print_terms(F1_R2_aixy_R2D_aixy, 'F1R2aixyR2Daixy_3body.txt')
F1_R2_aixy_R2D_aixy = op.simplify_three_body_HF(F1_R2_aixy_R2D_aixy)
pt.print_terms(F1_R2_aixy_R2D_aixy, 'F1R2aixyR2Daixy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(F1_R2_aixy_R2D_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R2_aixy_R2D_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R2_aixy_R2D_aixy)
pt.print_terms(F1_R2_aixy_R2D_aixy, 'F1R2aixyR2Daixy_new.txt')

# 9 c)
# ----------------------------
F1_R2D_aixy_R2_aixy = comm(comm([F1], [R2D_aixy], 0), [R22_aixy], 1)
pt.print_terms(F1_R2D_aixy_R2_aixy, 'F1R2DaixyR2aixy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2D_aixy_R2_aixy)
F1_R2D_aixy_R2_aixy = op.three_body_decompose(F1_R2D_aixy_R2_aixy)
pt.print_terms(F1_R2D_aixy_R2_aixy, 'F1R2DaixyR2aixy_3body.txt')
F1_R2D_aixy_R2_aixy = op.simplify_three_body_HF(F1_R2D_aixy_R2_aixy)
pt.print_terms(F1_R2D_aixy_R2_aixy, 'F1R2DaixyR2aixy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(F1_R2D_aixy_R2_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R2D_aixy_R2_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R2D_aixy_R2_aixy)
pt.print_terms(F1_R2D_aixy_R2_aixy, 'F1R2DaixyR2aixy_new.txt')

# 9 d)
# ----------------------------
F1_R2D_aixy_R2D_aixy = comm(comm([F1], [R2D_aixy], 0), [R22D_aixy], 1)
pt.print_terms(F1_R2D_aixy_R2D_aixy, 'F1R2DaixyR2Daixy.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1_R2D_aixy_R2D_aixy)
F1_R2D_aixy_R2D_aixy = op.three_body_decompose(F1_R2D_aixy_R2D_aixy)
pt.print_terms(F1_R2D_aixy_R2D_aixy, 'F1R2DaixyR2Daixy_3body.txt')
F1_R2D_aixy_R2D_aixy = op.simplify_three_body_HF(F1_R2D_aixy_R2D_aixy)
pt.print_terms(F1_R2D_aixy_R2D_aixy, 'F1R2DaixyR2Daixy_3body_simplified.txt')
op.excited_states_cabs_plus_to_pure_cabs(F1_R2D_aixy_R2D_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes(F1_R2D_aixy_R2D_aixy)
op.excited_states_retain_only_one_two_cabs_amplitudes_upper_lower(F1_R2D_aixy_R2D_aixy)
pt.print_terms(F1_R2D_aixy_R2D_aixy, 'F1R2DaixyR2Daixy_new.txt')


f = open('test.py', 'w')
f.write('import numpy as np\n')

list_list_terms = [(H1_R2, 1.0, 'H1_R2'), (H1_R2D, -1.0, 'H1_R2D'), 
                   (F1_R2_R2, 0.5, 'F1_R2_R2'), (F1_R2_R2D, -0.5, 'F1_R2_R2D'), 
                   (F1_R2D_R2, -0.5, 'F1_R2D_R2'), (F1_R2D_R2D, 0.5, 'F1_R2D_R2D'), 
                   (V2_R2, 1.0, 'V2_R2'), (V2_R2D, -1.0, 'V2_R2D'),
                   (H1_R1, 1.0, 'H1_R1'), (H1_R1D, -1.0, 'H1_R1D'),
                   (V2_R1, 1.0, 'V2_R1'), (V2_R1D, -1.0, 'V2_R1D'), 
                   (F1_R1_R1, 0.5, 'F1_R1_R1'), (F1_R1_R1D, -0.5, 'F1_R1_R1D'), 
                   (F1_R1D_R1, -0.5, 'F1_R1D_R1'), (F1_R1D_R1D, 0.5, 'F1_R1D_R1D'),
                   (H1_R2_abxy, 1.0, 'H1_R2_abxy'), (H1_R2D_abxy, -1.0, 'H1_R2D_abxy'),
                   (V2_R2_abxy, 1.0, 'V2_R2_abxy'), (V2_R2D_abxy, -1.0, 'V2_R2D_abxy'), 
                   (F1_R2_abxy_R2_abxy, 0.5, 'F1_R2_abxy_R2_abxy'), 
                   (F1_R2_abxy_R2D_abxy, -0.5, 'F1_R2_abxy_R2D_abxy'), 
                   (F1_R2D_abxy_R2_abxy, -0.5, 'F1_R2D_abxy_R2_abxy'), 
                   (F1_R2D_abxy_R2D_abxy, 0.5, 'F1_R2D_abxy_R2D_abxy'), 
                   (H1_R2_aixy, 1.0, 'H1_R2_aixy'), (H1_R2D_aixy, -1.0, 'H1_R2D_aixy'),
                   (V2_R2_aixy, 1.0, 'V2_R2_aixy'), (V2_R2D_aixy, -1.0, 'V2_R2D_aixy'), 
                   (F1_R2_aixy_R2_aixy, 0.5, 'F1_R2_aixy_R2_aixy'), 
                   (F1_R2_aixy_R2D_aixy, -0.5, 'F1_R2_aixy_R2D_aixy'), 
                   (F1_R2D_aixy_R2_aixy, -0.5, 'F1_R2D_aixy_R2_aixy'), 
                   (F1_R2D_aixy_R2D_aixy, 0.5, 'F1_R2D_aixy_R2D_aixy')]

# list_list_terms = [(V2_R2D_aixy, -1.0, 'V2_R2D_aixy')]
# list_list_terms = [(V2_R1, 1.0, 'V2_R1')]
op.einsum_expressions(list_list_terms, f)
f.close()
