from graphics import *
import sys
import math
import random
import time
import statistics

def inside(rectangle,point):
    x1 = rectangle.getP1().x
    x2 = rectangle.getP2().x
    y1 = rectangle.getP1().y
    y2 = rectangle.getP2().y
    if (x1 < point.x and x2 > point.x and y1 < point.y and y2 > point.y):
        return True

def rollDice(dice,win,selectedList,bigPipList):
    if sum(dice) != 0:
        i = 0
        while i < 5:
            for item in bigPipList[i][dice[i]-1]:
                if selectedList[i] != 0:
                    continue
                item.undraw()
            i+=1

    num = 0
    while num < 2:
        i = 0
        while i < 5:
            if selectedList[i] != 0:
                    i += 1
                    continue
            x = random.randint(1,6)
            for item in bigPipList[i][x-1]:
                item.draw(win)
            i+=1
        time.sleep(0.5)
        i = 0
        while i < 5:
            if selectedList[i] != 0:
                    i += 1
                    continue
            for item in bigPipList[i][5]:
                item.undraw()
            bigPipList[i][0][0].undraw()
            i += 1
        num += 1
    n = 0
    while n < 5:
        if selectedList[n] == 0:
            dice[n] = random.randint(1,6)
            for item in bigPipList[n][dice[n]-1]:
                item.draw(win)
        n += 1
    
def analyze(dice,scorecard,win,turn,finalScore):
    ones = 0
    twos = 0
    threes = 0
    fours = 0
    fives = 0
    sixes = 0
    tok = 0
    fok = 0
    fh = 0
    ss = 0
    ls = 0
    chance = 0
    ytz = 0
    topTotal = 0
    bonus = 0
    
    for item in dice:
        chance += item
        if item == 1:
            ones += 1
        elif item == 2:
            twos += 2
        elif item == 3:
            threes += 3
        elif item == 4:
            fours += 4
        elif item == 5:
            fives += 5
        elif item == 6:
            sixes += 6

    if (ones == 5 or twos == 10 or threes == 15 or fours == 20 or fives == 25
        or sixes == 30):
        if finalScore[turn][13] == 0:
            ytz = 50
            tok += chance
            fok += chance
        elif finalScore[turn][13] == 1 and (int(scorecard[turn][13].getText()) != 0): 
            val = int(scorecard[turn][13].getText()) + 100
            scorecard[turn][13].setText(val)
            tok += chance
            fok += chance
            fh += 25
            ss += 30
            ls += 40
        elif (int(scorecard[turn][13].getText()) == 0):
            tok += chance
            fok += chance
            
    elif (ones >= 4 or twos >= 8 or threes >= 12 or fours >= 16 or fives >= 20
        or sixes >= 24):
        tok += chance
        fok += chance
    elif (ones >= 3 or twos >= 6 or threes >= 9 or fours >= 12 or fives >= 15
        or sixes >= 16):
        tok += chance
    if (tok != 0 and (ones == 2 or twos == 4 or threes == 6 or fours == 8
                      or fives == 10 or sixes == 12)):
        fh = 25
    elif((ones != 0 and twos != 0 and threes != 0 and fours != 0 and fives != 0)
         or (sixes != 0 and twos != 0 and threes != 0
            and fours != 0 and fives != 0)):
        ls = 40
        ss = 30
    elif((ones != 0 and twos != 0 and threes != 0 and fours != 0)
         or (twos != 0 and threes != 0 and fours != 0 and fives != 0) or
         (sixes != 0 and threes != 0 and fours != 0 and fives != 0)):
        ss = 30
    listCat = [ones,twos,threes,fours,fives,sixes,topTotal,bonus,
               tok,fok,fh,ss,ls,ytz,chance]
    n = 0
    num = 0
    while n < 6:
        if finalScore[turn][n] == 0:
            scorecard[turn][n].setText(listCat[n])
        num += finalScore[turn][n]
        n += 1
    if num == 6 and finalScore[turn][6] == 0:
        scorecard[turn][6].setTextColor("black")
        scorecard[turn][7].setTextColor("black")
        ind = 0
        while ind < 6:
            topTotal += int(scorecard[turn][ind].getText())
            ind += 1
        scorecard[turn][6].setText(topTotal)
        if topTotal >= 63:
            bonus = 35
        else:
            bonus = 0
        scorecard[turn][7].setText(bonus)
        finalScore[turn][6] = 1
        finalScore[turn][7] = 1
    n = 8
    while n < 15:
        if finalScore[turn][n] == 0:
            scorecard[turn][n].setText(listCat[n])
        n += 1

    
    
