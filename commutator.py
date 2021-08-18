#in order to put it on a same footing as make_cont output, aop=aop[0]
#Incomplete 2 : when both terms of a commutator are computed, comparing and adding and subtracting should take place
# to get rid of the first term.
#Problem incomplete : in compare level 3 : in case of T1T2VD1D2, both are not permuted together. they are separate.
#Possible bug : in compare function line 58, the range of coeff starts from 0, 0 can be an X type operator
#possible porblem in change_pqr->add_dict: the coeffs can be the same then ind can be added to a different operator name like V vs T1:

import copy

#import library.print_terms as pt
#from library.print_op import print_op
#import library.make_op as make_op
#import library.change_terms as ct
#import library.class_term as class_terms
#import library as lib
#import library.compare as cpre
import multi_cont
import change_terms as ct
import print_terms as pt
import special_conditions as cond
#import class_term as class_terms
#import library.compare_envelope as cpre_env
#import library.compare_overall as cpre_env2
#import library.special_conditions as cond
#from library.compare_test import create_matrices
removed=0
dict_ind={}

def populate_dict(a,b):
    print(type(a[0]))
    print(type(b[0]))
    if a[0].kind=='StOperator':
        for item in a[0].coeff:
            dict_ind[item] = a[0].name
    if b[0].kind=='StOperator':
        for item in b[0].coeff:
            dict_ind[item] = b[0].name
    return dict_ind



#comm should accept a list of terms/Alphabet operator and list of terms/Alphabet operator.
#1-> commutator on 2-> commutator off so only 1 term on-> whether commutator is on or it is just a product
# last-> if its the outside last commutator or not (for taking the fully contracted terms)

#def comm(a,b,dict_ind,last):
def comm(a,b,last):
    on=1
    #????assume prefactor of the term to be 1
    fc=1.0
    #print 'a: ', a ,'b: ', b
    a_st = []
    a_co = []
    for item in a:
        a_st.append(item.st)
        a_co.append(item.co)
    print('a.st: ', a_st)
    print('a.co: ', a_co)
    #develop dict_ind
    if a and b:
        print('there are contractions in this commutator')
    else:
        print('there are no contractions in this commutator')
        return []

    # AK: lets comment the code below!!!

    #if type(a[0])==str and type(b[0])==str:
    #    dict_add={}
    #    #This is to store the information that this is the first contraction. (used in special_conditions.py library)
    #    #b[0]=b[0]+'Z'
    #    #a[0]=a[0]+'Z'
    #elif type(a[0]) ==str or type(b[0])==str:
    #    if type(a[0])==str:
    #        dict_add=b[0].dict_ind
    #    elif type(b[0])==str:
    #        dict_add=a[0].dict_ind
    #else :
    #    dict_add=dict(a[0].dict_ind.items()+b[0].dict_ind.items())
    ##intelligently check input
    #first_cont=0
    #if type(a[0])==str:
    #build operator
    #    a,a_dict_add=make_op.make_op(a, dict_add)
    #    #a=a[0] #refer to the header
    #    a[0].map_org=a
    # else a is a list of terms contract directly.
    #if type(b[0])==str:
    #    name2=b
    #    b,b_dict_add=make_op.make_op(b,dict_add)
    #    #b=b[0]
    #    b[0].map_org=b


    #contract a,b and store in list_terms
    st2=[]
    st1=[]
    co2=[]
    co1=[]

    f = open("tec.txt", "w")
    fptr = open("AK.txt", "w")
    print('doing contraction through multi_cont')
    for t1 in a:
        for t2 in b:
            print('t1.st')
            print(t1.st)
            print('t1.co')
            print(t1.co) 
            print('t2.st')
            print(t2.st)
            print('t2.co')
            print(t2.co) 
            #print('type(t1.st)')
            #print(type(t1.st))
            stt,cot=multi_cont.multi_cont(t1.st,t2.st,t1.co,t2.co, f, fptr)
            #print('stt')
            #print(stt)
            #print('cot')
            #print(cot) 
            #print('type(t1.st[0][0])')
            #print(type(t1.st[0][0]))
            #print('type(t1.co)')
            #print(type(t1.co))
            #print('type(t1.co[0][0])')
            #print(type(t1.co[0][0]))

	    #COMMUTATOR CONDITION : removing element where length of input operator strings =
	    #length of output operator string
            for (term,termco) in zip(stt,cot):
                #lib.print_op.print_op(term,termco)
                present_op=0
                present_op1=0
                present_op2=0
                removed=0
                for op in term:
                    for op1 in t1.st[0]:
                        for op2 in t2.st[0]:
                            #print 'op'
                            #print op
                            #print 'op1'
                            #print op1
                            #print 'op2'
                            #print op2
                            if op.kind=='op' and op1.kind=='op' and op2.kind=='op' and len(op.upper)==(len(op1.upper)+len(op2.upper)):
                                print('there is a problem here', op.kind, len(op.upper),len(op1.upper),len(op2.upper))
                                removed=1
                                stt.remove(term)
                                cot.remove(termco)
                            if op2.kind=='op':
                                present_op2=1
                        if op1.kind=='op':
                            present_op1=1
                    if op.kind=='op':
                        present_op2=1
                if present_op1==0 or present_op2==0:
                    if removed==0:
                        #print('here in fully contracted')
                        stt.remove(term)
                        cot.remove(termco)
            #print('length of output string', len(stt))
            st1.extend(stt)
            co1.extend(cot)
            #print('st1')
            #print(st1)
            #print('co1')
            #print(co1) 

    #contract b,a and store in list_terms if on is 1 (commutator working)
    if on ==1:
        for t1 in b:
            for t2 in a:
                print('t1.st')
                print(t1.st) 
                print('t1.co')
                print(t1.co) 
                print('t2.st')
                print(t2.st) 
                print('t2.co')
                print(t2.co) 
                stt,cot=multi_cont.multi_cont(t1.st,t2.st,t1.co,t2.co, f, fptr)
                #print('stt')
                #print(stt)
                #print('cot')
                #print(cot) 
                for (term,termco) in zip(stt,cot):
                    #print 'new term'
                    present_op=0
                    present_op1=0
                    present_op2=0
                    removed=0
                    for op in term:
                        for op1 in t1.st[0]:
                            for op2 in t2.st[0]:
                                if op.kind=='op' and op1.kind=='op' and op2.kind=='op' and len(op.upper)==(len(op1.upper)+len(op2.upper)):
                                    print('there is a problem here', op.kind, len(op.upper),len(op1.upper),len(op2.upper))
                                    stt.remove(term)
                                    cot.remove(termco)
                                    removed=1
                                if op2.kind=='op':
                                    present_op2=1
                            if op1.kind=='op':
                                present_op1=1
                        if op.kind=='op':
                            present_op2=1
                    if  present_op1==0 or present_op2==0:
                        if removed==0:	
                            # print 'here in fully contracted'
                            stt.remove(term)
                            cot.remove(termco)
                #print 'length of output string', len(stt)
                st2.extend(stt)
                co2.extend(cot)
        #lib.print_op.print_op(st2,co2)
        #print('st2')
        #print(st2)
        #print('co2')
        #print(co2) 
    elif on!=0:
        print('error in commutator input on switch-------------------')
    
    f.close()
    fptr.close()

    #if last!=0:
	#fc=last
    #make terms of st and co and list of terms
    #print('a[0].map_org[0]')
    #print(a[0].map_org[0])
    #print('b[0].map_org[0]')
    #print(b[0].map_org[0])

