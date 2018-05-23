import random as rnd
from projection import *


class ProjectionLinear(Projection):
    def __init__(self):
        super().__init__()

    def theta(self, vector, z):
        N = len(vector)
        U = [i for i in range(N)]
        s = 0
        rho = 0
        iter = 0
        while len(U) > 0:
            iter += 1
            lenU = len(U)
            i = 0
            j = 0
            G = [-1] * lenU
            L = G[:]

            k0 = rnd.randint(0, lenU - 1)
            k = U[k0]
            ds = 0

            for m in U:
                iter += 1
                if m == k:
                    ds += vector[m]
                elif vector[m] >= vector[k]:
                    G[i] = m
                    ds += vector[m]
                    i += 1
                else:
                    L[j] = m
                    j += 1
            drho = i + 1
            if (s + ds) - (rho + drho) * vector[k] < z:
                s += ds
                rho += drho
                U = L[:j]
            else:
                U = G[:i]
        if rho == 0:
            print('Debug point')
            return None
        return (s - z) / rho


class LinearWorker(ProjectionWorker):
    def __init__(self, vector_struct, z, project_type: ProjectionSurface):
        super().__init__(vector_struct=vector_struct, z = z, project_type=project_type)
        self.projector = ProjectionLinear()

    def update(self, vector_struct):
        self.vector_struct = vector_struct

    def project(self):
        N = len(self.vector_struct)
        if self.project_type in (ProjectionSurface.BALL, ProjectionSurface.SPHERE):
            v_abs = list(map(abs, self.vector_struct))
        else:
            v_abs = self.vector_struct
        v_norm = sum(v_abs)
        if self.project_type is ProjectionSurface.BALL and v_norm <= z + self.eps:
            return self.vector_struct
        if self.project_type is ProjectionSurface.SPHERE and abs(v_norm - z) < self.eps:
            return self.vector_struct
        theta = self.projector.theta(v_abs, self.z)
        if theta is None:
            print('Error while making linear projection!!!')
            return None
        w = [0] * N
        if self.project_type in (ProjectionSurface.SPHERE, ProjectionSurface.BALL):
            for i in range(N):
                w[i] = max(v_abs[i] - theta, 0) if self.vector_struct[i] >= 0 else -max(v_abs[i] - theta, 0)
        else:
            for i in range(N):
                w[i] = max(v_abs[i] - theta, 0)
        return w

pr = LinearWorker([-2,1,0,0],1,ProjectionSurface.SIMPLEX)
v = pr.project()
print(v)
#pr = ProjectionLinear(project_type=ProjectionSurface.SIMPLEX)
#v = pr.project([0.5,1,0,0],1)

#print(v)