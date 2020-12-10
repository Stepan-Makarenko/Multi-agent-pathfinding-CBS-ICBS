from node import CTNode
from open import CTOpen
from close import CTClose


def HCBS(MAPF_instance, open_type=CTOpen, closed_type=CTClose):
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
    pass
