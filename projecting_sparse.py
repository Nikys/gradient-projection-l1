import numpy as np
from rb_tree import RBTree, RBTreeNode
from projection import *


class RBTreeVector:
    __slots__ = ['vector','nodes','tree','dim']

    def __init__(self, vector):
        self.vector = vector
        self.dim = len(vector)
        self.tree = RBTree()
        self.nodes = []
        for el in vector:
            if abs(el) < 1e-6:
                self.nodes.append(self.tree.nil)
            else:
                self.nodes.append(self.tree.insert(el))

    def update(self,new_vector):
        for i,el in enumerate(new_vector):
            if abs(new_vector[i] - el) < 1e-6:
                continue
            if self.nodes[i] != self.tree.nil:
                self.tree.delete_node(self.nodes[i])
            if abs(el) > 1e-6:
                self.nodes[i] = self.tree.insert(el)
            else:
                self.nodes[i] = self.tree.nil
        self.vector = new_vector


class ProjectionSparse(Projection):
    def __init__(self):
        super().__init__()

    def theta(self, vector_struct: RBTreeVector, z):
        global v0, rho0, s0, T
        T = vector_struct.tree
        v0 = np.inf
        rho0 = vector_struct.dim + 1
        s0 = z

        def pivot_search(v: RBTreeNode, rho, s):
            global v0, rho0, s0, T
            """
            Main procedure that works with subtrees in aforementioned method
            :param v: subtree (node) of Red-Black-tree
            :param rho: parameter for finding amount of non-zero components
            :param s: sum-parameter
            :return: theta-parameter for initializing projected vector
            """
            rho_t = rho + v.right_amount + 1
            s_t = s + v.right_sum + v.key
            if s_t < v.key * rho_t + z:
                """v>=pivot"""
                if v0 > v.key:
                    v0 = v.key
                    rho0 = rho_t
                    s0 = s_t
                if T.is_leaf(v) or v.left_amount == 0:
                    return (s0 - z) / rho0
                return pivot_search(v.left, rho_t, s_t)
            else:
                """v<pivot"""
                if T.is_leaf(v) or v.right_amount == 0:
                    return (s0 - z) / rho0
                return pivot_search(v.right, rho, s)

        return pivot_search(T.root.left, 0, 0)


class SparseWorker(ProjectionWorker):
    def __init__(self, vector_struct, z, project_type: ProjectionSurface):
        super().__init__(vector_struct=RBTreeVector(vector_struct), z=z, project_type=project_type)
        self.projector = ProjectionSparse()

    def update(self, vector_struct):
        self.vector_struct.update(vector_struct)

    def project(self):
        N = self.vector_struct.dim
        if self.project_type in (ProjectionSurface.BALL, ProjectionSurface.SPHERE):
            v_abs = list(map(abs, self.vector_struct.vector))
            v_struct = RBTreeVector(v_abs)
        else:
            v_abs = self.vector_struct.vector
            v_struct = self.vector_struct
        v_norm = sum(v_abs)
        if self.project_type is ProjectionSurface.BALL and v_norm <= self.z + self.eps:
            return self.vector_struct.vector
        if self.project_type is ProjectionSurface.SPHERE and abs(v_norm - self.z) < self.eps:
            return self.vector_struct.vector
        theta = self.projector.theta(v_struct, self.z)
        w = [0] * N
        if self.project_type in (ProjectionSurface.SPHERE, ProjectionSurface.BALL):
            for i in range(N):
                w[i] = max(v_abs[i] - theta, 0) if self.vector_struct.vector[i] >= 0 else -max(v_abs[i] - theta, 0)
        else:
            for i in range(N):
                w[i] = max(v_abs[i] - theta, 0)
        return w

pr = SparseWorker([-2,1,0,0],1,ProjectionSurface.SIMPLEX)
v = pr.project()

#pr = ProjectionSparse(project_type=ProjectionSurface.SIMPLEX)
#v = pr.project([0.5,1,0,0],1)

print(v)