import copy
class matrix_con(object):
    def __init__(self):
	self.upper=[]
	self.lower=[]
    def make_for(self, u, l):
	for item in u:
	    self.upper.append(u.spin)
	for item in l:
	    self.lower.append(l.spin)

def equality_check(contracted, store):
    count_eq = 0
    flag1=0
    lim_count = len(contracted)
    if len(contracted)==len(store):
	for itema in contracted:
	    for itemb in store:
	        if len(itema)==len(itemb):
		    flag1=0
		    for index in range(len(itema)):
		        if itema[index].pos!=itemb[index].pos:
		            flag1=1
		            #break
		    if flag1==0:
		        count_eq=count_eq+1
		    flag1=0
		    if count_eq == lim_count:
			return 1
    else:
	return 0
index = 0
def arrange(cum_d, cum_n, cum_d_pos, cum_n_pos):
    cum_d
    for index in range(len(cum_d)):
	for item in cum_n:
	    if cum_d[index].pair==item.pos:
		#exchange the terms in pos and main
	        swap_v = cum_n[index]
		pos_item = cum_n.index(item)
		cum_n[index]=item
		cum_n[pos_item] = swap_v

		#exchange positions
		swap_p = cum_n_pos[index]
		pos_item = cum_n_pos.index(item.pos)
		cum_n_pos[index]=item.pos
		cum_n_pos[pos_item] = swap_p







'''
def cummulant(contracted, full_formed, new_list, cumulant_present): 
    if (contracted):
        for item1 in contracted:
            cum_nord = []
            cum_norn = []
            cum_pos = []
            cum_norn1 = []
            cum_norn2 = []
            cum_norn_pos = []
            cum_norn1_pos = []
            cum_norn2_pos = []
            cum_nor_pos = []
            for item2 in item1:
                cum_pos.append(item2.pos)
                if item2.dag == '1':
                    cum_nord.append(item2)
                    cum_nor_pos.append(item2.pos)
            for item2 in item1:
                if item2.dag == '0':
                    if item2.string == 1:
                        cum_norn1_pos.append(item2.pos)
                        cum_norn1.append(item2)
                    else :
                        cum_norn2_pos.append(item2.pos)
                        cum_norn2.append(item2)
            #reverse non daggered from each string and print its name
            cum_norn1.reverse()
            cum_norn2.reverse()             
            cum_norn.extend(cum_norn1)
            cum_norn.extend(cum_norn2)
            #reverse nondaggered from each string and reverse the whole to see the sign
            cum_norn1_pos.reverse()
            cum_norn2_pos.reverse()
            cum_norn_pos.extend(cum_norn1_pos)
            cum_norn_pos.extend(cum_norn2_pos)
            
            arrange(cum_nord, cum_norn, cum_nor_pos, cum_norn_pos)
            cum_norn_pos.reverse()
            cum_nor_pos.extend(cum_norn_pos)
             
            #change operator to str
            cum_d_name = []
            cum_n_name = []
            for item in cum_nord:
                    cum_d_name.append(item.name)
            for item in cum_norn:
                    cum_n_name.append(item.name)
            cumulant_present=1
	    new_list.append('\Lambda^{'+''.join(cum_d_name)+'}_{'+''.join(cum_n_name)+'}')
            #if parity.parity(cum_nor_pos, cum_pos):
            #    sign=sign*(-1)
            full_formed.extend(cum_nor_pos)
	    return cumulant_present
'''

def list_of_excp(degree, i, j):
    excep=[]
    if degree == 2:


	a_cum = matrix_con()
	b_cum = matrix_con()
	c_cum = matrix_con()
	

	a_cum.upper = [0, 0]
	a_cum.lower = [0, 0]
	b_cum.upper = [0, 1]
	b_cum.lower = [0, 1]
	c_cum.upper = [0, 1]
	c_cum.lower = [1, 0]


	if a_cum.upper[i]!=a_cum.lower[j]:
	    excep.append('a')
	if b_cum.upper[i]!=b_cum.lower[j]:
	    excep.append('b')
	if c_cum.upper[i]!=c_cum.lower[j]:
	    excep.append('c')
	
	return excep
    else :
	return excep

def addition_matrix(degree, exceptions):
    matrix = []
    const = 1.0
    if degree == 2:
	matrix = [1, -1]
	for item in exceptions :
	    if item == 'a':
		matrix[0]-=1
		matrix[1]+=1
	    elif item == 'b':
		matrix[0]-=2
		matrix[1]-=1
	    elif item == 'c':
		matrix[0]+=2
		matrix[1]+=1
	#find GCF : not necessary in degree 2

	const = 2.0/6.0
	if matrix[1]==0 and matrix[0]!=0:
	    const=const*matrix[0]
	    matrix[0]=1
    return const, matrix
