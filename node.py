import math


# Node for grid
class GridNode:
    def __init__(self, i=-1, j=-1, g=math.inf, h=math.inf, f=None, parent=None):
        self.i = i
        self.j = j
        self.g = g
        if f is None:
            self.f = self.g + h
        else:
            self.f = f
        self.parent = parent

    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)


# Node for Constraint Tree (CT)
class CTNode:
    def __init__(self, constrains, solution, cost, f=None, parent=None):
        # TODO implement CT node with following list of fields:
        #   constraints - set of constrains in format (agent_id, vertex, timestep)
        #   solution - set of paths, one path for each agent, each path is consistent with constrains
        #   cost - the total cost of current solution
        pass

    def __eq__(self, other):
        pass
