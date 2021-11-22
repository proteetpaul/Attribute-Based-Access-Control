from rtree_node import node
import pickle

def get_depth():
    inputfile = open("rtree.pkl", "rb")
    root = pickle.load(inputfile)
    x=node(1)
    print(root.height+1)