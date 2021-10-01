import func_ewt
# import operators as op
from class_term import get_parameters
import copy
import print_terms as pt
func = func_ewt

# Define operator and standard operator classes here!


# Pure operator
class operator(object):
    def __init__(self, kind, dag, pos, name, st, pair, spin):
        self.kind = kind
        self.dag = dag
        self.pos = pos
        self.name = name
        self.string = st
        self.pair = pair
        self.spin = spin

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


# Standard Operator (with amplitudes etc.)
class StOperator(object):
    def __init__(self, name, fac, sum_ind, coeff, st, co):
        self.kind = 'StOperator'
        self.name = name
        self.fac = fac
        self.sum_ind = sum_ind
        self.coeff = coeff
        self.st = st
        self.co = co
        self.map_org = []

    def __repr__(self):
        return self.name


def initialize_stoperator(name, prefac, summ_ind, coeff_ind=None):
    opp = func_ewt.contractedobj('op', 1, 1)
    # summ and coeff would be identical!
    summ = [item for sublist in summ_ind for item in sublist]
    if coeff_ind:
        coeff = coeff_ind
    else:
        coeff = [item for sublist in summ_ind for item in sublist]
    opp.upper = summ_ind[0]
    opp.lower = summ_ind[1]
    stp = [[opp]]
    co = [[1, 1]]
    St_op = StOperator(name, prefac, summ, coeff, stp, co)
    St_op.map_org = [St_op]
    return St_op


def simplify_for_HF(list_terms):
    term_to_remove = []
    for index, items in enumerate(list_terms):
        removed = items.simplify_for_HF_ref()
        if removed:
            print('removed!')
            term_to_remove.append(index)
    for index in sorted(term_to_remove, reverse=True):
        list_terms.pop(index)
    # want to call the compress function here!
    for item in list_terms:
        print('be4 resolve_gammas_HF:\n')
        item.print_term()
        #item.resolve_gammas_HF() # TODO: need to correct this! as only occupied indices should be populated!
        #print('after resolve_gammas_HF and be4 compress_AK_HF:\n')
        #item.print_term()
        item.compress_AK_HF()
        print('after compress AK_HF:\n')
        item.print_term()
    count = 0
    for item in list_terms:
        print('count: ', count)
        item.resolve_cabs_to_vir()
        count += 1
    count = 0
    print('inside F12 intermediates section!!')
    for item in list_terms:
        flag = item.identify_f12_intermediates()
        if flag:
            count += 1
    print('number of V/B terms: ', count)
    print('-----------------------------\n')
    print('-----------------------------\n')
    print('-----------------------------\n')
    # I need to experiment a bit with EBC and GBC
    # Disabled the gbc_ebc function for now!
    '''
    term_to_remove = []
    for index, items in enumerate(list_terms):
        removed = items.gbc_ebc()
        if removed:
            term_to_remove.append(index)
    for index in sorted(term_to_remove, reverse=True):
        list_terms.pop(index)
    '''
    term_to_remove = []
    for index, items in enumerate(list_terms):
        removed = items.check_for_2_cabs_index()
        if removed:
            print('these terms have 2 cabs indices and hence removed!!!\n')
            items.print_term()
            term_to_remove.append(index)
    for index in sorted(term_to_remove, reverse=True):
        list_terms.pop(index)


def allocate_memory(file=None):
    if file:
        # file.write('H_1body = np.zeros((ngen, ngen))\n')
        # file.write('H_2body = np.zeros((ngen, ngen, ngen, ngen))\n')
        file.write('    slice_o = slice(0, nocc)\n')
        file.write('    slice_v = slice(nocc, ngen)\n')