def cummulant(contracted, full_formed, new_list): 
    if (contracted):
        for item1 in contracted:
            cum_nord = []
            cum_norn = []
            cum_pos = []
            cum_norn1 = []
            cum_norn2 = []
            cum_norn_pos = []
            cum_norn1_pos = []
            cum_norn2_pos = []
            cum_nor_pos = []
            for item2 in item1:
                cum_pos.append(item2.pos)
                if item2.dag == '1':
                    cum_nord.append(item2)
                    cum_nor_pos.append(item2.pos)
            for item2 in item1:
                if item2.dag == '0':
                    if item2.string == 1:
                        cum_norn1_pos.append(item2.pos)
                        cum_norn1.append(item2)
                    else :
                        cum_norn2_pos.append(item2.pos)
                        cum_norn2.append(item2)
            #reverse non daggered from each string and print its name
            cum_norn1.reverse()
            cum_norn2.reverse()             
            cum_norn.extend(cum_norn1)
            cum_norn.extend(cum_norn2)
            #reverse nondaggered from each string and reverse the whole to see the sign
            cum_norn1_pos.reverse()
            cum_norn2_pos.reverse()
            cum_norn_pos.extend(cum_norn1_pos)
            cum_norn_pos.extend(cum_norn2_pos)
            
            arrange(cum_nord, cum_norn, cum_nor_pos, cum_norn_pos)
            cum_norn_pos.reverse()
            cum_nor_pos.extend(cum_norn_pos)


	    
	    #make matrix of contraction of cummulant
	    cum_spin=matrix_con()
            cum_d_spin = []
            cum_n_spin = []
            for item in cum_nord:
                    cum_d_spin.append(item.spin)
            for item in cum_norn:
                    cum_n_spin.append(item.spin)
	    cum_spin.upper = cum_d_spin
	    cum_spin.lower = cum_n_spin

	    print "Here is the cumulant spin list", cum_spin.upper, cum_spin.lower
            exceptions = [] #the list of the terms that do not follow the condition of the 
	    #conditions for the degree of cummulant
	    degree_cum=len(cum_spin.upper)
	    #store the terms whose summition is not required: small lambdas [01][10] kind of
	    for i in range(len(cum_spin.upper)) :
		for j in range(len(cum_spin.lower)):
		    if cum_spin.upper[i]==cum_spin.lower[j]:
			#print "I dont know whats happening"
			exceptions.extend(list_of_excp(degree_cum, i, j))
	    #do the addition matrix
	    const, value_mat = addition_matrix(degree_cum, set(exceptions))
	    print "\n\nconstand and matrix = ", const, value_mat, exceptions
            #change operator to str
            cum_d_name = []
            cum_n_name = []
            for item in cum_nord:
                    cum_d_name.append(item.name)
            for item in cum_norn:
                    cum_n_name.append(item.name)
	    if value_mat:
	        new_list.append('(')
	        if value_mat[0]==1:


	    	    new_list.append('\Lambda^{'+''.join(cum_d_name)+'}_{'+''.join(cum_n_name)+'}')
	        elif value_mat[0]>1:

	    	    new_list.append(str(value_mat[0])+'\Lambda^{'+''.join(cum_d_name)+'}_{'+''.join(cum_n_name)+'}')
	        if value_mat[0]!=0 and value_mat[1]!=0 and value_mat[1]!=-1:
		    new_list.append('+')
		cum_n_name.reverse()
	        if value_mat[1]==1:
	    	    new_list.append('\Lambda^{'+''.join(cum_d_name)+'}_{'+''.join(cum_n_name)+'}')
	        elif value_mat[1]==-1:
	    	    new_list.append('-'+'\Lambda^{'+''.join(cum_d_name)+'}_{'+''.join(cum_n_name)+'}')
	        elif abs(value_mat[1])>1:
	    	    new_list.append(str(value_mat[1])+'\Lambda^{'+''.join(cum_d_name)+'}_{'+''.join(cum_n_name)+'}')
		new_list.append(')')
	    else :
		
	    	new_list.append('\Lambda^{'+''.join(cum_d_name)+'}_{'+''.join(cum_n_name)+'}')
		
            #if parity.parity(cum_nor_pos, cum_pos):
            #    sign=sign*(-1)
            full_formed.extend(cum_nor_pos)
	    return const
	    
def normal_order(full, output, output_pos, full_formed):
    for item1 in full:
        if item1.dag=='1' and item1.string == 1:
            output.append(item1)
            output_pos.append(item1.pos)
    for item1 in full:
        if item1.dag=='1' and item1.string == 2:
            output.append(item1)
            output_pos.append(item1.pos)
    for item1 in full:
        if item1.dag=='0' and item1.string == 2:
            output.append(item1)
            output_pos.append(item1.pos)
    for item1 in full:
        if item1.dag=='0' and item1.string == 1:
            output.append(item1)
            output_pos.append(item1.pos)
    full_formed.extend(output_pos)
