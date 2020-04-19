#
## File for handling graph backend
## We are representing potential polyomino tilings as a bipartite graph
## where nodes on the left side are the set of polyominos tiled and right
## side is the cells on the grid and the edges in between signify which
## polyomino occupies how many and which cells. Our problem will be trying
## to find an exact cover, aka a subset of A whose union of neighborhoods
## pairwise disjointly covers all cells in B

LEFT = 0
RIGHT = 1
### 0 for left 1 for right
### Boilerplate adapted from geeksforgeeks
# A class to represent the adjacency list of the node
class AdjNode:
    def __init__(self, data, bipartition):
        self.vertex = data
        self.next = None
        self.bipartition = bipartition


# A class to represent a graph. A graph
# is the list of the adjacency lists.
# Size of the array will be the no. of the
# vertices "V"
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [None] * self.V

    # Function to add an edge in an undirected graph
    def add_edge(self, src, dest):
        # Adding the node to the source node
        node = AdjNode(dest)
        node.next = self.graph[src]
        self.graph[src] = node

        # Adding the source node to the destination as
        # it is the undirected graph
        node = AdjNode(src)
        node.next = self.graph[dest]
        self.graph[dest] = node


# Graph representation data structure for representing graph tiling
## Header for bipartite graph representation of the grid
class bipartite:
    # A and B are the sets
    def __init__(self, grid):
        self.grid = grid
        self.graph = self.initializeGraph()

    def initializeGraph(self):
        pass

    # bool return can a subset have a perfect matching with B or not
    def checkExactCover(self):
        pass
