import numpy as np
from rb_tree import RBTree, RBTreeNode


def theta_project_sparse(T: RBTree,N,z):
    """
    Finding parameter theta for projecting positive vector of sparse data on simplex
    :param T: Red-Black-tree with data
    :param z: scalar that represents l1-constraints
    :return: theta-parameter for initializing projected vector
    """
    global v0, rho0, s0
    v0 = np.inf
    rho0 = N+1
    s0 = z
    def pivot_search(v: RBTreeNode,rho,s):
        global v0, rho0, s0
        """
        Main procedure that works with subtrees in aforementioned method
        :param v: subtree (node) of Red-Black-tree
        :param rho: parameter for finding amount of non-zero components
        :param s: sum-parameter
        :return: theta-parameter for initializing projected vector
        """
        rho_t = rho+v.right_amount+1
        s_t = s + v.right_sum + v.key
        if s_t < v.key * rho_t + z:
            """v>=pivot"""
            if v0 > v.key:
                v0 = v.key
                rho0 = rho_t
                s0 = s_t
            if T.is_leaf(v):
                return (s0-z)/rho0
            return pivot_search(v.left,rho_t,s_t)
        else:
            """v<pivot"""
            if T.is_leaf(v):
                return (s0-z)/rho0
            return pivot_search(v.right,rho,s)
    return pivot_search(T.root.left,0,0)

"""theta_vector = []
theta_sum = 0
v = [10,20,30,80,20,0,0]
N = len(v)
T = RBTree()
for v_el in v:
    #non-zero components, actually - positive
    if abs(v_el) > 1e-6:
        T.insert(v_el)
"""