def takeTurn(win,dice,turn,scorecard,diceBoxList,
             selectedList,boxScore,finalScore,bigPipList):
    roll = 0
    while roll < 4:
        mouseCheck = False
        while not mouseCheck:
            mouse = win.getMouse()
            if (mouse.x > 169 and mouse.x < 391 and mouse.y > 410
                and mouse.y < 470 and roll < 3):
                mouseCheck = True
                rollDice(dice,win,selectedList,bigPipList)
            if (mouse.x > 430 and mouse.x < 590
                and mouse.y > 525 and mouse.y < 585):
                win.close()
                sys.exit()
            elif (mouse.x > 210 and mouse.x < 370
                  and mouse.y > 525 and mouse.y < 585):
                win.close()
                main()
            elif roll > 0:
                i = 0
                while i < 5:
                    if inside(diceBoxList[i],mouse):
                        if selectedList[i] == 0:
                            diceBoxList[i].move(0,100)
                            for item in bigPipList[i][dice[i]-1]:
                                item.move(0,100)
                        else:
                            diceBoxList[i].move(0,-100)
                            for item in bigPipList[i][dice[i]-1]:
                                item.move(0,-100)
                        selectedList[i] = abs(selectedList[i]-1)
                    i += 1
                n = 0
                while n < 6:
                    if (inside(boxScore[turn][n],mouse)
                        and finalScore[turn][n] == 0):
                        scorecard[turn][n].setTextColor("black")
                        finalScore[turn][n] = 1
                        analyze(dice,scorecard,win,turn,finalScore)
                        return
                    n += 1
                n = 8
                while n < 15:
                    if (inside(boxScore[turn][n],mouse) and
                        finalScore[turn][n] == 0):
                        scorecard[turn][n].setTextColor("black")
                        finalScore[turn][n] = 1
                        return
                    n += 1
        
        analyze(dice,scorecard,win,turn,finalScore)
        roll += 1

