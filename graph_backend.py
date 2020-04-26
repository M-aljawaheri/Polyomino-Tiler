iPiece = [
    [True, True, True, True]
]

iPiece90 = [
    [True],
    [True],
    [True],
    [True]
]

jPiece = [
    [ True,  False, False],
    [ True,   True, True ]
]

jPiece90 = [
    [ True, True ],
    [ True, False],
    [ True, False]
]

jPiece180 = [
    [ True, True, True],
    [False, False, True]
]

jPiece270 = [
    [ False, True ],
    [ False, True ],
    [  True, True ]
]

lPiece = [
    [ False, False,  True],
    [ True, True,  True]
]

lPiece90 = [
    [True, True],
    [False, True],
    [False, True]
]

lPiece180 =[
    [False, False, True],
    [True, True, True]
]

lPiece270 = [
    [True, False],
    [True, False],
    [True, True]
]

oPiece = [
    [True, True],
    [True, True]
]

sPiece = [
    [False, True, True],
    [True, True, False]

]

sPiece90 = [
    [True, False],
    [True, True],
    [False, True]
]

tPiece = [
    [False, True, False],
    [True, True, True]
]

tPiece90 = [
    [False, True],
    [True, True],
    [False, True]
]


tPiece180 = [
    [True, True, True],
    [False, True, False]

]

tPiece270 = [
    [True, False],
    [True, True],
    [True, False]

]

zPiece = [
    [True, True, False],
    [False, True, True]
]

zPiece90 = [
    [False, True],
    [True, True ],
    [True, False]
]

allPieces = [iPiece,iPiece90,jPiece,jPiece90, jPiece180,\
    jPiece270, lPiece, lPiece90, lPiece180, lPiece270,\
    oPiece, sPiece, sPiece90, tPiece,tPiece90,\
    tPiece180, tPiece270, zPiece, zPiece90]

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

# Takes an upperbound n to form a big enough n x n board that
# encloses current board
def generatePlacements(width, height):
    genericPieces = []
    n = width*height
    for i in range(n):
        # Check if generic piece placement holds
        if i % width <= width - 4:  # Horizontal iPiece 0 deg
            genericPieces.append({i, i+1, i+2, i+3})
        if i <= n - 3*width - 1:  # Vertical iPiece 90 deg
            genericPieces.append({i, width+i, 2*width+i, 3*width+i})
        if i % width <= width - 3 and i < n - width:  # jPiece 0 deg
            genericPieces.append({i, width+i, width+i+1, width+i+2})
        if i % width != width-1 and i < n - 2*width:  # jPiece 90 deg
            genericPieces.append({i, i+1, width+i, 2*width+i})
        if i % width <= width - 3 and i < n - width:  # jPiece 180 deg
            genericPieces.append({i, i+1, i+2, width+i+2})
        if i % width != width - 1 and i < n - 2*width:  # jPiece 270 deg
            genericPieces.append({i+1, width+i+1, 2*width+i, 2*width+i+1})
        if i % width <= width - 3 and i < n - width:  # lPiece 0 deg
            genericPieces.append({i+2, width+i, width+i+1, width+i+2})
        if i % width != width - 1 and i < n - 2*width:  # lPiece 90 deg
            genericPieces.append({i, i+1, width+i+1, 2*width+i+1})
        if i % width <= width - 3 and i < n - width:  # lPiece 180
            genericPieces.append({i, i+1, i+2, width+i})
        if i % width != width-1 and i < n - 2*width:  # lPiece 270
            genericPieces.append({i, width+i, 2*width+i, 2*width+i+1})
        if i % width != width - 1 and i < n - width:  # oPiece
            genericPieces.append({i, i + 1, width + i, width + i + 1})
        if i % width <= width - 3 and i < n - width:  # sPiece 0 deg
            genericPieces.append({i + 1, i + 2, width + i, width + i + 1})
        if i % width != width - 1 and i < n - 2 * width:  # sPiece 90 deg
            genericPieces.append({i, width + i, width + i + 1, 2 * width + i + 1})
        if i % width <= width - 3 and i < n - width:  # tPiece 0 deg
            genericPieces.append({i + 1, width + i, width + i + 1, width + i + 2})
        if i % width != width - 1 and i < n - 2 * width:  # tPiece 90 deg
            genericPieces.append({i + 1, width + i, width + i + 1, 2 * width + i + 1})
        if i % width <= width - 3 and i < n - width:  # tPiece 180 deg
            genericPieces.append({i, i + 1, i + 2, width + i + 1})
        if i % width != width - 1 and i < n - 2 * width:  # tPiece 270 deg
            genericPieces.append({i, width + i, width + i + 1, 2 * width + i})
        if i % width <= width - 3 and i < n - width:  # zPiece 0 deg
            genericPieces.append({i, i + 1, width + i + 2, width + i + 1})
        if i % width != width - 1 and i < n - 2 * width:  # zPiece 90 deg
            genericPieces.append({i + 1, width + i, width + i + 1, 2 * width + i})
    return genericPieces





####### GENERATING LEFT BIPARTITION ########
#  Functions to
## Generate all possible placements of all polyominos

#
## Naive specification function
def naiveGenerate(app):
    placedPieces = []
    for piece in allPieces:
        for row in range(app.rows):
            for col in range(app.cols):
                placementWorks = True
                placementIndices = []
                for pieceRow in range(len(piece)):
                    for pieceCol in range(len(piece[0])):
                        if row+pieceRow >= 1 and row+pieceRow < app.rows-1 and col+pieceCol >=1 and col+pieceCol < app.cols-1:
                            placementWorks = False
                        placementIndices.append(row+pieceRow*app.cols + col+pieceCol)
                if placementWorks:
                    placedPieces.append(placementIndices)
    return placedPieces