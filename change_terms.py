# accompanied always with term.cond_cont in order to generate map_org
# dont need the dict correct later

import class_term
import print_op
import copy


def change_terms1(a, b, fac, dict_ind, list_op_used):

    sum_ind = []
    coeff = []
    list_terms = []

    if fac != 0:
        for op in list_op_used:
            # print 'op: ', op
            fac = op.fac*fac
            # Only multiply op.fac when computing the outermost commutator
            sum_ind.extend(op.sum_ind)
            coeff.append(op.coeff)
            # print 'sum_ind: ', sum_ind
            # print 'coeff: ', coeff
        print(fac, 'fac is this for each term')
    else:
        fac = 1.0
        for op in list_op_used:
            sum_ind.extend(op.sum_ind)
            coeff.append(op.coeff)
            # print 'op: ', op
            # print 'sum_ind: ', sum_ind
            # print 'coeff: ', coeff

    for (t, c) in zip(a, b):
        t = [t]  # as t is a list of terms and each term has operators like delta and op
        c = [c]
        # to make coeff list of the operator so that it can be compared in the compare function
        # AK: deleted the comment!
        flag = 0
        temp = []
        for item in t[0]:
            if item.kind == 'op':
                temp = []
                flag = 1
                temp.extend(item.upper)
                temp.extend(item.lower)
        if flag == 1:  # if there is an operator
            coeff.append(temp)
        # print 'coeff: ', coeff
        # x=class_term.term(copy.copy(fac*c[0][0]), copy.copy(sum_ind), copy.copy(coeff), list_op_used,t, c)
        x = class_term.term(copy.copy(fac*c[0][0]*c[0][1]), copy.copy(sum_ind), copy.copy(coeff), list_op_used, t, c)
        # AK c[0][1] was missing!!!
        x.dict_ind = dict_ind
        if flag == 1:
            coeff.pop()
        # print c
        # print_op.print_op(t,c)
        # print c,fac, sum_ind, coeff
        list_terms.append(x)
    return list_terms
