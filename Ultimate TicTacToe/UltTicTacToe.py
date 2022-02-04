from graphics import *
import sys
import math

def restrictMouse(mouse,activeArea,win,bigHash,board,bigRow,bigCol,lilRow,lilCol):
    x1 = activeArea.getP1().x
    y1 = activeArea.getP1().y
    x2 = activeArea.getP2().x
    y2 = activeArea.getP2().y

    if(mouse.x > x1 and mouse.x < x2 and mouse.y > y1 and mouse.y < y2
       and board[bigRow][bigCol][lilRow][lilCol] == 0 and bigHash[bigRow][bigCol] == 0):
        return True
    elif (mouse.x > 430 and mouse.x < 590 and mouse.y > 525 and mouse.y < 585):
        win.close()
        sys.exit()
    else:
        return False

def checkWin(board):
    if((board[0][0]==board[0][1] and board[0][1]==board[0][2] and board[0][0] != 0) or
       (board[1][0]==board[1][1] and board[1][1]==board[1][2] and board[1][0] != 0) or
       (board[2][0]==board[2][1] and board[2][1]==board[2][2] and board[2][0] != 0) or
       (board[0][0]==board[1][0] and board[1][0]==board[2][0] and board[0][0] != 0) or
       (board[0][1]==board[1][1] and board[1][1]==board[2][1] and board[0][1] != 0) or
       (board[0][2]==board[1][2] and board[1][2]==board[2][2] and board[0][2] != 0) or
       (board[0][0]==board[1][1] and board[1][1]==board[2][2] and board[0][0] != 0) or
       (board[0][2]==board[1][1] and board[1][1]==board[2][0] and board[0][2] != 0)):
        return 1
    else:
        arbNum = 1
        n = 0
        while n < 3:
            i = 0
            while i < 3:
                arbNum = arbNum * board[n][i]
                i += 1
            n += 1
        if arbNum != 0:
            return 2
        else:
            return 0

def takeTurn(board,turn,win,boardList,message,boardList2):
    bigHash = [[0,0,0],[0,0,0],[0,0,0]]
    activeArea = Rectangle(Point(67,27),Point(553,513))

    while checkWin(bigHash) == 0:
        mouseCheck = False
        while not mouseCheck:
            mouse = win.getMouse()
            y = mouse.y - 27.0
            x = mouse.x - 67.0
            bigRow = math.floor(y/162.0)
            bigCol = math.floor(x/162.0)
            lilRow = math.floor((y-162*bigRow)/54.0)
            lilCol = math.floor((x-162*bigCol)/54.0)
            mouseCheck = restrictMouse(mouse,activeArea,win,bigHash,board,bigRow,bigCol,lilRow,lilCol)

        board[bigRow][bigCol][lilRow][lilCol] = turn + 1
        markerPlace = Point(math.floor(x/54.0)*54+27+67,math.floor(y/54.0)*54+27+27)
        if turn == 0:
            marker = Text(markerPlace, "X")
            marker.setTextColor("red")
        elif turn == 1:
            marker = Text(markerPlace, "O")
            marker.setTextColor("blue")
        marker.setSize(20) 
        marker.draw(win)
        val = checkWin(board[bigRow][bigCol])

        if val == 1:
            boardList2[bigRow][bigCol].setFill("white")
            boardList2[bigRow][bigCol].draw(win)

            pt = Point(bigCol * 162 + 67 + 81, bigRow * 162 + 27 + 81)
            if turn == 0:
                marker2 = Text(pt, "X")
                marker2.setTextColor("red")
                bigHash[bigRow][bigCol] = 1
            elif turn == 1:
                marker2 = Text(pt, "O")
                marker2.setTextColor("blue")
                bigHash[bigRow][bigCol] = 2
            marker2.setSize(36) 
            marker2.draw(win)
            
        elif val == 2:
            boardList2[bigRow][bigCol].setFill("gray")
            boardList2[bigRow][bigCol].draw(win)
            bigHash[bigRow][bigCol] = 3
            
        turn = abs(turn-1)
        message.setText("Player " + str(turn+1) + "'s Turn")

        if bigHash[lilRow][lilCol] == 0:
            activeArea = boardList[lilRow][lilCol]
            boardList[bigRow][bigCol].setFill("white")
            boardList[lilRow][lilCol].setFill("pink")
        else:
            boardList[bigRow][bigCol].setFill("white")
            activeArea = Rectangle(Point(67,27),Point(553,513))

    if checkWin(bigHash) == 1:
        message.setText("Player " + str(abs(turn-1)+1) + " Wins!")

    else:
        message.setText("It's a Tie")
    
def main():
    # Set up the board
    board = [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]]
    turn = 0

    win = GraphWin("Ultimate Tic-Tac-Toe", 620, 600)

    holder = Rectangle(Point(67,27),Point(553,513))
    holder.setFill("white")
    holder.draw(win)

    message = Text(Point(100,555),"Player 1's Turn")
    message.draw(win)

    quitBox = Rectangle(Point(430,525),Point(590,585))
    quitBox.setFill("red")
    quitBox.draw(win)

    quitMessage = Text(Point(510,555), "Quit")
    quitMessage.draw(win)

    BigBoardList = [[0,0,0],[0,0,0],[0,0,0]]
    BigBoardList2 = [[0,0,0],[0,0,0],[0,0,0]]

    # Bigger boxes
    row = 0
    boxNum = 0
    while row < 3:
        col = 0
        while col < 3:
            box = Rectangle(Point((67 + 162*col), (27 + 162*row)),
                            Point((67 + 162*(col+1)), (27 + 162*(row+1))))
            box.setWidth(5)
            BigBoardList[row][col] = box.clone()
            BigBoardList2[row][col] = BigBoardList[row][col].clone()
            BigBoardList[row][col].draw(win)
            boxNum += 1
            col += 1
        row += 1
  
    # Smaller Boxes
    row = 0
    while row < 9:
        col = 0
        while col < 9:
            box = Rectangle(Point((67 + 54*col), (27 + 54*row)),
                            Point((67 + 54*(col+1)), (27 + 54*(row+1))))
            box.draw(win)
            col += 1
        row += 1

    
    takeTurn(board,turn,win,BigBoardList,message,BigBoardList2)

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
