import numpy as np
from collections import defaultdict
from node import GridNode
from open import GridOpen
from close import GridClose


def calculate_cost(i1, j1, i2, j2):
    # Wait action costs 1
    return max(1, np.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2))


def diagonal_distance(i1, j1, i2, j2):
    d = 1
    d2 = np.sqrt(2)
    dx = abs(i1 - i2)
    dy = abs(j1 - j2)
    return d * (dx + dy) + (d2 - 2 * d) * min(dx, dy)


def manhattan_distance(i1, j1, i2, j2):
    return abs(i1 - i2) + abs(j1 - j2)


def AStar(grid_map, agent, constraints=set(), use_pc=False, heuristic_function=manhattan_distance, open_type=GridOpen,
          closed_type=GridClose):
    """
    :param grid_map: variable of class Map, represents map with obstacles
    :param agent: variable of class Agent, consisting of the start and goal coordinates
    :param constraints: set of restrictions that prohibits an agent from occupying a specific cell
    :param use_pc: flag that determines whether to use the conflict priority or not
    :param heuristic_function: define heuristic function to use
    :param open_type: define open class to use for nodes processing
    :param closed_type: define closed class to use for nodes processing
    :return: optimal_path, optimal_g, (widths if use_pc else None)
    """
    def make_path(goal):
        final_state = GridNode(goal.i, goal.j, t=-1)
        current = goal
        # delete extra nodes:
        while current.parent and current.parent == final_state:
            current = current.parent

        length = current.g
        path = []

        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)

        return path[::-1], length

    OPEN = open_type()
    CLOSED = closed_type()

    # time step mapping to optimal path widths
    widths = defaultdict(int)
    opt_cost = float('inf')
    first_found_path = None

    # Get maximum time when we can encounter constraint
    max_constrain_t = max(constraints, key=lambda x: x[-1], default=[0])[-1]
    goal = GridNode(agent.goal_i, agent.goal_j, t=-1)
    OPEN.add_node(GridNode(agent.start_i, agent.start_j, t=0, g=0, h=0))

    # Add time dimension
    while len(OPEN) != 0:
        state = OPEN.get_best_node()
        CLOSED.add_node(state)

        if state == goal and state.t > max_constrain_t:
            if use_pc:
                if state.g <= opt_cost:
                    path, opt_cost = make_path(state)
                    if not first_found_path:
                        first_found_path = path
                    # Init Direct Acyclic Graph
                    DAG = defaultdict(set)
                    OPEN = GridOpen()
                    OPEN.add_node(GridNode(agent.start_i, agent.start_j, t=0, g=0, h=0))
                    nodes_levels = []
                    while len(OPEN) != 0:
                        state = OPEN.get_best_node()
                        if state.f > opt_cost:
                            continue
                        if state == goal and state.g == opt_cost:
                            nodes_levels.insert(0, DAG[(state.i, state.j, state.t)])
                            widths[state.t-1] += len(DAG[(state.i, state.j, state.t)])
                            while True:
                                w = set()
                                for s in nodes_levels[0]:
                                    w = w.union(DAG[s])
                                if not w:
                                    break
                                nodes_levels.insert(0, w)
                                widths[s[-1]-1] += len(w)

                        next_coords = grid_map.get_neighbors(state.i, state.j)
                        for next_coord in next_coords:
                            next_g = state.g + calculate_cost(state.i, state.j, next_coord[0], next_coord[1])
                            heuristic_dist = heuristic_function(next_coord[0], next_coord[1], goal.i, goal.j)
                            next_state = GridNode(next_coord[0], next_coord[1], g=next_g,
                                                  t=state.t + 1, h=heuristic_dist, f=None, parent=state)
                            if (agent.id, next_state.i, next_state.j, next_state.t) in constraints \
                                    or (
                            agent.id, state.i, state.j, next_state.i, next_state.j, next_state.t) in constraints:
                                continue
                            if state:
                                DAG[(next_state.i, next_state.j, next_state.t)].add((state.i, state.j, state.t))
                            OPEN.add_node(next_state)

                    return first_found_path, opt_cost, widths
            else:
                return make_path(state)

        next_coords = grid_map.get_neighbors(state.i, state.j)
        for next_coord in next_coords:
            next_g = state.g + calculate_cost(state.i, state.j, next_coord[0], next_coord[1])
            heuristic_dist = heuristic_function(next_coord[0], next_coord[1], goal.i, goal.j)
            next_state = GridNode(next_coord[0], next_coord[1], g=next_g,
                                  t=state.t + 1, h=heuristic_dist, f=None, parent=state)
            if CLOSED.was_expanded(next_state) or (agent.id, next_state.i, next_state.j, next_state.t) in constraints \
               or (agent.id, state.i, state.j, next_state.i, next_state.j, next_state.t) in constraints:
                continue
            OPEN.add_node(next_state)

    return first_found_path, opt_cost