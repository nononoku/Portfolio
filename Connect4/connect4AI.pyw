from graphics import *
import time
import sys
import copy
import itertools
import random
import math

CPU_turn = random.randint(0,1)
MAX_AI_DEPTH = 3
ROUND = 0


class HashTable: 
  
    # Create empty bucket list of given size 
    def __init__(self, size): 
        self.size = size 
        self.hash_table = self.create_buckets() 
  
    def create_buckets(self): 
        return [[] for _ in range(self.size)] 
  
    # Insert values into hash map 
    def set_val(self, key, val): 
        
        # Get the index from the key 
        # using hash function 
        hashed_key = hash(key) % self.size 
          
        # Get the bucket corresponding to index 
        bucket = self.hash_table[hashed_key] 
  
        found_key = False
        for index, record in enumerate(bucket): 
            record_key, record_val = record 
              
            # check if the bucket has same key as 
            # the key to be inserted 
            if record_key == key: 
                found_key = True
                break
  
        # If the bucket has same key as the key to be inserted, 
        # Update the key value 
        # Otherwise append the new key-value pair to the bucket 
        if found_key: 
            bucket[index] = (key, val) 
        else: 
            bucket.append((key, val)) 
  
    # Return searched value with specific key 
    def get_val(self, key): 
        
        # Get the index from the key using 
        # hash function 
        hashed_key = hash(key) % self.size 
          
        # Get the bucket corresponding to index 
        bucket = self.hash_table[hashed_key] 
  
        found_key = False
        for index, record in enumerate(bucket): 
            record_key, record_val = record 
              
            # check if the bucket has same key as  
            # the key being searched 
            if record_key == key: 
                found_key = True
                break
  
        # If the bucket has same key as the key being searched, 
        # Return the value found 
        # Otherwise indicate there was no record found 
        if found_key: 
            return record_val 
        else: 
            return 0
  
    # Remove a value with specific key 
    def delete_val(self, key): 
        
        # Get the index from the key using 
        # hash function 
        hashed_key = hash(key) % self.size 
          
        # Get the bucket corresponding to index 
        bucket = self.hash_table[hashed_key] 
  
        found_key = False
        for index, record in enumerate(bucket): 
            record_key, record_val = record 
              
            # check if the bucket has same key as 
            # the key to be deleted 
            if record_key == key: 
                found_key = True
                break
        if found_key: 
            bucket.pop(index) 
        return

#Me from a year and a half ago was dumb but as with much of this project
#I'm too lazy to fix the badness that was the original implementation
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

    
        
    return True
            
    
def checkWin2(board,turn):
    if not checkWin(board,turn):
        return False
    
    # Checks for a tie
    return  not (board[0][5] != 0 and board[1][5] != 0
            and board[2][5] != 0 and board[3][5] != 0
            and board[4][5] != 0 and board[5][5]!= 0
            and board[6][5] != 0)


# This is the new stuff

def rating(board,turn,rating_chart):
    rating_score = 0
    m = 10 # Modifier
    if turn: m = -10

    # Checks col
    for i in range(7):
        sequence = []
        for n in range(6):
            sequence.append(board[i][n])
        rating_score += rating_chart.get_val(str(sequence[0:4])) * m
        rating_score += rating_chart.get_val(str(sequence[1:5])) * m
        rating_score += rating_chart.get_val(str(sequence[2:6])) * m

    m *= 1.5
    # Checks the rows
    n = 5
    while n >= 0:
        i = 0
        sequence = []
        while i < 7:
            sequence.append(board[i][n])
            i += 1
        rating_score += rating_chart.get_val(str(sequence[0:4])) * m
        rating_score += rating_chart.get_val(str(sequence[1:5])) * m
        rating_score += rating_chart.get_val(str(sequence[2:6])) * m
        rating_score += rating_chart.get_val(str(sequence[3:7])) * m
        rating_score += rating_chart.get_val(str(sequence[4:8])) * m
        n -= 1

    m = m/1.5
    m = m * 1.7
    
    # Checks the left diagonals
    i = 0
    n = 3
    rowsize = 4
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i += 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence)) * m

    i = 0
    n = 4
    rowsize = 5
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i += 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m

    i = 0
    n = 5
    rowsize = 6
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i += 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m
    rating_score += rating_chart.get_val(str(sequence[2:6])) * m
        
    i = 1
    n = 5
    rowsize = 6
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i += 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m
    rating_score += rating_chart.get_val(str(sequence[2:6])) * m

    i = 2
    n = 5
    rowsize = 5
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i += 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m
    
    i = 3
    n = 5
    rowsize = 4
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i += 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence)) * m
    
    i = 6
    n = 3
    rowsize = 4
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i -= 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m
    rating_score += rating_chart.get_val(str(sequence[2:6])) * m

    i = 6
    n = 4
    rowsize = 5
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i -= 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m

    i = 6
    n = 5
    rowsize = 6
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i -= 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m
    rating_score += rating_chart.get_val(str(sequence[2:6])) * m

    i = 5
    n = 5
    rowsize = 6
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i -= 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m
    rating_score += rating_chart.get_val(str(sequence[2:6])) * m

    i = 4
    n = 5
    rowsize = 5
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i -= 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence[0:4])) * m
    rating_score += rating_chart.get_val(str(sequence[1:5])) * m

    i = 3
    n = 5
    rowsize = 4
    index = 0
    sequence = []
    while index < rowsize:
        sequence.append(board[i][n])
        i -= 1
        n -= 1
        index += 1
    rating_score += rating_chart.get_val(str(sequence)) * m

    return rating_score

