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
import graph_backend
from cmu_112_graphics import *

#################################################
# Configuration function
#################################################
def gridDimensions():
    # return (15,10,20,25)
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
    # look for a pl ace to start filling
    if board[i][j] == grid.emptyColor:   # access is safe; edges are occupied
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
        self.whiteBlocks = (self.rows-2)*(self.cols-2)


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
        if row != 0 and row != self.rows-1 and col != 0 and col != self.cols -1:
            if self.board[row][col] == self.emptyColor:
                self.board[row][col] = "black"
                self.whiteBlocks -= 1
            else:
                self.board[row][col] = self.emptyColor
                self.whiteBlocks += 1
    # heuristic functions


#     A      B    where A is set of a potential placement of all n polyominos
#     * ---> *    and B is set of all cells in the grid
#     * ---> *
#     * ---> *
#     * ---> *
#     * ---> *

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


# VIEW -- DRAW COMPONENT INFO TEXT
def drawText(app, canvas):
    # 45 MAGIC NUMBER SORRY
    canvas.create_text(math.floor(app.width) - (2/12)*app.width + 45, app.height//3,
                       text="Connected components: ", font='Arial 8 bold')
    if app.grid.whiteBlocks % 4 == 0:
        fill = 'green'
    else:
        fill = 'red'
    canvas.create_text(math.floor(app.width) - (2/12)*app.width + 45, app.height//3 + 40,
                       text=f'{app.grid.whiteBlocks} blocks', font='Arial 8 bold', fill=fill)


# VIEW -- DRAW BOARD
def drawBoard(app, canvas):
    # 50 magic number for right side margin
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'orange')
    canvas.create_rectangle(app.grid.margin, app.grid.margin,\
                            app.grid.margin + app.grid.cols*(app.grid.cellSize + 2),\
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
    col = math.floor((event.x - margin - 2)/(size + 2))
    row = math.floor((event.y - margin - 2)/(size + 2))

    if (row <= app.grid.rows and col <= app.grid.cols and row >= 0 and col >= 0):
        app.grid.blockifyCell(row, col)


# VIEW - MAIN DRAW FUNCTION
def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawText(app, canvas)
    return


# GAME LOOP
def runPolyominoTiling():
    myDimensions = gridDimensions()
    rows = myDimensions[0]
    cols = myDimensions[1]
    cellSize = myDimensions[2]
    margin = myDimensions[3]
    runApp(width=(round((margin*2 + cols*(cellSize + 2))*1.2)),\
    height=(margin*2 + rows*(cellSize + 2)))


#################################################
# main
#################################################

runPolyominoTiling()
