from node import GridNode, CTNode


class CTClose:
    def __init__(self):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        pass

    # add_node is the method that inserts the node to CLOSED
    def add_node(self, item: CTNode, *args):
        pass

    # was_expanded is the method that checks if a node has been expanded
    def was_expanded(self, item: CTNode, *args):
        pass


class GridClose:
    def __init__(self):
        self.coord_to_node = {}

    def __iter__(self):
        return iter(self.coord_to_node.values())

    def __len__(self):
        return len(self.coord_to_node)

    # AddNode is the method that inserts the node to CLOSED
    def add_node(self, item: GridNode, *args):
        self.coord_to_node[(item.i, item.j, item.t)] = item

    # WasExpanded is the method that checks if a node has been expanded
    def was_expanded(self, item: GridNode, *args):
        return (item.i, item.j, item.t) in self.coord_to_node