def checkHyp(board,turn,row,col):

    inarow = 1
    x, y = copy.copy(col),copy.copy(row)

    # Checks Columns
    while(x < 6):
        x += 1
        if board[x][y] != turn + 1:
            break
        else:
            inarow += 1
    if(inarow >= 4):
        return False

    x = copy.copy(col)

    while(x > 0):
        x -= 1
        if board[x][y] != turn + 1:
            break
        else:
            inarow += 1
    if(inarow >= 4):
        return False

    inarow = 1
    x = copy.copy(col)

    # Checks Rows
    while(y < 5):
        y += 1
        if board[x][y] != turn + 1:
            break
        else:
            inarow += 1
    if(inarow >= 4):
        return False

    y = copy.copy(row)

    while(y > 0):
        y -= 1
        if board[x][y] != turn + 1:
            break
        else:
            inarow += 1
    if(inarow >= 4):
        return False

    inarow = 1
    x, y = copy.copy(col),copy.copy(row)

    # Checks left diagonals
    while(x < 6 and y > 0):
        x += 1
        y -= 1
        if board[x][y] != turn + 1:
            break
        else:
            inarow += 1
    if(inarow >= 4):
        return False
    
    x, y = copy.copy(col),copy.copy(row)
    while(x > 0 and y < 5):
        x -= 1
        y += 1
        if board[x][y] != turn + 1:
            break
        else:
            inarow += 1
    if(inarow >= 4):
        return False

    inarow = 1
    x, y = copy.copy(col),copy.copy(row)

    # Checks right diagonals
    while(x > 0 and y > 0):
        x -= 1
        y -= 1
        if board[x][y] != turn + 1:
            break
        else:
            inarow += 1
    if(inarow >= 4):
        return False
    
    x, y = copy.copy(col),copy.copy(row)
    while(x < 6 and y < 5):
        x += 1
        y += 1
        if board[x][y] != turn + 1:
            break
        else:
            inarow += 1
    if(inarow >= 4):
        return False

    # Checks for a tie
    if (board[0][5] and board[1][5] and board[2][5] and board[3][5]
        and board[4][5] and board[5][5] and board[6][5]):
        return False
        
    return True

def calc_rating2(rb,turn,rating_chart,num_cycles):
    if num_cycles == MAX_AI_DEPTH-1:
        return rating(rb,turn,rating_chart)

    rating_list = [0,0,0,0,0,0,0]

    for i in range(7):
        if(rb[i][5]):
            rating_list[i] = -math.inf
            continue
        n = 5
        while n > 0 and rb[i][n-1] == 0:
            n -= 1
        rb[i][n] = (turn + 1)
        if not checkHyp(rb,turn,n,i):
            rating_list[i] = math.inf
            rb[i][n] = 0
            break

        opp_r_list = [0,0,0,0,0,0,0]
        for x in range(7):
            if(rb[x][5]):
                opp_r_list[i] = math.inf
                continue
            m = 5
            while m > 0 and rb[x][m-1] == 0:
                m -= 1
            rb[x][m] = ((turn + 1)%2 + 1)
            if not checkHyp(rb,abs(turn-1),m,x):
                opp_r_list[x] = -math.inf
                rb[x][m] = 0
                break
            opp_r_list[x] = calc_rating2(rb,turn,rating_chart,
                                               num_cycles+1)
            rb[x][m] = 0
        rb[i][n] = 0

        rating_list[i] = min(opp_r_list)

    return max(rating_list)
                
