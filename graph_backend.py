## File for handling graph backend
## We are representing potential polyomino tilings as a bipartite graph
## where nodes on the left side are the set of polyominos tiled and right
## side is the cells on the grid and the edges in between signify which
## polyomino occupies how many and which cells. Our problem will be trying
## to find an exact cover, aka a subset of A whose union of neighborhoods
## pairwise disjointly covers all cells in B
# BASIC CONSTS
# Seven "standard" pieces (tetrominoes)
# Initialize the pieces

#
## Helper function to fill in one possible placement
import copy
from Interface import*

# For each index in 1D representation of our
# grid we check if we can place a piece there, if we can then we fill a
# row of our exact cover matrix with a possible placement
def generatePlacements(width, height):
    genericPieces = []
    n = width*height
    for i in range(n):
        # Check if generic piece placement holds
        if i % width <= width - 4:  # Horizontal iPiece 0 deg
            L = [i, i+1, i+2, i+3]
            fillGeneric(L, genericPieces, height, width)
        if i <= n - 3*width - 1:  # Vertical iPiece 90 deg
            L = [i, width+i, 2*width+i, 3*width+i]
            fillGeneric(L, genericPieces, height, width)
        if i % width <= width - 3 and i < n - width:  # jPiece 0 deg
            L = [i, width+i, width+i+1, width+i+2]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width-1 and i < n - 2*width:  # jPiece 90 deg
            L = [i, i+1, width+i, 2*width+i]
            fillGeneric(L, genericPieces, height, width)
        if i % width <= width - 3 and i < n - width:  # jPiece 180 deg
            L = [i, i+1, i+2, width+i+2]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width - 1 and i < n - 2*width:  # jPiece 270 deg
            L = [i+1, width+i+1, 2*width+i, 2*width+i+1]
            fillGeneric(L, genericPieces, height, width)
        if i % width <= width - 3 and i < n - width:  # lPiece 0 deg
            L = [i+2, width+i, width+i+1, width+i+2]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width - 1 and i < n - 2*width:  # lPiece 90 deg
            L = [i, i+1, width+i+1, 2*width+i+1]
            fillGeneric(L, genericPieces, height, width)
        if i % width <= width - 3 and i < n - width:  # lPiece 180
            L = [i, i+1, i+2, width+i]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width-1 and i < n - 2*width:  # lPiece 270
            L = [i, width+i, 2*width+i, 2*width+i+1]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width - 1 and i < n - width:  # oPiece
            L = [i, i + 1, width + i, width + i + 1]
            fillGeneric(L, genericPieces, height, width)
        if i % width <= width - 3 and i < n - width:  # sPiece 0 deg
            L = [i + 1, i + 2, width + i, width + i + 1]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width - 1 and i < n - 2 * width:  # sPiece 90 deg
            L = [i, width + i, width + i + 1, 2 * width + i + 1]
            fillGeneric(L, genericPieces, height, width)
        if i % width <= width - 3 and i < n - width:  # tPiece 0 deg
            L = [i + 1, width + i, width + i + 1, width + i + 2]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width - 1 and i < n - 2 * width:  # tPiece 90 deg
            L = [i + 1, width + i, width + i + 1, 2 * width + i + 1]
            fillGeneric(L, genericPieces, height, width)
            L = [i, i + 1, i + 2, width + i + 1]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width - 1 and i < n - 2 * width:  # tPiece 270 deg
            L = [i, width + i, width + i + 1, 2 * width + i]
            fillGeneric(L, genericPieces, height, width)
        if i % width <= width - 3 and i < n - width:  # zPiece 0 deg
            L = [i, i + 1, width + i + 2, width + i + 1]
            fillGeneric(L, genericPieces, height, width)
        if i % width != width - 1 and i < n - 2 * width:  # zPiece 90 deg
            L = [i + 1, width + i, width + i + 1, 2 * width + i]
            fillGeneric(L, genericPieces, height, width)

    return genericPieces

 # For each thing: loop through indices and make  them 1
