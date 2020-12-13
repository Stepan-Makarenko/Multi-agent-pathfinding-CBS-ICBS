class Agent:
    id = 0

    def __init__(self, start_i, start_j, goal_i, goal_j):
        self.start_i = start_i
        self.start_j = start_j
        self.goal_i = goal_i
        self.goal_j = goal_j
        self.id = Agent.id
        Agent.id += 1
