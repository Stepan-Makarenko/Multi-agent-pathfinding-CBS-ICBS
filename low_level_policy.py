import numpy as np
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


def AStar(grid_map, agent, constraints, heuristic_function=diagonal_distance, open_type=GridOpen,
          closed_type=GridClose):

    def make_path(goal):
        length = goal.g
        current = goal
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        return path[::-1], length

    # TODO think about time dependence of occupation grid and  what this function should output
    OPEN = open_type()
    CLOSED = closed_type()

    goal = GridNode(agent.goal_i, agent.goal_j, t=-1)

    # TODO start node should depend on agent!
    OPEN.add_node(GridNode(agent.start_i, agent.start_j, t=0, g=0, h=0))
    # Add time dimension
    while len(OPEN) != 0:
        state = OPEN.get_best_node()
        if state == goal:
            return make_path(state)

        CLOSED.add_node(state)
        next_coords = grid_map.get_neighbors(state.i, state.j)
        for next_coord in next_coords:
            next_g = state.g + calculate_cost(state.i, state.j, next_coord[0], next_coord[1])
            heuristic_dist = heuristic_function(next_coord[0], next_coord[1], goal.i, goal.j)
            next_state = GridNode(next_coord[0], next_coord[1], g=next_g,
                                  t=state.t+1, h=heuristic_dist, f=None, parent=state)
            if CLOSED.was_expanded(next_state) or (agent.id, next_state.i, next_state.j, next_state.t) in constraints \
               or (agent.id, state.i, state.j, next_state.i, next_state.j, next_state.t) in constraints:
                continue
            OPEN.add_node(next_state)

    return None, float('inf')
