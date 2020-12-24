from low_level_policy import manhattan_distance
from map_handler import Map
from tqdm import tqdm
import numpy as np
import math
import heapq


# Define MAP class without wait action
class MapNoWait(Map):
    def get_neighbors(self, i, j):
        neighbors = []
        delta = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        for d in delta:
            if self.in_bounds(i + d[0], j + d[1]) and self.traversable(i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))
        return neighbors


# Define node without t dimension
class Node:
    def __init__(self, i=-1, j=-1, g=math.inf, h=math.inf, F=None, parent=None):
        self.i = i
        self.j = j
        self.g = g
        if F is None:
            self.F = self.g + h
        else:
            self.F = F
        self.parent = parent

    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)

# Define OPEN for Node without t dimension
class Open:
    def __init__(self):
        self.queue = []
        self.coord_to_node = {}
        self.entry_counter = 0

    def __iter__(self):
        return len(self.queue)

    def __len__(self):
        return len(self.queue)

    def is_empty(self):
        if len(self.queue) != 0:
            return False
        return True

    def get_best_node(self):
        best = heapq.heappop(self.queue)
        return best[2]

    def add_node(self, item: Node):
        if (item.i, item.j) in self.coord_to_node:
            if self.coord_to_node[(item.i, item.j)].g > item.g:
                self.coord_to_node[(item.i, item.j)].F = item.F
                self.coord_to_node[(item.i, item.j)].g = item.g
                self.coord_to_node[(item.i, item.j)].parent = item.parent
                heapq.heappush(self.queue, (item.F, self.entry_counter, item))
                self.entry_counter += 1
        else:
            self.coord_to_node[(item.i, item.j)] = item
            heapq.heappush(self.queue, (item.F, self.entry_counter, item))
            self.entry_counter += 1


# Define CLOSE for Node without t dimension
class Close:
    def __init__(self):
        self.coord_to_node = {}

    def __iter__(self):
        return iter(self.coord_to_node.values())

    def __len__(self):
        return len(self.coord_to_node)

    # AddNode is the method that inserts the node to CLOSED
    def add_node(self, item: Node, *args):
        self.coord_to_node[(item.i, item.j)] = item

    # WasExpanded is the method that checks if a node has been expanded
    def was_expanded(self, item: Node, *args):
        return (item.i, item.j) in self.coord_to_node


# Define calculate cost without wait action
def calculate_cost(i1, j1, i2, j2):
    return math.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)


# Define Astar without time dimension
def AStar(gridMap, iStart, jStart, iGoal, jGoal, heuristic_function=manhattan_distance, openType=Open,
          closedType=Close):
    OPEN = openType()
    CLOSED = closedType()

    goal = Node(iGoal, jGoal)

    OPEN.add_node(Node(iStart, jStart, 0, 0))
    while len(OPEN) != 0:
        state = OPEN.get_best_node()
        if state == goal:
            return True, state.g

        CLOSED.add_node(state)
        next_coords = gridMap.get_neighbors(state.i, state.j)
        for next_coord in next_coords:
            next_g = state.g + calculate_cost(state.i, state.j, next_coord[0], next_coord[1])
            heuristic_dist = heuristic_function(next_coord[0], next_coord[1], goal.i, goal.j)
            # Add clear F func
            next_state = Node(next_coord[0], next_coord[1], next_g, heuristic_dist, None, state)
            if CLOSED.was_expanded(next_state):
                continue
            OPEN.add_node(next_state)

    return False, None


def map_and_task_generator(num_maps=100, height=8, width=8, obstacle_percentage=15, max_agents=16):
    """
    :param num_maps: num maps to be generated
    :param height: height of each map
    :param width: width of each map
    :param obstacle_percentage: percentage of obstacles to be placed on map
    :param max_agents: max number of agents to run on each map
    :return: None, save maps and scens in dir ./generated_*
    """
    mu = height * width * (obstacle_percentage / 100)
    loc = mu / 3
    obstacles_number = np.random.normal(mu, loc, num_maps)

    for i in tqdm(range(num_maps)):
        while True:
            # generate map
            gen_map = np.zeros(64)
            gen_map[:int(obstacles_number[i])] = 1
            gen_map = np.random.permutation(gen_map).reshape((8, 8))
            grid_map = MapNoWait()
            grid_map.set_grid_cells(height, width, gen_map, diagonal_movements=False)
            valid = True

            # check is map valid
            non_obstacles = np.argwhere(gen_map == 0)
            start_point = non_obstacles[0]
            goal_points = non_obstacles[1:]
            for goal in goal_points:
                path, _ = AStar(grid_map, start_point[0], start_point[1], goal[0], goal[1],
                                heuristic_function=manhattan_distance)
                if not path:
                    valid = False
                    break
            if valid:
                break

        # save generated map to file
        gen_str = '\n'.join([' '.join(['.' if el == 0 else '#' for el in row]) for row in gen_map])
        map_name = '8x8v{}'.format(i)
        with open('./generated_map/' + map_name + '.map', 'w+') as f:
            f.write('type octile\n')
            f.write('height {}\n'.format(height))
            f.write('width {}\n'.format(width))
            f.write('map\n')
            f.write(gen_str)

        # generate goal and start points
        grid_map = Map()
        grid_map.set_grid_cells(height, width, gen_map, diagonal_movements=False)
        opt_cost = []

        # Need to simulate movements of all agents simultaneously
        starts = [tuple(el) for el in np.random.permutation(non_obstacles)[:max_agents]]
        i = 0
        goals = starts.copy()
        while (i < 10 ** 5) or any([starts[i] == goals[i] for i in range(max_agents)]):
            for ind in np.random.permutation(np.arange(max_agents)):
                for j in range(max_agents):
                    if j != ind:
                        grid_map.cells[goals[j][0], goals[j][1]] = 1
                neighbor = grid_map.get_neighbors(goals[ind][0], goals[ind][1])
                goals[ind] = neighbor[np.random.choice(len(neighbor))]
                for j in range(max_agents):
                    if j != ind:
                        grid_map.cells[goals[j][0], goals[j][1]] = 0
            i += 1
        for i in range(max_agents):
            _, cost = AStar(grid_map, starts[i][0], starts[i][1], goals[i][0], goals[i][1],
                            heuristic_function=manhattan_distance)
            opt_cost.append(cost)

        # save task scen
        data = np.array([np.ones(len(starts)), np.array([map_name + '.map'] * len(starts)),
                         np.ones(len(starts)) * width, np.ones(len(starts)) * height,
                         np.array(starts)[:, 1], np.array(starts)[:, 0], np.array(goals)[:, 1],
                         np.array(goals)[:, 0], opt_cost])
        data = data.T

        datafile_path = "./generated_scen/" + map_name + '.scen'
        with open(datafile_path, 'w+') as f:
            for row in data:
                f.write(
                    str(row[0]) + '\t' + row[1] + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' + str(row[4]) + '\t'
                    + str(row[5]) + '\t' + str(row[6]) + '\t' + str(row[7]) + '\t' + str(row[8]) + '\n')