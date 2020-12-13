from node import CTNode
from open import CTOpen
from low_level_policy import AStar


def HCBS(MAPF_instance, agents, low_level_policy=AStar, open_type=CTOpen):
    # TODO implement high level policy to handle Constraint Tree
    #   use following pseudo code:
    #       Input: MAPF instance
    #       Root.constraints = ∅
    #       Root.solution = find individual paths by the low level()
    #       Root.cost = SIC(Root.solution)
    #       insert Root to OPEN
    #       while OPEN not empty do
    #       P ← best node from OPEN // lowest solution cost
    #       Validate the paths in P until a conflict occurs.
    #       if P has no conflict then
    #           return P.solution // P is goal
    #       C ← first conflict (ai,a j, v,t) in P
    #       foreach agent ai in C do
    #           A ← new node
    #           A.constraints ← P.constraints + (ai, v,t)
    #           A.solution ← P.solution
    #           Update A.solution by invoking low level(ai)
    #           A.cost = SIC(A.solution)
    #           if A.cost < ∞ // A solution was found then
    #               Insert A to OPEN
    OPEN = open_type()

    root = CTNode(constraints=None, solution=None, cost=None, parent=None, entry=0)
    id_to_agent = {agent.id: agent for agent in agents}
    root.solution = {agent.id: low_level_policy(MAPF_instance, agent, constrains=None) for agent in agents}
    root.cost = sum([root.solution[agent.id][1] for agent in agents])
    OPEN.add_node(root)
    while len(OPEN) != 0:
        p = OPEN.get_best_node()
        conflict = p.validate_conflicts() # (a_0_id, a_1_id, ..., a_k_id grid_node)
        conflicting_agents = conflict[:-1]
        if not conflict:
            return p.solution

        # Try to avoid duplicate detection
        for i, _ in enumerate(conflicting_agents):
            a = CTNode(constraints=None, solution=None, cost=None, parent=None, entry=0)
            new_constrains = p.constrains.copy()
            a.solution = p.solution
            for j, agent_id in enumerate(conflicting_agents):
                if i != j:
                    new_constrains[(agent_id, conflict[-1])] = 0
                    a.solution[agent_id] = low_level_policy(MAPF_instance, id_to_agent[agent_id],
                                                            constrains=new_constrains)
            a.constraints = new_constrains
            a.cost = sum([root.solution[agent.id][1] for agent in agents])
            if a.cost < float('inf'):
                OPEN.add_node(a)
