import numpy as np
from node import GridNode
from open import GridOpen
from close import GridClose


def calculate_cost(i1, j1, i2, j2):
    return np.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)


def diagonal_distance(i1, j1, i2, j2):
    d = 1
    d2 = np.sqrt(2)
    dx = abs(i1 - i2)
    dy = abs(j1 - j2)
    return d * (dx + dy) + (d2 - 2 * d) * min(dx, dy)


def AStar(grid_map, i_start, j_start, i_goal, j_goal, agent, constrains, heuristic_function=diagonal_distance, open_type=GridOpen,
          closed_type=GridClose):

    # TODO think about time dependence of occupation grid and  what this function should output
    OPEN = open_type()
    CLOSED = closed_type()

    goal = GridNode(i_goal, j_goal, t=-1)

    # TODO start node should depend on agent!
    OPEN.add_node(GridNode(i_start, j_start, t=0, g=0, h=0))
    # Add time dimension
    time = 0
    while len(OPEN) != 0:
        state = OPEN.get_best_node()
        if state == goal:
            return True, state, len(CLOSED) + len(OPEN), len(CLOSED)

        CLOSED.add_node(state)
        next_coords = grid_map.GetNeighbors(state.i, state.j)
        for next_coord in next_coords:
            next_g = state.g + calculate_cost(state.i, state.j, next_coord[0], next_coord[1])
            heuristic_dist = heuristic_function(next_coord[0], next_coord[1], goal.i, goal.j)
            # Add clear F func
            next_state = GridNode(next_coord[0], next_coord[1], g=next_g,
                                  t=time+1, h=heuristic_dist, f=None, parent=state)
            if CLOSED.was_expanded(next_state) or next_state in constrains:
                continue
            OPEN.add_node(next_state)
        time += 1

    return False, None, len(CLOSED) + len(OPEN), len(CLOSED)