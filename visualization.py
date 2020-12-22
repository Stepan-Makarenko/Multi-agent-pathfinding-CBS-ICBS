import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML
from node import GridNode


def draw(grid_map, agents=None, solution=None, fig_size=(6.4, 6.4), nodesExpanded=None, nodesOpened=None):
    # Assign different collor for different agents:
    collors = [tuple(np.random.randint(0, 255, 3)) for i in range(len(agents))]
    if solution is not None:
        fig = plt.figure(figsize=fig_size)
        fig.set_size_inches(*fig_size)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        images = []

        for t in range(max(map(lambda x: len(x[0]), solution.values()))):
            k = 5
            hIm = grid_map.height * k
            wIm = grid_map.width * k
            im = Image.new('RGB', (wIm, hIm), color='white')
            draw = ImageDraw.Draw(im)

            for i in range(grid_map.height):
                for j in range(grid_map.width):
                    if (grid_map.cells[i][j] == 1):
                        draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))
                    elif (grid_map.cells[i][j] == 2):
                        draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill='green')

            for i, (path, length) in enumerate(solution.values()):
                step = path[min(t, len(path) - 1)]
                if (grid_map.traversable(step.i, step.j)):
                    draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1),
                                   fill=collors[i], width=0)
                else:
                    draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1),
                                   fill=(230, 126, 34), width=0)

            for i, agent in enumerate(agents):
                start = GridNode(agent.start_i, agent.start_j)
                goal = GridNode(agent.goal_i, agent.goal_j)
                if (start is not None) and (grid_map.traversable(start.i, start.j)):
                    draw.rectangle((start.j * k + 1, start.i * k + 1, (start.j + 1) * k - 2, (start.i + 1) * k - 2),
                                   fill=collors[i], width=0)

                if (goal is not None) and (grid_map.traversable(goal.i, goal.j)):
                    draw.ellipse((goal.j * k + 1, goal.i * k + 1, (goal.j + 1) * k - 2, (goal.i + 1) * k - 2),
                                   fill=collors[i], width=0)

                    #             fig, ax = plt.subplots(dpi=150)
                    #             ax.axes.xaxis.set_visible(False)
                    #             ax.axes.yaxis.set_visible(False)
                    #             plt.imshow(im, animated=True)
            img = plt.imshow(im, animated=True)
            #             print(img)
            images.append([img])
        ani = animation.ArtistAnimation(fig, images, interval=400, blit=True, repeat_delay=100)
        HTML(ani.to_html5_video())
        print("Solution was found, cost = ", sum([el[1] for el in solution.values()]))
        return ani
    else:
        k = 5
        hIm = grid_map.height * k
        wIm = grid_map.width * k
        im = Image.new('RGB', (wIm, hIm), color='white')
        draw = ImageDraw.Draw(im)

        for i in range(grid_map.height):
            for j in range(grid_map.width):
                if (grid_map.cells[i][j] == 1):
                    draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))
                elif (grid_map.cells[i][j] == 2):
                    draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill='green')

        for i, agent in enumerate(agents):
            start = GridNode(agent.start_i, agent.start_j)
            goal = GridNode(agent.goal_i, agent.goal_j)
            if (start is not None) and (grid_map.traversable(start.i, start.j)):
                draw.rectangle((start.j * k, start.i * k, (start.j + 1) * k - 1, (start.i + 1) * k - 1),
                               fill=collors[i], width=0)

            if (goal is not None) and (grid_map.traversable(goal.i, goal.j)):
                draw.ellipse((goal.j * k, goal.i * k, (goal.j + 1) * k - 1, (goal.i + 1) * k - 1), fill=collors[i],
                               width=0)

        fig, ax = plt.subplots(dpi=150)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        plt.imshow(np.asarray(im))
