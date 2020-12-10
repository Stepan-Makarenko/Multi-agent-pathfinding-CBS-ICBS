import numpy as np
from node import GridNode
from open import GridOpen
from close import GridClose


def CalculateCost(i1, j1, i2, j2):
    return np.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)


def diagonal_distance(i1, j1, i2, j2):
    D = 1
    D2 = np.sqrt(2)
    dx = abs(i1 - i2)
    dy = abs(j1 - j2)
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


def AStar(grid_map, i_start, j_start, i_goal, j_goal, heuristic_function=diagonal_distance, open_type=GridOpen,
          closed_type=GridClose):

    # TODO think about what this function should output
    OPEN = open_type()
    CLOSED = closed_type()

    goal = GridNode(i_goal, j_goal)

    OPEN.add_node(GridNode(i_start, j_start, 0, 0))
    while len(OPEN) != 0:
        state = OPEN.get_best_node()
        if state == goal:
            return True, state, len(CLOSED) + len(OPEN), len(CLOSED)

        CLOSED.add_node(state)
        next_coords = grid_map.GetNeighbors(state.i, state.j)
        for next_coord in next_coords:
            next_g = state.g + CalculateCost(state.i, state.j, next_coord[0], next_coord[1])
            heuristic_dist = heuristic_function(next_coord[0], next_coord[1], goal.i, goal.j)
            # Add clear F func
            next_state = GridNode(next_coord[0], next_coord[1], next_g, heuristic_dist, None, state)
            if CLOSED.was_expanded(next_state):
                continue
            OPEN.add_node(next_state)

    return False, None, len(CLOSED) + len(OPEN), len(CLOSED)