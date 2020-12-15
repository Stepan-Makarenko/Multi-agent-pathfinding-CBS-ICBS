from node import CTNode
from open import CTOpen
from low_level_policy import AStar


def HCBS(MAPF_instance, agents, low_level_policy=AStar, open_type=CTOpen, **kwargs):
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
    entry = 0
    root = CTNode(constraints=None, solution=None, cost=None, parent=None, entry=entry)
    id_to_agent = {agent.id: agent for agent in agents}
    root.constraints = set()
    root.solution = {agent.id: low_level_policy(MAPF_instance, agent,
                                                constraints=root.extract_all_constraints(), **kwargs) for agent in agents}
    root.cost = sum([root.solution[agent.id][1] for agent in agents])
    OPEN.add_node(root)
    while len(OPEN) != 0:
        p = OPEN.get_best_node()
        conflict = p.validate_conflicts()  # tuple (a_0_id, a_1_id, ..., a_k_id, x, y, t)
        if not conflict:
            return p.solution
        conflicting_agents = conflict[:-3]
        vertex_and_time = conflict[-3:]

        # Try to avoid duplicate detection
        for i, _ in enumerate(conflicting_agents):
            a = CTNode(constraints=set(), solution=p.solution.copy(), cost=None, parent=p, entry=0)
            for j, agent_id in enumerate(conflicting_agents):
                if i != j:
                    a.constraints.add((agent_id, *vertex_and_time))
                    a.solution[agent_id] = low_level_policy(MAPF_instance, id_to_agent[agent_id],
                                                            constraints=a.extract_all_constraints(), **kwargs)
            a.cost = sum([a.solution[agent.id][1] for agent in agents])
            if a.cost < float('inf'):
                entry += 1
                a.entry = entry
                OPEN.add_node(a)
