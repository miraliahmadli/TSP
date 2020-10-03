import os
import sys
import time
import argparse

root_dir = os.path.realpath(__file__)
while not root_dir.endswith("TSP"):
  root_dir = os.path.dirname(root_dir)
sys.path.append(root_dir)

from graph.graph import Vertex, Edge, Graph
from aco.aco import ACO


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str,
                         default="ACO", help="Choose algorithm")
    parser.add_argument('-p', type=str,
                         default="./data/a280.tsp", 
                         help="path to the input file")
    parser.add_argument('-cs', type=int,
                         default=50, help="colony size")
    parser.add_argument('-it', type=int,
                         default=100, help="Number of iterations")
    parser.add_argument('-a', type=float,
                         default=1.0, help="pheromone weight")
    parser.add_argument('-b', type=float,
                         default=3.0, help="visibility weight")
    parser.add_argument('-er', type=float,
                         default=0.2, help="evaporation rate")
    args = parser.parse_args()
    return args


def read_data(file_path): 
    # Vertices
    vertices = []
    with open(file_path, "r") as f:
        # coordinates start from the 7th line, end with EOF
        for _ in range(6):
            f.readline()
        for line in f:
            splitted_line = line.split()
            if len(splitted_line) == 3:
                idx, loc_x, loc_y = splitted_line
                v = Vertex(int(idx), float(loc_x), float(loc_y))
                vertices.append(v)

    return vertices


def read_solution(file_path):
    tour = []
    with open(file_path, "r") as f:
        for line in f:
            if "-" in line:
                break
            splitted_line = line.split()
            for v in splitted_line:
                tour.append(int(v) - 1)
    return tour

def main(args):
    print("Reading data and building graph")
    vertices = read_data(args.p)
    graph = Graph(vertices)
    print(f"{args.mode} algorithm")
    if args.mode == "ACO":
        aco = ACO(graph=graph,
                colony_size=args.cs,
                a=args.a, b=args.b,
                evaporation_rate=args.er,
                iters=args.it)
        start = time.time()
        aco.run()
        end = time.time()
        elapsed =  end - start
        assert len(set(aco.best_tour)) == len(aco.best_tour)
        print(f"Elapsed time: {elapsed:.2f}")
        print(f"Best distance by ACO : {aco.best_distance:.2f}")
        aco.plot()
        # Solutions
        # if you have optimal/better solution for x.tsp, 
        # put it in xsol.tsp and visualize using this code 

        # f_path = args.p.replace(".tsp", "sol.tsp")
        # best_tour = read_solution(f_path)
        # aco.best_tour = best_tour
        # best_distance = aco.get_tour_distance(best_tour)
        # print("Best distance :", best_distance)
        # aco.plot()
    else:
        raise NotImplementedError

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
