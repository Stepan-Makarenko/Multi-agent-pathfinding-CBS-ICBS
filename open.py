import heapq
from node import GridNode, CTNode


class CTOpen:
    def __init__(self):
        self.queue = []

    def __iter__(self):
        return iter(self.queue)

    def __len__(self):
        return len(self.queue)

    def is_empty(self):
        if len(self.queue) != 0:
            return False
        return True

    def get_best_node(self):
        best = heapq.heappop(self.queue)
        return best

    def add_node(self, item: CTNode):
        heapq.heappush(self.queue, item)


class GridOpen:
    def __init__(self):
        self.queue = []
        self.coord_to_node = {}
        self.entry_counter = 0

    def __iter__(self):
        return iter(self.queue)

    def __len__(self):
        return len(self.queue)

    def is_empty(self):
        if len(self.queue) != 0:
            return False
        return True

    def get_best_node(self):
        best = heapq.heappop(self.queue)
        return best[2]

    def add_node(self, item: GridNode):
        if (item.i, item.j, item.t) in self.coord_to_node:
            if self.coord_to_node[(item.i, item.j, item.t)].g > item.g:
                self.coord_to_node[(item.i, item.j, item.t)].f = item.f
                self.coord_to_node[(item.i, item.j, item.t)].g = item.g
                self.coord_to_node[(item.i, item.j, item.t)].parent = item.parent
                heapq.heappush(self.queue, (item.f, self.entry_counter, item))
                self.entry_counter += 1
        else:
            self.coord_to_node[(item.i, item.j, item.t)] = item
            heapq.heappush(self.queue, (item.f, self.entry_counter, item))
            self.entry_counter += 1
