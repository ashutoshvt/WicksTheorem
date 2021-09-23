import eq8
import numpy as np
import copy
import operators as op


class term(object):
    def __init__(self, fac, sum_list, coeff_list, lol, st, co):
        self.kind = 'term'
        self.fac = fac
        self.sum_list = sum_list
        self.coeff_list = copy.deepcopy(coeff_list)
        self.large_op_list = copy.deepcopy(lol)
        self.st = st
        self.co = co
        self.map_org = []
        self.dict_ind = {}
        self.imatrix = np.zeros((len(coeff_list), len(coeff_list)))
        self.amatrix = np.zeros((len(coeff_list), len(coeff_list)))

    def compress(self):
        for terms in self.st:
            for oper in terms:
                # print op
                if oper.kind == 'delta':
                    if 'p' <= oper.upper[0].name[0] <= 'u':
                        # find name in coeff
                        # self.coeff_list=[[w.replace(op.upper[0].name, op.lower[0].name)
                        # for w in l] for l in self.coeff_list]
                        for c1 in self.coeff_list:
                            for n, i in enumerate(c1):
                                if i == oper.upper[0].name:
                                    c1[n] = oper.lower[0].name
                        self.sum_list.remove(oper.upper[0].name)
                    elif 'p' <= oper.lower[0].name[0] <= 'u':
                        # self.coeff_list=[[w.replace(op.lower[0].name, op.upper[0].name)
                        # for w in l] for l in self.coeff_list]
                        for c1 in self.coeff_list:
                            for n, i in enumerate(c1):
                                if i == oper.lower[0].name:
                                    c1[n] = oper.upper[0].name
                        self.sum_list.remove(oper.lower[0].name)
                    elif (oper.upper[0].name in self.sum_list) and (oper.lower[0].name in self.sum_list):
                        if oper.upper[0].name[0] >= oper.lower[0].name[0]:
                            # self.coeff_list=[[w.replace(op.upper[0].name, op.lower[0].name)
                            # for w in l] for l in self.coeff_list]
                            for c1 in self.coeff_list:
                                for n, i in enumerate(c1):
                                    if i == oper.upper[0].name:
                                        c1[n] = oper.lower[0].name
                            self.sum_list.remove(oper.upper[0].name)
                        elif oper.upper[0].name[0] < oper.lower[0].name[0]:
                            # self.coeff_list=[[w.replace(op.lower[0].name, op.upper[0].name)
                            # for w in l] for l in self.coeff_list]
                            for c1 in self.coeff_list:
                                for n, i in enumerate(c1):
                                    if i == oper.lower[0].name:
                                        c1[n] = oper.upper[0].name
                            self.sum_list.remove(oper.lower[0].name)

                    elif oper.lower[0].name in self.sum_list:
                        # self.coeff_list=[[w.replace(op.lower[0].name, op.upper[0].name)
                        # for w in l] for l in self.coeff_list]
                        for c1 in self.coeff_list:
                            for n, i in enumerate(c1):
                                if i == oper.lower[0].name:
                                    c1[n] = oper.upper[0].name
                        self.sum_list.remove(oper.lower[0].name)
                    elif oper.upper[0].name in self.sum_list:
                        # self.coeff_list=[[w.replace(op.upper[0].name, op.lower[0].name)
                        # for w in l] for l in self.coeff_list]
                        for c1 in self.coeff_list:
                            for n, i in enumerate(c1):
                                if i == oper.upper[0].name:
                                    c1[n] = oper.lower[0].name
                        self.sum_list.remove(oper.upper[0].name)

    # lets resolve gamma as well (and eta if there!)
    # assuming gammas only involve the non-zero pieces!
    def resolve_gammas_HF(self):
        for i, oper in enumerate(self.st[0]):
            if oper.kind == 'gamma':
                print('constants')
                print(self.co[0])
                self.st[0][i].kind = 'delta'
                self.co[0][1] *= 2.0
                self.fac *= 2.0
                print(self.co[0])

    # resolving deltas of CABS+ indices
    # after this resolve the other deltas as well!
    # after this function, identify the f12 intermediates as the final step!
    def compress_AK_HF(self):
        print('compress: ', self.st[0])
        # print(len(self.st[0]))
        # print(self.co[0])
        ops_to_remove = []
        count = 0
        cabs_upper = False
        cabs_lower = False
        for oper in self.st[0]:
            print('terms: ', oper)
            print('terms.kind: ', oper.kind)
            if oper.kind == 'delta':
                if 'A' <= oper.upper[0][0] <= 'H':
                    print('upper')
                    cabs_upper = True
                if 'A' <= oper.lower[0][0] <= 'H':
                    print('lower')
                    cabs_lower = True
                if cabs_upper and not cabs_lower:
                    print('cabs_upper; not cabs_lower')
                    if 'p' <= oper.lower[0][0] <= 'u':
                        for i, item in enumerate(self.coeff_list):
                            if oper.lower[0] in item:
                                index = self.coeff_list[i].index(oper.lower[0])
                                self.coeff_list[i][index] = oper.upper[0]
                        for i, item in enumerate(self.sum_list):
                            if oper.lower[0] == item:
                                self.sum_list[i] = oper.upper[0]
                        self.sum_list = list(set(self.sum_list))  # unique!
                    ops_to_remove.append(count)
                elif cabs_lower and not cabs_upper:
                    print('cabs_lower; not cabs_upper')
                    if 'p' <= oper.upper[0][0] <= 'u':
                        for i, item in enumerate(self.coeff_list):
                            if oper.upper[0] in item:
                                index = self.coeff_list[i].index(oper.upper[0])
                                self.coeff_list[i][index] = oper.lower[0]
                        for i, item in enumerate(self.sum_list):
                            if oper.upper[0] == item:
                                self.sum_list[i] = oper.lower[0]
                        self.sum_list = list(set(self.sum_list))
                    ops_to_remove.append(count)
                elif cabs_upper and cabs_lower:
                    print('cabs_lower; cabs_upper')
                    for i, item in enumerate(self.coeff_list):
                        if oper.upper[0] in item:
                            index = self.coeff_list[i].index(oper.upper[0])
                            self.coeff_list[i][index] = oper.lower[0]
                    for i, item in enumerate(self.sum_list):
                        if oper.upper[0] == item:
                            self.sum_list[i] = oper.lower[0]
                    self.sum_list = list(set(self.sum_list))
                    ops_to_remove.append(count)
                else:
                    # resolve deltas not containing any CABS indices
                    # if general index is present, make sure it becomes
                    # equal to other indices!
                    print('not cabs_lower; not cabs_upper')
                    lower_ge = False
                    upper_ge = False
                    if 'p' <= oper.lower[0][0] <= 'u':
                        lower_ge = True
                    if 'p' <= oper.upper[0][0] <= 'u':
                        upper_ge = True
                    for i, item in enumerate(self.coeff_list):
                        if upper_ge:
                            if oper.upper[0] in item:
                                index = self.coeff_list[i].index(oper.upper[0])
                                self.coeff_list[i][index] = oper.lower[0]
                        elif lower_ge:
                            if oper.lower[0] in item:
                                index = self.coeff_list[i].index(oper.lower[0])
                                self.coeff_list[i][index] = oper.upper[0]
                        else:
                            if oper.upper[0] in item:
                                index = self.coeff_list[i].index(oper.upper[0])
                                self.coeff_list[i][index] = oper.lower[0]
                    # lists are un-ordered!
                    for i, item in enumerate(self.sum_list):
                        if upper_ge:
                            if oper.upper[0] == item:
                                index = self.sum_list.index(item)
                                self.sum_list[index] = oper.lower[0]
                        if lower_ge:
                            if oper.lower[0] == item:
                                index = self.sum_list.index(item)
                                self.sum_list[index] = oper.upper[0]
                        if not upper_ge and not lower_ge:
                            if oper.upper[0] == item:
                                index = self.sum_list.index(item)
                                self.sum_list[index] = oper.lower[0]
                        self.sum_list = list(set(self.sum_list))
                    print('final sum: ', self.sum_list)
                    ops_to_remove.append(count)
            count += 1
            cabs_upper = False
            cabs_lower = False
        for item in sorted(ops_to_remove, reverse=True):
            self.st[0].pop(item)
        print('final_st[0]: ', self.st[0])

    def compare(self, term2):
        """
        for (c1,c2, t) in zip(self.coeff_list, term2.coeff_list, self.map_org):
            num=1.0
            if t[1]=='2' and t[0]!='X':
                #print self.coeff_list[1], term2.coeff_list[1]

                num=num*eq82.eq82(c1,c2, self, term2)
            elif t[1]=='1' and t[0]!='X':
                num=num*eq82.eq81(c1, c2, self, term2)
        else :
            return num
        """
        num = 1.0

        for (c1, t1) in zip(self.coeff_list,  self.map_org):
            flag = 0
            # print t1
            for (c2, t2) in zip(term2.coeff_list, self.map_org):
                # print t2
                if t1[1] == t2[1] and t1[0] == t2[0] and t1[0] != 'X':

                    if t1[1] == '2' and eq8.eq8(c1, c2, self, term2):
                        num = num*eq8.eq8(c1, c2, self, term2)
                        flag = 1
                        break
                    elif t1[1] == '1' and eq8.eq8(c1, c2, self, term2):
                        num = num*eq8.eq8(c1, c2, self, term2)
                        flag = 1
                        break
                elif t1[0] == 'X':
                    flag = 1
                    break
            if flag == 0:
                # print "case to study is happening"
                return 0
        # return num

        if (self.fac*term2.fac) < 0 and num != 0:
            print(num, '-1')
            return -1
        elif (self.fac*term2.fac) > 0 and num != 0:
            print(num, '1')
            return 1
        else:
            print(num, '0')
            return 0

    # algorithm to condition that each contraction should have 1 end to H
    # once reach H, store coeff of H in ind
    # store all other Ts in map_org
    # from dict and mapping, locate all ends of contraction
    # check whether all operators are in mapping

    def cond_cont(self, dict_ind):
        map_org = []
        mapping = []
        ind = []
        for item in self.large_op_list:
            if item.name[0] == 'T' or item.name[0] == 'D':
                map_org.append(item)
            if item.name == 'F1' or item.name == 'V2':
                ind = self.large_op_list.index(item)
        for item in self.coeff_list[ind]:
            mapping.append(dict_ind[item])
        for item in map_org:
            if item.name not in mapping:
                self.fac = 0.0
        # self.map_org=map_org
        # self.build_map_org()

    def isa(self, x):

        if 'a' <= x <= 'h':
            return 1

        elif len(x) == 2 and 'a' <= x[0] <= 'h':
            return 1
        else: 
            return 0

    def isi(self, x):
        if 'i' <= x <= 'n':
            return 1
        elif len(x) == 2 and 'i' <= x[0] <= 'n':
            return 1
        else:
            return 0

    def isp(self, x):
        if 'p' <= x <= 't':
            return 1
        elif len(x) == 2 and 'p' <= x[0] <= 't':
            return 1
        else:
            return 0

    def is_dummy(self, x):
        if x in self.sum_list:
            return 1
        else:
            return 0

    def type(self, x):
        if self.isa(x):
            return 'a'
        elif self.isi(x):
            return 'i'
        elif self.isp(x):
            return 'p'

    def cpre_cstm(self, term2, a, b):
        for i, j in zip(a, b):
            # print a,b
            # print i,self.sum_list,j,term2.sum_list
            if i in self.sum_list and j in term2.sum_list:
                if self.isi(i) and self.isi(j):
                    pass
                    # flag1 = 1 This is not used!!
                elif self.isa(i) and self.isa(j):
                    pass
                    # flag1 = 1
                else:
                    return 0
            # elif i not in self.sum_list or j not in self.sum_list:
                # return 0
            elif i == j:
                pass
                # flag1 = 1
            else:
                return 0

            # print i,j, flag1
        return 1

    def mapping(self):
        map1 = []
        for item in self.large_op_list:
            map1.append(item.name)
        self.map_org = map1

    def dummy_check(self, term2):
        count_eql = 0
        # print self.map_org
        for i in self.map_org:
            flag = 0
            # print 'self',i
            for j in term2.map_org:
                # print 'matching', j
                if i[0] == j[0] and i[1] == j[1] and flag == 0 and i[0] != 'X' and j[0] != 'X':
                    ind1 = self.map_org.index(i)
                    ind2 = self.map_org.index(j)

                    if self.cpre_cstm(term2, self.coeff_list[ind1], term2.coeff_list[ind2]):
                        count_eql += 1
                        flag = 1
                        # print 'match',j, count_eql
            if flag == 0:
                # flag2 = 1 Not used!
                pass
                # continue
        if count_eql == (len(self.map_org)-1):
            # if flag2 == 0:
            # print "changing"
            self.fac += term2.fac
            term2.fac = 0.0

    def print_term(self):
        print(self.fac)
        print('Sum', self.sum_list)
        for i in range(len(self.large_op_list)):
            if self.large_op_list[i].name[0] != 'X':
                print(self.large_op_list[i].name[0], self.coeff_list[i])
        # Here I need to also print eta and gamma terms: AK
        for terms in self.st[0]:
            if terms.kind == 'gamma':
                print(str(terms))
            if terms.kind == 'eta':
                print(str(terms))
            if terms.kind == 'delta':
                print(str(terms))
        # operator is in last position!
        if self.st[0][-1].kind == 'op':
            print('E^', self.st[0][-1].upper, '_', self.st[0][-1].lower)
        print('\n')

    def print_latex(self, f):
        # f=open('exp_out_latex.txt','a')
        f.write(str(self.fac))
        if self.sum_list:
            f.write(r"\sum_{")
            for item in self.sum_list:
                f.write(item+' ')
            f.write("}")
        for i in range(0, len(self.large_op_list)):
            if self.large_op_list[i].name[0] != 'V' and self.large_op_list[i].name[0] != 'X':
                # f.write(self.large_op_list[i].name[0])
                f.write(self.large_op_list[i].name)
                f.write("^{")

            elif self.large_op_list[i].name[0] == 'V':
                f.write("<")

            if self.large_op_list[i].name[0] != 'X':
                for it1 in range(0, int(len(self.coeff_list[i])/2)):
                    f.write(self.coeff_list[i][it1])

            if self.large_op_list[i].name[0] != 'V' and self.large_op_list[i].name[0] != 'X':
                f.write("}_{")
            elif self.large_op_list[i].name[0] == 'V':
                # f.write("||")
                f.write("|")  # AK: spin_free

            if self.large_op_list[i].name[0] != 'X':
                for it2 in range(int(len(self.coeff_list[i])/2), len(self.coeff_list[i])):
                    f.write(self.coeff_list[i][it2])
            if self.large_op_list[i].name[0] != 'V' and self.large_op_list[i].name[0] != 'X':
                f.write("}")
            elif self.large_op_list[i].name[0] == 'V':
                f.write(">")
        # Here I need to also print eta and gamma terms: AK
        for terms in self.st[0]:
            if terms.kind == 'gamma':
                f.write(terms.printlatex())
            if terms.kind == 'eta':
                f.write(terms.printlatex())
            if terms.kind == 'delta':
                f.write(terms.printlatex())
        if self.st[0][-1].kind == 'op':
            f.write("E^{")
            for it1 in self.st[0][-1].upper:
                # print 'it1'
                # print type(it1)
                # print it1
                f.write(str(it1))
            f.write("}_{")
            for it1 in self.st[0][-1].lower:
                f.write(str(it1))
            f.write("}")
        f.write('\\\\ \n')

    def build_map_org(self):
        for item in self.large_op_list:
            self.map_org.append(item)

    # I would like to implement all the rules for HF now!
    # Rule 1: Density terms with CABS indices must be zero!
    # Rule 2: Eta terms:
    #         a) if eta term contains only general indices or occupied and virtual
    #            in other words, no CABS+ indices  --> zero! --> NOPES!
    #            what about eta^p_a?? the gamma term would be zero but the delta
    #            term should remain!! so what should be the modified rule?
    #            lets resolve only the CABS case. We will resolve other cases
    #            later by expanding general indices into occupied and virtual cases!
    #         b) if eta term contains CABS+ indices --> replace 
    #            eta by delta and then replace the corresponding 
    #            general index to the CABS+ index --> second half in compress function!
    # Rule 3: a) If an operator contains CABS+ index, replace by
    #            corresponding virtual: A0 ---> a0,
    #            need to be careful if R amplitude contains both virtual and CABS indices
    #            which is very well the case for excited states!
    #         b) also if 2 CABS indices are present in operator,
    #             remove that term!
    # Rule 4: Remove 3 body operators
    # Rule 5: Look for 3 kinds of patterns:
    #            V == g^{pq}_{\alpha\beta} * G^{\alpha\beta}_{ij}      
    #            X == G^{\alpha\beta}_{ij} * G^{\alpha\beta}_{kl}      
    #            B == G^{\alpha\beta}_{ij} * f^{\alpha}_{\gamma} * G^{\gamma\beta}_{kl}      
    #               + G^{\alpha\beta}_{ij} * f^{\beta}_{\gamma} * G^{\alpha\gamma}_{kl}      
    #
    # Rule 6: Remove fully contracted terms!
    # Rule 7: Remove indices appearing in the operators from self.sum_list
    # lets focus on removal of terms first!: Rule 1, Rule 2a, Rule 3b, Rule 4, Rule 6
    # Try to update the st and coeff members of standard operators as well!
    # Do I need that??? maybe because term objects do have a list of standard operators!
    # so, I can update that as well!!

    def simplify_for_HF_ref(self):
        CABS_inds = ['A0', 'B0', 'A1', 'B1', 'A2', 'B2']
        CABS_pairs = [['A0', 'B0'], ['A1', 'B1'], ['A2', 'B2']]
        flag = 0
        f_contract = 1
        # print('self.coeff:{}'.format(self.coeff_list))
        for terms in self.st:
            for oper in terms:
                # Rule 1.
                if oper.kind == 'gamma':
                    if oper.upper[0] in CABS_inds or oper.lower[0] in CABS_inds:
                        flag = 1
                        return flag
                if oper.kind == 'eta':
                    # Rule 2a. Modified it but needs to be tested!
                    # if one of the indices is occupied and other is general --> zero!
                    # if one of the indices is virtual and other is general --> delta!
                    # the below if only works when: (occ, occ), (general, occ), (general, general)[NA here!]
                    if oper.upper[0].upper() not in CABS_inds and oper.lower[0].upper() not in CABS_inds:
                        flag = 1
                        return flag
                    # Rule 2b.
                    else:
                        # occ-vir is also delta!! --> need to change it!
                        # general-vir
                        oper.kind = 'delta'
                if oper.kind == 'op':
                    f_contract = 0
                    # Rule 4
                    if len(oper.upper) >= 3:
                        flag = 1
                        return flag
                    # Rule 3b
                    cabs_list = []
                    for item in oper.upper:
                        if item in CABS_inds:
                            cabs_list.append(item)
                    for item in oper.lower:
                        if item in CABS_inds:
                            cabs_list.append(item)
                    for i, item in enumerate(CABS_pairs):
                        if CABS_pairs[i][0] in cabs_list and CABS_pairs[i][1] in cabs_list:
                            # cabs_list.remove(CABS_pairs[i][0])
                            # cabs_list.remove(CABS_pairs[i][1])
                            flag = 1
                            return flag
                    # Rule 7
                    op_indices = []
                    for item in oper.upper:
                        op_indices.append(item)
                    for item in oper.lower:
                        op_indices.append(item)
                    for item in op_indices:
                        self.sum_list.remove(item)
                    # Rule 3a
                    # (replace in self.coeff_list, self.st[op.upper,op.lower] as well!)
                    # A0 --> a0 (need to revisit for excited states!)
                    for item in cabs_list:
                        for i in range(len(self.coeff_list)):
                            if item in self.coeff_list[i]:
                                index = self.coeff_list[i].index(item)
                                self.coeff_list[i][index] = self.coeff_list[i][index].lower()
                        if item in oper.upper:
                            index = oper.upper.index(item)
                            oper.upper[index] = oper.upper[index].lower()
                        if item in oper.lower:
                            index = oper.lower.index(item)
                            oper.lower[index] = oper.lower[index].lower()
        # Rule 6
        if f_contract == 1:
            flag = 1
        return flag

    def identify_f12_intermediates(self):
        # identify pattern for for intermediate V: (A)
        CABS_inds = ['A0', 'B0', 'A1', 'B1', 'A2', 'B2']
        CABS_pairs = [['A0', 'B0'], ['A1', 'B1'], ['A2', 'B2']]
        V2 = False
        R2 = False
        flag = 0
        i_indx = 0
        # applicable for [V2,R2-R2D]
        size = len(self.large_op_list)
        large_op_list_names = [self.large_op_list[i].name for i in range(size)]
        print(large_op_list_names)
        if 'V2' in large_op_list_names and ('R2' or 'R2D' in large_op_list_names):
            # grab the V2 and R2/R2D indices
            V2_index = large_op_list_names.index('V2')
            if 'R2' in large_op_list_names:
                R2_index = large_op_list_names.index('R2')
            else:
                R2_index = large_op_list_names.index('R2D')
            print('V2_index: ', V2_index)
            print('R2_index: ', R2_index)
            # print('self.coeff_list', self.coeff_list)
            for i, item in enumerate(CABS_pairs):
                if CABS_pairs[i][0] in self.coeff_list[V2_index] and CABS_pairs[i][1] in self.coeff_list[V2_index]:
                    V2 = True
                    if CABS_pairs[i][0] in self.coeff_list[R2_index] and CABS_pairs[i][1] in self.coeff_list[R2_index]:
                        R2 = True
                        i_indx = i
            if V2 and R2:
                print('looks like V intermediate!')
                print('V2: ', self.coeff_list[V2_index])
                print('R2: ', self.coeff_list[R2_index])
                print('op: ', self.st[0][0])
                # I need to re-order the coefficients if B comes before A
                # in both V2 and R2: 
                for i, items in enumerate(self.coeff_list):
                    Ai = 'A' + str(i_indx)
                    Bi = 'B' + str(i_indx)
                    index_A = items.index(Ai)
                    index_B = items.index(Bi)
                    # swap 0,1 and 2,3
                    if index_B < index_A:
                        tmp = self.coeff_list[i][1]
                        self.coeff_list[i][1] = self.coeff_list[i][0]
                        self.coeff_list[i][0] = tmp
                        tmp = self.coeff_list[i][3]
                        self.coeff_list[i][3] = self.coeff_list[i][2]
                        self.coeff_list[i][2] = tmp
                new_coeff = copy.deepcopy(self.coeff_list)
                # re-populate self.coeff_list
                for i, items in enumerate(self.coeff_list):
                    Ai = 'A' + str(i_indx)
                    Bi = 'B' + str(i_indx)
                    index_A = items.index(Ai)
                    index_B = items.index(Bi)
                    # B before A is important!
                    new_coeff[i].pop(index_B)
                    new_coeff[i].pop(index_A)
                print('new_coeff: ', new_coeff)
                self.coeff_list = []
                tmp_list = []
                for i in range(2):
                    for items in new_coeff[i]:
                        tmp_list.append(items)
                self.coeff_list.append(tmp_list)
                print('self.coeff: ', self.coeff_list)

                # change the operator name to V_F12
                # V2 and R2 operators should be removed!
                # So, only one element in the coeff_list!
                # All I care about is the coeff_list and name
                # rest of the member variables of Stoperator can
                # be empty!

                V_F12 = op.initialize_stoperator('A', 1.0, [[], []])
                self.large_op_list = []
                self.large_op_list.append(V_F12)

                print('test: ', self.large_op_list[0].name[0])

                # remove Ai, Bi from sum_list
                self.sum_list.remove(CABS_pairs[i_indx][0])
                self.sum_list.remove(CABS_pairs[i_indx][1])
                flag = 1
        # identify the pattern for for intermediate X: (C)
        # X(i0,j0,i1,j1) = R^{AB}_{i0j0} * R^{AB}_{i1j1}
        # assuming a fixed pattern, need to adapt! TODO!
        if len(self.large_op_list) == 3:
            index_F = large_op_list_names.index('F1')
            ops = [i for i in range(3)]
            ops.pop(index_F)
            R2_1 = False
            R2_2 = False
            # print('self.large_op_list: ', self.large_op_list)
            print('ops: ', ops)
            for i, item in enumerate(CABS_pairs):
                if CABS_pairs[i][0] in self.coeff_list[ops[0]] and CABS_pairs[i][1] in self.coeff_list[ops[0]]:
                    R2_1 = True
                    if CABS_pairs[i][0] in self.coeff_list[ops[1]] and CABS_pairs[i][1] in self.coeff_list[ops[1]]:
                        R2_2 = True
                        i_indx = i
            if R2_1 and R2_2:
                print('looks like X intermediate!')
                print('coeff[0]: ', self.coeff_list[0])
                print('coeff[1]: ', self.coeff_list[1])
                print('coeff[2]: ', self.coeff_list[2])
                # I need to re-order the coefficients if B comes before A
                # in both R2 and R22
                for i, items in enumerate(self.coeff_list):
                    Ai = 'A' + str(i_indx)
                    Bi = 'B' + str(i_indx)
                    if Ai in items:
                        index_A = items.index(Ai)
                    else:
                        index_A = 0
                    if Bi in items:
                        index_B = items.index(Bi)
                    else:
                        index_B = 0
                    # swap 0,1 and 2,3
                    if index_B < index_A:
                        tmp = self.coeff_list[i][1]
                        self.coeff_list[i][1] = self.coeff_list[i][0]
                        self.coeff_list[i][0] = tmp
                        tmp = self.coeff_list[i][3]
                        self.coeff_list[i][3] = self.coeff_list[i][2]
                        self.coeff_list[i][2] = tmp
                new_coeff = copy.deepcopy(self.coeff_list)
                print('coeff[0] after swap: ', self.coeff_list[0])
                print('coeff[1] after swap: ', self.coeff_list[1])
                print('coeff[2] after swap: ', self.coeff_list[2])
                print('self.coeff_list: ', self.coeff_list)
                # re-populate self.coeff_list
                for i, items in enumerate(self.coeff_list):
                    Ai = 'A' + str(i_indx)
                    Bi = 'B' + str(i_indx)
                    print('Ai, Bi, items: ', Ai, Bi, items)
                    if Bi in items:
                        index_B = items.index(Bi)
                        print('index_B: ', index_B)
                        new_coeff[i].pop(index_B)
                    if Ai in items:
                        index_A = items.index(Ai)
                        print('index_A: ', index_A)
                        new_coeff[i].pop(index_A)
                X_F12 = op.initialize_stoperator('C', 1.0, [[], []])
                # remove R2
                self.large_op_list.pop(ops[1])
                # remove R22
                self.large_op_list.pop(ops[0])
                # F, X_F12
                self.large_op_list.append(X_F12)

                print('test: ', self.large_op_list[0].name[0])
                print('test: ', self.large_op_list[1].name[0])

                # merge 0 and 2
                print('new_coeff: ', new_coeff)
                # remove R2
                self.coeff_list.pop(ops[1])
                # remove R22
                self.coeff_list.pop(ops[0])
                tmp_list = []
                for i, items in enumerate(new_coeff):
                    if i in ops:
                        for items_i in new_coeff[i]:
                            tmp_list.append(items_i)
                print('tmp_list: ', tmp_list)

                self.coeff_list.append(tmp_list)
                print('self.coeff1: ', self.coeff_list)

                # remove Ai, Bi from sum_list
                if CABS_pairs[i_indx][0] in self.sum_list:
                    self.sum_list.remove(CABS_pairs[i_indx][0])
                if CABS_pairs[i_indx][1] in self.sum_list:
                    self.sum_list.remove(CABS_pairs[i_indx][1])
                flag = 1

        # # identify the B intermediate now!
        # # B(i0,j0,i1,j1) = R^{AB}_{i0j0} * f^{A}_{C} * R^{CB}_{i1j1} (1)
        # #                + R^{AB}_{i0j0} * f^{B}_{C} * R^{AC}_{i1j1} (2)
        # # So, I would need to compare two terms now!
        # # maybe I can do something like this! (1) - D, (2) - E
        # # and then combine D and E later in some other place!
        # # (f.upper in R2/R22 and f.lower in R2/R22) and both R contains
        # # a common CABS index (B or A)
        # # I guess just one term is fine!
        # # B(i0,j0,i1,j1) = R^{AB}_{i0j0} * f^{A}_{C} * R^{CB}_{i1j1}
        # # Just use this pattern only!
        # # make sure you cast the appropriate terms into the above pattern!
        # # I can't assume the following order, so need to change logic! TODO!
        # # R22/R22D F R2/R2D
        #
        if len(self.large_op_list) == 3:
            print('Trying to identify B intermediate\n')
            index_F = large_op_list_names.index('F1')
            F_upper = self.coeff_list[index_F][0]
            F_lower = self.coeff_list[index_F][1]
            F_upper_0 = False
            F_upper_1 = False
            F_lower_0 = False
            F_lower_1 = False
            # print('F_upper: ', F_upper)
            # print('F_lower: ', F_lower)
            index_F_upper_0 = 0
            index_F_lower_1 = 0
            ops = [i for i in range(3)]
            ops.pop(index_F)
            print('ops: ', ops)
            if F_upper in self.coeff_list[ops[0]] and F_upper in CABS_inds:
                F_upper_0 = True
                index_F_upper_0 = self.coeff_list[ops[0]].index(F_upper)
            if F_upper in self.coeff_list[ops[1]] and F_upper in CABS_inds:
                F_upper_1 = True
            if F_lower in self.coeff_list[ops[0]] and F_lower in CABS_inds:
                F_lower_0 = True
            if F_lower in self.coeff_list[ops[1]] and F_lower in CABS_inds:
                F_lower_1 = True
                index_F_lower_1 = self.coeff_list[ops[1]].index(F_lower)
            if (F_upper_0 and F_lower_1) or (F_upper_1 and F_lower_0):
                # check for a common CABS index in self.coeff[0] and self.coeff[2]
                intersect = [value for value in self.coeff_list[ops[0]] if value in self.coeff_list[ops[1]]
                             and value in CABS_inds]
                print('intersect: ', intersect)
                if intersect:
                    print('looks like B intermediate!')
                    # make sure the following pattern order is matched!!
                    # B(i0,j0,i1,j1) = R^{i0j0}_{A0B0} * f^{A0}_{C0} * R^{C0B0}_{i1j1}
                    # make sure f.upper and f.lower appears first!
                    # in other words, f.upper = 2 and f.lower = 0
                    # [or f.upper = 0 and f.lower = 2 --> will check this later!]
                    # print('F_upper_0: ', F_upper_0)  # True
                    # print('F_upper_1: ', F_upper_1)  # False
                    # print('F_lower_0: ', F_lower_0)  # False
                    # print('F_lower_1: ', F_lower_1)  # True
                    # Assuming the above combination of True, False to stay true
                    # for all the elements
                    print('index_F_upper_0: ', index_F_upper_0)
                    print('index_F_lower_1: ', index_F_lower_1)
                    print('self.st: ', self.st[0])
                    print('self.sum: ', self.sum_list)
                    if index_F_upper_0 != 2:
                        # swap coefficients and operator indices of 0 please!
                        temp = self.coeff_list[ops[0]][0]
                        self.coeff_list[ops[0]][0] = self.coeff_list[ops[0]][1]
                        self.coeff_list[ops[0]][1] = temp
                        self.st[0][0].upper.reverse()
                    if index_F_lower_1 != 0:
                        # swap coefficients and operator indices of 2 please!
                        temp = self.coeff_list[ops[1]][2]
                        self.coeff_list[ops[1]][2] = self.coeff_list[ops[1]][3]
                        self.coeff_list[ops[1]][3] = temp
                        self.st[0][0].lower.reverse()
                    # operator == [coeff[0][0], coeff[0][1], coeff[2][0], coeff[2][1]]
                    print('self.st after: ', self.st[0])
                    # self.sum_list = []
                    temp_list = [self.coeff_list[ops[0]][0], self.coeff_list[ops[0]][1],
                                 self.coeff_list[ops[1]][2], self.coeff_list[ops[1]][3]]
                    print('coeff[0]: ', self.coeff_list[0])
                    print('coeff[1]: ', self.coeff_list[1])
                    print('coeff[2]: ', self.coeff_list[2])
                    print('temp_list', temp_list)
                    print('self.coeff', self.coeff_list)
                    self.coeff_list = []
                    self.coeff_list.append(temp_list)
                    print('self.coeff', self.coeff_list)
                    B_F12 = op.initialize_stoperator('B', 1.0, [[], []])
                    self.large_op_list = []
                    self.large_op_list.append(B_F12)
                    if intersect[0] in self.sum_list:
                        self.sum_list.remove(intersect[0])
                    if F_upper in self.sum_list:
                        self.sum_list.remove(F_upper)
                    if F_lower in self.sum_list:
                        self.sum_list.remove(F_lower)
            return flag

    def resolve_cabs_to_vir(self):
        print('inside resolve cabs\n')
        cabs_indx = ''
        cabs_vir_map = {'A0': 'x0', 'A1': 'x1', 'B0': 'y0', 'B1': 'y1'}
        tmp_map = {'0': 2, '2': 0}
        # I can't assume a given order, so need to change logic! TODO!
        if len(self.large_op_list) == 3:
            # if 0 and 2 contains a vir index
            # and a CABS+ index --> change CABS+ to CABS
            print('coeff[0]: ', self.coeff_list[0])
            print('coeff[1]: ', self.coeff_list[1])
            print('coeff[2]: ', self.coeff_list[2])
            for coeff_ind in range(0, 3, 2):
                vir = 0
                CABS_plus = 0
                indx = 0
                pure_cabs = 0
                for i, items in enumerate(self.coeff_list[coeff_ind]):
                    if 'a' <= items[0] <= 'h':
                        vir += 1
                    if 'x' <= items[0] <= 'z':
                        pure_cabs += 1
                    if 'A' <= items[0] <= 'H':
                        CABS_plus += 1
                        indx = i
                        cabs_indx = items
                if vir == 1 and CABS_plus == 1:
                    self.coeff_list[coeff_ind][indx] = cabs_vir_map[cabs_indx]
                    j = [1, tmp_map[str(coeff_ind)]]
                    for j_x in j:
                        if cabs_indx in self.coeff_list[j_x]:
                            ind = self.coeff_list[j_x].index(cabs_indx)
                            self.coeff_list[j_x][ind] = cabs_vir_map[cabs_indx]
                    if cabs_indx in self.sum_list:
                        ind = self.sum_list.index(cabs_indx)
                        self.sum_list[ind] = cabs_vir_map[cabs_indx]
            # I need to replace the CABS_plus, pure_CABS case
            for coeff_ind in range(0, 3, 2):
                CABS_plus = 0
                indx = 0
                pure_cabs = 0
                for i, items in enumerate(self.coeff_list[coeff_ind]):
                    if 'x' <= items[0] <= 'z':
                        pure_cabs += 1
                    if 'A' <= items[0] <= 'H':
                        CABS_plus += 1
                        indx = i
                        cabs_indx = items
                    if CABS_plus == 1 and pure_cabs == 1:
                        self.coeff_list[coeff_ind][indx] = cabs_indx.lower()
                        j = [1, tmp_map[str(coeff_ind)]]
                        for j_x in j:
                            if cabs_indx in self.coeff_list[j_x]:
                                ind = self.coeff_list[j_x].index(cabs_indx)
                                self.coeff_list[j_x][ind] = cabs_indx.lower()
                            if cabs_indx in self.sum_list:
                                ind = self.sum_list.index(cabs_indx)
                                self.sum_list[ind] = cabs_indx.lower()
            print('coeff[0] after: ', self.coeff_list[0])
            print('coeff[1] after: ', self.coeff_list[1])
            print('coeff[2] after: ', self.coeff_list[2])
        else:
            # [F1, R2], [V2, R2] etc.
            # print('self.large_op_list: ', self.large_op_list)
            # print('coeff[0]: ', self.coeff_list[0])
            # print('coeff[1]: ', self.coeff_list[1])
            print('self.st: ', self.st)
            vir = 0
            CABS_plus = 0
            indx = 0
            i_star = 0
            for i in range(len(self.large_op_list)):
                if self.large_op_list[i].name[0] == 'R':
                    i_star = i
            for i, items in enumerate(self.coeff_list[i_star]):
                if 'a' <= items[0] <= 'h':
                    vir += 1
                if 'A' <= items[0] <= 'H':
                    CABS_plus += 1
                    indx = i
                    cabs_indx = items
                if vir == 1 and CABS_plus == 1:
                    self.coeff_list[i_star][indx] = cabs_vir_map[cabs_indx]
                    if i_star == 0:
                        j_star = 1
                    else:
                        j_star = 0
                    if cabs_indx in self.coeff_list[j_star]:
                        ind = self.coeff_list[j_star].index(cabs_indx)
                        self.coeff_list[j_star][ind] = cabs_vir_map[cabs_indx]
                    if cabs_indx in self.sum_list:
                        ind = self.sum_list.index(cabs_indx)
                        self.sum_list[ind] = cabs_vir_map[cabs_indx]
            # print('coeff[0] after: ', self.coeff_list[0])
            # print('coeff[1] after: ', self.coeff_list[1])

    def check_for_2_cabs_index(self):
        for i in range(len(self.large_op_list)):
            count = 0
            for j in range(len(self.coeff_list[i])):
                if 'x' <= self.coeff_list[i][j][0] <= 'z' and len(self.coeff_list[i]) == 4:
                    count += 1
            if count == 2:
                return 1
        return 0

    def gbc_ebc(self):
        # generalized BC --> GBC : F^i_alpha = 0
        # extended BC --> EBC: F^a_alpha = 0
        # So, EBC + GBC: F^p_CABS = 0
        # EBC: Such condition is only fulfilled if the basis set
        # is saturated for each angular momentum involved in this basis set
        # Not sure if this is true for these tiny basis-sets!
        flag = 0
        if len(self.large_op_list) == 3:
            gen_index = False
            CABS_index = False
            occ_index = False
            vir_index = False
            for items in self.coeff_list[1]:
                if 'a' <= items[0] <= 'h':
                    vir_index = True
                if 'p' <= items[0] <= 'u':
                    gen_index = True
                if 'i' <= items[0] <= 'n':
                    occ_index = True
                if 'A' <= items[0] <= 'H':
                    CABS_index = True
                if (gen_index or occ_index or vir_index) and CABS_index:
                    flag = 1
                    return flag
        return flag

    def convert_into_einsum(self, f, sign):
        numpy_map = {'i0': 'i', 'j0': 'j', 'i1': 'k', 'j1': 'l',
                     'a0': 'a', 'b0': 'b', 'a1': 'c', 'b1': 'd',
                     'A0': 'A', 'B0': 'B', 'A1': 'C', 'B1': 'D',
                     'p0': 'p', 'q0': 'q', 'r0': 'r', 's0': 's',
                     'p1': 't', 'q1': 'u', 
                     'x0': 'x', 'y0': 'y', 'x1': 'w', 'y1': 'z'}
        final_string = ''
        Hamiltonian_block = ''
        if len(self.st[0][0].upper) == 2:
            Hamiltonian_block += 'H_2body['
        else:
            Hamiltonian_block += 'H_1body['
        # print(self.st[0][0].upper)
        # print(self.st[0][0].lower)
        for item in self.st[0][0].upper:
            if 'p' <= item[0] <= 'u':
                Hamiltonian_block += ':, '
            if 'a' <= item[0] <= 'h':
                Hamiltonian_block += 'slice_v, '
            if 'i' <= item[0] <= 'n':
                Hamiltonian_block += 'slice_o, '
        for item in self.st[0][0].lower:
            if 'p' <= item[0] <= 'u':
                Hamiltonian_block += ':, '
            if 'a' <= item[0] <= 'h':
                Hamiltonian_block += 'slice_v, '
            if 'i' <= item[0] <= 'n':
                Hamiltonian_block += 'slice_o, '
        Hamiltonian_block = Hamiltonian_block[0:len(Hamiltonian_block)-2]
        Hamiltonian_block += ']'
        new_coeff = []
        tmp_list = []
        size = len(self.large_op_list)
        for i in range(size):
            for items in self.coeff_list[i]:
                tmp_list.append(items)
            new_coeff.append(tmp_list)
            tmp_list = []
        print('new_coeff before: ', new_coeff)
        print('self.large_op_list before: ', self.large_op_list)
        # put everything in ijab format!, rename R22 to R2
        for i, items in enumerate(self.large_op_list):
            if items.name == 'R2' or items.name == 'R22':
                self.large_op_list[i].name = 'R2'
                # swap (0,1) with (2,3)
                temp = new_coeff[i][2]
                temp1 = new_coeff[i][3]
                new_coeff[i][2] = new_coeff[i][0]
                new_coeff[i][3] = new_coeff[i][1]
                new_coeff[i][0] = temp
                new_coeff[i][1] = temp1
        # rename everything to R2
        for i, items in enumerate(self.large_op_list):
            if items.name == 'R2D' or items.name == 'R22D':
                self.large_op_list[i].name = 'R2'
        # here I want to convert R2, V2_CABS to a fixed layout!
        # A/Q MPQC: <i j| R |b a’>,  <p' r'| G |s' a'>
        # CABS at the end of R2 and V2_CABS
        flag = 0
        i_star = 0
        j_star = 0
        for i, items in enumerate(self.large_op_list):
            if items.name == 'V2':
                for j in range(4):
                    if 'x' <= new_coeff[i][j][0] < 'z':
                        flag = 1
                        i_star = i
                        j_star = j
                        break
                if flag:
                    self.large_op_list[i].name = 'V2_gg_gc'
                    temp_0 = new_coeff[i_star][0]
                    temp_1 = new_coeff[i_star][1]
                    temp_2 = new_coeff[i_star][2]
                    temp_3 = new_coeff[i_star][3]
                    if j_star == 0:
                        # make it [[3,2], [1,0]]
                        new_coeff[i_star][0] = temp_3
                        new_coeff[i_star][1] = temp_2
                        new_coeff[i_star][2] = temp_1
                        new_coeff[i_star][3] = temp_0
                    elif j_star == 1:
                        # make it [[2,3], [0,1]]
                        new_coeff[i_star][0] = temp_2
                        new_coeff[i_star][1] = temp_3
                        new_coeff[i_star][2] = temp_0
                        new_coeff[i_star][3] = temp_1
                    elif j_star == 2:
                        # make it [[1,0], [3,2]]
                        new_coeff[i_star][0] = temp_1
                        new_coeff[i_star][1] = temp_0
                        new_coeff[i_star][2] = temp_3
                        new_coeff[i_star][3] = temp_2
                    else:
                        pass
                else:
                    self.large_op_list[i].name = 'V2_gg_gg'
        print('self.large_op_list: ', self.large_op_list)
        for i, items in enumerate(self.large_op_list):
            if items.name == 'R2':
                for j in range(4):
                    if 'x' <= new_coeff[i][j][0] < 'z':
                        i_star = i
                        j_star = j
                        break
                print('i_star: ', i_star)
                print('j_star: ', j_star)
                print('new_coeff[i_star]: ', new_coeff[i_star])
                print('new_coeff: ', new_coeff)
                temp_0 = new_coeff[i_star][0]
                temp_1 = new_coeff[i_star][1]
                temp_2 = new_coeff[i_star][2]
                temp_3 = new_coeff[i_star][3]
                if j_star == 2:
                    # make it [[1,0],[3,2]]
                    new_coeff[i_star][0] = temp_1
                    new_coeff[i_star][1] = temp_0
                    new_coeff[i_star][2] = temp_3
                    new_coeff[i_star][3] = temp_2
        print('self.large_op_list after: ', self.large_op_list)
        print('new_coeff (R2D, R22, R22D, V2_CABS) after : ', new_coeff)
        oper_list = ''
        # need to modify oper_list for adding slices of Fock matrix!
        # Also, need to have Fock_CABS_gen (bring everything into this format)
        # and Fock_CABS_CABS
        Fock_block = ''
        cabs_count = 0
        for i in range(size):
            Fock_block = ''
            if self.large_op_list[i].name == 'F1' or self.large_op_list[i].name == 'H1':
                Fock_block += self.large_op_list[i].name
                for indices in new_coeff[i]:
                    if 'x' <= indices[0] <= 'z':
                        cabs_count += 1
                print('cabs_count: ', cabs_count)
                if not cabs_count:
                    Fock_block += '_gg'
                    for indices in new_coeff[i]:
                        if 'p' <= indices[0] <= 'u':
                            Fock_block += ':, '
                        elif 'i' <= indices[0] <= 'n':
                            Fock_block += 'slice_o, '
                        elif 'a' <= indices[0] <= 'h':
                            Fock_block += 'slice_v, '
                        else:
                            pass
                    Fock_block = Fock_block[:5] + '[' + Fock_block[5:]
                    Fock_block = Fock_block[0:len(Fock_block)-2]
                    Fock_block += ']'
                if cabs_count == 1:
                    # make sure cabs index appears last 
                    if 'x' <= new_coeff[i][0][0]  <= 'z':
                        temp = new_coeff[i][1]
                        new_coeff[i][1] = new_coeff[i][0]
                        new_coeff[i][0] = temp
                    Fock_block += '_gc['
                    # now the slicing : slice_o, slice_v and :,
                    if 'p' <= new_coeff[i][0][0] <= 'u':
                        Fock_block += ':'
                    if 'i' <= new_coeff[i][0][0] <= 'n':
                        Fock_block += 'slice_o'
                    if 'a' <= new_coeff[i][0][0] <= 'h':
                        Fock_block += 'slice_v'
                    Fock_block += ', :]'
                if cabs_count == 2:
                    # F_x_x
                    Fock_block += '_cc'
                oper_list += Fock_block
            elif self.large_op_list[i].name == 'A':
                # make sure V_F12 is in the format V^ij_pq
                if 'i' <= new_coeff[i][2][0] <= 'n' and 'i' <= new_coeff[i][3][0] <= 'n':
                    # swap 0,1 withn 2,3
                    tmp_0 = new_coeff[i][0]
                    tmp_1 = new_coeff[i][1]
                    tmp_2 = new_coeff[i][2]
                    tmp_3 = new_coeff[i][3]
                    new_coeff[i][0] = tmp_2
                    new_coeff[i][1] = tmp_3
                    new_coeff[i][2] = tmp_0
                    new_coeff[i][3] = tmp_1
                tmp_str = 'V_F12_oo_gg[:, :, '
                for j in range(2, 4):
                    if 'p' <= new_coeff[i][j][0] <= 'u':
                        tmp_str += ':, '
                    if 'i' <= new_coeff[i][j][0] <= 'n':
                        tmp_str += 'slice_o, '
                    if 'a' <= new_coeff[i][j][0] <= 'h':
                        tmp_str += 'slice_v, '
                tmp_str = tmp_str[0:len(tmp_str)-2]
                tmp_str += ']'
                oper_list += tmp_str
            elif self.large_op_list[i].name == 'B':
                oper_list += 'B_F12_oo_oo'
            elif self.large_op_list[i].name == 'C':
                oper_list += 'X_F12_oo_oo'
            elif self.large_op_list[i].name == 'V2_gg_gc':
                tmp_str = 'V2_gg_gc['
                for j in range(3):
                    if 'p' <= new_coeff[i][j][0] <= 'u':
                        tmp_str += ':, '
                    if 'i' <= new_coeff[i][j][0] <= 'n':
                        tmp_str += 'slice_o, '
                    if 'a' <= new_coeff[i][j][0] <= 'h':
                        tmp_str += 'slice_v, '
                tmp_str = tmp_str[0:len(tmp_str)-2]
                tmp_str += ', :]'
                oper_list += tmp_str
            elif self.large_op_list[i].name == 'R2':
                 oper_list += 'R2_oo_vc'
            else:
                oper_list += self.large_op_list[i].name
            if i != size-1:
                oper_list += ', '
        print('oper_list: ', oper_list)
        for i in range(size):
            for j in range(len(new_coeff[i])):
                new_coeff[i][j] = numpy_map[new_coeff[i][j]]
        print('new_coeff after: ', new_coeff)
        for i in range(size):
            for j in range(len(new_coeff[i])):
                final_string += new_coeff[i][j]
            if i != size-1 and size > 1:
                final_string += ','
        final_string += '->'
        for item in self.st[0][0].upper:
            tmp_list.append(numpy_map[item])
        for item in self.st[0][0].lower:
            tmp_list.append(numpy_map[item])
        for items in tmp_list:
            final_string += items
        print('final_string: ', final_string)
        prefactor = self.fac * sign
        if 'B_F12_oo_oo' in oper_list and 'H_1body' in Hamiltonian_block:
            f.write('    # {} += {} * np.einsum(\'{}\', {})\n'.format(Hamiltonian_block, prefactor, final_string, oper_list))
        elif 'X_F12_oo_oo' in oper_list and 'H_1body' in Hamiltonian_block:
            f.write('    # {} += {} * np.einsum(\'{}\', {})\n'.format(Hamiltonian_block, prefactor, final_string, oper_list))
        elif 'V_F12_oo_gg' in oper_list and 'H_1body' in Hamiltonian_block:
            f.write('    # {} += {} * np.einsum(\'{}\', {})\n'.format(Hamiltonian_block, prefactor, final_string, oper_list))
        elif 'V_F12_oo_gg' in oper_list and 'H_2body' in Hamiltonian_block:
            f.write('    # {} += {} * np.einsum(\'{}\', {})\n'.format(Hamiltonian_block, prefactor, final_string, oper_list))
        else:
            f.write('    {} += {} * np.einsum(\'{}\', {})\n'.format(Hamiltonian_block, prefactor, final_string, oper_list))


def get_parameters(f):
    ngen = '    ngen = info[0]\n'
    f.write(ngen)
    nocc = '    nocc = info[1]\n'
    f.write(nocc)
    nvir = '    nvir = info[2]\n'
    f.write(nvir)
    H1_gg = '    H1_gg = info[3]\n'
    f.write(H1_gg)
    H1_gc = '    H1_gc = info[4]\n'
    f.write(H1_gc)
    F1_gg = '    F1_gg = info[5]\n'
    f.write(F1_gg)
    F1_g_c = '    F1_gc = info[6]\n'
    f.write(F1_g_c)
    F1_c_c = '    F1_cc = info[7]\n'
    f.write(F1_c_c)
    V2_gg_gg = '    V2_gg_gg = info[8]\n'
    f.write(V2_gg_gg)
    V2_CABS = '    V2_gg_gc = info[9]\n'
    f.write(V2_CABS)
    R2 = '    R2_oo_vc = info[10]\n'
    f.write(R2)
    A = '    V_F12_oo_gg = info[11]\n'
    f.write(A)
    C = '    X_F12_oo_oo = info[12]\n'
    f.write(C)
    B = '    B_F12_oo_oo = info[13]\n'
    f.write(B)