## AK : I am commenting out these terms for now!
## Let me get the mult_cont function to return things correctly for now!


    # AK: lets populate dict_ind here!
    dict_ind = populate_dict(a,b)
    print('--------------------------------------------------------')
    print(dict_ind)
    list_terms=ct.change_terms1(st1,co1,last,dict_ind, a[0].map_org+b[0].map_org)#Problem : how to make lou?

    #print('list_terms after change_terms1 function called')
    #print(list_terms) 
    #pt.print_terms(list_terms,'latex_terms.txt')
    
    #print len(list_terms)
    if on==1:
        terms_tmp=ct.change_terms1(st2,co2,last,dict_ind, b[0].map_org+a[0].map_org)
        for item in terms_tmp:
            item.fac=item.fac*-1.0
            item.co[0][0]=item.co[0][0]*-1.0
        list_terms.extend(terms_tmp)

    #pt.print_terms(list_terms,'latex_terms.txt')

    
    for item in list_terms:
        item.compress()
        item.build_map_org()
        #item.cond_cont(item.dict_ind) only for CCSD noy for general case
    #print('after compress')
    #pt.print_terms(list_terms,'latex_terms.txt')

    if last!=0:
        #Special condition- when there are atlaest three operators, atleast two are equivalent and one of them is not contracting with a previous
        #..chunk of operators (H in the case of 3 commutators.
        list_terms=cond.startequiv_cond(list_terms)

    #pt.print_terms(list_terms,filename)
   
   # this actually happens inside compare_envelope function,
   # but since I am not using it right now, let me put that code 
   # explicitly here!
    for term in list_terms:
        if len(term.coeff_list)==len(term.map_org)+1:
            #print 'deleting operator coeff'
            term.coeff_list.pop()

    #pt.print_terms(list_terms,filename)
    

    #for term in list_terms:
    #    #print(type(term))
    #    #print(type(term.st[0][0]))
    #    #print(type(term.st[0][1]))
    #    print ((term.st))
    #    print ((term.sum_list))
    #    print ((term.coeff_list))
    #    print ((term.large_op_list))
    
    '''
    for term in list_terms:
            create_matrices(term)
    cpre_env2.compare_envelope(list_terms, fc, last)    
    list_terms=pt.clean_list(list_terms)
    pt.print_terms(list_terms,'latex_terms.txt')



    for term in list_terms:
	term.co[0][0]=term.fac
    #pt.print_terms(list_terms,'latex_terms.txt')
    #print 'length of list_terms passed', len(list_terms)
    '''
    return list_terms



# Some examples below, I guess??

'''
comm(['X1'],comm(comm(['V2'],['T1'],1,0),['T11'],1,0),0,1)
comm(['X1'],comm(comm(['V2'],['D1'],1,0),['T11'],1,0),0,1)
comm(['X1'],comm(comm(['V2'],['T1'],1,0),['D11'],1,0),0,1)
comm(['X1'],comm(comm(['V2'],['D1'],1,0),['D11'],1,0),0,1)
'''
#'''
#comm(comm(['V2'],['T1'],1,0),['T11'],1,1)
#comm(comm(['V2'],['D1'],1,0),['T11'],1,1)
#comm(comm(['V2'],['T1'],1,0),['D11'],1,1)
#comm(comm(['V2'],['D1'],1,0),['D11'],1,1)
#'''
# Only test case at the moment is this commutator being computed.
#comm(['V2'],['T2'],1,1)
'''
comm(['X2'], comm(['V2'],['D1'],1,0),0,1)

comm(['X2'], comm(['V2'],['T2'],1,0),0,1)
comm(['X2'], comm(['V2'],['D2'],1,0),0,1)
'''
