#################################################
# Hw5
# Your andrewID: catherid
# Your section: C
#################################################

def tetrisCollaborators():
    return "joannam1"

# Updated Animation Starter Code

from tkinter import *
import random
import copy

####################################
# customize these functions
####################################

#sets game dimensions
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

#initializes board coordinates, types of tetris pieces, the row/col of the 
#tetris piece, colors, and the score
def init(data):
    data.rows = gameDimensions()[0]
    data.cols = gameDimensions()[1]
    data.cellSize = gameDimensions()[2]
    data.margin = gameDimensions()[3]
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]
    data.isGameOver = False
    data.iPiece = [
        [  True,  True,  True,  True ]]
    data.jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]]
    data.lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]]
    data.oPiece = [
        [  True,  True ],
        [  True,  True ]]
    data.sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]]
    data.tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]]
    data.zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]]
    data.tetrisPieces = [data.iPiece, data.jPiece, data.lPiece, data.oPiece, \
    data.sPiece, data.tPiece, data.zPiece]
    data.tetrisPieceColors = \
    [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    data.fallingPiece = 0
    data.fallingPieceColor = 0
    data.numFallingPieceCols = 0
    data.fallingPieceCol = 0
    data.firstPiece = newFallingPiece(data)
    data.fallingPieceRow = 0
    data.numFallingPieceRow = 0
    data.timerDelay = 200
    data.score = 0

def mousePressed(event, data):
    # use event.x and event.y
    pass

#shifts the piece to the right and left with corresponding arrow keys
#rotates piece 90 degrees if up arrow key is pressed
#restarts the game if r key is pressed
def keyPressed(event, data):
    # use event.char and event.keysym
    if data.isGameOver == False:
        if event.keysym == "Left":
            moveFallingPiece(data, 0, -1)
        elif event.keysym == "Right":
            moveFallingPiece(data, 0, 1)
        elif event.keysym == "Up":
            rotateFallingPiece(data)
    if event.char == "r":
        init(data)

#if the falling piece can't go further down it's placed on the board
#a new random falling piece is created after the old one is placed
#if the falling piece is immediately illegal, the game is over
#once a row is filled, we remove it from the board and shift everything down
def timerFired(data):
    if moveFallingPiece(data, 1, 0) == False:
        placeFallingPlace(data)
        if data.isGameOver == False:
            newFallingPiece(data)
        if moveFallingPiece(data, 1, 0) == False:
            data.isGameOver = True
    removeFullRows(data)

#uses helper functions drawboard, drawscore and drawpiece to draw the view
def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0, 0, data.width, data.height, fill="yellow")
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)
    if data.isGameOver == True:
        canvas.create_text(110,18,text="Game Over. Press R to restart!")

#draws the whole board
def drawBoard(canvas, data):
    rows = data.rows
    cols = data.cols
    for row in range(cols):
        for col in range(rows):
            cellColor = data.board[col][row]
            drawCell(canvas, data, row, col, cellColor)
 
#draws the individual cell in the board
def drawCell(canvas, data, row, col, color):
    margin = data.margin
    canvas.create_rectangle(row * data.cellSize + margin, col * \
    data.cellSize + margin, (row+1)* data.cellSize + margin, (col+1) * \
    data.cellSize + margin, fill=color)

#randomly chooses a new falling piece and places it on the board
def newFallingPiece(data):
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    data.fallingPieceRow = 0
    count = 0
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[i])):
            if data.fallingPiece[i][j] == True:
                count+=1
    #positions it relatively in the center of the board proportional to size
    #of piece
    data.numFallingPieceCols = count
    data.fallingPieceCol = data.cols//2 - data.numFallingPieceCols // 2

#similar to drawboard, but we use drawcell to draw the shape of the piece
def drawFallingPiece(canvas, data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[i])):
            if data.fallingPiece[i][j] == True:
                drawCell(canvas, data, j+data.fallingPieceCol, i + \
                data.fallingPieceRow, data.fallingPieceColor)

#performs a move based on keypressed and immediately undoes it if the move
#is illegal
def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if fallingPieceIsLegal(data) == False:
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True

#checks to see if move is legal by seeing if the move caused the piece to go
#off the board or if there's already a piece at the location
def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            if data.fallingPiece[row][col] == True:
                pieceRow = data.fallingPieceRow + row
                pieceCol = data.fallingPieceCol + col
                if pieceRow < 0 or pieceRow >= data.rows or pieceCol < 0 or \
                pieceCol >= data.cols or \
                data.board[pieceRow][pieceCol] != "blue":
                    return False
    return True

#changes the corresponding cells of data.board's colors when the piece has 
#reached as far down as it can go
def placeFallingPlace(data):
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[i])):
            if data.fallingPiece[i][j] == True:
                data.board[data.fallingPieceRow + i][data.fallingPieceCol + j] \
                = data.fallingPieceColor

#rotates the falling piece by shiftinge the rol and col dimensions when up
#arrow key is pressed
def rotateFallingPiece(data):
    fallingPiece = data.fallingPiece
    currentRow, currentCol = len(data.fallingPiece), len(data.fallingPiece[0])
    newPiece = [([None] * currentRow) for i in range(currentCol)]
    oldRow = data.fallingPieceRow
    oldNumRows = len(data.fallingPiece)
    oldCol = data.fallingPieceCol
    oldNumCols = len(data.fallingPiece[0])
    newRow = data.fallingPieceCol
    newNumRows = len(data.fallingPiece[0])
    newCol = data.fallingPieceRow
    newNumCols = len(data.fallingPiece)
    oldCenterRow = oldRow + oldNumRows//2
    newCenterRow = newRow + newNumRows//2
    oldCenterCol = oldCol + oldNumCols//2
    newCenterCol = newCol + newNumCols//2
    newRow = oldRow + oldNumRows//2 - newNumRows//2
    newCol = oldCol + oldNumCols//2 - newNumCols//2
    for row in range(0, len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[row])):
            newPiece[col][oldNumRows-1-row] = data.fallingPiece[row][col]
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    data.fallingPiece = newPiece
    if fallingPieceIsLegal(data) == False:
        data.fallingPiece = fallingPiece
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol
 
#clears out a full row by making copies of the non-full rows and shifting
#them down
def removeFullRows(data):
    atIndex = len(data.board) -1
    score = 0
    for row in range(len(data.board)-1, -1, -1):
        count = 0
        newRow = []
        for col in range(len(data.board[row])):
            if data.board[row][col] == "blue":
                count+=1
        if count > 0:
            for color in data.board[row]:
                newRow.append(color)
            data.board[atIndex] = newRow
            atIndex -= 1
        else:
            score += 1
    data.score += score**2

#keeps track of the score
def drawScore(canvas, data):
    canvas.create_text(data.width/2, 7, text="Score:" + str(data.score))
####################################
# use the run function as-is
####################################

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = cols * cellSize + margin * 2
    height = rows * cellSize + margin * 2
    run(width, height)

playTetris()