def normal_order_two(list_terms):
    # normal order 2 body operators
    # operator only, no fully contracted terms!
    new_list = []
    for items in list_terms:
        tmp = copy.deepcopy(items)
        upper = tmp.st[0][-1].upper
        lower = tmp.st[0][-1].lower
        # first term!
        new_list.append(tmp)
        print('upper: ', upper)
        print('lower: ', lower)
        # next terms --> need to add densities 
        # need to change prefactors and op to 1 body as well!
        pairs = [[0, 0, 1, 1], [1, 1, 0, 0], [0, 1, 1, 0], [1, 0, 0, 1]]
        for i, pair in enumerate(pairs): 
            tmp = copy.deepcopy(items)
            opp = func_ewt.contractedobj('gamma', 1, 1)
            opp.upper = [upper[pair[0]]]
            opp.lower = [lower[pair[1]]]
            tmp.st = [[items.st[0][0]]]
            tmp.st[0].append(opp) 
            opp = func_ewt.contractedobj('op', 1, 1)
            opp.upper = upper[pair[2]]
            opp.lower = lower[pair[3]]
            tmp.st[0].append(opp) 
            if i == 0 or i == 1:
                tmp.fac *= -1.0
            else:
                tmp.fac *= 0.5
            new_list.append(tmp)
    for elements in new_list:
        print('new_list.st: ', elements.st)
    return new_list    


def permute_three_rdm(term):
    upper = term.st[0][0].upper
    lower = term.st[0][0].lower
    print('upper: permute_three: ', upper)
    print('lower: permute_three: ', lower)
    # gamma: ^{0}_{0}, ^{1}_{1}, ^{2}_{2}
    pairs = [[0,0], [1,1], [2,2]]
    new_list = []
    for pair in pairs:
        two_body_term = copy.deepcopy(term)
        opp = func_ewt.contractedobj('gamma', 1, 1)
        opp.upper = [upper[pair[0]]]
        opp.lower = [lower[pair[1]]]
        print('opp.upper: permute_three: ', opp.upper)
        print('opp.lower: permute_three: ', opp.lower)
        two_body_term.st[0][0].upper.pop(pair[0])
        two_body_term.st[0][0].lower.pop(pair[1])
        two_body_term.st[0].append(opp)
        # op should be at the end!
        two_body_term.st[0].reverse()
        print('two_body_term.st: ', two_body_term.st)
        tmp_list = normal_order_two([two_body_term])
        for items in tmp_list:
            new_list.append(items)
    # gamma: ^{0,1}_{0,1}, ^{1,2}_{1,2}, ^{0,2}_{0,2}
    pairs = [[0,1], [1,2], [0,2]]
    for pair in pairs:
        one_body_term = copy.deepcopy(term)
        opp = func_ewt.contractedobj('gamma', 1, 1)
        opp.upper = [upper[pair[0]], upper[pair[1]]]
        opp.lower = [lower[pair[0]], lower[pair[1]]]
        one_body_term.st[0][0].upper.pop(pair[1])
        one_body_term.st[0][0].upper.pop(pair[0])
        one_body_term.st[0][0].lower.pop(pair[1])
        one_body_term.st[0][0].lower.pop(pair[0])
        one_body_term.st[0].append(opp)
        one_body_term.st[0].reverse()
        new_list.append(one_body_term)
    for elements in new_list:
        print('new_list.st: ', elements.st)
    return new_list


def permute_six_rdm(term):
    upper = term.st[0][0].upper
    lower = term.st[0][0].lower
    print('upper: permute_six: ', upper)
    print('lower: permute_six: ', lower)
    # gamma: ^{0}_{1}, ^{0}_{2}, ^{1}_{0}
    # ^{1}_{2}, ^{0}_{1}, ^{0}_{2}
    pairs = [[0,1], [0,2], [1,0], [1,2], [2,0], [2,1]]
    new_list = []
    for pair in pairs:
        two_body_term = copy.deepcopy(term)
        opp = func_ewt.contractedobj('gamma', 1, 1)
        opp.upper = [upper[pair[0]]]
        opp.lower = [lower[pair[1]]]
        two_body_term.st[0][0].upper.pop(pair[0])
        two_body_term.st[0][0].lower.pop(pair[1])
        two_body_term.st[0].append(opp)
        # op should be at the end!
        two_body_term.st[0].reverse()
        two_body_term.fac *= -0.5
        tmp_list = normal_order_two([two_body_term])
        for items in tmp_list:
            new_list.append(items)
    for pair in pairs:
        one_body_term = copy.deepcopy(term)
        opp = func_ewt.contractedobj('op', 1, 1)
        opp.upper = [upper[pair[0]]]
        opp.lower = [lower[pair[1]]]
        one_body_term.st = [[opp]]
        opp = func_ewt.contractedobj('gamma', 1, 1)
        opp.upper = copy.deepcopy(upper) 
        opp.lower = copy.deepcopy(lower) 
        opp.upper.pop(pair[0])
        opp.lower.pop(pair[1])
        one_body_term.st[0].append(opp)
        # op should be at the end!
        one_body_term.st[0].reverse()
        print('one_body_term.st: ', one_body_term.st)
        one_body_term.fac *= -0.5
        new_list.append(one_body_term)
    return new_list


