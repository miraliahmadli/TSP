import math
import random
from matplotlib import pyplot as plt

from aco.ant import Ant

class ACO:
    '''
    Ant Colony Optimization solver for TSP
    '''
    def __init__(self, graph, 
                colony_size=10, 
                a=1.0, b=3.0,
                evaporation_rate=0.1, 
                initial_pheromone=1.0, 
                iters=100):
        self.vertices, self.edges = graph
        # self.graph = graph
        self.n = len(self.vertices)

        self.a = a
        self.b = b
        self.evap_rate = 1 - evaporation_rate
        self.iters = iters

        self.colony = [Ant(self.a, self.b,
                            self.n, self.edges) 
                                for _ in range(colony_size)]
        self.best_tour = []
        self.best_distance = float("inf")

    def get_tour_distance(self, tour):
        distance = 0.0
        for i in range(self.n - 1):
            u, v = tour[i], tour[i+1]
            distance += self.edges[u][v].weight
        return distance

    def update_pheromone(self):
        '''
        Apply evaporation rate for all of the edges
        '''
        for u in range(self.n):
            for v in range(u+1, self.n):
                self.edges[u][v].pheromone *= self.evap_rate
                self.edges[v][u].pheromone *= self.evap_rate

    def run(self):
        goal_factor = 0.5
        incr_rate = 0.4 / self.iters
        for it in range(self.iters):
            for ant in self.colony:
                ant.complete_tour()
                if ant.total_distance < self.best_distance:
                    self.best_distance = ant.total_distance
                    self.best_tour = ant.tour[:]
                    print(f"Step {it}, Best distance {self.best_distance:.2f}")
            self.update_pheromone()
            for ant in self.colony:
                ant.update_used_pheromones(self.best_distance * goal_factor)
            goal_factor += incr_rate

    def plot(self, line_width=1, point_radius=math.sqrt(2.0), annotation_size=8, dpi=120, save=False, name=None):
        x = [self.vertices[i].x for i in self.best_tour]
        x.append(x[0])
        y = [self.vertices[i].y for i in self.best_tour]
        y.append(y[0])
        plt.plot(x, y, linewidth=line_width)
        plt.scatter(x, y, s=math.pi * (point_radius ** 2.0))
        plt.title("ACO")
        for i in self.best_tour:
            plt.annotate(self.vertices[i].index, 
                        (self.vertices[i].x, self.vertices[i].y),
                         size=annotation_size)
        if save:
            if name is None:
                name = '{0}.png'.format("ACO")
            plt.savefig(name, dpi=dpi)
        plt.show()
        plt.gcf().clear()
