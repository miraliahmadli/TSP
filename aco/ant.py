import numpy as np

class Ant:
    def __init__(self, a, b, num_vertices, graph):
        # weights a and b balances decision of ant
        self.a = a
        self.b = b
        self.n = num_vertices
        self.graph = graph  # nxn matrix
        self.reset()
    
    def reset(self):
        '''Reset everything before starting tour
        '''
        self.unvisited = [i for i in range(self.n)]
        self.tour = []
        self.total_distance = 0.0

    def select_edge(self, u):
        '''
        Selecting next vertex / edge for given last vertex
        Probability of choosing edge uv (vertex v from given u) is:
            p = ((phrm_uv)^a * (1 / dist_uv)^b) / (sum over all unvisited vertices and u)
                phrm is pheromone and dist is weight of edge uv
        '''
        probs = []
        for v in self.unvisited:
            prob = pow(self.graph.pheromones[u][v], self.a) /\
                     pow(self.graph.weights[u][v], self.b)
            probs.append(prob)

        probs = np.array(probs)
        probs = probs / probs.sum()
        v = np.random.choice(self.unvisited, p=probs)
        self.unvisited.remove(v)
        return v
    
    def fix_tour_4(self):
        '''
        This function iterates over the completed tour and tries to fix irregularities
        
        In every iteration, it takes 4 consecutive vertices (x -> y -> z -> w)
        and tries to optimize it by looking at all possible permutations of (y, z) vertices,
        
        In other words it looks at (x -> y -> z -> w) amd (x -> z -> y -> w)
        and chooses minimum of these
        '''
        for i in range(self.n - 4):
            x, y, z, w = self.tour[i], self.tour[i+1],\
                        self.tour[i+2], self.tour[i+3]
            if self.graph.weights[x][z] + self.graph.weights[y][w] <\
                self.graph.weights[x][y] + self.graph.weights[z][w]:
                self.tour[i+1], self.tour[i+2] = self.tour[i+2], self.tour[i+1]
                self.total_distance -= (self.graph.weights[x][y] + self.graph.weights[z][w])
                self.total_distance += (self.graph.weights[x][z] + self.graph.weights[y][w])
    
    def fix_tour_5(self):
        '''
        This function iterates over the completed tour and tries to fix irregularities
        
        In every iteration, it takes 5 consecutive vertices (x -> y -> z -> u -> v)
        and tries to optimize it by looking at all possible permutations of 
        (y, z, u) vertices and chooses minimum result
        '''
        for i in range(self.n - 5):
            x, y, z, u, v = self.tour[i], self.tour[i+1],\
                        self.tour[i+2], self.tour[i+3], self.tour[i+4]
            xy, xz, xu = self.graph.weights[x][y], self.graph.weights[x][z],\
                            self.graph.weights[x][u]
            yz, yu, yv = self.graph.weights[y][z], self.graph.weights[y][u],\
                            self.graph.weights[y][v]
            zu, zv, uv = self.graph.weights[z][u], self.graph.weights[z][v],\
                            self.graph.weights[v][u]

            path1 = xy + yz + zu + uv
            path2 = xy + yu + zu + zv
            path3 = xz + yz + yu + uv
            path4 = xz + zu + yu + yv
            path5 = xu + zu + yz + yv
            path6 = xu + yu + yz + zv
            poss_paths = [path1, path2, path3, path4, path5, path6]
            min_path = min(poss_paths)

            if min_path == path1:
                continue
            elif min_path == path2:
                x1, y1, z1, u1, v1 =  x, y, u, z, v
            elif min_path == path3:
                x1, y1, z1, u1, v1 =  x, z, y, u, v
            elif min_path == path4:
                x1, y1, z1, u1, v1 =  x, z, u, y, v
            elif min_path == path5:
                x1, y1, z1, u1, v1 =  x, u, z, y, v
            elif min_path == path6:
                x1, y1, z1, u1, v1 =  x, u, y, z, v
            self.tour[i], self.tour[i+1],\
                    self.tour[i+2], self.tour[i+3], self.tour[i+4] = x1, y1, z1, u1, v1
            self.total_distance = self.total_distance - path1 + min_path
    
    def complete_tour(self):
        '''
        Completes one tour by choosing starting vertex randomly and 
        every time chooses next vertex by calling select_edge function
        '''
        self.reset()

        u = np.random.choice(self.unvisited)
        self.tour.append(u)
        self.unvisited.remove(u)

        for _ in range(self.n - 1):
            v = self.select_edge(u)
            self.tour.append(v)
            self.total_distance += self.graph.weights[u][v]
            u = v
        
        self.fix_tour_5()

    def update_used_pheromones(self, Q):
        '''
        Add pheromone deposit to used edges in tour
        '''
        deposit = Q / self.total_distance
        for i in range(self.n - 1):
            u, v = self.tour[i], self.tour[i+1]
            self.graph.pheromones[v][u] += deposit
            self.graph.pheromones[u][v] += deposit
