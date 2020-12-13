import math


# Node for grid
class GridNode:
    def __init__(self, i=-1, j=-1, t=0, g=math.inf, h=math.inf, f=None, parent=None):
        self.i = i
        self.j = j
        self.g = g
        # Add time dimension
        self.t = 0
        if f is None:
            self.f = self.g + h
        else:
            self.f = f
        self.parent = parent

    def __eq__(self, other):
        # Use t = -1 to define goal_state timestep
        return (self.i == other.i) and (self.j == other.j) and ((self.t == other.t) or self.t == -1)


# Node for Constraint Tree (CT)
class CTNode:
    def __init__(self, constraints, solution, cost, parent=None, entry=0):
        # TODO implement CT node with following list of fields:
        #   constraints - set of constrains in format (agent_id, vertex, timestep)
        #   solution - set of paths, one path for each agent, each path is consistent with constrains
        #   cost - the total cost of current solution
        #   entry - to break ties in OPEN in FIFO manner
        self.constraints = constraints
        self.solution = solution
        self.cost = cost
        self.parent = parent
        self.entry = entry
        self.conflicts = []
        pass

    def __eq__(self, other):
        return self.solution == other.solution

    def __lt__(self, other):
        # CT nodes must be ordered by their costs.
        # Ties are broken in favor of CT nodes whose associated solution contains fewer conflicts.
        # Further ties are broken in a FIFO manner.
        if self.cost > other.cost:
            return False
        if self.cost < other.cost:
            return True
        if len(self.conflicts) > len(other.conflicts):
            return False
        if len(self.conflicts) < len(other.conflicts):
            return True
        return self.entry < other.entry

    def validate_conflicts(self):
        pass
