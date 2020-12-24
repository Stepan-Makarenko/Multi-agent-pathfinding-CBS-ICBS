# Multi-agent-pathfinding
Conflict-based search for optimal multi-agent pathfinding
## Getting started
Run the following command:
```bash
git clone https://github.com/Stepan-Makarenko/Multi-agent-pathfinding.git
```
or download this repository.  
## Problem definition
In the multi-agent pathfinding problem (MAPF) we are given a set of agents each with respective start and goal positions. The task is to find paths for all agents while avoiding collisions.
## Algorithm
The [**CBS algorithm**](http://www.bgu.ac.il/~felner/2015/CBSjur.pdf) and its [**modification**](https://www.ijcai.org/Proceedings/15/Papers/110.pdf), CBS + PC, that uses conflict prioritization, were implemented in Python. 
## Input format
It is recommended to use maps and tasks (where agents' start and goal positions are given) in the .map and .scen Moving AI formats.  
The data can be found [**here**](https://www.movingai.com/benchmarks/mapf.html).  
The formats are described [**here**](https://www.movingai.com/benchmarks/formats.html).  
It is also possible to run the code on maps represented as strings (. - an empty space, # - an obstacle) and agents represented as tuples (x start, y start, x goal, g goal). 
## Output format
The algorithm solves the MAPF instance and returns a set of non-conflicting paths for all agents and their respective costs. Additionally, it can return an image and an .mp4 video demonstrating agents' start and goal positions and movements.  
## Working with MAPF instances
Run test from tests.py on maps represented as strings and agents represented as tuples.  
Run movingai_test from tests.py on Moving AI data.  
The parametrs use_pc and diagonal_movements are responsible for conflict prioritization and whether diagonal movements of agents are allowed.  
The examples of both test and movingai_test applied to maps and tasks are presented in Explore.ipynb.
## Working examples
![1](media/empty.gif)


![2](media/room.gif)
