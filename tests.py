import random
from visualization import draw
from agent import Agent
from map_handler import Map, read_map, read_tasks


def test(SearchFunction, height, width, mapstr, agents, use_pc=False, diagonal_movements=False, draw_anim=False,
         **kwargs):
    """
        :param SearchFunction: function to solve mapf
        :param height: height of the map
        :param width: width of the map
        :param mapstr: string representation of the map
        :param agents: list of agents (class Agent instances)
        :param use_pc: flag that determines whether to use the conflict prioritization or not
        :param diagonal_movements: flag that determines whether to allow diagonal movements of agents or not
        :param draw_anim: flag that determines whether to draw animation of agents or not
        :param kwargs: additional parameters to be passed to the SearchFunction
        :return: (solution, animation) if draw_anim and not experiment_mode of the SearchFunction else solution
    """
    task_map = Map()
    task_map.read_from_string(mapstr, width, height, diagonal_movements=diagonal_movements)
    Agent.id = 0
    solution = SearchFunction(task_map, agents, use_pc, **kwargs)
    if draw_anim:
        if isinstance(solution, dict):
            return solution, draw(task_map, agents, solution)
        print('Mode set to experiment, no animation is drawn')
        return solution
    return solution


def movingai_test(SearchFunction, map_file, task_file, n_agents, random_choice=True, start_task=0, use_pc=False, diagonal_movements=False, rseed=None,
                  draw_anim=False, **kwargs):
    """
        :param SearchFunction: function to solve mapf
        :param map_file: path to .map file
        :param task_file: path to .scen file
        :param n_agents: number of agents
        :param random_choice: flag that determines whether select n_agents tasks randomly from .scen or not
        :param start_task: if random_choice is set to False, n_agents tasks starting from index start_task are selected
        :param use_pc: flag that determines whether to use the conflict prioritization or not
        :param diagonal_movements: flag that determines whether to allow diagonal movements of agents or not
        :param rseed: random seed, used if random_choice=True
        :param draw_anim: flag that determines whether to draw animation of agents or not
        :param kwargs: additional parameters to be passed to the SearchFunction
        :return: (solution, animation) if draw_anim and not experiment_mode of the SearchFunction else solution
    """
    if random_choice:
        random.seed(rseed)
        tasks = random.sample(read_tasks(task_file), n_agents)
    else:
        tasks = read_tasks(task_file)[start_task:start_task + n_agents]
    mapstr = read_map(map_file)
    Agent.id = 0
    agents = []
    for i in range(n_agents):
        bucket, path, width, height, jStart, iStart, jGoal, iGoal, length = tasks[i]
        agents += [Agent(iStart, jStart, iGoal, jGoal)]
    task_map = Map()
    task_map.read_from_string(mapstr, width, height, diagonal_movements=diagonal_movements)
    solution = SearchFunction(task_map, agents, use_pc, **kwargs)
    if draw_anim:
        if isinstance(solution, dict):
            return solution, draw(task_map, agents, solution)
        print('Mode set to experiment, no animation is drawn')
        return solution
    return solution