def resolve_2rdm_1rdm(term):
    new_list = []
    for i, oper in enumerate(term.st[0]):
        if oper.kind == 'gamma':
            upper = oper.upper
            lower = oper.lower
            if len(oper.upper) == 2:
                # form: gamma^{p,q}_{r,s} E^{}_{}
                print('upper: ', upper)
                print('lower: ', lower)
                first_term = copy.deepcopy(term)
                first_term.st[0].reverse()
                print('first_term.st[0]: ', first_term.st[0])
                opp = func_ewt.contractedobj('gamma', 1, 1)
                opp.upper = [upper[0]]
                opp.lower = [lower[0]]
                first_term.st[0][1] = opp
                opp = func_ewt.contractedobj('gamma', 1, 1)
                opp.upper = [upper[1]]
                opp.lower = [lower[1]]
                first_term.st[0].append(opp)
                first_term.st[0].reverse()
                new_list.append(first_term)
                print('first_term.st[0]: ', first_term.st[0])
                # second term now!
                second_term = copy.deepcopy(term)
                second_term.st[0].reverse()
                opp = func_ewt.contractedobj('gamma', 1, 1)
                opp.upper = [upper[0]]
                opp.lower = [lower[1]]
                second_term.st[0][1] = opp
                opp = func_ewt.contractedobj('gamma', 1, 1)
                opp.upper = [upper[1]]
                opp.lower = [lower[0]]
                second_term.st[0].append(opp)
                second_term.st[0].reverse()
                second_term.fac *= -0.5
                new_list.append(second_term)
                print('second_term.st[0]: ', second_term.st[0])
                return new_list
    return [term]


def resolve_gammas(term):
    # only general index and occ indexes are left in gammas!
    # so, just make the general index equal to occ_index 
    # and multiply by a factor of 2.0 
    st_i = []
    for i, oper in enumerate(term.st[0]):
        if oper.kind == 'gamma':
            # if general index is present, make sure it becomes
            # equal to the occ index
            lower_ge = False
            upper_ge = False
            st_i.append(i)
            if 'p' <= oper.lower[0][0] <= 'u':
                lower_ge = True
            if 'p' <= oper.upper[0][0] <= 'u':
                upper_ge = True
            for i, item in enumerate(term.coeff_list):
                if upper_ge:
                    if oper.upper[0] in item:
                        index = term.coeff_list[i].index(oper.upper[0])
                        term.coeff_list[i][index] = oper.lower[0]
                elif lower_ge:
                    if oper.lower[0] in item:
                        index = term.coeff_list[i].index(oper.lower[0])
                        term.coeff_list[i][index] = oper.upper[0]
                else:
                    if oper.upper[0] in item:
                        index = term.coeff_list[i].index(oper.upper[0])
                        term.coeff_list[i][index] = oper.lower[0]
            # lists are un-ordered!
            for i, item in enumerate(term.sum_list):
                if upper_ge:
                    if oper.upper[0] == item:
                        index = term.sum_list.index(item)
                        term.sum_list[index] = oper.lower[0]
                if lower_ge:
                    if oper.lower[0] == item:
                        index = term.sum_list.index(item)
                        term.sum_list[index] = oper.upper[0]
                if not upper_ge and not lower_ge:
                    if oper.upper[0] == item:
                        index = term.sum_list.index(item)
                        term.sum_list[index] = oper.lower[0]
                term.sum_list = list(set(term.sum_list))
            # print('final sum: ', term.sum_list) 
    st_i.reverse()
    for items in st_i:
        term.st[0].pop(items)    
    # print('term.st[0]: ', term.st[0])


