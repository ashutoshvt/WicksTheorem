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

class contractedobj(object):
    def __init__(self, kind, sign, const):
        self.kind = kind
        self.upper = []
        self.lower = []
        self.sign = sign
        self.const = const
        self.anti = 0
        self.matrix = []
        self.strings=[1,2]
    def __repr__(self):
        return str.upper(self.kind)+ '^'+str(self.upper)+'_'+str(self.lower)
    def value(self, mat):
        return 1
    def __str__(self):
        quote_upper = (', '.join("'" + str(item) + "'" for item in self.upper))
        quote_lower = (', '.join("'" + str(item) + "'" for item in self.lower))
        return str(self.kind)+'^'+'['+str(quote_upper)+']'+'_['+str(quote_lower)+']'
        #return str.upper(self.kind)+'^'+'['+str(quote_upper)+']'+'_['+str(quote_lower)+']'
    def printlatex(self):
        return "\\" + str(self.kind)+'^'+str(self.upper)+'_'+str(self.lower)
        
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
            print("item name is ", item.name)
            tmp_4 = item.name
            new_list.append(tmp_4)
    for item in reversed(output) :
        if ( item.dag=='0') and item.string ==2:
            print("item name is ", item.name)
            tmp_4 = item.name
            new_list.append(tmp_4)
    new_list.append('}\\}')

def write_normal_order_AK(new_list, tensor_order_map):
    new_list.append('\\{E^{') # upper
    upper_indices=[]
    lower_indices=[]
    for key in tensor_order_map:
        upper_indices.append(key.name)    
        lower_indices.append(tensor_order_map[key].name)    
    new_list.append(''.join(upper_indices)) 
    new_list.append('}_{')
    new_list.append(''.join(lower_indices)) 
    new_list.append('}\\}') # lower
    print('new_list')
    a = ''.join(new_list)
    print(a)

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

def is_present_in_dict(item, parent_dict, output):
    flag = False
    for key in parent_dict:
        #print type(key)
        #print type(item)
        #print key
        #print key.pos 
        #print item.pos 
        if key.pos == item.pos:
            flag = True
            output.append(parent_dict[key])
            break
    return flag 

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
        print("spin list empty")
        return 0
    if loop_start==-1:
        print("loop start executed")
        loop_start=spin_list_upper[counter]
    if spin_list_upper[counter]==spin_list_lower[counter]:
        print("found acon contraction")
        spin_list_upper.remove(spin_list_upper[counter])
        spin_list_lower.remove(spin_list_lower[counter])
    else :
        if spin_list_lower[counter]==loop_start:
            print("congratulations the loop present worked")
            return 1
        found_match=0
        print("trying to find the same spin in upper")
        for item in spin_list_upper:
            print("2. trying to find the same spin in upper", item, spin_list_lower[counter])
            if item==spin_list_lower[counter]:
                found_match=1
                print("matched")
                spin_list_upper.remove(spin_list_upper[counter])
                spin_list_lower.remove(spin_list_lower[counter])
                print("deleted upper lower", spin_list_upper, spin_list_lower, len(spin_list_upper))
                for i in range(len(spin_list_upper)):
                    if spin_list_upper[i]==item:
                        counter=i
                print("cunter new = ", counter)
                return loop_present(spin_list_upper, spin_list_lower, loop_start, counter)
        if found_match==0:
            print("not found in upper spin, deleting")
            spin_list_upper.remove(spin_list_upper[counter])
            spin_list_lower.remove(spin_list_lower[counter])
            loop_present(spin_list_upper, spin_list_lower, -1, 0)
