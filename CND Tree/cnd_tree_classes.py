from anytree import NodeMixin

class cnd_tree_node(NodeMixin):
    """ Class to represent node of cnd tree """

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.dmbrs = []
        self.cmbrs = []
        self.children_ = list()
        self.isLeaf = True
        self.parent = None

class hds_rectangle:
    """ Class to represent a rectangle in the HDS """

    def __init__(self):
        self.c_arr = []
        self.d_arr = []

class aux_tree_node(NodeMixin):
    """ Class to represent a node of the auxiliary tree """

    def __init__(self):
        super().__init__()
        self.letters = set()
        self.freq = 0
        self.sets = set()
        self.children_ = list()
