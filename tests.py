import random
from visualization import draw
from agent import Agent
from map_handler import Map, read_map, read_tasks


def test(SearchFunction, height, width, mapstr, agents, use_pc=False, diagonal_movements=False, draw_anim=False,
         **kwargs):
    task_map = Map()
    task_map.read_from_string(mapstr, width, height, diagonal_movements=diagonal_movements)
    Agent.id = 0
    solution = SearchFunction(task_map, agents, use_pc, **kwargs)
    if draw_anim:
        anim = draw(task_map, agents, solution)
        return solution, anim
    return solution


def movingai_test(map_file, task_file, n_agents, SearchFunction, use_pc=False, diagonal_movements=False, rseed=None,
                  draw_anim=False, **kwargs):
    random.seed(rseed)
    mapstr = read_map(map_file)
    tasks = random.sample(read_tasks(task_file), n_agents)
    Agent.id = 0
    agents = []
    for i in range(n_agents):
        bucket, path, width, height, jStart, iStart, jGoal, iGoal, length = tasks[i]
        agents += [Agent(iStart, jStart, iGoal, jGoal)]
    task_map = Map()
    task_map.read_from_string(mapstr, width, height, diagonal_movements=diagonal_movements)
    solution = SearchFunction(task_map, agents, use_pc, **kwargs)
    if draw_anim:
        anim = draw(task_map, agents, solution)
        return solution, anim
    return solution
