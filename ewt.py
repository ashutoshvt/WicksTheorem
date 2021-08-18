#Here we discuss How this program works : 

#Thing to do here : 
#take input in the form if E and change it to the operator form.
#send them to the required functionsfor making contractions



#Comments
#In case you need any information that is not here and you are feeling lazy, drop me a e-mail at ayushasthana15@gmail.com and let me help you
# So this program does 1 thing in 3 cases : It generates the Extended Wicks Theorem for 1. One unordered operator string 2. Two normal ordered operator strings and 3. Commutator of two normal ordered operator strings

#sample input for option 1 : i1j0a1b0u1v1w0x0
#sample input for option 2 : string 1 :u1v0  ; string 2 :w1x0
#sample input for option 3 : string 1 :u1v0  ; string 2 :w1x0

#Are you stuck with debugging it or want to add something? This portion will help you for the same.

#ewt.py file contains the outer outline of the program i.e it takes input of menu and strings and sends the required information to make_c function in make_c file. The purpose of this file is to : store strings; make 'full' strings of operators (of class operators) in list full; initialize required variables and send them in make_c
#make_c file has the function make_c which makes cummulants in a string. It forms all the possible arrangements of cummulants and sent them in function fix of file fix_uv.
#fix_uv file contains the function fix which fixes contractions in an operator string. It either forms a contraction and then print it in tec.txt or simply prints in tec.txt without forming contractions, as required.

import fix_uv
import func_ewt
import operators as op
import copy
import sys
from collections import deque
import make_c
fix_temp = fix_uv
func = func_ewt

# string1_upper: ex: p0q0
# string1_lower: ex: r0s0
# some menu related logic needs to change as well--> refer to ayush's code!
# for now, make menu to be 2 by default!

