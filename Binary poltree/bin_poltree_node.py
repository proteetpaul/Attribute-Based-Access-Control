from anytree import NodeMixin

class node(NodeMixin):
    """Class to represent node of the binary policy tree"""
    def __init__(self,id):
        super(node, self).__init__()
        self.id=id
        self.attrib=None
        self.value = None
        self.left = None
        self.right = None
        self.avp_list = dict()