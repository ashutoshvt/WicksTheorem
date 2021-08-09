# Here I should define the standard operators (need to define the class) and call 
# the ewt function on top!
# pass commutator as an arg to the function
# get the list of contracted objects 
# process the above list to generate final programmable equations!
# lets do this for every form of A operator separately
# the problem is double commutator, I think I need to borrow Ayush's 
# commutator function and make it work!! 
# So this should be very similar to commutator.py but I need to define a 
# standard operator class and use it to initialize standard operators in 
# the input file and not pre-define them!
# Ok, lets begin then!

import func_ewt
func=func_ewt
import operators as op
import commutator as comm


list_oper = []
dict_index = {}

# Define V2 Operator! wrap below in a function later!
prefac=1.0/2.0
summ  =  ['p0','q0','r0','s0']
coeff =  ['p0','q0','r0','s0']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['p0','q0']
opp.lower = ['r0','s0']
dict_index['p0'] = 'V2'
dict_index['q0'] = 'V2'
dict_index['r0'] = 'V2'
dict_index['s0'] = 'V2'
stp=[[opp]]
co=[[1,1]]
V2 = op.StOperator('V2',prefac, summ, coeff, stp, co)
list_oper.append(V2)


# Define T1 Operator! 
prefac=1.0
summ  =  ['a0','i0']
coeff =  ['a0','i0']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['a0']
opp.lower = ['i0']
dict_index['a0'] = 'T1'
dict_index['i0'] = 'T1'
stp=[[opp]]
co=[[1,1]]
T1 = op.StOperator('T1',prefac, summ, coeff, stp, co)
list_oper.append(T1)

# call commutator function now with V2,T1
print'case of [V,T1]'
list_terms=comm.comm([V2],[T1],1)