def calc_rating(board,turn,rating_chart):
    
    rating_list = [0,0,0,0,0,0,0]
    turn_lost = [math.inf,math.inf,math.inf,math.inf,math.inf,math.inf,math.inf]

    for i in range(7):
        if(board[i][5]):
            rating_list[i] = -math.inf
            continue
        n = 5
        while n > 0 and board[i][n-1] == 0:
            n -= 1
        board[i][n] = (turn + 1)
        if not checkHyp(board,turn,n,i):
            board[i][n] = 0
            return i

        opp_r_list = [0,0,0,0,0,0,0]
        for x in range(7):
            if(board[x][5]):
                opp_r_list[i] = math.inf
                continue
            m = 5
            while m > 0 and board[x][m-1] == 0:
                m -= 1
            board[x][m] = ((turn + 1)%2 + 1)
            if not checkHyp(board,abs(turn-1),m,x):
                opp_r_list[x] = -math.inf
                board[x][m] = 0
                break
            opp_r_list[x] = calc_rating2(board,turn,rating_chart,0)
            board[x][m] = 0
        board[i][n] = 0
        rating_list[i] = min(opp_r_list)

    max_value = max(rating_list)
    maxes = []
    for i in range(7):
        if (rating_list[i] == max_value and not board[i][5]):
            maxes.append(i)
    return random.choice(maxes)

        

def set_ratings(rating_chart):
    L = set(itertools.permutations([1,0,1,1]))
    for n in L:
        rating_chart.set_val(str(n),150)

    L = set(itertools.permutations([2,0,2,2]))
    for n in L:
        rating_chart.set_val(str(n),-150)

    L = set(itertools.permutations([1,0,0,1]))
    for n in L:
        rating_chart.set_val(str(n),60)

    L = set(itertools.permutations([2,0,0,2]))
    for n in L:
        rating_chart.set_val(str(n),-60)

    L = set(itertools.permutations([1,0,0,0]))
    for n in L:
        rating_chart.set_val(str(n),1)

    L = set(itertools.permutations([2,0,0,0]))
    for n in L:
        rating_chart.set_val(str(n),-1)

    rating_chart.set_val(str([1,1,1,1]),1000000)
    rating_chart.set_val(str([2,2,2,2]),-1000000)

def takeTurn(board, turn, win,rating_chart):
    validColumn = False
    column = 0 # This is just a placeholder
    if turn != CPU_turn:
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

    else:
        global ROUND
        global MAX_AI_DEPTH
        #print(ROUND)
        if ROUND < 5:
            MAX_AI_DEPTH = 2
            column = calc_rating(board,turn,rating_chart)
            ROUND += 1
        else:
            MAX_AI_DEPTH = 3
            column = calc_rating(board,turn,rating_chart)
        
    
    # Iterate through the column until you hit a peice
    i = 5
    while i > 0 and board[column][i-1] == 0:
        i -= 1
    board[column][i] = (turn + 1)
    movePeice(board, column, i, turn, win)
    return checkWin2(board, turn)
   
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

    rating_chart = HashTable(81) 
    set_ratings(rating_chart)
    
    col = 0
    while col < 7:
        row = 5
        while row >= 0:
            slot = Circle(Point((70 + 80*col), (70 + 80*row)), 30)
            slot.setFill("SteelBlue3")
            slot.draw(win)
            row -= 1
        col += 1

    #start = time.time() # Start time
    while takeTurn(board,turn,win,rating_chart) == True:
        turn = abs(turn-1)
        message.setText("Player " + str(turn+1) + "'s Turn")
        #end = time.time() #end time
        #print(end-start)
        #start = time.time()

    if (board[0][5] != 0 and board[1][5] != 0 and
        board[2][5] != 0 and board[3][5] != 0 and board[4][5] != 0
        and board[5][5] != 0 and board[6][5] != 0 and checkWin(board,turn)):
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
            global ROUND
            ROUND = 0
            global CPU_turn
            CPU_turn = abs(CPU_turn-1)
            main()
        
main()
