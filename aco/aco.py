import math
import random

from tqdm import tqdm
from matplotlib import pyplot as plt

from aco.ant import Ant

class ACO:
    '''
    Ant Colony Optimization solver for TSP
    Args:
        graph (Graph): graph that contains information
                about vertices and edges (pheromone levels and weights)
        colony_size (int): Colony size, number of ants in the ACO
        a (float): Hyperparameter that balances importance of pheromone of edges
        b (float): Hyperparameter that balances importance of weight of edges
        evaporation_rate (float): Evaporation rate of pheromone after each iteration
        iters (int): Number of iterations to make
    '''
    def __init__(self, graph, 
                colony_size=10, 
                a=1.0, b=1.0,
                evaporation_rate=0.1, 
                iters=100, log=False):
        self.graph = graph
        self.n = self.graph.n

        self.a = a
        self.b = b
        self.evap_rate = 1 - evaporation_rate
        self.iters = iters

        self.colony = [Ant(self.a, self.b,
                            self.n, self.graph) 
                                for _ in range(colony_size)]
        self.best_tour = []
        self.best_distance = float("inf")

        self.log = log
        if self.log:
            self.best_distances = [] # best distance after each iteration

    def get_tour_distance(self, tour):
        '''
        Calculate distance for given tour
        '''
        distance = 0.0
        for i in range(self.n - 1):
            u, v = tour[i], tour[i+1]
            distance += self.graph.weights[u][v]
        return distance

    def update_pheromone(self):
        '''
        Apply evaporation rate for all of the edges
        '''
        self.graph.pheromones *= self.evap_rate

    def run(self):
        goal_factor = 0.5
        incr_rate = 0.4 / self.iters
        for it in range(self.iters):
            tqdm_batch = tqdm(total=len(self.colony), dynamic_ncols=True)
            for ant_id, ant in enumerate(self.colony):
                ant.complete_tour()
                if ant.total_distance < self.best_distance:
                    self.best_distance = ant.total_distance
                    self.best_tour = ant.tour[:]
                    self.write_data(f'solutions/solution.csv')

                tqdm_update = "Ant={0:04d},ant_dist={1:08.2f}".format(ant_id+1, ant.total_distance)
                tqdm_batch.set_postfix_str(tqdm_update)
                tqdm_batch.update()

            self.update_pheromone()
            for ant in self.colony:
                ant.update_used_pheromones(self.best_distance * goal_factor)
            goal_factor += incr_rate

            tqdm_batch.close()
            print(f"Iteration={it+1}, best_dist={self.best_distance}")

            if self.log:
                self.best_distances.append(self.best_distance)
        self.save_results()

        if self.log:
            self.plot_convergence()

    def plot(self, save=True, name=None):
        '''
        Plot best tour
        '''
        x = [self.graph.vertices[i].x for i in self.best_tour]
        x.append(x[0])
        y = [self.graph.vertices[i].y for i in self.best_tour]
        y.append(y[0])
        plt.plot(x, y, linewidth=1)
        plt.scatter(x, y, s=math.pi * 2)
        plt.title("Ant Colony Optim")
        for i in self.best_tour:
            plt.annotate(self.graph.vertices[i].index, 
                        (self.graph.vertices[i].x, self.graph.vertices[i].y),
                         size=8)
        if save:
            if name is None:
                name = '{0}.png'.format("ACO")
            plt.savefig(name, dpi=120)
        plt.show()
        plt.gcf().clear()

    def plot_convergence(self, save=True, name=None):
        x = [i+1 for i in range(self.iters)]
        y = self.best_distances
        plt.plot(x, y, linewidth=1)
        plt.scatter(x, y, s=math.pi * 2)
        plt.title("Best distance vs Iteration")
        if save:
            if name is None:
                name = '{0}.png'.format("logs")
            plt.savefig(name, dpi=120)
        plt.show()
        plt.gcf().clear()

    def write_data(self, f_name):
        '''
        Write best tour to csv file
        '''
        tour = [self.graph.vertices[i].index for i in self.best_tour]
        with open(f_name, mode='w+') as f:
            for vertex in tour:
                f.write(str(vertex)) 
                f.write('\n') 

    def save_results(self):
        self.write_data('solutions/solution.csv')
