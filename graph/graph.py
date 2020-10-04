import numpy as np
import math

def dist2D(u,  v):
    '''
    Distance between 2 vertices 
    '''
    return math.sqrt((u.x - v.x)**2 + (u.y - v.y)**2)


class Vertex:
    '''
    Index and 2D Location of vertex
    '''
    def __init__(self, idx, x, y):
        self.index = idx
        self.x = x
        self.y = y


class Graph:
    '''
    Graph object that contains all of the necessary information 
    about given given graph (vertices and edges)

    Note:
        As all of the deposit pheromone will be set to some value
        less than one, initial pheromone level is set to one

    Attributes:
        n (int): number of vertices in graph
        vertices (list[Vertex]): list of Vertex objects
        pheromones (ndarray): n by n numpy array that contains
            information about pheromone levels of edges
        weights (ndarray): n by n numpy array that contains 
            distance between vertices
    '''

    def __init__(self, vertices):
        self.n = len(vertices)
        self.vertices = vertices
        self.pheromones = np.ones((self.n, self.n))
        self.weights = np.array(
                [[dist2D(vertices[i], vertices[j]) + 1e-6\
                    for i in range(self.n)]
                        for j in range(self.n)])