def fillGeneric(L, genericP, rows, cols):
    placement = [-1] * (rows * cols)
    for index in L:
        # build list placement of size rows*cols with placement[index] = 1
        placement[index] = index
    genericP.append(placement)
    return


def getOnesInCol(possiblePlacements, curCol):
    rows = len(possiblePlacements)
    allOnes = []
    for row in range(rows):
        if possiblePlacements[row][curCol] != -1:
            allOnes.append(row)
    return allOnes


def deleteBlackWalls(app):
    possiblePlacements = app.placementList
    # get all 1s in the row
    cols = sorted([x for x in app.grid.wallList])  # not unocupied
    if len(cols) == 0:
        return

    #deletedRows = {y for x in cols for y in getOnesInCol(possiblePlacements, x)}  # all rows we should delete
    deletedRows = set()
    for x in cols:
        tempList = getOnesInCol(possiblePlacements, x)
        for elem in tempList:
            deletedRows.add(elem)

    initialList = [possiblePlacements[x] for x in range(len(possiblePlacements)) if x not in deletedRows]

    final = []
    cols += [len(possiblePlacements[0])]
    slice1 = -1
    for i in range(len(initialList)):
        slice1 = -1
        newListhaha = []
        for slicePortion in cols:
            newListhaha += initialList[i][slice1+1:slicePortion]
            slice1 = slicePortion
        final.append(newListhaha)

    # slices off all unnecessary columns
    app.placementList = final


# def deleteColumn(possiblePlacements, rows, col):
#     for row in range(rows):
#         del possiblePlacements[row][col]
def updateMatrix(possiblePlacements, row, currentCol):
    # get all 1s in the row
    cols = [x for x in range(len(possiblePlacements[row])) if possiblePlacements[row][x] != -1]  # not unocupied
    #deletedRows = {y for x in cols for y in getOnesInCol(possiblePlacements, x)}  # all rows we should delete
    deletedRows = set()
    for x in cols:
        tempList = getOnesInCol(possiblePlacements, x)
        for elem in tempList:
            deletedRows.add(elem)

    initialList = [possiblePlacements[x] for x in range(len(possiblePlacements)) if x not in deletedRows]

    loffset = 0
    for col in cols:
        if col < currentCol:
            loffset += 1

    newListhaha = []
    for i in range(len(initialList)):
        newListhaha.append(initialList[i][0:cols[0]]       \
                     + initialList[i][cols[0]+1:cols[1]]   \
                     + initialList[i][cols[1]+1:cols[2]]   \
                     + initialList[i][cols[2]+1:cols[3]]   \
                     + initialList[i][cols[3]+1:])
    # slices off all unnecessary columns
    return newListhaha, currentCol - loffset


#
## Exact cover solve
## We have a matrix of dimensions rows*cols x allPossiblePlacements
## index [i][j] indicates that placement i covers entry j in the grid
def determineExactCoverSubset(app, possiblePlacements, c):
    # 1. If the matrix A has no columns, the current partial solution
        # is a valid solution; terminate successfully.

    rows = len(possiblePlacements)
    if len(possiblePlacements) == 0 and app.grid.whiteBlocks == 0:
        return "Success"
    elif len(possiblePlacements) <= 0:
        return "Failure"
    if len(possiblePlacements[0]) == 0:
        return "Success"
    else:
        cols = len(possiblePlacements[0])

    # 2. Otherwise, choose a column c (deterministically).
    # 3. Choose a row r such that A[r] = 1 (nondeterministically).
    allOnes = getOnesInCol(possiblePlacements, c)
    for row in allOnes:
        drawPiece(app, possiblePlacements[row], 0)  # 0 for normal col
        # update matrix and pass new copy down the recursion tree
        newPlacements, c = updateMatrix(possiblePlacements, row, c)
        res = determineExactCoverSubset(app, newPlacements, c)
        if res == "Success":
            return "Success"
        drawPiece(app, possiblePlacements[row], 1)  # 1 for white col

    return "Failure"