def resolve_cabs_in_operator(term):
    CABS_inds = ['A0', 'B0', 'A1', 'B1', 'A2', 'B2']
    CABS_pairs = [['A0', 'B0'], ['A1', 'B1'], ['A2', 'B2']]
    flag = 0
    # somehow, one body operators don't have upper and lower variables as lists
    for oper in term.st[0]:
        if oper.kind == 'op':
            if isinstance(oper.upper, str):
                oper.upper = [oper.upper]
                oper.lower = [oper.lower]
    for oper in term.st[0]:
        if oper.kind == 'op':
            cabs_list = []
            print(type(oper.upper))
            print(type(oper.lower))
            for item in oper.upper:
                if item in CABS_inds:
                    cabs_list.append(item)
            for item in oper.lower:
                if item in CABS_inds:
                    cabs_list.append(item)
            for i, item in enumerate(CABS_pairs):
                if CABS_pairs[i][0] in cabs_list and CABS_pairs[i][1] in cabs_list and len(oper.upper) < 3:
                    flag = 1
                    return flag
            if cabs_list:
                for item in cabs_list:
                    for i in range(len(term.coeff_list)):
                        if item in term.coeff_list[i]:
                            index = term.coeff_list[i].index(item)
                            term.coeff_list[i][index] = term.coeff_list[i][index].lower()
                    if item in oper.upper:
                        index = oper.upper.index(item)
                        oper.upper[index] = oper.upper[index].lower()
                    if item in oper.lower:
                        index = oper.lower.index(item)
                        oper.lower[index] = oper.lower[index].lower()
    return flag      


def three_body_decompose(list_terms):
    new_list = []
    for items in list_terms: 
        length = len(items.st[0][0].upper)
        if length == 3:
            tmp_list = permute_three_rdm(items)
            for elements in tmp_list:
                new_list.append(elements)
            tmp_list = permute_six_rdm(items)
            for elements in tmp_list:
                new_list.append(elements)
        else:
            new_list.append(items)
    return new_list


def simplify_three_body_HF(list_terms):
    # 1. remove density terms containing CABS indices!
    term_to_remove = []
    for index, items in enumerate(list_terms):
        removed = items.remove_cabs_density_three_body()
        if removed:
            term_to_remove.append(index)
    for index in sorted(term_to_remove, reverse=True):
        list_terms.pop(index)
    pt.print_terms(list_terms, 'new_list_simplified_1.txt')
    # 2. resolve 2 body densities into 1 body densities!
    new_list = []
    for index, items in enumerate(list_terms):
        tmp_list = resolve_2rdm_1rdm(items) 
        for elements in tmp_list:
            new_list.append(elements)
    for items in new_list:
        resolve_gammas(items)
    # remove if 2 CABS indices on same amplitude in an operator
    # change CABS to vir for others 
    term_to_remove = []
    for index, items in enumerate(new_list):
        removed = resolve_cabs_in_operator(items)
        if removed:
            term_to_remove.append(index)
    print('term_to_remove: ', term_to_remove)
    for index in sorted(term_to_remove, reverse=True):
        new_list.pop(index)
    pt.print_terms(new_list, 'new_list_simplified_2.txt')
    # resolve CABS+ to either CABS_pure or vir
    for items in new_list:
        items.resolve_cabs_to_vir()
    return new_list


def einsum_expressions(list_list_terms, file=None):
    if file:
        file.write('\n\ndef construct_transcorr_H(H_1body, H_2body, info):\n')
        file.write('\n    # Getting parameters!\n')
        get_parameters(file)
        file.write('\n    # slices !!\n')
        allocate_memory(file)
        file.write('\n    # Einsum expressions!!\n')
        for list_terms in list_list_terms:
            file.write('    #  {}  \n'.format(list_terms[2]))
            for items in list_terms[0]:
                items.convert_into_einsum(file, list_terms[1])
            # file.write('# ----------------------------------------------------\n')