def takeTurnCPU(win,dice,turn,scorecard,diceBoxList,
             selectedList,boxScore,finalScore,bigPipList):
    roll = 0
    while roll < 4:
        chosenDice = [0,0,0,0,0]
        num = 0
        val = statistics.mode(dice)
        mouse = Point(0,0)
        if roll == 0:
            rollDice(dice,win,selectedList,bigPipList)
        # CPU Decision Making
        else: 
            time.sleep(2)
            if int(scorecard[turn][13].getText()) == 50 and finalScore[turn][13] == 0:
                mouse = boxScore[turn][13].getCenter()
            elif int(scorecard[turn][12].getText()) == 40 and finalScore[turn][12] == 0:
                mouse = boxScore[turn][12].getCenter()
            elif (int(scorecard[turn][11].getText()) == 30 and finalScore[turn][11] == 0 and
                  (roll == 3 or (int(scorecard[turn][12].getText()) == 40 and finalScore[turn][12] == 1))):
                mouse = boxScore[turn][11].getCenter()
            elif int(scorecard[turn][11].getText()) == 30 and finalScore[turn][11] == 0 and (roll < 3 and finalScore[turn][12] == 0):
                if(1 in dice and 2 in dice and 3 in dice and 4 in dice):
                    diceNum = 0
                    randomList = []
                    while diceNum < 5:
                        if 6 in dice:
                            randomList += [6]
                        if dice[diceNum] not in randomList:
                            randomList += [dice[diceNum]]
                            chosenDice[diceNum] = 1
                        diceNum += 1
                elif(5 in dice and 2 in dice and 3 in dice and 4 in dice):
                    diceNum = 0
                    randomList = []
                    while diceNum < 5:
                        if dice[diceNum] not in randomList:
                            randomList += [dice[diceNum]]
                            chosenDice[diceNum] = 1
                        diceNum += 1
                elif(5 in dice and 6 in dice and 3 in dice and 4 in dice):
                    diceNum = 0
                    randomList = []
                    while diceNum < 5:
                        if 1 in dice:
                            randomList += [1]
                        if dice[diceNum] not in randomList:
                            randomList += [dice[diceNum]]
                            chosenDice[diceNum] = 1
                        diceNum += 1
            elif int(scorecard[turn][10].getText()) == 25 and finalScore[turn][10] == 0:
                mouse = boxScore[turn][10].getCenter()

            elif(finalScore[turn][val-1] == 1 and roll == 3 and (int(scorecard[turn][8].getText()) != 0) and
                                                                  finalScore[turn][8] == 0) or (((int(scorecard[turn][9].getText()) != 0) and
                                                                 finalScore[turn][9] == 0) and roll == 3):
                
                
                if int(scorecard[turn][9].getText()) != 0 and finalScore[turn][9] == 0:
                    t = 0
                    currentScore = 0
                    while t < 6:
                        if finalScore[turn][t] == 1 and t+1 != val:
                            currentScore += int(scorecard[turn][t].getText())
                        else:
                            currentScore += 3*(t+1)
                        t+=1
                    if (currentScore < 63 and currentScore + val >= 63 and finalScore[turn][val-1] == 0):
                        mouse = boxScore[turn][val-1].getCenter()
                    else:
                        mouse = boxScore[turn][9].getCenter()
                    
                
                elif int(scorecard[turn][8].getText()) != 0 and finalScore[turn][8] == 0:
                    mouse = boxScore[turn][8].getCenter()
            elif roll < 3 and sum(finalScore[turn][0:6]) != 6:
                uber = [0,0,0,0,0,0]
                z = 0
                while z < 6:
                    if finalScore[turn][z] == 0:
                        uber[z] = z + 1
                    z+=1
                val = statistics.mode(dice)
                secondarySet = []
                y = 0
                placeholder = 0
                while y < 5:
                    if dice[y] != val:
                        secondarySet += [dice[y]]
                    else:
                        placeholder += 1
                    y+=1
                y = 0
                place2 = 0
                
                if placeholder != 5:
                    val2 = statistics.mode(secondarySet)
                else:
                    val2 = 0
                while y < 5:
                    if dice[y] == val2:
                        place2 += 1
                    y+=1
                if val2 > val and place2 == placeholder and finalScore[turn][val2-1] == 0:
                    val = val2
                if placeholder < 3 and val not in uber and sum(finalScore[turn][0:5]) != 6 or sum(finalScore[turn][8:10])==2:
                    thingy = 0
                    for item in dice:
                        if item in uber:
                            val = item
                            thingy += 1
                    diceNum = 0
                    if thingy != 0:
                        while diceNum < 5:
                            if dice[diceNum] == val:
                                chosenDice[diceNum] = 1
                            diceNum+=1
                    
                elif ((finalScore[turn][val-1] == 1 ) and (finalScore[turn][8] == 0)):
                    if  (val >= 4 and placeholder >= 2) or placeholder == 4 or (placeholder == 4 and finalScore[turn][13] == 0) or (finalScore[turn][13] > 0 and
                                                                                                              int(scorecard[turn][13].getText()) > 0):
                        diceNum = 0
                        while diceNum < 5:
                            if dice[diceNum] == val:
                                chosenDice[diceNum] = 1
                            diceNum+=1
                    else:
                        secondarySet = []
                        y = 0
                        while y < 5:
                            if dice[y] != val:
                                secondarySet += [dice[y]]
                            y+=1
                        if len(secondarySet) > 0:
                            val = statistics.mode(secondarySet)
                        if finalScore[turn][val-1] == 0:
                            diceNum = 0
                            while diceNum < 5:
                                if dice[diceNum] == val:
                                    chosenDice[diceNum] = 1
                                diceNum+=1
                else:    
                    diceNum = 0
                    while diceNum < 5:
                        if dice[diceNum] == val:
                            chosenDice[diceNum] = 1
                        diceNum+=1
            elif sum(finalScore[turn][0:6]) == 6 and (finalScore[turn][8] == 0 or finalScore[turn][9] == 0 or finalScore[turn][13]==0) and roll < 3:
                val = statistics.mode(dice)
                secondarySet = []
                y = 0
                placeholder = 0
                while y < 5:
                    if dice[y] != val:
                        secondarySet += [dice[y]]
                    else:
                        placeholder += 1
                    y+=1
                y = 0
                place2 = 0

                if placeholder != 5:
                    val2 = statistics.mode(secondarySet)
                else:
                    val2 = 0
                while y < 5:
                    if dice[y] == val2:
                        place2 += 1
                    y+=1
                if val2 > val and place2 == placeholder:
                    val = val2
                diceNum = 0
                while diceNum < 5:
                    if dice[diceNum] == val:
                        chosenDice[diceNum] = 1
                    diceNum+=1
            elif roll == 3 and sum(finalScore[turn][0:6]) != 6:
                n = 0
                scores = []
                while n < 6:
                    if finalScore[turn][n] == 0:
                        scores += [3*(n+1) - int(scorecard[turn][n].getText())]
                    else:
                        scores += [30]
                    n += 1
                favorite = scores.index(min(scores))
                if min(scores) > 2 and finalScore[turn][14] == 0:
                    mouse = boxScore[turn][14].getCenter()
                elif finalScore[turn][13] == 0 and min(scores) > 2:
                    mouse = boxScore[turn][13].getCenter()
                else:
                    mouse = boxScore[turn][favorite].getCenter()
            elif roll == 3:
                selectThing = False
                n = 14
                while n > 7:
                    if finalScore[turn][n] == 0 and not selectThing:
                        mouse = boxScore[turn][n].getCenter()
                        selectThing = True
                    n = n - 1
                
            i = 0
            while i < 5:
                if (chosenDice[i] == 1):
                    if selectedList[i] == 0:
                        diceBoxList[i].move(0,100)
                        for item in bigPipList[i][dice[i]-1]:
                            item.move(0,100)
                    else:
                        diceBoxList[i].move(0,-100)
                        for item in bigPipList[i][dice[i]-1]:
                            item.move(0,-100)
                    selectedList[i] = abs(selectedList[i]-1)
                i += 1
            n = 0
            while n < 6:
                if (inside(boxScore[turn][n],mouse)
                    and finalScore[turn][n] == 0):
                    scorecard[turn][n].setTextColor("black")
                    finalScore[turn][n] = 1
                    analyze(dice,scorecard,win,turn,finalScore)
                    return
                n += 1
            n = 8
            while n < 15:
                if (inside(boxScore[turn][n],mouse) and
                    finalScore[turn][n] == 0):
                    scorecard[turn][n].setTextColor("black")
                    finalScore[turn][n] = 1
                    return
                n += 1
        
        
        if roll > 0 and roll < 3:
            rollDice(dice,win,selectedList,bigPipList)
            time.sleep(1)
        analyze(dice,scorecard,win,turn,finalScore)
        while num < 5:
            if selectedList[num] == 1:
                diceBoxList[num].move(0,-100)
                for item in bigPipList[num][dice[num]-1]:
                    item.move(0,-100)
                selectedList[num] = abs(selectedList[num]-1)
            num+=1
        roll += 1

