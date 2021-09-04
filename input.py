import func_ewt
import operators as op
from commutator import comm
import print_terms as pt
from class_term import get_parameters

func = func_ewt

# let me try to reproduce the trans-correlated Hamiltonian
# for ground state first (used in Shiozaki's paper!)
# lets define all the operators here!


F1   = op.initialize_stoperator('F1', 1.0, [['p0'], ['q0']])
V2   = op.initialize_stoperator('V2', 0.5, [['p0', 'q0'], ['r0', 's0']])
R2   = op.initialize_stoperator('R2', 0.5, [['A0', 'B0'], ['i0', 'j0']])
R22  = op.initialize_stoperator('R22', 0.5, [['A1', 'B1'], ['i1', 'j1']])
R2D  = op.initialize_stoperator('R2D', 0.5, [['i0', 'j0'], ['A0', 'B0']])
R22D = op.initialize_stoperator('R22D', 0.5, [['i1', 'j1'], ['A1', 'B1']])

f = open('final_hamiltonian.py', 'w')
f.write('import numpy as np\n')
f.write('import input_parameters as inp\n')
f.write('\n\n# Getting parameters!\n\n')
get_parameters(f)


# 1.  [F1, R2-R2+] == [F1, R2] - [F1,R2+] 
#                        a)        b)

# a)

F1R2 = comm([F1], [R2], 1)
pt.print_terms(F1R2, 'F1R2.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1R2)
pt.print_terms(F1R2, 'F1R2_new.txt')


# # b)

F1R2D = comm([F1], [R2D], 1)
pt.print_terms(F1R2D, 'F1R2D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1R2D)
pt.print_terms(F1R2D, 'F1R2D_new.txt')


# 2.  [[F1, R2-R2+], R2-R2+] ==  [[F1, R2], R2] - [[F1, R2], R2+] - [[F1,R2+],R2] + [F1,R2+],R2+]
#                                       a)               b)               c)             d)

# a)

F1R2R2 = comm(comm([F1], [R2], 0), [R22], 1)
pt.print_terms(F1R2R2, 'F1R2R2.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1R2R2)
pt.print_terms(F1R2R2, 'F1R2R2_new.txt')


# b)

F1R2R2D = comm(comm([F1], [R2], 0), [R22D], 1)
pt.print_terms(F1R2R2D, 'F1R2R2D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1R2R2D)
pt.print_terms(F1R2R2D, 'F1R2R2D_new.txt')


# c)

F1R2DR2 = comm(comm([F1], [R2D], 0), [R22], 1)
pt.print_terms(F1R2DR2, 'F1R2DR2.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1R2DR2)
pt.print_terms(F1R2DR2, 'F1R2DR2_new.txt')


# d)

F1R2DR2D = comm(comm([F1], [R2D], 0), [R22D], 1)
pt.print_terms(F1R2DR2D, 'F1R2DR2D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(F1R2DR2D)
pt.print_terms(F1R2DR2D, 'F1R2DR2D_new.txt')


# 3.  [V2, R2-R2+] == [V2,R2] - [V2,R2+]
#                       a)        b)

# a)

V2R2 = comm([V2], [R2], 1)
pt.print_terms(V2R2, 'V2R2.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2R2)
pt.print_terms(V2R2, 'V2R2_new.txt')


# b)

V2R2D = comm([V2], [R2D], 1)
pt.print_terms(V2R2D, 'V2R2D.txt')
print('Simplification for HF ref:')
op.simplify_for_HF(V2R2D)
pt.print_terms(V2R2D, 'V2R2D_new.txt')


# Write all the terms to the file in
# the einsum routine
list_list_terms = [F1R2, F1R2D, F1R2R2, F1R2R2D, F1R2DR2, F1R2DR2D, V2R2, V2R2D]
f.write('\n\n# Allocating shapes and memory!!\n\n')
op.allocate_memory(list_list_terms, f)
f.write('\n\n# Einsum expressions!!\n\n')
op.einsum_expressions(list_list_terms, f)

# Append all this in the einsum notation to
# the main file final_hamiltonian.py
# of course after resolving the CABS logic!!!
f.close()
