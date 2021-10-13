def clean_list(list_terms):
    final_terms = []
    for term in list_terms:
        # if term.fac!=0.0 and abs(term.fac)>0.0000001:
        if term.fac != 0.0:
            # print term.fac
            final_terms.append(term)
    # print 'length of final terms',len(final_terms)
    return final_terms


def print_terms(list_terms, filename=None):
    # pfile = open(filename,'a')
    if filename:
        pfile = open(filename, 'w')
    for term in list_terms:
        if term.fac != 0.0:
            term.print_term()
            if filename:
                term.print_latex(pfile)
    if filename:
        pfile.write("------------\\\\ \n")