def mainCPU(win):
    turn = 0
    row = 0

    # Scoreboard setup
    scoreboard = Rectangle(Point(543,27), Point(783,513))
    scoreboard.setFill("white")
    scoreboard.draw(win)
    p1ScoreCard = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    p2ScoreCard = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    scorecard = [p1ScoreCard,p2ScoreCard]
    boxScore = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    while row < 17:
        box = Rectangle(Point(543, (27 + 28.588*row)),
                        Point(683, (27 + 28.588*(row+1))))
        box.draw(win)
        box2 = Rectangle(Point(683, (27 + 28.588*row)),
                        Point(733, (27 + 28.588*(row+1))))
        box2.draw(win)
        box3 = Rectangle(Point(733, (27 + 28.588*row)),
                        Point(783, (27 + 28.588*(row+1))))
        box3.draw(win)
        if row > 0:
            scoreTxt1 = Text(Point(708,41.3+28.6*row),"")
            p1ScoreCard[row-1] = scoreTxt1.clone()
            p1ScoreCard[row-1].draw(win)

            scoreTxt2 = Text(Point(758,41.3+28.6*row),"")
            p2ScoreCard[row-1] = scoreTxt2.clone()
            p2ScoreCard[row-1].draw(win)
            boxScore[0][row-1] = box2.clone()
            boxScore[1][row-1] = box3.clone()
        
        row += 1
    for item in scorecard[0]:
        item.setTextColor("red")
    for item in scorecard[1]:
        item.setTextColor("gray")

    # Naming the rows
    p = Point(613,69.9)

    rowName = Text(p, "Ones")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Twos")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Threes")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Fours")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Fives")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Sixes")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Sum")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Bonus")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Three of a kind")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Four of a kind")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Full house")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Small straight")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Large straight")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Yahtzee")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Chance")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "TOTAL SCORE")
    rowName.draw(win)
    p.y += 28.6

    playerCol = Text(Point(708,41.3),"P1")
    playerCol.draw(win)
    playerCol = Text(Point(758,41.3),"CPU")
    playerCol.draw(win)

    upperBox = Rectangle(Point(543,27), Point(783,227.2))
    upperBox.setWidth(3)
    upperBox.draw(win)

    midBox = Rectangle(Point(543,227.2),Point(783,284.4))
    midBox.setWidth(3)
    midBox.draw(win)

    lowerBox = Rectangle(Point(543,284.4),Point(783,484.6))
    lowerBox.setWidth(3)
    lowerBox.draw(win)

    lastBox = Rectangle(Point(543,484.6),Point(783,513))
    lastBox.setWidth(3)
    lastBox.draw(win)

    rollBox = Rectangle(Point(169,410),Point(391,470))
    rollBox.setFill("LightSteelBlue")
    rollBox.draw(win)

    message = Text(Point(280,440),"Roll Dice")
    message.setSize(15)
    message.draw(win)

    # Distance between dice: 18.6 dice width: 60
    
    d1 = Rectangle(Point(55.6, 90),Point(115.6,150))
    d1.setFill("white")
    d1.setWidth(2)
    d1.draw(win)

    d2 = d1.clone()
    d2.move(97.2,0)
    d2.draw(win)

    d3 = d2.clone()
    d3.move(97.2,0)
    d3.draw(win)

    d4 = d3.clone()
    d4.move(97.2,0)
    d4.draw(win)

    d5 = d4.clone()
    d5.move(97.2,0)
    d5.draw(win)

    diceBoxList = [d1,d2,d3,d4,d5]
    selectedList = [0,0,0,0,0]

    pip1 = Circle(Point(85.6,120),5)
    pip1.setFill("LightSteelBlue")

    pip2 = pip1.clone()
    pip2.move(17,17)
    
    pip3 = pip1.clone()
    pip3.move(-17,-17)

    pip4 = pip1.clone()
    pip4.move(17,-17)

    pip5 = pip1.clone()
    pip5.move(-17,17)

    pip6 = pip1.clone()
    pip6.move(17,0)

    pip7 = pip1.clone()
    pip7.move(-17,0)

    pipList1 = [[pip1],[pip2,pip3],[pip1,pip2,pip3],[pip2,pip3,pip4,pip5],
                [pip1,pip2,pip3,pip4,pip5],[pip2,pip3,pip4,pip5,pip6,pip7]]
    pipRefList1 = [pip1,pip2,pip3,pip4,pip5,pip6,pip7]
    pipRefList2 = [0,0,0,0,0,0,0]
    pipRefList3 = [0,0,0,0,0,0,0]
    pipRefList4 = [0,0,0,0,0,0,0]
    pipRefList5 = [0,0,0,0,0,0,0]

    pipList2 = [0,0,0,0,0,0]
    pipList3 = [0,0,0,0,0,0]
    pipList4 = [0,0,0,0,0,0]
    pipList5 = [0,0,0,0,0,0]

    bigPipList = [pipList1,pipList2,pipList3,pipList4,pipList5]
    
    
    overallRefList = [pipRefList1,pipRefList2,pipRefList3,pipRefList4,
                      pipRefList5]
    num = 1
    while num < 5:
        i = 0
        while i < 7:
            overallRefList[num][i] = overallRefList[num-1][i].clone()
            overallRefList[num][i].move(97.2,0)
            i += 1
        bigPipList[num] = [[overallRefList[num][0]],
                           overallRefList[num][1:3],
                           overallRefList[num][0:3],
                           overallRefList[num][1:5],
                           overallRefList[num][0:5],
                           overallRefList[num][1:]]
        num += 1

    
    
    # Dice setup
    dice = [0,0,0,0,0]

    finalScore = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    n = 0
    while n < 26:
        if turn == 0:
            takeTurn(win,dice,turn,scorecard,diceBoxList,selectedList,
                 boxScore,finalScore,bigPipList)
        else:
            takeTurnCPU(win,dice,turn,scorecard,diceBoxList,selectedList,
                 boxScore,finalScore,bigPipList)
        i = 0
        while i < 15:
            if finalScore[turn][i] == 0:
                scorecard[turn][i].setText("")
            i += 1
        turn = abs(turn-1)
        i = 0
        while i < 5:
            for item in bigPipList[i][dice[i]-1]:
                item.undraw()
                if selectedList[i] == 1:
                    item.move(0,-100)
            i+=1
        dice = [0,0,0,0,0]
        for item in diceBoxList:
            if selectedList[diceBoxList.index(item)] == 1:
                item.move(0,-100)
        selectedList = [0,0,0,0,0]
        n += 1

    x = 8
    P1Score = int(scorecard[0][6].getText())+int(scorecard[0][7].getText())
    P2Score = int(scorecard[1][6].getText())+int(scorecard[1][7].getText())
    while x < 15:
        P1Score += int(scorecard[0][x].getText())
        P2Score += int(scorecard[1][x].getText())
        x += 1
    scorecard[0][15].setText(P1Score)
    scorecard[1][15].setText(P2Score)
    if P1Score > P2Score:
        message.setText("Player 1 wins!")
    elif P2Score>P1Score:
        message.setText("CPU wins!")
    else:
        message.setText("It's a tie.")
    

    endGame = False
    while endGame == False:
        mouse = win.getMouse()
        if (mouse.x > 430 and mouse.x < 590 and mouse.y > 525 and mouse.y < 585):
            win.close()
            sys.exit()
        elif (mouse.x > 210 and mouse.x < 370 and mouse.y > 525 and mouse.y < 585):
            win.close()
            main()
    
