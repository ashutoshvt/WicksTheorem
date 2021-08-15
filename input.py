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
from commutator import comm
import print_terms as pt


list_oper_A = []
list_oper_B = []
list_oper_C = []

## Define V2 Operator! wrap below in a function later!
'''
prefac=0.5
summ  =  ['p0','q0','r0','s0']
coeff =  ['p0','q0','r0','s0']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['p0','q0']
opp.lower = ['r0','s0']
stp=[[opp]]
co=[[1,1]]
V2 = op.StOperator('V2',prefac, summ, coeff, stp, co)
list_oper_A.append(V2)
V2.map_org=list_oper_A
'''

# Define F1 Operator! 

prefac=1.0
summ  =  ['p0','q0']
coeff =  ['p0','q0']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['p0']
opp.lower = ['q0']
stp=[[opp]]
co=[[1,1]]
F1 = op.StOperator('F1',prefac, summ, coeff, stp, co)
list_oper_A.append(F1)
F1.map_org=list_oper_A


# Define F11 Operator! 
'''
prefac=1.0
summ  =  ['r0','s0']
coeff =  ['r0','s0']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['r0']
opp.lower = ['s0']
stp=[[opp]]
co=[[1,1]]
F11 = op.StOperator('F11',prefac, summ, coeff, stp, co)
list_oper_B.append(F11)
F11.map_org=list_oper_B
'''

# Define R1 Operator (CABS SINGLES)! 
'''
prefac=1.0
summ  =  ['A0','i0']
coeff =  ['A0','i0']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['A0']
opp.lower = ['i0']
stp=[[opp]]
co=[[1,1]]
R1 = op.StOperator('R1',prefac, summ, coeff, stp, co)
list_oper_B.append(R1)
R1.map_org=list_oper_B
'''

# Define R11 Operator (CABS SINGLES)! 
'''
prefac=1.0
summ  =  ['A1','i1']
coeff =  ['A1','i1']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['A1']
opp.lower = ['i1']
stp=[[opp]]
co=[[1,1]]
R11 = op.StOperator('R11',prefac, summ, coeff, stp, co)
list_oper_C.append(R11)
R11.map_org=list_oper_C
'''

# Define R2 Operator 

prefac=0.5
summ  =  ['A0','B0','i0','j0']
coeff  =  ['A0','B0','i0','j0']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['A0','B0']
opp.lower = ['i0','j0']
stp=[[opp]]
co=[[1,1]]
R2 = op.StOperator('R2',prefac, summ, coeff, stp, co)
list_oper_B.append(R2)
R2.map_org=list_oper_B

# Define R22 Operator 

prefac=0.5
summ  =  ['A1','B1','i1','j1']
coeff  =  ['A1','B1','i1','j1']
opp = func_ewt.contractedobj('op', 1, 1)
opp.upper = ['A1','B1']
opp.lower = ['i1','j1']
stp=[[opp]]
co=[[1,1]]
R22 = op.StOperator('R22',prefac, summ, coeff, stp, co)
list_oper_C.append(R22)
R22.map_org=list_oper_C

# outermost commutator must be 1

#print'case of [V2,R1]'
#V2R1_SC=comm([V2],[R1],1)
#pt.print_terms(V2R1_SC,'V2R1_SC.txt')

#print'case of [V2,R2]'
#V2R2_SC=comm([V2],[R2],1)
#pt.print_terms(V2R2_SC,'V2R2_SC.txt')

#print'case of [[V2,R1],R11]'
#V2R1_DC=comm(comm([V2],[R1],0),[R11],1)
#pt.print_terms(V2R1_DC,'V2R1_DC.txt')

#print'case of [F1,R2]'
#F1R2_SC=comm([F1],[R2],1)
#pt.print_terms(F1R2_SC,'F1R2_SC.txt')

print'case of [[F1,R2],R22]'
F1R2_DC=comm(comm([F1],[R2],0), [R22],1)
pt.print_terms(F1R2_DC,'F1R2_DC.txt')

#print'case of [F1,R1]'
#F1R1_SC=comm([F1],[R1],1)
#pt.print_terms(F1R1_SC,'F1R1_SC.txt')

#print'case of [F1,F11]'
#F1F11_SC=comm([F1],[F11],1)
#pt.print_terms(F1F11_SC,'F1F11_SC.txt')

#print'case of [[F1,R1],R1]'
#F1R1_DC=comm(comm([F1],[R1],dict_index,0,'F1R1_DC.txt'), [R11],dict_index,1,'F1R1_DC.txt')
