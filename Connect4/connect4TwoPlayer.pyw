from graphics import *
import time
import sys

def movePeice(board, column, row, turn, win):
    endpoint = Point((70+80*column), (70+80*(5-row)))
    peice = Circle(Point(endpoint.x,70), 30)
    if turn == 0:
        peice.setFill("yellow")
    else:
        peice.setFill("red")
    peice.draw(win)

    y = 70
    while y < endpoint.y:
       peice.move(0,40)
       time.sleep(0.02)
       y += 40
    

def checkWin(board, turn):
    # Checks the columns
    target = str((turn+1)) + str((turn+1)) + str((turn+1)) + str((turn+1))
    i = 0
    while i < 7:
        sequence = ""
        n = 0
        while n < 6:
            sequence += str(board[i][n])
            n += 1
        if sequence.find(target) != -1:
            return False
        i += 1

    # Checks the rows
    n = 5
    while n >= 0:
        i = 0
        sequence = ""
        while i < 7:
            sequence += str(board[i][n])
            i += 1
        if sequence.find(target) != -1:
            return False
        n -= 1
    
    # Checks the left diagonals
    i = 0
    n = 3
    rowsize = 4
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i += 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 0
    n = 4
    rowsize = 5
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i += 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 0
    n = 5
    rowsize = 6
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i += 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False
    i = 1
    n = 5
    rowsize = 6
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i += 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 2
    n = 5
    rowsize = 5
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i += 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 3
    n = 5
    rowsize = 4
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i += 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 6
    n = 3
    rowsize = 4
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i -= 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 6
    n = 4
    rowsize = 5
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i -= 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 6
    n = 5
    rowsize = 6
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i -= 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 5
    n = 5
    rowsize = 6
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i -= 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 4
    n = 5
    rowsize = 5
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i -= 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    i = 3
    n = 5
    rowsize = 4
    index = 0
    sequence = ""
    while index < rowsize:
        sequence += str(board[i][n])
        i -= 1
        n -= 1
        index += 1
    if sequence.find(target) != -1:
            return False

    # Checks for a tie
    if (board[0][5] != 0 and board[1][5] != 0 and board[2][5] != 0 and board[3][5] != 0 and board[4][5] != 0 and board[5][5] != 0 and board[6][5] != 0):
        return False
        
    return True
            
    

def takeTurn(board, turn, win):
    validColumn = False
    column = 0 # This is just a placeholder
    while validColumn == False:
        validColumn = True
        mouse = win.getMouse()
        if (mouse.x > 40 and mouse.x < 100 and mouse.y > 40 and mouse.y < 500):
            column = 1
        elif (mouse.x > 120 and mouse.x < 180 and mouse.y > 40 and mouse.y < 500):
            column = 2
        elif (mouse.x > 200 and mouse.x < 260 and mouse.y > 40 and mouse.y < 500):
            column = 3
        elif (mouse.x > 280 and mouse.x < 340 and mouse.y > 40 and mouse.y < 500):
            column = 4
        elif (mouse.x > 360 and mouse.x < 420 and mouse.y > 40 and mouse.y < 500):
            column = 5
        elif (mouse.x > 440 and mouse.x < 500 and mouse.y > 40 and mouse.y < 500):
            column = 6
        elif (mouse.x > 520 and mouse.x < 580 and mouse.y > 40 and mouse.y < 500):
            column = 7
        elif (mouse.x > 430 and mouse.x < 590 and mouse.y > 525 and mouse.y < 585):
            win.close()
            sys.exit()
        else: validColumn = False
        
        if board[column-1][5] != 0: 
            validColumn = False
        
    column -= 1
    # Iterate through the column until you hit a peice
    i = 5
    while i > 0 and board[column][i-1] == 0:
        i -= 1
    board[column][i] = (turn + 1)
    movePeice(board, column, i, turn, win)
    return checkWin(board, turn)
    

def main():
    # Set up the board
    board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    turn = 0

    win = GraphWin("Connect 4", 620, 600)

    holder = Rectangle(Point(30,30),Point(590,510))
    holder.setFill("DeepSkyBlue2")
    holder.draw(win)

    message = Text(Point(100,555),"Player 1's Turn")
    message.draw(win)

    quitBox = Rectangle(Point(430,525),Point(590,585))
    quitBox.setFill("red")
    quitBox.draw(win)

    quitMessage = Text(Point(510,555), "Quit")
    quitMessage.draw(win)
    

    col = 0
    while col < 7:
        row = 5
        while row >= 0:
            slot = Circle(Point((70 + 80*col), (70 + 80*row)), 30)
            slot.setFill("SteelBlue3")
            slot.draw(win)
            row -= 1
        col += 1

    while takeTurn(board,turn,win) == True:
        turn = abs(turn-1)
        message.setText("Player " + str(turn+1) + "'s Turn")

    if (board[0][5] != 0 and board[1][5] != 0 and board[2][5] != 0 and board[3][5] != 0 and board[4][5] != 0 and board[5][5] != 0 and board[6][5] != 0):
        message.setText("It's a draw")
    else:
        message.setText("Player " + str(turn + 1) + " wins!")

    playAgainBox = Rectangle(Point(210,525),Point(370,585))
    playAgainBox.setFill("LightSteelBlue")
    playAgainBox.draw(win)
    playAgain = Text(Point(290,555),"Play Again?")
    playAgain.draw(win)

    endGame = False
    while endGame == False:
        mouse = win.getMouse()
        if (mouse.x > 430 and mouse.x < 590 and mouse.y > 525 and mouse.y < 585):
            win.close()
            sys.exit()
        elif (mouse.x > 210 and mouse.x < 370 and mouse.y > 525 and mouse.y < 585):
            win.close()
            main()
        
main()