'''
def write_normal_order(new_list, output):
    new_list.append('\\{')
    for item in output:
        if item.dag=='1' and item.string==1:
            tmp_4 = 'a^+_{'+item.name+'}'
            new_list.append(tmp_4)
    for item in output :
        if ( item.dag=='1') and item.string ==2:
            tmp_4 = 'a^+_{'+item.name+'}'
            new_list.append(tmp_4)
    for item in output:
        if item.dag=='0' and item.string==2:
            tmp_4 = 'a_{'+item.name+'}'
            new_list.append(tmp_4)
    for item in output :
        if ( item.dag=='0') and item.string ==1:
            tmp_4 = 'a_{'+item.name+'}'
            new_list.append(tmp_4)
    new_list.append('\\}')
'''
#------------changed in order to print in the form of E(abc)(efg)
def write_normal_order(new_list, output):
    new_list.append('\\{E^{')
    for item in output:
        if item.dag=='1' and item.string==1:
            tmp_4 = item.name

            new_list.append(tmp_4)
    for item in output :
        if ( item.dag=='1') and item.string ==2:
            tmp_4 = item.name
            new_list.append(tmp_4)
    new_list.append('}_{')
    for item in reversed(output):
	#remember here the 1st string comes first as in writig in E has different rules than straight 
        if item.dag=='0' and item.string==1:

	    print "item name is ", item.name

            tmp_4 = item.name
	    new_list.append(tmp_4)
    for item in reversed(output) :
        if ( item.dag=='0') and item.string ==2:
	    
	    print "item name is ", item.name
            tmp_4 = item.name
	    new_list.append(tmp_4)
    new_list.append('}\\}')
def normal_order_adv(full, output):
    for item1 in full:
        flag=0
        for item2 in output:
            if item1.pos==item2.pos:
                flag=1
        if (not flag) and (item1.dag=='1') and item1.string ==1:
            output.append(item1)
    for item1 in full:
        flag=0
        for item2 in output:
            if item1.pos==item2.pos:
                flag=1
        if (not flag) and (item1.dag=='1') and item1.string==2:
            output.append(item1)
    for item1 in full:
        flag=0
        for item2 in output:
            if item1.pos==item2.pos:
                flag=1
        if (not flag) and (item1.dag=='0') and item1.string ==2:
            output.append(item1)
    for item1 in full:
        flag=0
        for item2 in output:
            if item1.pos==item2.pos:
                flag=1
        if (not flag) and (item1.dag=='0') and item1.string==1:
            output.append(item1)

def check_for_same_contraction(spin_list_upper, spin_list_lower, counter):
    if spin_list_lower[counter]==spin_list_upper[counter]:
        '''
	garbage=spin_list_upper[counter]
        spin_list_upper.remove(garbage)
        spin_list_lower.remove(garbage)
        counter=0
        loop_start=spin_list_upper[counter]	
	'''
def loop_present(spin_list_upper, spin_list_lower, loop_start, counter):
    if not spin_list_upper:
	print "spin list empty"
	return 0
    if loop_start==-1:
	print "loop start executed"
	loop_start=spin_list_upper[counter]
    if spin_list_upper[counter]==spin_list_lower[counter]:

	print "found acon contraction"


	spin_list_upper.remove(spin_list_upper[counter])
	spin_list_lower.remove(spin_list_lower[counter])

    else :
	if spin_list_lower[counter]==loop_start:
	    print "congratulations the loop present worked"
	    return 1
	found_match=0

	print "trying to find the same spin in upper"
	for item in spin_list_upper:
	    print "2. trying to find the same spin in upper", item, spin_list_lower[counter]
	    if item==spin_list_lower[counter]:
		found_match=1
		print "matched"
		spin_list_upper.remove(spin_list_upper[counter])
		spin_list_lower.remove(spin_list_lower[counter])
		print "deleted upper lower", spin_list_upper, spin_list_lower, len(spin_list_upper)
		for i in range(len(spin_list_upper)):
		    if spin_list_upper[i]==item:
			counter=i
		print "cunter new = ", counter
		return loop_present(spin_list_upper, spin_list_lower, loop_start, counter)
	if found_match==0:
	    print "not found in upper spin, deleting"
	    spin_list_upper.remove(spin_list_upper[counter])
	    spin_list_lower.remove(spin_list_lower[counter])
	    loop_present(spin_list_upper, spin_list_lower, -1, 0)
