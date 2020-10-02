import numpy as np
import math

def dist2D(u,  v):
    '''
    Distance between 2 vertices 
    '''
    return math.sqrt((u.x - v.x)**2 + (u.y - v.y)**2)


class Vertex:
    '''
    Index and Location of vertex
    '''
    def __init__(self, idx, x, y):
        self.index = idx
        self.x = x
        self.y = y


class Edge:
    '''
    Edge has 4 arguments:
    u and v denotes enpoints of edge
    weight is the distance between vertex u and vertex v
    pheromone denotes pheromone level of edge and will be updated after each iteration
    '''
    def __init__(self, u, v, pheromone = 1.):
        self.u = u
        self.v = v
        self.weight = dist2D(u, v)
        self.pheromone = pheromone

class Graph:
    def __init__(self, vertices):
        self.n = len(vertices)
        self.vertices = vertices
        self.pheromones = np.ones((self.n, self.n))
        self.weights = np.array(
                [[dist2D(vertices[i], vertices[j])\
                    for i in range(self.n)]
                        for j in range(self.n)])
