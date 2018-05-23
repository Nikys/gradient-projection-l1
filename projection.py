from enum import Enum


class ProjectionSurface(Enum):
    SIMPLEX = 1
    SPHERE = 2
    BALL = 3


class Projection:
    def __init__(self):
        pass

    def theta(self, vector_struct, z):
        pass


class ProjectionWorker:
    __slots__ = ['project_type','projector', 'eps', 'vector_struct', 'z']

    def __init__(self, vector_struct, z, project_type: ProjectionSurface):
        self.vector_struct = vector_struct
        self.z = z
        self.project_type = project_type
        self.eps = 1e-6

    def update(self, vector_struct):
        pass

    def project(self):
        pass
