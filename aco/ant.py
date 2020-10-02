import numpy as np

class Ant:
    def __init__(self, a, b, num_vertices, edges):
        # weights a and b balances decision of ant
        self.a = a
        self.b = b
        self.n = num_vertices
        self.edges = edges  # nxn matrix
        self.reset()
    
    def reset(self):
        '''Reset everything before starting tour
        '''
        self.unvisited = [i for i in range(self.n)]
        self.tour = []
        self.total_distance = 0.0

    def select_edge(self, u):
        '''
        Selecting next edge from last vertex
        Probability of choosing vertex v from u is:
            p = ((phrm_uv)^a * (1 / dist_uv)^b) / sum over all unvisited vertices and u
                phrm is pheromone and dist is weight of edge uv
        '''
        probs = []
        for v in self.unvisited:
            edge = self.edges[u][v]
            prob = pow(edge.pheromone, self.a) / pow(edge.weight, self.b)
            probs.append(prob)

        probs = np.array(probs)
        probs = probs / probs.sum()
        v = np.random.choice(self.unvisited, p=probs)
        self.unvisited.remove(v)
        return v
    
    def fix_tour_4(self):
        for i in range(self.n - 4):
            x, y, z, w = self.tour[i], self.tour[i+1],\
                        self.tour[i+2], self.tour[i+3]
            if self.edges[x][z].weight + self.edges[y][w].weight <\
                self.edges[x][y].weight + self.edges[z][w].weight:
                self.tour[i+1], self.tour[i+2] = self.tour[i+2], self.tour[i+1]
                self.total_distance -= (self.edges[x][y].weight + self.edges[z][w].weight)
                self.total_distance += (self.edges[x][z].weight + self.edges[y][w].weight)
    
    def fix_tour_5(self):
        for i in range(self.n - 5):
            x, y, z, u, v = self.tour[i], self.tour[i+1],\
                        self.tour[i+2], self.tour[i+3], self.tour[i+4]
            path1 = self.edges[x][y].weight + self.edges[y][z].weight+\
                    self.edges[z][u].weight + self.edges[u][v].weight
            path2 = self.edges[x][y].weight + self.edges[y][u].weight+\
                    self.edges[u][z].weight + self.edges[z][v].weight
            path3 = self.edges[x][z].weight + self.edges[z][y].weight+\
                    self.edges[y][u].weight + self.edges[u][v].weight
            path4 = self.edges[x][z].weight + self.edges[z][u].weight+\
                    self.edges[u][y].weight + self.edges[y][v].weight
            path5 = self.edges[x][u].weight + self.edges[u][z].weight+\
                    self.edges[z][y].weight + self.edges[y][v].weight
            path6 = self.edges[x][u].weight + self.edges[u][y].weight+\
                    self.edges[y][z].weight + self.edges[z][v].weight
            poss_paths = [path1, path2, path3, path4, path5, path6]
            min_path = min(poss_paths)
            if min_path == path1:
                continue
            elif min_path == path2:
                x1, x2, x3, x4, x5 =  x, y, u, z, v
            elif min_path == path3:
                x1, x2, x3, x4, x5 =  x, z, y, u, v
            elif min_path == path4:
                x1, x2, x3, x4, x5 =  x, z, u, y, v
            elif min_path == path5:
                x1, x2, x3, x4, x5 =  x, u, z, y, v
            elif min_path == path6:
                x1, x2, x3, x4, x5 =  x, u, y, z, v
            self.tour[i], self.tour[i+1],\
                    self.tour[i+2], self.tour[i+3], self.tour[i+4] = x1, x2, x3, x4, x5
            self.total_distance = self.total_distance - path1 + min_path
    
    def complete_tour(self):
        self.reset()

        u = np.random.choice(self.unvisited)
        self.tour.append(u)
        self.unvisited.remove(u)

        for _ in range(self.n - 1):
            v = self.select_edge(u)
            self.tour.append(v)
            self.total_distance += self.edges[u][v].weight
            u = v
        
        self.fix_tour_5()

    def update_used_pheromones(self, Q):
        '''
        Add pheromone deposit to used edges in tour
        '''
        deposit = Q / self.total_distance
        for i in range(self.n - 1):
            u, v = self.tour[i], self.tour[i+1]
            self.edges[v][u].pheromone += deposit
            self.edges[u][v].pheromone += deposit
