import math
from collections import defaultdict


def item_in_list(l, idx):
    try:
        return l[idx].i, l[idx].j
    except IndexError:
        return l[-1].i, l[-1].j


def list_duplicates(seq):
    # Return conflict vertexes and edges

    # Vertex conflict handler
    count = defaultdict(list)
    for i, item in enumerate(seq[1]):
        count[item].append(i)
    # generates ('v', [agent_id1 ... agent_idk], (x,y))
    all_conflicts = [('v', locs, key) for key, locs in count.items() if len(locs) > 1]

    # Edge conflict handler
    count = defaultdict(int)
    for i, (item1, item2) in enumerate(zip(*seq)):  # item* - (x*, y*) /* in [1,2]
        item = item1 + item2
        count[item] = i
        if item[2:4] != item[0:2] and item[2:4] + item[0:2] in count:
            all_conflicts.append(('e', [count[item[2:4] + item[0:2]], i], item[2:4] + item[0:2]))
    # generates ('e', [agent_id1 agent_id2], (x1, y1, x2, y2))
    return all_conflicts


# Node for grid
class GridNode:
    def __init__(self, i=-1, j=-1, t=0, g=math.inf, h=math.inf, f=None, parent=None):
        self.i = i
        self.j = j
        self.g = g
        # Add time dimension
        self.t = t
        if f is None:
            self.f = self.g + h
        else:
            self.f = f
        self.parent = parent

    def __eq__(self, other):
        # Use t = -1 to define goal_state timestep
        return (self.i == other.i) and (self.j == other.j) and ((self.t == other.t) or self.t == -1 or other.t == -1)


# Node for Constraint Tree (CT)
class CTNode:
    def __init__(self, constraints, solution, cost, parent=None, entry=0):
        # TODO implement CT node with following list of fields:
        #   constraints - set of (agent_id, i, j, t), only the last set is stored
        #   solution - (agent_id: (path, length)}, each path is consistent with constrains
        #   cost - the total cost of current solution
        #   entry - to break ties in OPEN in FIFO manner
        self.constraints = constraints
        self.solution = solution
        self.cost = cost
        self.parent = parent
        self.entry = entry
        self.n_conflicts = None

    def __eq__(self, other):
        return self.solution == other.solution

    def __lt__(self, other):
        # CT nodes must be ordered by their costs.
        if self.cost > other.cost:
            return False
        if self.cost < other.cost:
            return True
        # Ties are broken in favor of CT nodes whose associated solution contains fewer conflicts.
        self_conflicts = self.count_n_of_conflicts()
        other_conflicts = other.count_n_of_conflicts()
        if self_conflicts > other_conflicts:
            return False
        if self_conflicts < other_conflicts:
            return True
        # Further ties are broken in a FIFO manner.
        return self.entry < other.entry

    def validate_conflicts(self):
        t = 1
        max_t = max(map(lambda x: len(x[0]), self.solution.values()))
        while True:
            all_locations = [[item_in_list(self.solution[i][0], ts) for i in range(len(self.solution))]
                             for ts in [t - 1, t]]
            for coord_ids in list_duplicates(all_locations):
                # (conflict_type, agent_id1 ... agent_idk, x, y, t)
                return (*coord_ids[0], *coord_ids[1], *coord_ids[2], t)  # a conflict found, validation halts, it's a non-goal node
            t += 1
            if t == max_t:
                break
        return None

    def count_n_of_conflicts(self):
        # returns number of all conflicts, used only to break ties
        if self.n_conflicts:
            return self.n_conflicts
        t = 1
        max_t = max(map(lambda x: len(x[0]), self.solution.values()))
        confl_counter = 0
        while True:
            all_locations = [[item_in_list(self.solution[i][0], ts) for i in range(len(self.solution))]
                             for ts in [t - 1, t]]
            for coord_ids in list_duplicates(all_locations):
                confl_counter += len(coord_ids[1])
            t += 1
            if t == max_t:
                break
        self.n_conflicts = confl_counter
        return confl_counter

    def extract_all_constraints(self):
        # One does not have to save all cumulative constraints for a given node.
        # Instead, we can save only its latest constraint and extract the other constraints
        # by traversing the path from N to the root via its ancestors.
        if self.constraints:
            current = self
            constraints = set()
            while current.parent:
                constraints = constraints.union(current.constraints)
                current = current.parent
            return constraints
        return set()