from node import CTNode
from open import CTOpen
from low_level_policy import AStar
import time

from collections import defaultdict
def HCBS(MAPF_instance, agents, use_pc=False, experiment_mode=False, max_time=300, verbose=False, low_level_policy=AStar, open_type=CTOpen, **kwargs):
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
    root.solution = {agent.id: low_level_policy(MAPF_instance, agent, use_pc=use_pc,
                                                constraints=root.extract_all_constraints(), **kwargs) for agent in agents}
    root.cost = sum([root.solution[agent.id][1] for agent in agents])
    OPEN.add_node(root)
    start_time = time.time()
    if verbose:
        print(use_pc, max_time)
    while len(OPEN) != 0:
        p = OPEN.get_best_node()

        paths = defaultdict(list)
        for agent in p.solution:
            for ts, node in enumerate(p.solution[agent][0]):
                paths[agent].append((ts, node.i, node.j))

        conflict = p.validate_conflicts(use_pc=use_pc)  # tuple (type, a_0_id, a_1_id, ..., a_k_id, x, y, t)
        runtime = time.time() - start_time
        if runtime > max_time:
            return False
        if not conflict:
            solution = {agent_id: p.solution[agent_id][0:2] for agent_id in p.solution}
            if experiment_mode:
                return entry + 1, runtime
            return solution
        if conflict[0] == 'v':
            conflicting_agents = conflict[1:-3]
            vertex_and_time = conflict[-3:]
        else:
            conflicting_agents = conflict[1:3]
            vertex_and_time1 = conflict[3:]
            vertex_and_time2 = vertex_and_time1[2:4] + vertex_and_time1[0:2] + vertex_and_time1[-1:]
            vertex_and_time = (vertex_and_time1, vertex_and_time2)

        if conflict[0] == 'e':
            # Edge conflict handler
            for i in range(2):
                a = CTNode(constraints=set(), solution=p.solution.copy(), cost=None, parent=p, entry=0)
                a.constraints.add((conflicting_agents[i], *vertex_and_time[i]))
                a.solution[conflicting_agents[i]] = low_level_policy(MAPF_instance, id_to_agent[conflicting_agents[i]],
                                                                     use_pc=use_pc,
                                                                     constraints=a.extract_all_constraints(), **kwargs)
                a.cost = sum([a.solution[agent.id][1] for agent in agents])
                entry += 1
                if a.cost < float('inf'):
                    a.entry = entry
                    OPEN.add_node(a)
        else:
            # Vertex conflict handler
            for i in conflicting_agents:
                a = CTNode(constraints=set(), solution=p.solution.copy(), cost=None, parent=p, entry=0)
                for agent_id in conflicting_agents:
                    if i != agent_id:
                        a.constraints.add((agent_id, *vertex_and_time))
                        a.solution[agent_id] = low_level_policy(MAPF_instance, id_to_agent[agent_id], use_pc=use_pc,
                                                                constraints=a.extract_all_constraints(), **kwargs)
                a.cost = sum([a.solution[agent.id][1] for agent in agents])
                entry += 1
                if a.cost < float('inf'):
                    a.entry = entry
                    OPEN.add_node(a)
