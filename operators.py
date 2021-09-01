import func_ewt
# import operators as op
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
            term_to_remove.append(index)
    for index in sorted(term_to_remove, reverse=True):
        list_terms.pop(index)
    # want to call the compress function here!
    for item in list_terms:
        item.resolve_gammas_HF()
        item.compress_AK_HF()
    count = 0
    for item in list_terms:
        flag = item.identify_f12_intermediates()
        if flag:
            count += 1
        item.resolve_cabs_to_vir()
    print('number of V/B terms: ', count)
    # I need to experiment a bit with EBC and GBC
    # Disabled the gbc_ebc function for now!
    # term_to_remove = []
    # for index, items in enumerate(list_terms):
    #     removed = items.gbc_ebc()
    #     if removed:
    #         term_to_remove.append(index)
    # for index in sorted(term_to_remove, reverse=True):
    #     list_terms.pop(index)


def allocate_memory(list_list_terms, file=None):
    if file:
        Hamiltonian_arr = []
        sizes_arr = []
        for list_terms in list_list_terms:
            for items in list_terms:
                Hamiltonian_block, sizes = items.allocate_shapes_memory(file)
                print(Hamiltonian_block)
                if Hamiltonian_block not in Hamiltonian_arr:
                    # Hamiltonian_arr.append([Hamiltonian_block, sizes])
                    Hamiltonian_arr.append(Hamiltonian_block)
                    sizes_arr.append(sizes)
                    print('H_arr: ', Hamiltonian_arr)
        for i, items in enumerate(Hamiltonian_arr):
            file.write('{} = np.zeros({})\n'.format(Hamiltonian_arr[i], sizes_arr[i]))


def einsum_expressions(list_list_terms, file=None):
    if file:
        for list_terms in list_list_terms:
            for items in list_terms:
                items.convert_into_einsum(file)






