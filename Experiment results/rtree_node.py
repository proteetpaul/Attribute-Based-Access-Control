from anytree import NodeMixin

class node(NodeMixin):
    """ Class to represent rtree node """

    def __init__(self, id):
        super(node, self).__init__()
        self.id = id
        self.bounding_rectangles = list()
        self.children_ = list()
        self.isLeaf = True
        self.parent = None