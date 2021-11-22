from cnd_tree_classes import cnd_tree_node
import pickle

def get_depth():
    inputfile = open("cnd_tree.pkl", "rb")
    root = pickle.load(inputfile)
    print('Depth=' + str(root.height+1))
