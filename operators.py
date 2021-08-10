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
    def __init__(self,name, fac, sum_ind, coeff, st, co):
        self.name=name
        self.fac=fac
        self.sum_ind=sum_ind
        self.coeff=coeff
        self.st=st
        self.co=co
    	self.map_org=[]
    def __repr__(self):
        return self.name