def ewt(string1_upper, string1_lower, string2_upper, string2_lower, f, fptr, menu='2'):
    # contracted objects and constants to be populated 
    # by make_c function
    contr_obj = []
    const_obj = [] 
    #class operator defined
    string2 = []
    string1 = []

    print('string1_upper')
    print(string1_upper)
    print('string2_upper')
    print(string2_upper)
    print('string1_lower')
    print(string1_lower)
    print('string2_lower')
    print(string2_lower)

    #class operator(object):
    #    def __init__(self, kind, dag, pos, name, st, pair, spin):
    #        self.kind = kind
    #	self.dag = dag
    #	self.pos = pos
    #	self.name = name
    #	self.string = st
    #	self.pair = pair
    #	self.spin = spin
    #    def __repr__(self):
    #	return self.name
    #
    #...........input for spin free wicks therem
    
    #print "\n Spin Free GWT\n"
    #
    ##input menu and strings
    #print "\n----------------------------------------------------------------\n    Hello, this is EWT expression generator. \n    Chose what you want to do by entering the number across the option. \n-------------------------------------------------------\n"
    #menu = raw_input("            MENU \n1 - Single string EWT generator\n2 - Two normal ordered strings EWT generator\n3 - Commutator type two string EWT generator\n")
    #if menu=='1' or menu=='2' or menu=='3':
    #    pass
    #else:
    #    print "Did you enter a number in (1, 2, 3) ? If no, kindly co-operate, I am a computer and do not understand much :(. Run Again !"
    #    sys.exit()
    #commutator=0
    #if menu == '1':
    #
    #    string1_upper = list(raw_input("Enter Operator :\nInput the upper indices of E E(a,b,c)_(e,f,g) \n(i,j..-holes; u,v...-active; a,b...-excited; 1-daggered; 0-undaggered)\nExample : uv\nOperator string: "))
    #    string1_lower = list(raw_input("input the lower indices of E E(a,b,c)_(e,f,g) \n(i,j..-holes; u,v...-active; a,b...-excited; 1-daggered; 0-undaggered)\nExample : uv\nOperator string: "))
    #elif menu=='2' or menu=='3':
    #    string1_upper = list(raw_input("Enter Operator 1 : Input the upper indices of E E(a,b,c)_(e,f,g) \n(i,j..-holes; u,v...-active; a,b...-excited; 1-daggered; 0-undaggered)\nExample : uv\nOperator string: "))
    #    string1_lower = list(raw_input("input the lower indices of E E(a,b,c)_(e,f,g) \n(i,j..-holes; u,v...-active; a,b...-excited; 1-daggered; 0-undaggered)\nExample : uv\nOperator string: "))
    #    string2_upper = list(raw_input("Enter Operator 2 : Input the upper indices of E E(a,b,c)_(e,f,g) \n(i,j..-holes; u,v...-active; a,b...-excited; 1-daggered; 0-undaggered)\nExample : uv\nOperator string: "))
    #    string2_lower = list(raw_input("input the lower indices of E E(a,b,c)_(e,f,g) \n(i,j..-holes; u,v...-active; a,b...-excited; 1-daggered; 0-undaggered)\nExample : uv\nOperator string: "))
    #else:
    #    pass
    #
    #if menu == '3':
    #    commutator = 1
    #    #string1 = list(raw_input("input the strings \n(i,j..-holes; u,v...-active; a,b...-excited; 1-daggered; 0-undaggered)\nExample : u1v0\nOperator 1: "))
    #    #string2 = list(raw_input("Operator 2: "))
    #
    ### AK Start 

    commutator = 0
    if menu == '3':
        commutator = 1

    String1=[]
    String2=[]
    #for index in range(0, len(string1_upper),2):
    #    String1.append([string1_upper[index], string1_upper[index+1]])
    #    #String1.append('1')
    #for index in range(len(string1_lower)-1, -1, -2):
    #    String1.append([string1_lower[index-1], string1_lower[index]])
    #    #String1.append('0')
    #print 'My String1'
    #print String1

    String1.append(string1_upper)
    String1.append(string1_lower[::-1])

    print('My String1')
    print(String1)

    if menu=='2' or menu=='3':
        String2.append(string2_upper)
        String2.append(string2_lower[::-1])
        print('My String2')
        print(String2)

    
    #if menu=='2' or menu=='3' :
    #    for index in range(0, len(string2_upper),2):
    #        String2.append([string2_upper[index], string2_upper[index+1]])
    #        #String2.append('1')
    #    for index in range(len(string2_lower)-1, -1, -2):
    #        String2.append([string2_lower[index-1], string2_lower[index]])
    #        #String2.append('0')
    #    print 'My String2'
    #    print String2
    
    ### AK done 
    
    #for index in range(0, len(string1_upper)):
    #    string1.append(string1_upper[index])
    #    string1.append('1')
    #for index in range(len(string1_lower)-1, -1, -1):
    #    string1.append(string1_lower[index])
    #    string1.append('0')
    #print 'Original String1'
    #print string1
    #
    #if menu=='2' or menu=='3' :
    #    for index in range(0, len(string2_upper)):
    #        string2.append(string2_upper[index])
    #        string2.append('1')
    #    for index in range(len(string2_lower)-1, -1, -1):
    #        string2.append(string2_lower[index])
    #        string2.append('0')
    #    print 'Original String2'
    #    print string2
    
    #!!!!!!!! I am fixing the commutator to 0 by force here. Remember to remove this line when incorporating the menu !!!!
    #commutator=0
    
    
    a = deque([])
    i = deque([])
    u = deque([])
    g = deque([])
    full = []
    full1 = [] #first string
    full2 = [] #second string
    full_pos = [] #positions of full
    p = 0
    spin=0
    
    ##make 3 lists : a-particle operators, i-hole operators, u-active state operators
    #for index in range(0, len(string1), 2):
    #    print('String1[index][0]')
    #    print(String1[index][0])
    #    print('String1[index+1]')
    #    print(String1[index+1])
    #    if (string1[index] == 'o' or string1[index] == 't'):
    #	x = operator('ac', string1[index+1], p+1, string1[index], 1, -1, 1)
    #	u.append(x) 
    #	full1.append(x)
    #	full.append(x)
    #	p=p+1
    #    elif (string1[index] >= 'a') and (string1[index] < 'h') :
    #	x = operator('pa', string1[index+1], p+1, string1[index], 1, -1, 1)
    #	a.append(x) 
    #	full1.append(x)
    #	full.append(x)
    #	p=p+1
    #    elif (string1[index] >= 'i') and (string1[index] < 'p') :
    #	x = operator('ho', string1[index+1], p+1, string1[index],1, -1, 1)
    #	i.append(x) 
    #	full1.append(x)
    #	full.append(x)
    #	p=p+1
    #    elif (string1[index] >='u' and string1[index]<='z'):
    #	x = operator('ac', string1[index+1], p+1, string1[index], 1, -1, 1)
    #	u.append(x) 
    #	full1.append(x)
    #	full.append(x)
    #	p=p+1
    #    elif (string1[index] >='p' and string1[index]<='s'):
    #	x = operator('ge', string1[index+1], p+1, string1[index], 1, -1, 1)
    #	i.append(x) 
    #	u.append(x) 
    #	a.append(x) 
    #	full1.append(x)
    #	full.append(x)
    #	p=p+1
    #if string2:
    #    for index in range(0, len(String2), 2):
    #        if (string2[index] == 'o' or string2[index] == 't'):
    #	    x = operator('ac', string2[index+1], p+1, string2[index], 2, -1, 1)
    #	    u.append(x) 
    #	    full2.append(x)
    #	    p=p+1
    #        elif (string2[index] >= 'a') and (string2[index] < 'h') :
    #	    x = operator('pa', string2[index+1], p+1, string2[index], 2, -1, 1)
    #	    a.append(x) 
    #	    full2.append(x)
    #	    p=p+1
    #        elif (string2[index] >= 'i') and (string2[index] < 'p') :
    #	    x = operator('ho', string2[index+1], p+1, string2[index], 2, -1, 1)
    #	    i.append(x) 
    #	    full2.append(x)
    #	    p=p+1
    #        elif (string2[index] >='u' and string2[index]<='z'):
    #	    x = operator('ac', string2[index+1], p+1, string2[index], 2, -1, 1)
    #	    u.append(x) 
    #	    full2.append(x)
    #	    p=p+1
    #        elif (string2[index] >='p' and string2[index]<='s'):
    #	    x = operator('ge', string2[index+1], p+1, string2[index], 2, -1, 1)
    #	    i.append(x) 
    #	    a.append(x) 
    #	    u.append(x) 
    #	    full2.append(x)
    #	    p=p+1
    
    # AK: Start
    #make 3 lists : a-particle operators, i-hole operators, u-active state operators
    dagger = '1'
    for item in String1:
        for item1 in item:
            print('item1')
            print(item1)
            if (item1[0] == 'o' or item1[0] == 't'):
    	        x = op.operator('ac', dagger, p+1, item1, 1, -1, 1)
    	        u.append(x) 
    	        full1.append(x)
    	        #full.append(x)
    	        p=p+1
                # Full CABS space A, B, C, D, E, F, G, H
                # These are just full virtual space
                # Breaking of A into pure virtual and pure CABS can be done later!
            #elif (((String1[index][0] >= 'a') and (String1[index][0] < 'h')) or 
            #     ((String1[index][0] >= 'A') and (String1[index][0] < 'H'))) :
            elif (((item1[0] >= 'a') and (item1[0] < 'h')) or 
                 ((item1[0] >= 'A') and (item1[0] < 'H'))) :
    	        x = op.operator('pa', dagger, p+1, item1, 1, -1, 1)
    	        a.append(x) 
    	        full1.append(x)
    	        #full.append(x)
    	        p=p+1
            elif (item1[0] >= 'i') and (item1[0] < 'p') :
    	        x = op.operator('ho', dagger, p+1, item1, 1, -1, 1)
    	        i.append(x) 
    	        full1.append(x)
    	        #full.append(x)
    	        p=p+1
            elif (item1[0] >='u' and item1[0]<='z'):
    	        x = op.operator('ac', dagger, p+1, item1, 1, -1, 1)
    	        u.append(x) 
    	        full1.append(x)
    	        #full.append(x)
    	        p=p+1
            elif (item1[0] >='p' and item1[0]<='s'):
    	        x = op.operator('ge', dagger, p+1, item1, 1, -1, 1)
                #print('x.kind')
                #print(x.kind)
                #print('x.dag')
                #print(x.dag)
                #print('x.pos')
                #print(x.pos)
    	        i.append(x) 
    	        u.append(x) 
    	        a.append(x) 
    	        full1.append(x)
    	        #full.append(x)
    	        p=p+1
        dagger = '0'

    dagger = '1'
    if String2:
        #for index in range(0, len(String2), 2):
        for item in String2:
            for item1 in item:
                #if (String2[index][0] == 'o' or String2[index][0] == 't'):
                if item1[0] == 'o' or item1[0] == 't':
    	            x = op.operator('ac', dagger, p+1, item1, 2, -1, 1)
    	            u.append(x) 
    	            full2.append(x)
    	            p=p+1
                    # Full CABS space A, B, C, D, E, F, G, H
                    # These are just full virtual space
                    # Breaking of A into pure virtual and pure CABS can be done later!
                #elif (((String2[index][0] >= 'a') and (String2[index][0] < 'h')) or 
                #     ((String2[index][0] >= 'A') and (String2[index][0] < 'H'))) :
                elif (((item1[0] >= 'a') and (item1[0] < 'h')) or 
                     ((item1[0] >= 'A') and (item1[0] < 'H'))) :
    	            x = op.operator('pa', dagger, p+1, item1, 2, -1, 1)
    	            a.append(x) 
    	            full2.append(x)
                    #print 'x.kind'
                    #print x.kind
                    #print 'x.dag'
                    #print x.dag
                    #print 'x.pos'
                    #print x.pos
    	            p=p+1
                elif (item1[0] >= 'i') and (item1[0] < 'p') :
    	            x = op.operator('ho', dagger, p+1, item1, 2, -1, 1)
    	            i.append(x) 
    	            full2.append(x)
                    #print 'x.kind'
                    #print x.kind
                    #print 'x.dag'
                    #print x.dag
                    #print 'x.pos'
                    #print x.pos
    	            p=p+1
                elif (item1[0] >='u' and item1[0] <='z'):
    	            x = op.operator('ac', dagger, p+1, item1, 2, -1, 1)
    	            u.append(x) 
    	            full2.append(x)
    	            p=p+1
                elif (item1[0] >='p' and item1[0] <='s'):
    	            x = op.operator('ge', dagger, p+1, item1, 2, -1, 1)
    	            i.append(x) 
    	            a.append(x) 
    	            u.append(x) 
    	            full2.append(x)
    	            p=p+1
            dagger = '0'
    # AK: Finished
    
    final_contr_obj=[]
    final_const_obj=[]
    
    #make list for all possible contractions for any operator
    #The commutator here is 1 when menu=3, so 2 set of terms wille be needed (commutator +1)
    for i_c in range(commutator+1):
        print('################################################')
        print('i_c')
        print(i_c)
        full = []
        full_pos = []
        store_for_repeat = []
        poss= deque([])
        y = deque([])
        if not i_c:
            full.extend(full1)
            full.extend(full2)
        else :
            for item in full1:
                item.string=2
            for item in full2:
                item.string=1
            full.extend(full2)
            full.extend(full1)
            count = 1
            for item in full:
                item.pos = count 
                count += 1
        for item in full:
            full_pos.append(item.pos)
        #----------------------------------------Pairing of the operators
        #---------------------------------------Storing the spin of the operators
        is_pair=1
        spin_tracker=0
        if is_pair:
            for index in range(len(full1)/2):
    	        full1[index].pair=full1[len(full1)-index-1].pos
    	        full1[len(full1)-index-1].pair=full1[index].pos
    	        full1[index].spin=spin_tracker
    	        full1[len(full1)-index-1].spin=spin_tracker
    	        spin_tracker=spin_tracker+1
            for index in range(len(full2)/2):
                full2[index].pair=full2[len(full2)-index-1].pos
                full2[len(full2)-index-1].pair=full2[index].pos
                full2[index].spin=spin_tracker
                full2[len(full2)-index-1].spin=spin_tracker
                spin_tracker=spin_tracker+1
    
        #-------------------------all the possible contracting operators of each operator is being sored in poss here
        #poss is a matrix 
        if menu=='1':#self normal ordering
            for operator in full:
                y = deque([])
                if operator.kind == 'pa' and operator.dag=='0':
    	            for item in a:
    	                if operator.pos<item.pos and item.dag=='1':
                            y.append(item)
                elif operator.kind == 'ho' and operator.dag=='1':
      	            for item in i:
                        if operator.pos<item.pos and item.dag=='0':
                            y.append(item)
                elif operator.kind == 'ac':  #because active states will have eta and gamma
    	            for item in u:
                        if operator.pos<item.pos and int(item.dag)!=int(operator.dag):
                            y.append(item)
                elif operator.kind == 'ge' and operator.dag=='0':
                    for item in a:
                        if operator.pos<item.pos and item.dag=='1':
                            y.append(item)
                elif operator.kind == 'ge' and operator.dag=='1':
      	            for item in i:
                        if operator.pos<item.pos and item.dag=='0':
                            y.append(item)
                if operator.kind == 'ge':  #because active states will have eta and gamma
                    for item in u:
                        if operator.pos<item.pos and int(item.dag)!=int(operator.dag) and item.kind!='ge':#ge operator already added in i and a case
                            y.append(item)
                poss.append(y) #list of list in dictionary order i.e 1st annhilation -> possible creation then 2nd ...   
        else:
            #### Need to revise this logic after consulting with Ayush!
            print('am I reaching here??')
            for operator in full:
                #print('operator.kind')
                #print(operator.kind)
                #print('operator.dag')
                #print(operator.dag)
                #print('operator.string')
                #print(operator.string)
                y = deque([])

                if operator.kind == 'pa' and operator.dag=='0': 
    	            for item in a:
                        if operator.pos<item.pos and item.dag=='1' and operator.string!=item.string:
                            y.append(item)
                elif operator.kind == 'pa' and operator.dag=='1': # AK: assuming gamma_ai == 0, will document elsewhere!
                    for item in a:
                        #print('item.string')
                        #print(item.string)
                        #print('operator.pos')
                        #print(operator.pos) 
                        #print('item.pos')
                        #print(item.pos)
                        if operator.pos<item.pos and item.dag=='0' and operator.string!=item.string:
                            y.append(item)
                elif operator.kind == 'ho' and operator.dag=='1':
      	            for item in i:
    	                if operator.pos<item.pos and item.dag=='0' and operator.string!=item.string:
                            y.append(item)
                elif operator.kind == 'ho' and operator.dag=='0':
      	            for item in i:
                        if operator.pos<item.pos and item.dag=='1' and operator.string!=item.string:
                            y.append(item)
                elif operator.kind == 'ac':  #because active states will have eta and gamma
                    for item in u:
                        if operator.pos<item.pos and int(item.dag)!=int(operator.dag) and operator.string!=item.string:
                            y.append(item)
                elif operator.kind == 'ge' and operator.dag=='0':
                    for item in a:
                        if operator.pos<item.pos and item.dag=='1' and operator.string!=item.string:
                            y.append(item)
      	            #for item in i: # AK added --> think about it later!
    	            #    if operator.pos<item.pos and item.dag=='0' and operator.string!=item.string:
                    #        y.append(item)
                elif operator.kind == 'ge' and operator.dag=='1':
                    #print('am I reaching here??')
      	            for item in i:
                        #print('item')
                        #print(item)
                        #print('item.pos')
                        #print(item.pos)
                        #print('operator.pos')
                        #print(operator.pos)
                        #print('item.dag')
                        #print(item.dag)
                        #print('item.dag')
                        #print(item.dag)
                        #print('item.string')
                        #print(item.string)
                        #print('operator.string')
                        #print(operator.string)
                        if operator.pos<item.pos and item.dag=='0' and operator.string!=item.string:
                            y.append(item)
    	            #for item in a: # AK added --> think about it later!
                    #    if operator.pos<item.pos and item.dag=='0' and operator.string!=item.string:
                    #        y.append(item)
                if operator.kind == 'ge':  #because active states will have eta and gamma
                    for item in u:
                        if operator.pos<item.pos and int(item.dag)!=int(operator.dag) and operator.string!=item.string  and item.kind!='ge':#ge operator already added in i and a case
                            y.append(item)
        #if (y): remember that empty strings are also included
                poss.append(y) #list of list in dictionary order i.e 1st annhilation -> possible creation then 2nd ...   
        no = len(full)/2
        contracted = []
        tmp_l = []
    
        #---------------------The first term of the PDF file is being printed here (not important)
    
        tmp_lower=[]
        
        if not i_c:
            if menu == '1' or menu =='2':
                tmp_l.append("Doing : Normal ordering of String\\\\")
            else :    
                tmp_l.append("Doing : Commutator expression Generation\\\\")
            tmp_l.append('Here are the operator strings : \[E^{')
            for item in full1:
                if item.dag=='1':
                    tmp_upper=item.name
                    tmp_l.append(tmp_upper)
            tmp_l.append('}_{')
            for item in full1:
                if item.dag=='0':
                    tmp_lower.append(item.name)
    
            tmp_lower=tmp_lower[::-1]
            tmp_l=tmp_l+tmp_lower
            tmp_lower=[]
            tmp_l.append('} , ')
            if menu=='2' or menu=='3':
                tmp_l.append(' E^{')
                for item in full2:
                    if item.dag=='1':
                        tmp_upper=item.name
                        tmp_l.append(tmp_upper)
                tmp_l.append('}_{')
                for item in full2:
    	            if item.dag=='0':
                        tmp_lower.append(item.name)
                tmp_lower=tmp_lower[::-1]
                tmp_l=tmp_l+tmp_lower
                tmp_lower=[]
                tmp_l.append('}')
    
    
            tmp_l.append('\]')
            tmp_6 = "Equation : "+'$$'+''.join(tmp_l)+'\\\\'+'$$'+'\n'+"Answer :\n"
            f.write(tmp_6)
            fptr.write(tmp_6)
        if not i_c and commutator:
            f.write("\nThis is where the first terms start\\\\\n")
            fptr.write("\nThis is where the first terms start\\\\\n")
        elif commutator : 
            f.write("\nThis is where the second terms start\\\\\n")
            fptr.write("\nThis is where the second terms start\\\\\n")
        print('a i u full poss full_pos')
        print(a, i, u, full, poss, full_pos)
        contr_obj = []
        const_obj = [] 
        make_c.make_c(len(full), contracted, a, i, u, full, poss, f, fptr, store_for_repeat, full_pos, i_c, menu, contr_obj, const_obj)
        print('contr_obj')
        print(contr_obj)
        print('const_obj')
        print(const_obj)
        final_contr_obj.append(contr_obj)
        final_const_obj.append(const_obj)
    print("\n-------------------------------------------------------------------------------------\n     ITS DONE :D Have a look at the tec.txt file !\n     !!CHEERS !!")
    #f.close()
    #fptr.close()
    
    print('final contr_obj')
    print(final_contr_obj)
    print('final_const_obj')
    print(final_const_obj)
    return final_contr_obj[0], final_const_obj[0]
