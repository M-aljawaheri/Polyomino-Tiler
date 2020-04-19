#################################################################
################### LOOKING AT SHAPES PROJECT ###################
######## Authors: Mohammed Al-jawaheri && Igli Mlloja ###########
#################################################################
# Time: 2:01 AM

#
## Polyomino Tiler, implemented intrepreting grids as bipartite graphs
# and attempting to solve exact cover. We consider a potential polyomino
# placement a node in a bipartite graph with edges connected to all of
# the cells it occupies in a given placement.
#     A      B    where A is set of a potential placement of all n polyominos
#     * ---> *    and B is set of all cells in the grid
#     * ---> *
#     * ---> *
#     * ---> *
#     * ---> *

import math, copy, random
from cmu_112_graphics import *

#################################################
# Configuration function
#################################################
def gridDimensions():
    #return (15,10,20,25)
    return (30, 25, 20, 25)

# BASIC CONSTS
# Seven "standard" pieces (tetrominoes)
# Initialize the pieces
iPiece = [
    [  True,  True,  True,  True ]
]

jPiece = [
    [  True, False, False ],
    [  True,  True,  True ]
]

lPiece = [
    [ False, False,  True ],
    [  True,  True,  True ]
]

oPiece = [
    [  True,  True ],
    [  True,  True ]
]

sPiece = [
    [ False,  True,  True ],
    [  True,  True, False ]
]

tPiece = [
    [ False,  True, False ],
    [  True,  True,  True ]
]

zPiece = [
    [  True,  True, False ],
    [ False,  True,  True ]
]


# Helper functions for determining disconnected subcomponents of a grid
#
## Get size of a connected component of grid
def floodFill(grid, i, j):
    board = grid.board
    # look for a place to start filling
    if board[i][j] == grid.emptyColor:
        return 1 + floodFill(grid, i + 1, j) + floodFill(grid, i - 1, j) + floodFill(grid, i, j + 1) + floodFill(grid, i, j - 1)
    else:
        return 0



# Our grid for making the polyomino representation
class grid:
    def __init__(self):
        # setting up the game state
        self.myDimensions = gridDimensions()
        self.rows = self.myDimensions[0]
        self.cols = self.myDimensions[1]
        self.cellSize = self.myDimensions[2]
        self.margin = self.myDimensions[3]

        # initialize the board
        self.emptyColor = "white"
        self.board = [[self.emptyColor for x in range(self.cols)] for x in range(self.rows)]
        # make a black border
        self.board[0] = ["black"] * self.cols
        self.board[self.rows-1] = ["black"] * self.cols
        for i in range(1, self.rows - 1):
            self.board[i][0] = "black"
            self.board[i][self.cols-1] = "black"

    def blockifyCell(self, row, col):
        self.board[row][col] = "black"

    # heuristic functions


#     A      B    where A is set of a potential placement of all n polyominos
#     * ---> *    and B is set of all cells in the grid
#     * ---> *
#     * ---> *
#     * ---> *
#     * ---> *
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


# MODEL - INITIALIZATION
def appStarted(app):
    app.grid = grid()
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]


# VIEW -- DRAW CELL
def drawCell(app, canvas, row, col, color):
    canvas.create_rectangle(app.grid.margin + 2 + col*(app.grid.cellSize + 2),
                            app.grid.margin + 2 + row*(app.grid.cellSize  + 2),
                            app.grid.margin + 2 + col*(app.grid.cellSize  + 2) + app.grid.cellSize,
                            app.grid.margin + 2 + row*(app.grid.cellSize  + 2) + app.grid.cellSize,
                            fill=color)


# VIEW -- DRAW BOARD
def drawBoard(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'orange')
    canvas.create_rectangle(app.grid.margin, app.grid.margin,\
                            app.width - app.grid.margin,\
                            app.height - app.grid.margin, fill='black')
    # Iterate through each row/col in our model
    for row in range(app.grid.rows):
        for col in range(app.grid.cols):
            drawCell(app, canvas, row, col, color=app.grid.board[row][col])


# CONTROLLER - KEY PRESSES
def keyPressed(app, event):
    if event.key == 'Up':
        pass

def mousePressed(app, event):
    size = app.grid.cellSize
    margin = app.grid.margin
    # col = margin - 2 - 2*- event.x
    row = math.floor((event.y) / size) - 2
    col = math.floor((event.x) / size) - 2
    if (row <= app.grid.rows and col <= app.grid.cols and row >= 0 and col >= 0):
        app.grid.blockifyCell(row, col)

# VIEW - MAIN DRAW FUNCTION
def redrawAll(app, canvas):
    drawBoard(app, canvas)
    return


# GAME LOOP
def runPolyominoTiling():
    myDimensions = gridDimensions()
    runApp(width=(myDimensions[3]*2 + myDimensions[1]*(myDimensions[2] + 2)),\
    height=(myDimensions[3]* 2 + myDimensions[0]*(myDimensions[2] + 2)))


#################################################
# main
#################################################

runPolyominoTiling()
