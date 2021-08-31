# Ant Colony Optimization for Traveling Salesman Problem
## Abstract
Traveling Salesman Problem is one of the most critical NPhard
problem and it has a lot of applications in many fields.
In this report, I propose a non-deterministic model based
on Ant Colony Optimization (ACO) algorithm that finds relatively
optimal solution in polynomial time compared to traditional
deterministic non-polynomial time algorithms. 

## About
This repository is implementation of ACO algorithm for TSP with novel shortest path estimation algortihm and deterministic tour fixing regularization to help model to converge faster in few iteerations.

For more details, please check `report.pdf` file which includes __Design Decisions, Optimization methods, Experiment setup, and Quantitative & Qualitative analysis__

## Running guide:
__Note__: Repository was tested using Python3.7 and latest packages in requirements.txt. Make sure you don't have older Python version and you don't have cached the old versions of packages, as some parts may not work.

+ It is recommended to use virtual environment
  -  Create and activate virtual environment:  
```virtualenv -p python3 venv  ```  
```source venv/bin/activate ```

+ To install dependencies, run:  
```pip3 install -r requirements.txt```

+ Run the model:  
```python3 main.py -p [path_to_file] -cs [colony_size] -it [num_iters] -er [evap_rate] -a [float] -b [float]```

+ After model finishes running, it will plot the final graph for the best tour. 

+ Results will be in `solutions/solution.csv` file.  
