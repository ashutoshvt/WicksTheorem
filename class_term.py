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
                    if 'p' <= oper.upper[0].name[0] <= 's':
                        # find name in coeff
                        # self.coeff_list=[[w.replace(op.upper[0].name, op.lower[0].name)
                        # for w in l] for l in self.coeff_list]
                        for c1 in self.coeff_list:
                            for n, i in enumerate(c1):
                                if i == oper.upper[0].name:
                                    c1[n] = oper.lower[0].name
                        self.sum_list.remove(oper.upper[0].name)
                    elif 'p' <= oper.lower[0].name[0] <= 's':
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
                    if 'p' <= oper.lower[0][0] <= 's':
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
                    if 'p' <= oper.upper[0][0] <= 's':
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
                    if 'p' <= oper.lower[0][0] <= 's':
                        lower_ge = True
                    if 'p' <= oper.upper[0][0] <= 's':
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
                    for i, item in enumerate(self.sum_list):
                        if upper_ge:
                            if oper.upper[0] == item:
                                self.sum_list[i] = oper.lower[0]
                        if lower_ge:
                            if oper.lower[0] == item:
                                self.sum_list[i] = oper.upper[0]
                        if not upper_ge and not lower_ge:
                            if oper.upper[0] == item:
                                self.sum_list[i] = oper.lower[0]
                        self.sum_list = list(set(self.sum_list))
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
        # 0-> V2, 1 -> R2, 2 -> R22 etc!
        if len(self.large_op_list) == 2:
            # print('self.coeff_list', self.coeff_list)
            for i, item in enumerate(CABS_pairs):
                if CABS_pairs[i][0] in self.coeff_list[0] and CABS_pairs[i][1] in self.coeff_list[0]:
                    V2 = True
                    if CABS_pairs[i][0] in self.coeff_list[1] and CABS_pairs[i][1] in self.coeff_list[1]:
                        R2 = True
                        i_indx = i
            if V2 and R2:
                print('looks like V intermediate!')
                print('V2: ', self.coeff_list[0])
                print('R2: ', self.coeff_list[1])
                # I need to re-order the coefficients if B comes before A
                # in both V2 and R2
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
                # print('new_coeff: ', new_coeff)
                self.coeff_list = []
                tmp_list = []
                for i in range(2):
                    for items in new_coeff[i]:
                        tmp_list.append(items)
                    self.coeff_list.append(tmp_list)
                    tmp_list = []
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
        if len(self.large_op_list) == 3:
            R2_1 = False
            R2_2 = False
            # print('self.large_op_list: ', self.large_op_list)
            for i, item in enumerate(CABS_pairs):
                if CABS_pairs[i][0] in self.coeff_list[0] and CABS_pairs[i][1] in self.coeff_list[0]:
                    R2_1 = True
                    if CABS_pairs[i][0] in self.coeff_list[2] and CABS_pairs[i][1] in self.coeff_list[2]:
                        R2_2 = True
                        i_indx = i
            if R2_1 and R2_2:
                # print('looks like X intermediate!')
                print('X0: ', self.coeff_list[0])
                print('X1: ', self.coeff_list[1])
                print('X2: ', self.coeff_list[2])
                print('coeff: ', self.coeff_list)
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
                # re-populate self.coeff_list
                for i, items in enumerate(self.coeff_list):
                    Ai = 'A' + str(i_indx)
                    Bi = 'B' + str(i_indx)
                    if Bi in items:
                        index_B = items.index(Bi)
                        new_coeff[i].pop(index_B)
                    if Ai in items:
                        index_A = items.index(Ai)
                        new_coeff[i].pop(index_A)
                X_F12 = op.initialize_stoperator('C', 1.0, [[], []])
                # remove R2
                self.large_op_list.pop(0)
                # remove R22
                self.large_op_list.pop(1)
                # F, X_F12
                self.large_op_list.append(X_F12)

                print('test: ', self.large_op_list[0].name[0])

                # merge 0 and 2
                print('new_coeff: ', new_coeff)
                # remove R2
                self.coeff_list.pop(0)
                # remove R22
                self.coeff_list.pop(1)
                tmp_list = []
                for i, items in enumerate(new_coeff):
                    if i == 0 or i == 2:
                        for items_i in new_coeff[i]:
                            tmp_list.append(items_i)
                print('tmp_list: ', tmp_list)

                self.coeff_list.append(tmp_list)
                print('self.coeff1: ', self.coeff_list)

                # remove Ai, Bi from sum_list
                self.sum_list.remove(CABS_pairs[i_indx][0])
                self.sum_list.remove(CABS_pairs[i_indx][1])

                flag = 1
        # identify the B intermediate now!
        # B(i0,j0,i1,j1) = R^{AB}_{i0j0} * f^{A}_{C} * R^{CB}_{i1j1} (1)
        #                + R^{AB}_{i0j0} * f^{B}_{C} * R^{AC}_{i1j1} (2)
        # So, I would need to compare two terms now!
        # maybe I can do something like this! (1) - D, (2) - E
        # and then combine D and E later in some other place! --> OK!
        # (f.upper in R2/R22 and f.lower in R2/R22) and both R contains
        # a common CABS index (B or A)
        # TODO: ON IT NOW!
        # R22/R22D F R2/R2D
        if len(self.large_op_list) == 3:
            F_upper = self.coeff_list[1][0]
            F_lower = self.coeff_list[1][1]
            F_upper_0 = False
            F_upper_1 = False
            F_lower_0 = False
            F_lower_1 = False
            first_pos = False
            second_pos = False
            # print('F_upper: ', F_upper)
            # print('F_lower: ', F_lower)
            index_F_upper_0 = 0
            index_F_upper_1 = 0
            index_F_lower_0 = 0
            index_F_lower_1 = 0
            if F_upper in self.coeff_list[0] and F_upper in CABS_inds:
                F_upper_0 = True
                index_F_upper_0 = self.coeff_list[0].index(F_upper)
            if F_upper in self.coeff_list[2] and F_upper in CABS_inds:
                F_upper_1 = True
                index_F_upper_1 = self.coeff_list[2].index(F_upper)
            if F_lower in self.coeff_list[0] and F_lower in CABS_inds:
                F_lower_0 = True
                index_F_lower_0 = self.coeff_list[0].index(F_lower)
            if F_lower in self.coeff_list[2] and F_lower in CABS_inds:
                F_lower_1 = True
                index_F_lower_1 = self.coeff_list[2].index(F_lower)
            if (F_upper_0 and F_lower_1) or (F_upper_1 and F_lower_0):
                # make sure the order is correct!!!
                # check for a common CABS index in self.coeff[0] and self.coeff[2]
                intersect = [value for value in self.coeff_list[0] if value in self.coeff_list[2] and value in CABS_inds]
                print('intersect: ', intersect)
                if intersect:
                    index_0 = self.coeff_list[0].index(intersect[0])
                    index_1 = self.coeff_list[2].index(intersect[0])
                    if index_0 == 0 and index_1 == 0:
                        print(self.coeff_list[0])
                        # print(self.coeff_list[1])
                        print(self.coeff_list[2])
                        print('D term!')
                    else:
                        print('E term!')
        return flag