def main():
    # Set up the board
    turn = 0

    win = GraphWin("Yahtzee", 820, 600)

    holder = Rectangle(Point(0,0),Point(820,600))
    holder.setFill("green")
    holder.draw(win)

    quitBox = Rectangle(Point(430,525),Point(590,585))
    quitBox.setFill("red")
    quitBox.draw(win)

    quitMessage = Text(Point(510,555), "Quit")
    quitMessage.draw(win)

    playAgainBox = Rectangle(Point(210,525),Point(370,585))
    playAgainBox.setFill("SkyBlue")
    playAgainBox.draw(win)
    playAgain = Text(Point(290,555),"Restart")
    playAgain.draw(win)

    onePlayerBox = Rectangle(Point(55,250),Point(255,325))
    onePlayerBox.setFill("LightSteelBlue")
    onePlayerBox.draw(win)

    twoPlayerBox = onePlayerBox.clone()
    twoPlayerBox.move(250,0)
    twoPlayerBox.draw(win)

    P1Text = Text(onePlayerBox.getCenter(),"One Player")
    P1Text.draw(win)

    P2Text = Text(twoPlayerBox.getCenter(),"Two Players")
    P2Text.draw(win)

    while True:
        mouse = win.getMouse()
        if (inside(quitBox,mouse)):
            win.close()
            sys.exit()
        elif (inside(playAgainBox,mouse)):
            win.close()
            main()
        elif (inside(twoPlayerBox,mouse)):
            P1Text.undraw()
            P2Text.undraw()
            twoPlayerBox.undraw()
            onePlayerBox.undraw()
            break
        elif (inside(onePlayerBox,mouse)):
            P1Text.undraw()
            P2Text.undraw()
            twoPlayerBox.undraw()
            onePlayerBox.undraw()
            mainCPU(win)
    row = 0

    # Scoreboard setup
    scoreboard = Rectangle(Point(543,27), Point(783,513))
    scoreboard.setFill("white")
    scoreboard.draw(win)
    p1ScoreCard = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    p2ScoreCard = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    scorecard = [p1ScoreCard,p2ScoreCard]
    boxScore = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


    
    
    while row < 17:
        box = Rectangle(Point(543, (27 + 28.588*row)),
                        Point(683, (27 + 28.588*(row+1))))
        box.draw(win)
        box2 = Rectangle(Point(683, (27 + 28.588*row)),
                        Point(733, (27 + 28.588*(row+1))))
        box2.draw(win)
        box3 = Rectangle(Point(733, (27 + 28.588*row)),
                        Point(783, (27 + 28.588*(row+1))))
        box3.draw(win)
        if row > 0:
            scoreTxt1 = Text(Point(708,41.3+28.6*row),"")
            p1ScoreCard[row-1] = scoreTxt1.clone()
            p1ScoreCard[row-1].draw(win)

            scoreTxt2 = Text(Point(758,41.3+28.6*row),"")
            p2ScoreCard[row-1] = scoreTxt2.clone()
            p2ScoreCard[row-1].draw(win)
            boxScore[0][row-1] = box2.clone()
            boxScore[1][row-1] = box3.clone()
        
        row += 1
    for item in scorecard[0]:
        item.setTextColor("red")
    for item in scorecard[1]:
        item.setTextColor("blue")

    # Naming the rows
    p = Point(613,69.9)

    rowName = Text(p, "Ones")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Twos")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Threes")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Fours")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Fives")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Sixes")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Sum")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Bonus")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Three of a kind")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Four of a kind")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Full house")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Small straight")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Large straight")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Yahtzee")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "Chance")
    rowName.draw(win)
    p.y += 28.6

    rowName = Text(p, "TOTAL SCORE")
    rowName.draw(win)
    p.y += 28.6

    playerCol = Text(Point(708,41.3),"P1")
    playerCol.draw(win)
    playerCol = Text(Point(758,41.3),"P2")
    playerCol.draw(win)

    upperBox = Rectangle(Point(543,27), Point(783,227.2))
    upperBox.setWidth(3)
    upperBox.draw(win)

    midBox = Rectangle(Point(543,227.2),Point(783,284.4))
    midBox.setWidth(3)
    midBox.draw(win)

    lowerBox = Rectangle(Point(543,284.4),Point(783,484.6))
    lowerBox.setWidth(3)
    lowerBox.draw(win)

    lastBox = Rectangle(Point(543,484.6),Point(783,513))
    lastBox.setWidth(3)
    lastBox.draw(win)

    rollBox = Rectangle(Point(169,410),Point(391,470))
    rollBox.setFill("LightSteelBlue")
    rollBox.draw(win)

    message = Text(Point(280,440),"Roll Dice")
    message.setSize(15)
    message.draw(win)

    # Distance between dice: 18.6 dice width: 60
    
    d1 = Rectangle(Point(55.6, 90),Point(115.6,150))
    d1.setFill("white")
    d1.setWidth(2)
    d1.draw(win)

    d2 = d1.clone()
    d2.move(97.2,0)
    d2.draw(win)

    d3 = d2.clone()
    d3.move(97.2,0)
    d3.draw(win)

    d4 = d3.clone()
    d4.move(97.2,0)
    d4.draw(win)

    d5 = d4.clone()
    d5.move(97.2,0)
    d5.draw(win)

    diceBoxList = [d1,d2,d3,d4,d5]
    selectedList = [0,0,0,0,0]

    pip1 = Circle(Point(85.6,120),5)
    pip1.setFill("LightSteelBlue")

    pip2 = pip1.clone()
    pip2.move(17,17)
    
    pip3 = pip1.clone()
    pip3.move(-17,-17)

    pip4 = pip1.clone()
    pip4.move(17,-17)

    pip5 = pip1.clone()
    pip5.move(-17,17)

    pip6 = pip1.clone()
    pip6.move(17,0)

    pip7 = pip1.clone()
    pip7.move(-17,0)

    pipList1 = [[pip1],[pip2,pip3],[pip1,pip2,pip3],[pip2,pip3,pip4,pip5],
                [pip1,pip2,pip3,pip4,pip5],[pip2,pip3,pip4,pip5,pip6,pip7]]
    pipRefList1 = [pip1,pip2,pip3,pip4,pip5,pip6,pip7]
    pipRefList2 = [0,0,0,0,0,0,0]
    pipRefList3 = [0,0,0,0,0,0,0]
    pipRefList4 = [0,0,0,0,0,0,0]
    pipRefList5 = [0,0,0,0,0,0,0]

    pipList2 = [0,0,0,0,0,0]
    pipList3 = [0,0,0,0,0,0]
    pipList4 = [0,0,0,0,0,0]
    pipList5 = [0,0,0,0,0,0]

    bigPipList = [pipList1,pipList2,pipList3,pipList4,pipList5]
    
    
    overallRefList = [pipRefList1,pipRefList2,pipRefList3,pipRefList4,
                      pipRefList5]
    num = 1
    while num < 5:
        i = 0
        while i < 7:
            overallRefList[num][i] = overallRefList[num-1][i].clone()
            overallRefList[num][i].move(97.2,0)
            i += 1
        bigPipList[num] = [[overallRefList[num][0]],
                           overallRefList[num][1:3],
                           overallRefList[num][0:3],
                           overallRefList[num][1:5],
                           overallRefList[num][0:5],
                           overallRefList[num][1:]]
        num += 1

    
    
    # Dice setup
    dice = [0,0,0,0,0]

    finalScore = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    n = 0
    while n < 26:
        takeTurn(win,dice,turn,scorecard,diceBoxList,selectedList,
                 boxScore,finalScore,bigPipList)
        i = 0
        while i < 15:
            if finalScore[turn][i] == 0:
                scorecard[turn][i].setText("")
            i += 1
        turn = abs(turn-1)
        i = 0
        while i < 5:
            for item in bigPipList[i][dice[i]-1]:
                item.undraw()
                if selectedList[i] == 1:
                    item.move(0,-100)
            i+=1
        dice = [0,0,0,0,0]
        for item in diceBoxList:
            if selectedList[diceBoxList.index(item)] == 1:
                item.move(0,-100)
        selectedList = [0,0,0,0,0]
        n += 1

    x = 8
    P1Score = int(scorecard[0][6].getText())+int(scorecard[0][7].getText())
    P2Score = int(scorecard[1][6].getText())+int(scorecard[1][7].getText())
    while x < 15:
        P1Score += int(scorecard[0][x].getText())
        P2Score += int(scorecard[1][x].getText())
        x += 1
    scorecard[0][15].setText(P1Score)
    scorecard[1][15].setText(P2Score)
    if P1Score > P2Score:
        message.setText("Player 1 wins!")
    elif P2Score>P1Score:
        message.setText("Player 2 wins!")
    else:
        message.setText("It's a tie.")
    

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
 
