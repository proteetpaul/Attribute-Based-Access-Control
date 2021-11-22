# represents a user entity
class user:
    def __init__(self, id):
        self.id = id
        self.attrib = dict()

# represents an object entity
class object:
    def __init__(self, id):
        self.id = id
        self.attrib = dict()

# represents an environment entity
class env:
    def __init__(self, id):
        self.id = id
        self.attrib = dict()

# represents a list of entities, used to generate the policy tree
class entity_list:
    def __init__(self):
        self.user_list = []
        self.obj_list = []
        self.env_list = []