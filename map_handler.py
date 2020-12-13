# TODO find suitable maps to test algorithm and create a way to handle them
class Map:

    # Default constructor
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = []

    # Converting a string (with '#' representing obstacles and '.' representing free cells) to a grid
    def ReadFromString(self, cellStr, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for _ in range(width)] for _ in range(height)]
        cellLines = cellStr.split("\n")
        i = 0
        j = 0
        for l in cellLines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self.cells[i][j] = 0
                    elif c == '#':
                        self.cells[i][j] = 1
                    else:
                        continue
                    j += 1
                # TODO
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

    # Initialization of map by list of cells.
    def SetGridCells(self, width, height, gridCells):
        self.width = width
        self.height = height
        self.cells = gridCells

    # Check if the cell is on a grid.
    def inBounds(self, i, j):
        return (0 <= j < self.width) and (0 <= i < self.height)

    # Check if thec cell is not an obstacle.
    def Traversable(self, i, j):
        return not self.cells[i][j]

    # Get a list of neighbouring cells as (i,j) tuples.
    # It's assumed that grid is 4-connected (i.e. only moves into cardinal directions are allowed)
    def GetNeighbors(self, i, j):
        neighbors = []
        # Add wait step [0, 0]
        delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]

        for d in delta:
            if self.inBounds(i + d[0], j + d[1]) and self.Traversable(i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))

        return neighbors
