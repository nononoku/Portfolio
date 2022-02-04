from graphics import *
import sys
import math
import random
import statistics
import copy
import operator
import shelve

class Stats:
    def __init__(self):
        self.reb = 0
        self.pts = 0
        self.thrA = 0
        self.thrM = 0
        self.fgA = 0
        self.fgM = 0
        self.to = 0
        self.asst = 0
        self.blck = 0
        self.stl = 0
        self.thrPr = 0
        self.fgPr = 0
        self.mins = 0
        self.gp = 0
        
class History:
    def __init__(self):
        self.record = ""
        self.year = ""
        self.confFinish = 0
        self.tourneyExit = ""
        self.prestige = 0
        self.seed = 0
        
class Records:
    def __init__(self):
        self.reb = [[0,""],[0,""],[0,""],[0,""],[0,""]]
        self.pts = [[0,""],[0,""],[0,""],[0,""],[0,""]]
        self.thrM = [[0,""],[0,""],[0,""],[0,""],[0,""]]
        self.fgM = [[0,""],[0,""],[0,""],[0,""],[0,""]]
        self.to = [[0,""],[0,""],[0,""],[0,""],[0,""]]
        self.asst = [[0,""],[0,""],[0,""],[0,""],[0,""]]
        self.blck = [[0,""],[0,""],[0,""],[0,""],[0,""]]
        self.stl = [[0,""],[0,""],[0,""],[0,""],[0,""]]

# Definition of the Player struct/class 
class Player:
    def __init__(self, name, pos, year, thrPt, reb,
                 ins,perD,inD,passing,control,pot,ovr):
        self.name = name #player first and last name
        self.pos = pos #player position (G, F, C)
        self.year = year #player year of college
        self.thrPt = thrPt
        self.reb = reb
        self.ins = ins
        self.perD = perD
        self.inD = inD
        self.passing = passing
        self.control = control
        self.pot = pot
        self.ovr = ovr
        self.stats = Stats()
        self.gameStats = Stats()
        self.cost = 0
        self.clout = 0
        self.team = ""
        self.finalClout = 0

class System:
    def __init__(self,thrFreq,indTO,forceTO,rebMod,blkMod,dMult,tThrMod,tInMod,
                 indThrMod,indInMod,name):
        self.thrFreq = thrFreq
        self.indTO = indTO
        self.forceTO = forceTO
        self.rebMod = rebMod
        self.blkMod = blkMod
        self.dMult = dMult
        self.tThrMod = tThrMod
        self.tInMod = tInMod
        self.indThrMod = indThrMod
        self.indInMod = indInMod
        self.name = name

class Team:
    def __init__(self, name, prestige, conf, roster, ovr):
        self.name = name
        self.prestige = prestige
        self.conf = conf
        self.roster = roster
        self.ovr = ovr
        self.schedule = []
        self.record = []
        self.stats = Stats()
        self.starSlot = 0
        self.asstBonus = 0
        self.perDBonus = 0
        self.insDBonus = 0
        self.rebTotal = 0
        self.gameReb = 0
        self.gameStl = 0
        self.gameBlck = 0
        self.dist = []
        self.gameAsst = 0
        self.gamePoints = 0
        self.tourneyPoints = 0
        self.confWins = 0
        self.confLosses = 0
        self.confPct = 0
        self.wins = 0
        self.seed = 0
        self.gameStats = Stats()
        self.system = System(0,0,0,0,0,1,0,0,0,0,"Standard")
        self.gameRecords = Records()
        self.seasonRecords = Records()
        self.history = []

def fixtures(teams):
    if (len(teams) % 2 == 1):
        teams.append("nonconf")  # if team number is odd - use "nonconf" as fake team     

    rotation = list(teams)       # copy the list

    fixtures = []
    for i in range(0,20):
        fixtures.append(rotation)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    newFixtures = []
    y = 0
    for f in fixtures:
        newFixtures.append([])
        n = len(f)
        x = zip(f[0:int(n/2)],reversed(f[int(n/2):n]))
        for m in x:
            newFixtures[y].append(m)
        y += 1

    return newFixtures

# Returns whether the mouse was clicked inside a given box
def inside(rectangle,point):
    x1 = rectangle.getP1().x
    x2 = rectangle.getP2().x
    y1 = rectangle.getP1().y
    y2 = rectangle.getP2().y
    if (x1 < point.x and x2 > point.x and y1 < point.y and y2 > point.y):
        return True

def freq(sampleList,item):
    i = 0
    for x in sampleList:
        if x == item:
            i += 1
    return i

# Initial biasing of player stats based on age, team, and position for year 1
def bias(prestige, bias, firstNames, lastNames, age):
    

    baseRate = 62 + 13.0 * prestige/100.0 + 1.5*(age - 1.0)

    if prestige >= 0:
        if random.randint(0,100) < 10:
            baseRate = 72

        if random.randint(0,100) < 1:
            baseRate = 85
        

    #baseRate += random.randint(-3,3)
    
    thrPt = copy.copy(baseRate)
    thrPt += random.randint(-5,5)
    reb = copy.copy(baseRate)
    reb += random.randint(-5,5)
    ins = copy.copy(baseRate)
    ins += random.randint(-5,5)
    perD = copy.copy(baseRate)
    perD += random.randint(-5,5)
    inD = copy.copy(baseRate)
    inD += random.randint(-5,5)
    passing = copy.copy(baseRate)
    passing += random.randint(-5,5)
    control = copy.copy(baseRate)
    control += random.randint(-5,5)
    
    posRand = random.randint(1,5)
    if bias != "":
        posRand = 0
    if posRand == 1 or posRand == 2 or bias == "G":
        position = "G"
        thrPt += 7
        reb -= 5
        ins -= 5
        inD -= 7
        passing += 7
        control += 7

        rebV = 0.1
        thrPtV = 0.2
        insV = 0.10
        perDV = 0.17
        inDV = 0.07
        passingV = 0.19
        controlV = 0.17
        
    elif posRand == 3 or posRand == 4 or bias == "F":
        position = "F"
        perD += 5
        thrPt += 3
        control -= 3
        passing -= 5

        rebV = 0.16
        thrPtV = 0.13
        insV = 0.18
        perDV = 0.16
        inDV = 0.15
        passingV = 0.12
        controlV = 0.10
        
    else:
        position = "C"
        thrPt -= 10
        reb += 10
        ins += 5
        perD -= 5
        inD += 7
        passing -= 5
        control -= 4

        rebV = 0.24
        thrPtV = 0.05
        insV = 0.26
        perDV = 0.1
        inDV = 0.23
        passingV = 0.05
        controlV = 0.07

    thrPt = round(statistics.NormalDist(thrPt,7).samples(1)[0])
    reb = round(statistics.NormalDist(reb,7).samples(1)[0])
    ins = round(statistics.NormalDist(ins,7).samples(1)[0])
    perD = round(statistics.NormalDist(perD,7).samples(1)[0])
    inD = round(statistics.NormalDist(inD,7).samples(1)[0])
    passing = round(statistics.NormalDist(passing,7).samples(1)[0])
    control = round(statistics.NormalDist(control,7).samples(1)[0])
    pot = round(statistics.NormalDist(70,10).samples(1)[0])

    
    ovr = round(thrPt * thrPtV + reb * rebV + ins * insV + perD * perDV + inD * inDV + passing * passingV + control * controlV)
    
    playerName = firstNames[random.randint(0,1005)] + " " + lastNames[random.randint(0,1001)]
    return Player(playerName, position, age, thrPt, reb,
                 ins,perD,inD,passing,control,pot,ovr)

# Initial setup, returns the team that the player is playing as
def teamSelect(conference,win,conferenceList):
    n = 0
    boxList = []
    textList = []
    for item in conference:
        boxList.append(Rectangle(Point(0+250*(n % 4),0+75* int(n/4)),
                                     Point(250+250*(n % 4),75+75*int(n/4))))
        n += 1
    
    n = 0 
    for item in boxList:
        textPoint = item.getCenter()
        textText = (conference[n].name + ", " + str(conference[n].prestige) + " prestige")
        textList.append(Text(textPoint,textText))
        item.draw(win)
        textList[n].draw(win)
        n+=1

    backBox = Rectangle(Point(750,525), Point(1000,600))
    backBox.draw(win)
    backMsg = Text(backBox.getCenter(),"Back")
    backMsg.draw(win)

    thing = True
    while thing:
        mouse = win.getMouse()
        n = 0
        for item in boxList:
            if inside(item,mouse):
                selectedTeam = conference[n]
                thing = False
                break
            n += 1
        if inside(backBox,mouse):
            n = 0
            for item in boxList:
                item.undraw()
                textList[n].undraw()
                n += 1
            backBox.undraw()
            backMsg.undraw()
            thing = False
            return conferenceSelect(conferenceList,win)
    n = 0
    for item in boxList:
        item.undraw()
        textList[n].undraw()
        n += 1
    backBox.undraw()
    backMsg.undraw()

    return(selectedTeam)
# Initial setup, leads into team selection
def conferenceSelect(conferenceList,win):
    boxList = []
    textList = []
    row = 0
    while row < 8:
        col = 0
        while col < 4:
            boxList.append(Rectangle(Point(0+250*col,0+75*row),
                                     Point(250+250*col,75+75*row)))
            col += 1
        row += 1
    n = 0
    
    for item in boxList:
        textPoint = item.getCenter()
        textText = conferenceList[n][0].conf
        textList.append(Text(textPoint,textText))
        item.draw(win)
        textList[n].draw(win)
        n+=1
    hold = True
    while hold == True:
        mouse = win.getMouse()
        n = 0
        for item in boxList:
            if inside(item,mouse):
                conferenceNum = n
                hold = False
                break
            n += 1

    n = 0
    for item in boxList:
        item.undraw()
        textList[n].undraw()
        n += 1

    return teamSelect(conferenceList[conferenceNum],win,conferenceList)


def switchPlayers(rosterBox,mouse,playerTeam,rosterText,win):
    validPos = []
    validPos2 = []
    for item in rosterBox:
        for box in item:
            if inside(box,mouse):
                for item2 in item:
                    item2.setFill("pink")
                if rosterBox.index(item) < 2:
                    validPos = ["G"]
                elif rosterBox.index(item) == 2:
                    validPos = ["G","F"]
                elif rosterBox.index(item) == 3:
                    validPos = ["C","F"]
                else:
                    validPos = ["G","F","C"]

                mouse2 = win.getMouse()

                for item3 in rosterBox:
                    for box2 in item3:
                        if inside(box2,mouse2):
                            if rosterBox.index(item3) < 2:
                                validPos2 = ["G"]
                            elif rosterBox.index(item3) == 2:
                                validPos2 = ["G","F"]
                            elif rosterBox.index(item3) == 3:
                                validPos2 = ["C","F"]
                            else:
                                validPos2 = ["G","F","C"]
                            index2 = rosterBox.index(item3)
                            index1 = rosterBox.index(item)
                            if playerTeam.roster[index2].pos in validPos and playerTeam.roster[index1].pos in validPos2:
                                holderPlayer = copy.copy(playerTeam.roster[index1])
                                playerTeam.roster[index1] = playerTeam.roster[index2]
                                playerTeam.roster[index2] = holderPlayer

                                n = index1
                                rosterText[n][0].setText(playerTeam.roster[n].name)
                                rosterText[n][1].setText(playerTeam.roster[n].pos)
                                rosterText[n][2].setText(playerTeam.roster[n].ovr)
                                rosterText[n][3].setText(playerTeam.roster[n].year)

                                n = index2
                                rosterText[n][0].setText(playerTeam.roster[n].name)
                                rosterText[n][1].setText(playerTeam.roster[n].pos)
                                rosterText[n][2].setText(playerTeam.roster[n].ovr)
                                rosterText[n][3].setText(playerTeam.roster[n].year)
                                break
                for item2 in item:
                    item2.setFill("burlywood1")
                break

def expandRoster(roster,win):
    expStGra = []
    
    expandedStatsBox = Rectangle(Point(30,30),Point(970,570))
    expandedStatsBox.setFill("burlywood3")
    expandedStatsBox.draw(win)
    
    
    depthChartText = ["G", "G","G/F","F/C","Flex","Bench","Bench","Bench","Bench","Res.","Res.","Res."]

    rosterText = []
    rosterBox = []
    rosterBoxHeader = []
    rBoxHeadText = []

    headerBox1 = Rectangle(Point(207.5,50),Point(247.5,70))
    rosterBoxHeader.append(headerBox1)
    headerBox2 = Rectangle(Point(247.5,50),Point(367.5,70))
    rosterBoxHeader.append(headerBox2)
    
    
    testText = Text(headerBox2.getCenter(),"Player Name")
    testText2 = Text(headerBox1.getCenter(),"Depth")
    rBoxHeadText.append(testText2)
    rBoxHeadText.append(testText)
    
    
    n = 0
    shortHead = ["Pos","Ovr","Yr","3pt","Reb","Ins","PerD","InD","Pass","Cont","Pot"]
    
    while n < 11:
        rosterBoxHeader.append(Rectangle(Point(367.5+35*n,50),Point(402.5+35*n,70)))
        rBoxHeadText.append(Text(rosterBoxHeader[n+2].getCenter(),shortHead[n]))
        n+=1
    
    n = 1
    while n < 13:
        rosterBoxHeader.append(rosterBoxHeader[0].clone())
        rosterBoxHeader[n+12].move(0,20*n)
        rBoxHeadText.append(Text(rosterBoxHeader[n+12].getCenter(),depthChartText[n-1]))
        n += 1

    n = 0
    for item in rosterBoxHeader:
        item.draw(win)
        rBoxHeadText[n].setSize(10)
        rBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < 12:
        rosterText.append([])
        rosterBox.append([])
        i = 0
        for item in rosterBoxHeader[1:13]:
            rosterBox[n].append(item.clone())
            rosterBox[n][i].move(0,20*(n+1))
            rosterText[n].append(Text(rosterBox[n][i].getCenter(),""))
            rosterText[n][i].setSize(10)
            rosterBox[n][i].draw(win)
            rosterText[n][i].draw(win)
            i += 1
        n += 1
    n = 0
    while n < 12:
        rosterText[n][0].setText(roster[n].name)
        rosterText[n][1].setText(roster[n].pos)
        rosterText[n][2].setText(roster[n].ovr)
        rosterText[n][3].setText(roster[n].year)
        rosterText[n][4].setText(roster[n].thrPt)
        rosterText[n][5].setText(roster[n].reb)
        rosterText[n][6].setText(roster[n].ins)
        rosterText[n][7].setText(roster[n].perD)
        rosterText[n][8].setText(roster[n].inD)
        rosterText[n][9].setText(roster[n].passing)
        rosterText[n][10].setText(roster[n].control)
        rosterText[n][11].setText(roster[n].pot)
        n += 1

    expStGra.extend(rosterBoxHeader)
    expStGra.extend(rBoxHeadText)
    for item in rosterBox:
        expStGra.extend(item)
    for item in rosterText:
        expStGra.extend(item)
        
    backBox = Rectangle(Point(458.75,325),Point(558.75,355))
    backBox.draw(win)
    backText = Text(backBox.getCenter(),"Back")
    backText.setSize(10)
    backText.draw(win)
    expStGra.append(backBox)
    expStGra.append(backText)
    expStGra.append(expandedStatsBox)
    
    while True:
        mouse = win.getMouse()
        if inside(backBox,mouse):
            for item in expStGra:
                item.undraw()
            break
        
def scheduleBuild(conferenceList):
    n = 0
    while n < 10:
        allTeams = []
        for c in conferenceList:
            allTeams.append(copy.copy(c))
        for conference in allTeams:
            nonConference = []
            if len(conference) > 0:
                for item in allTeams:
                    if allTeams.index(item) > allTeams.index(conference) and len(item) > 0:
                        for team in item:
                            nonConference.append(team)
                i = 0
                while 0 < len(conference):
                    while len(nonConference) == 0:
                        newInd = random.randint(0,31)
                        newTeam = conferenceList[newInd][random.randint(0,len(conferenceList[newInd])-1)]
                        if newTeam.conf != conference[i].conf and newTeam.schedule[n].conf != conference[i].conf:
                            newTeam.schedule[n].schedule.remove(newTeam.schedule[n].schedule[n])
                            nonConference.append(newTeam.schedule[n])
                            newTeam.schedule[n] = conference[i]
                    matchupInd = random.randint(0,len(nonConference)-1)
                    oppTeam = nonConference.pop(matchupInd)
                    conference[i].schedule.append(oppTeam)
                    oppTeam.schedule.append(conference[i])
                    for x in allTeams:
                            if oppTeam in x:
                                x.remove(oppTeam)
                            elif len(conference) > 0 and conference[i] in x:
                                x.remove(conference[i])

        
        n += 1
                
    allTeams = []
    teamsSch = []
    for conference in conferenceList:
        allTeams.append(copy.copy(conference))
    for conference in allTeams:
        random.shuffle(conference)
        teamsSch.append(fixtures(conference))
    

    for i in range(0,20):
        oddTeams = []
        for conference in teamsSch:
            for num in range(0,len(conference[i])):
                team, oppTeam = conference[i][num]
                if team == "nonconf":
                    oddTeams.append(oppTeam)
                elif oppTeam == "nonconf":
                    oddTeams.append(team)
                else:
                    team.schedule.append(oppTeam)
                    oppTeam.schedule.append(team)

        
        while len(oddTeams) > 0:
            matchupInd = random.randint(0,len(oddTeams)-1)
            while matchupInd == 0:
                matchupInd = random.randint(0,len(oddTeams)-1)
            oppTeam = oddTeams.pop(matchupInd)
            oddTeams[0].schedule.append(oppTeam)
            oppTeam.schedule.append(oddTeams[0])
            oddTeams.remove(oddTeams[0])
        n += 1

def showSchedule(playerTeam,win):
    expStGra = []
    
    scheduleBox = Rectangle(Point(30,0),Point(970,600))
    scheduleBox.setFill("burlywood3")
    scheduleBox.draw(win)
    

    scheduleText = [[]]
    scheduleBoxList = [[]]
    
    headerText = ["Gm.","Team","Record","Ovr","W/L"]
    
    headerBox1 = Rectangle(Point(207.5-135,10),Point(247.5+-85,30))
    scheduleBoxList[0].append(headerBox1)
    headerBox2 = Rectangle(Point(247.5-85,10),Point(367.5-85,30))
    scheduleBoxList[0].append(headerBox2)
    scheduleText[0].append(Text(scheduleBoxList[0][0].getCenter(),headerText[0]))
    scheduleText[0].append(Text(scheduleBoxList[0][1].getCenter(),headerText[1]))
    
    n = 0
    while n < 3:
        scheduleBoxList[0].append(Rectangle(Point(367.5-85+70*n,10),Point(437.5-85+70*n,30)))
        scheduleText[0].append(Text(scheduleBoxList[0][n+2].getCenter(),headerText[n+2]))
        n+=1
    
    n = 0
    while n < 10:
        opponent = playerTeam.schedule[n]
        game = n + 1
        team = opponent.name
        wins = freq(opponent.record,1)
        losses = freq(opponent.record,0)
        record = (str(wins)+"-"+str(losses))
        ovr = opponent.ovr
        if len(opponent.record) > n:
            if opponent.record[n] == 1:
                outcome = "Loss"
            else:
                outcome = "Win"
        else:
            outcome = ""
        columns = [game, team, record, ovr, outcome]
        i = 0
        scheduleBoxList.append([])
        scheduleText.append([])
        while i < 5:
            scheduleBoxList[n+1].append(scheduleBoxList[n][i].clone())
            scheduleText[n+1].append(scheduleText[n][i].clone())
            scheduleText[n+1][i].setText(columns[i])
            scheduleBoxList[n+1][i].move(0,20)
            scheduleText[n+1][i].setSize(10)
            scheduleText[n+1][i].move(0,20)
            i += 1
        n+=1
    head2 = []
    head3 = []
    num = 0
    for item in scheduleBoxList[0]:
        head2.append(item.clone())
        head2[num].move(440,0)
        head3.append(scheduleText[0][num].clone())
        head3[num].move(440,0)
        num += 1
    expStGra.extend(head2)
    expStGra.extend(head3)
    while n < 30:
        opponent = playerTeam.schedule[n]
        game = n + 1
        team = opponent.name
        wins = freq(opponent.record,1)
        losses = freq(opponent.record,0)
        record = (str(wins)+"-"+str(losses))
        ovr = opponent.ovr
        if len(opponent.record) > n:
            if opponent.record[n] == 1:
                outcome = "Loss"
            else:
                outcome = "Win"
        else:
            outcome = ""
        columns = [game, team, record, ovr, outcome]
        i = 0
        scheduleBoxList.append([])
        scheduleText.append([])
        while i < 5:
            scheduleBoxList[n+1].append(head2[i].clone())
            scheduleText[n+1].append(head3[i].clone())
            scheduleText[n+1][i].setText(columns[i])
            scheduleBoxList[n+1][i].move(0,20*(n-9))
            scheduleText[n+1][i].setSize(10)
            scheduleText[n+1][i].move(0,20*(n-9))
            i += 1
        n+=1        

    
    for item in scheduleBoxList:
        expStGra.extend(item)
    for item in scheduleText:
        expStGra.extend(item)
        
    backBox = Rectangle(Point(458.75,300),Point(658.75,335))
    backText = Text(backBox.getCenter(),"Back")
    backBox.move(-300,0)
    backText.move(-300,0)
    expStGra.append(backBox)
    expStGra.append(backText)
    for item in expStGra:
        item.draw(win)
    expStGra.append(scheduleBox)
    while True:
        mouse = win.getMouse()
        if inside(backBox,mouse):
            for item in expStGra:
                item.undraw()
            break
def cloutCalculator(player):
    clout = 0
    eFG = 0
    stats = player.gameStats
    if stats.fgA > 0:
        eFG = (stats.fgM + (0.5 * stats.thrM))/stats.fgA
    clout = (stats.pts * 4 * eFG + stats.reb * 2 + stats.asst * 3 + stats.stl * 3 + stats.blck * 3 - stats.to * 2) / 100
    return clout
def simGame(team1,team2,playerTeam):
    team1.dist = []
    team2.dist = []
    team1.asstBonus = 0
    team1.perDBonus = 0
    team1.insDBonus = 0
    team2.asstBonus = 0
    team2.perDBonus = 0
    team2.insDBonus = 0
    team1.rebTotal = 0
    team2.rebTotal = 0
    team1.gameReb = 0
    team1.gameStl = 0
    team2.gameReb = 0
    team2.gameStl = 0
    team1.gameBlck = 0
    team2.gameBlck = 0
    team1.gamePoints = 0
    team2.gamePoints = 0
    team1.gameAsst = 0
    team2.gameAsst = 0
    team1.stats.gp += 1
    team2.stats.gp += 1

    for team in [team1,team2]:
        team.gameStats.reb = 0
        team.gameStats.pts = 0
        team.gameStats.thrA = 0
        team.gameStats.thrM = 0
        team.gameStats.fgA = 0
        team.gameStats.fgM = 0
        team.gameStats.to = 0
        team.gameStats.asst = 0
        team.gameStats.blck = 0
        team.gameStats.stl = 0
        team.gameStats.thrPr = 0
        team.gameStats.fgPr = 0
    
    for player in team1.roster:
        player.gameStats.reb = 0
        player.gameStats.pts = 0
        player.gameStats.thrA = 0
        player.gameStats.thrM = 0
        player.gameStats.fgA = 0
        player.gameStats.fgM = 0
        player.gameStats.to = 0
        player.gameStats.asst = 0
        player.gameStats.blck = 0
        player.gameStats.stl = 0
        player.gameStats.thrPr = 0
        player.gameStats.fgPr = 0
        if team1.roster.index(player) == team1.starSlot:
            player.gameStats.mins = 36
            player.stats.gp += 1
        elif team1.roster.index(player) < 5:
            player.gameStats.mins = 28
            player.stats.gp += 1
        elif team1.roster.index(player) < 9:
            player.gameStats.mins = 13
            player.stats.gp += 1
        else:
            player.gameStats.mins = 0
        playTimeMod = 0
        if team1.system.name == "Play Through Star":
            if team1.roster.index(player) == team1.starSlot:
                playTimeMod = 16
            elif team1.roster.index(player) < 5:
                playTimeMod = -4
        n = 0
        while n < (player.gameStats.mins + playTimeMod):
            team1.dist.append(player)
            n+=1
        team1.asstBonus += player.passing * (player.gameStats.mins / 200)
        team1.perDBonus += player.perD * (player.gameStats.mins / 200)
        team1.insDBonus += player.inD * (player.gameStats.mins / 200)
        team1.rebTotal += player.reb * (player.gameStats.mins / 200)
    team1.asstBonus = (team1.asstBonus - 70) * 0.5
    team1.perDBonus = (team1.perDBonus - 70) / 3
    team1.insDBonus = (team1.insDBonus - 70) / 2
        
        
    for player in team2.roster:
        player.gameStats.reb = 0
        player.gameStats.pts = 0
        player.gameStats.thrA = 0
        player.gameStats.thrM = 0
        player.gameStats.fgA = 0
        player.gameStats.fgM = 0
        player.gameStats.to = 0
        player.gameStats.asst = 0
        player.gameStats.blck = 0
        player.gameStats.stl = 0
        player.gameStats.thrPr = 0
        player.gameStats.fgPr = 0

        if team2.roster.index(player) == team2.starSlot:
            player.gameStats.mins = 36
            player.stats.gp += 1
        elif team2.roster.index(player) < 5:
            player.gameStats.mins = 28
            player.stats.gp += 1
        elif team2.roster.index(player) < 9:
            player.gameStats.mins = 13
            player.stats.gp += 1
        else:
            player.gameStats.mins = 0

        playTimeMod = 0
        if team2.system.name == "Play Through Star":
            if team2.roster.index(player) == team2.starSlot:
                playTimeMod = 16
            elif team2.roster.index(player) < 5:
                playTimeMod = -4
        n = 0
        while n < player.gameStats.mins + playTimeMod:
            team2.dist.append(player)
            n+=1
        team2.asstBonus += player.passing * (player.gameStats.mins / 200)
        team2.perDBonus += player.perD * (player.gameStats.mins / 200)
        team2.insDBonus += player.inD * (player.gameStats.mins / 200)
        team2.rebTotal += player.reb * (player.gameStats.mins / 200)

    team2.asstBonus = (team2.asstBonus - 70) * 0.5
    team2.perDBonus = (team2.perDBonus - 70) / 2
    team2.insDBonus = (team2.insDBonus - 70) / 2

    
        
    # This is where things get sketchy, if things go wrong, start burning it all down here        
    poss = 0
    possTeam = team1
    oppTeam = team2
    while poss < 150:
        playerInd = random.randint(0,199)
        player = possTeam.dist[playerInd]
        if player.pos == "G":
            toNum = 20
            thrNum = 35 + possTeam.system.thrFreq
        elif player.pos == "F":
            toNum = 13
            thrNum = 25 + possTeam.system.thrFreq
        else:
            toNum = 10
            thrNum = 15 + possTeam.system.thrFreq
        starTO = 0
        starThrMod = 0
        starInMod = 0
        if possTeam.roster.index(player) == possTeam.starSlot:
            starTO = possTeam.system.indTO
            starThrMod = possTeam.system.indThrMod
            starInMod = possTeam.system.indInMod
        #turnover or shot:
        toChance = random.randint(0,100)
        if toChance < toNum - 0.5 * (player.control - 70) + starTO + oppTeam.system.forceTO:
            player.gameStats.to += 1
            if random.randint(0,100) < 35 + oppTeam.perDBonus * 3 + oppTeam.system.forceTO * 4:
                oppTeam.gameStl += 1
            spareTeam = possTeam
            possTeam = oppTeam
            oppTeam = spareTeam
        else:
            thrPtProb = thrNum + (player.thrPt - 80) * 2
            shotProb = random.randint(0,100)
            player.gameStats.fgA += 1
            if shotProb < thrPtProb:
                # Take a three
                player.gameStats.thrA += 1
                thrPtShot = (35 + 0.4*(player.thrPt-75) + (0.4) * possTeam.asstBonus - oppTeam.perDBonus
                             * oppTeam.system.dMult + possTeam.system.tThrMod + starThrMod)
                if random.randint(0,100) < thrPtShot:
                    # Make a three
                    player.gameStats.thrM += 1
                    player.gameStats.fgM += 1
                    player.gameStats.pts += 3
                    spareTeam = possTeam
                    possTeam = oppTeam
                    oppTeam = spareTeam
                    if random.randint(0,100) < 40 + oppTeam.asstBonus * 2:
                        oppTeam.gameAsst += 1
                else:
                    #Rebound calculator
                    if random.randint(0,100) < 5 + (possTeam.rebTotal - oppTeam.rebTotal + possTeam.system.rebMod) * 0.5:
                        possTeam.gameReb += 1
                    else:
                        oppTeam.gameReb += 1
                        spareTeam = possTeam
                        possTeam = oppTeam
                        oppTeam = spareTeam
            else:
                twPtShot = (45 + 0.5*(player.ins-62) + possTeam.asstBonus - oppTeam.insDBonus * oppTeam.system.dMult
                            * 1.5 + possTeam.system.tInMod + starInMod)
                if random.randint(0,100) < twPtShot:
                    # Make a two
                    player.gameStats.fgM += 1
                    player.gameStats.pts += 2
                    spareTeam = possTeam
                    possTeam = oppTeam
                    oppTeam = spareTeam
                    if random.randint(0,100) < 40 + oppTeam.asstBonus * 2:
                        oppTeam.gameAsst += 1
                else:
                    if random.randint(0,100) < 15 + oppTeam.insDBonus + oppTeam.system.blkMod:
                        oppTeam.gameBlck += 1
                    #Rebound calculator
                    if random.randint(0,100) < 5 + (possTeam.rebTotal - oppTeam.rebTotal + possTeam.system.rebMod) * 0.5:
                        possTeam.gameReb += 1
                    else:
                        oppTeam.gameReb += 1
                        spareTeam = possTeam
                        possTeam = oppTeam
                        oppTeam = spareTeam
        poss += 1
    
    for team in [team1,team2]:
        asstAvg = team.asstBonus * 2 + 65
        asstDist = []
        rebDist = []
        stlDist = []
        blkDist = []
        for player in team.roster[0:9]:
            minPct = player.gameStats.mins / 200
            aNum = round((player.passing - asstAvg) * 2 * minPct)
            rNum = round((player.reb - 75) * minPct)
            sNum = round((player.perD - 70) * 2 * minPct)
            bNum = round((player.reb - 80) * 2 * minPct)
            if aNum > 0:
                for i in range(0,aNum):
                    asstDist.append(player)
            else:
                asstDist.append(player)

            if rNum > 0:
                for i in range(0,rNum):
                    rebDist.append(player)
            else:
                rebDist.append(player)

            if sNum > 0:
                for i in range(0,sNum):
                    stlDist.append(player)
            else:
                stlDist.append(player)

            if bNum > 0:
                for i in range(0,bNum):
                    blkDist.append(player)
            else:
                blkDist.append(player)

        for i in range(0,team.gameAsst):
            player = asstDist[random.randint(0,len(asstDist)-1)]
            player.gameStats.asst += 1
        for i in range(0,team.gameReb):
            player = rebDist[random.randint(0,len(rebDist)-1)]
            player.gameStats.reb += 1
        for i in range(0,team.gameStl):
            player = stlDist[random.randint(0,len(stlDist)-1)]
            player.gameStats.stl += 1
        for i in range(0,team.gameBlck):
            player = blkDist[random.randint(0,len(blkDist)-1)]
            player.gameStats.blck += 1


    for team in [team1,team2]:
        for player in team.roster[0:9]:
            team.gamePoints += player.gameStats.pts

    if team1.gamePoints == team2.gamePoints:
        if random.randint(0,100) < 50:
            team1.roster[team1.starSlot].gameStats.fgA += 1
            team1.roster[team1.starSlot].gameStats.fgM += 1
            team1.roster[team1.starSlot].gameStats.pts += 2
            team1.gamePoints += 2
        else:
            team2.roster[team2.starSlot].gameStats.fgA += 1
            team2.roster[team2.starSlot].gameStats.fgM += 1
            team2.roster[team2.starSlot].gameStats.pts += 2
            team2.gamePoints += 2


    for player in team1.roster:
        if player.gameStats.thrA > 0:
            player.gameStats.thrPr = round(player.gameStats.thrM/player.gameStats.thrA,2)
        if player.gameStats.fgA > 0:
            player.gameStats.fgPr =  round(player.gameStats.fgM/player.gameStats.fgA,2)
    for player in team2.roster:
        if player.gameStats.thrA > 0:
            player.gameStats.thrPr = round(player.gameStats.thrM/player.gameStats.thrA,2)
        if player.gameStats.fgA > 0:
            player.gameStats.fgPr =  round(player.gameStats.fgM/player.gameStats.fgA,2)

    
            
    for team in [team1,team2]:
        
        for player in team.roster[0:9]:
            team.stats.pts += player.gameStats.pts
            team.stats.fgA += player.gameStats.fgA
            team.stats.fgM += player.gameStats.fgM
            team.stats.thrA += player.gameStats.thrA
            team.stats.thrM += player.gameStats.thrM
            team.stats.stl += player.gameStats.stl
            team.stats.blck += player.gameStats.blck
            team.stats.asst += player.gameStats.asst
            team.stats.to += player.gameStats.to
            team.stats.reb += player.gameStats.reb

            team.gameStats.pts += player.gameStats.pts
            team.gameStats.fgA += player.gameStats.fgA
            team.gameStats.fgM += player.gameStats.fgM
            team.gameStats.thrA += player.gameStats.thrA
            team.gameStats.thrM += player.gameStats.thrM
            team.gameStats.stl += player.gameStats.stl
            team.gameStats.blck += player.gameStats.blck
            team.gameStats.asst += player.gameStats.asst
            team.gameStats.to += player.gameStats.to
            team.gameStats.reb += player.gameStats.reb

            player.stats.pts += player.gameStats.pts
            player.stats.fgA += player.gameStats.fgA
            player.stats.fgM += player.gameStats.fgM
            player.stats.thrA += player.gameStats.thrA
            player.stats.thrM += player.gameStats.thrM
            player.stats.stl += player.gameStats.stl
            player.stats.blck += player.gameStats.blck
            player.stats.asst += player.gameStats.asst
            player.stats.to += player.gameStats.to
            player.stats.mins += player.gameStats.mins
            player.stats.reb += player.gameStats.reb

            if team == playerTeam:
                for i in range(0,5):
                    if player.gameStats.pts > team.gameRecords.pts[i][0]:
                        team.gameRecords.pts.append([player.gameStats.pts,player.name])
                        team.gameRecords.pts.sort(key = lambda x: (x[0]),reverse = True)
                        team.gameRecords.pts = team.gameRecords.pts[0:5]
                        break
                for i in range(0,5):
                    if player.gameStats.fgM > team.gameRecords.fgM[i][0]:
                        team.gameRecords.fgM.append([player.gameStats.fgM,player.name])
                        team.gameRecords.fgM.sort(key = lambda x: (x[0]),reverse = True)
                        team.gameRecords.fgM = (team.gameRecords.fgM[0:5])
                        break
                for i in range(0,5):
                    if player.gameStats.thrM > team.gameRecords.thrM[i][0]:
                        team.gameRecords.thrM.append([player.gameStats.thrM,player.name])
                        team.gameRecords.thrM.sort(key = lambda x: (x[0]),reverse = True)
                        team.gameRecords.thrM = (team.gameRecords.thrM[0:5])
                        break
                for i in range(0,5):
                    if player.gameStats.stl > team.gameRecords.stl[i][0]:
                        team.gameRecords.stl.append([player.gameStats.stl,player.name])
                        team.gameRecords.stl.sort(key = lambda x: (x[0]),reverse = True)
                        team.gameRecords.stl = (team.gameRecords.stl[0:5])
                        break
                for i in range(0,5):
                    if player.gameStats.blck > team.gameRecords.blck[i][0]:
                        team.gameRecords.blck.append([player.gameStats.blck,player.name])
                        team.gameRecords.blck.sort(key = lambda x: (x[0]),reverse = True)
                        team.gameRecords.blck = (team.gameRecords.blck[0:5])
                        break
                for i in range(0,5):
                    if player.gameStats.asst > team.gameRecords.asst[i][0]:
                        team.gameRecords.asst.append([player.gameStats.asst,player.name])
                        team.gameRecords.asst.sort(key = lambda x: (x[0]),reverse = True)
                        team.gameRecords.asst = (team.gameRecords.asst[0:5])
                        break
                for i in range(0,5):
                    if player.gameStats.to > team.gameRecords.to[i][0]:
                        team.gameRecords.to.append([player.gameStats.to,player.name])
                        team.gameRecords.to.sort(key = lambda x: (x[0]),reverse = True)
                        team.gameRecords.to = (team.gameRecords.to[0:5])
                        break
                for i in range(0,5):
                    if player.gameStats.reb > team.gameRecords.reb[i][0]:
                        team.gameRecords.reb.append([player.gameStats.reb,player.name])
                        team.gameRecords.reb.sort(key = lambda x: (x[0]),reverse = True)
                        team.gameRecords.reb = (team.gameRecords.reb[0:5])
                        break
            if team == team1:
                player.clout += cloutCalculator(player) * (team2.ovr - 50)
            elif team == team2:
                player.clout += cloutCalculator(player) * (team1.ovr - 50)
    if team1.gamePoints < team2.gamePoints:
       team1.record.append(0)
       team2.record.append(1)
       team2.tourneyPoints += (team1.prestige + team1.ovr / 4)
       if team1.conf == team2.conf:
           team1.confLosses += 1
           team2.confWins += 1

    else:
        team1.record.append(1)
        team2.record.append(0)
        team1.tourneyPoints += (team2.prestige + team2.ovr / 4)
        if team1.conf == team2.conf:
           team2.confLosses += 1
           team1.confWins += 1
    
    
def changeStar(playerTeam,starCol,starText,mouse,win):
    for item in starCol:
        if inside(item,mouse):
            starCol[playerTeam.starSlot].setFill("burlywood1")
            newInd = starCol.index(item)
            starCol[newInd].setFill("yellow")
            starText.undraw()
            starText.move(0,20*(newInd - playerTeam.starSlot))
            starText.draw(win)
            playerTeam.starSlot = newInd

def boxScore(playerTeam,oppTeam,win):
    expStGra = []
    
    expandedStatsBox = Rectangle(Point(0,0),Point(1000,600))
    expandedStatsBox.setFill("burlywood3")
    expandedStatsBox.draw(win)
    
    
    depthChartText = ["G", "G","G/F","F/C","Flex","Bench","Bench","Bench","Bench"]

    rosterText = []
    rosterBox = []
    rosterBoxHeader = []
    rBoxHeadText = []

    headerBox1 = Rectangle(Point(30,50),Point(70,70))
    rosterBoxHeader.append(headerBox1)
    headerBox2 = Rectangle(Point(70,50),Point(190,70))
    rosterBoxHeader.append(headerBox2)
    
    
    testText = Text(headerBox2.getCenter(),"Player Name")
    testText2 = Text(headerBox1.getCenter(),"Depth")
    rBoxHeadText.append(testText2)
    rBoxHeadText.append(testText)
    
    
    n = 0
    shortHead = ["Pos","Ovr","Pts","Reb","Asst","FGM","FGA","FG%",
                 "3PM","3PA","3P%","Blck","Stl","TO","Mins"]
    
    while n < 15:
        rosterBoxHeader.append(Rectangle(Point(190+35*n,50),Point(225+35*n,70)))
        rBoxHeadText.append(Text(rosterBoxHeader[n+2].getCenter(),shortHead[n]))
        n+=1
    
    n = 1
    while n < 10:
        rosterBoxHeader.append(rosterBoxHeader[0].clone())
        rosterBoxHeader[n+16].move(0,20*n)
        rBoxHeadText.append(Text(rosterBoxHeader[n+16].getCenter(),depthChartText[n-1]))
        n += 1

    n = 0
    for item in rosterBoxHeader:
        item.draw(win)
        rBoxHeadText[n].setSize(10)
        rBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < 10:
        rosterText.append([])
        rosterBox.append([])
        i = 0
        for item in rosterBoxHeader[1:17]:
            rosterBox[n].append(item.clone())
            rosterBox[n][i].move(0,20*(n+1))
            rosterText[n].append(Text(rosterBox[n][i].getCenter(),""))
            rosterText[n][i].setSize(10)
            rosterBox[n][i].draw(win)
            rosterText[n][i].draw(win)
            i += 1
        n += 1
    n = 0
    while n < 9:
        rosterText[n][0].setText(playerTeam.roster[n].name)
        rosterText[n][1].setText(playerTeam.roster[n].pos)
        rosterText[n][2].setText(playerTeam.roster[n].ovr)
        rosterText[n][3].setText(playerTeam.roster[n].gameStats.pts)
        rosterText[n][4].setText(playerTeam.roster[n].gameStats.reb)
        rosterText[n][5].setText(playerTeam.roster[n].gameStats.asst)
        rosterText[n][6].setText(playerTeam.roster[n].gameStats.fgM)
        rosterText[n][7].setText(playerTeam.roster[n].gameStats.fgA)
        rosterText[n][8].setText(playerTeam.roster[n].gameStats.fgPr)
        rosterText[n][9].setText(playerTeam.roster[n].gameStats.thrM)
        rosterText[n][10].setText(playerTeam.roster[n].gameStats.thrA)
        rosterText[n][11].setText(playerTeam.roster[n].gameStats.thrPr)
        rosterText[n][12].setText(playerTeam.roster[n].gameStats.blck)
        rosterText[n][13].setText(playerTeam.roster[n].gameStats.stl)
        rosterText[n][14].setText(playerTeam.roster[n].gameStats.to)
        rosterText[n][15].setText(playerTeam.roster[n].gameStats.mins)
        n += 1

    n = 9
    rosterText[n][0].setText("Totals")
    rosterText[n][1].setText("N/A")
    rosterText[n][2].setText(playerTeam.ovr)
    rosterText[n][3].setText(round(playerTeam.gameStats.pts,1))
    rosterText[n][4].setText(round(playerTeam.gameStats.reb,1))
    rosterText[n][5].setText(round(playerTeam.gameStats.asst,1))
    rosterText[n][6].setText(round(playerTeam.gameStats.fgM,1))
    rosterText[n][7].setText(round(playerTeam.gameStats.fgA,1))
    if playerTeam.gameStats.fgA > 0:
        playerTeam.gameStats.fgPr = round(playerTeam.gameStats.fgM / playerTeam.gameStats.fgA,3)
    rosterText[n][8].setText(playerTeam.gameStats.fgPr)
    rosterText[n][9].setText(round(playerTeam.gameStats.thrM,1))
    rosterText[n][10].setText(round(playerTeam.gameStats.thrA,1))
    if playerTeam.gameStats.thrA > 0:
        playerTeam.gameStats.thrPr = round(playerTeam.gameStats.thrM / playerTeam.gameStats.thrA,3)
    rosterText[n][11].setText(playerTeam.gameStats.thrPr)
    rosterText[n][12].setText(round(playerTeam.gameStats.blck,1))
    rosterText[n][13].setText(round(playerTeam.gameStats.stl,1))
    rosterText[n][14].setText(round(playerTeam.gameStats.to,1))
    rosterText[n][15].setText("N/A")

    for item in rosterText[n]:
        item.setStyle("bold")
    
    expStGra.extend(rosterBoxHeader)
    expStGra.extend(rBoxHeadText)
    for item in rosterBox:
        expStGra.extend(item)
    for item in rosterText:
        expStGra.extend(item)
        
    orosterText = []
    orosterBox = []
    orosterBoxHeader = []
    orBoxHeadText = []

    oheaderBox1 = Rectangle(Point(30,320),Point(70,340))
    orosterBoxHeader.append(oheaderBox1)
    oheaderBox2 = Rectangle(Point(70,320),Point(190,340))
    orosterBoxHeader.append(oheaderBox2)
    
    
    otestText = Text(oheaderBox2.getCenter(),"Player Name")
    otestText2 = Text(oheaderBox1.getCenter(),"Depth")
    orBoxHeadText.append(otestText2)
    orBoxHeadText.append(otestText)
    
    
    n = 0
    
    while n < 15:
        orosterBoxHeader.append(Rectangle(Point(190+35*n,320),Point(225+35*n,340)))
        orBoxHeadText.append(Text(orosterBoxHeader[n+2].getCenter(),shortHead[n]))
        n+=1
    
    n = 1
    while n < 10:
        orosterBoxHeader.append(orosterBoxHeader[0].clone())
        orosterBoxHeader[n+16].move(0,20*n)
        orBoxHeadText.append(Text(orosterBoxHeader[n+16].getCenter(),depthChartText[n-1]))
        n += 1

    n = 0
    for item in orosterBoxHeader:
        item.draw(win)
        orBoxHeadText[n].setSize(10)
        orBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < 10:
        orosterText.append([])
        orosterBox.append([])
        i = 0
        for item in orosterBoxHeader[1:17]:
            orosterBox[n].append(item.clone())
            orosterBox[n][i].move(0,20*(n+1))
            orosterText[n].append(Text(orosterBox[n][i].getCenter(),""))
            orosterText[n][i].setSize(10)
            orosterBox[n][i].draw(win)
            orosterText[n][i].draw(win)
            i += 1
        n += 1
    n = 0
    while n < 9:
        orosterText[n][0].setText(oppTeam.roster[n].name)
        orosterText[n][1].setText(oppTeam.roster[n].pos)
        orosterText[n][2].setText(oppTeam.roster[n].ovr)
        orosterText[n][3].setText(oppTeam.roster[n].gameStats.pts)
        orosterText[n][4].setText(oppTeam.roster[n].gameStats.reb)
        orosterText[n][5].setText(oppTeam.roster[n].gameStats.asst)
        orosterText[n][6].setText(oppTeam.roster[n].gameStats.fgM)
        orosterText[n][7].setText(oppTeam.roster[n].gameStats.fgA)
        orosterText[n][8].setText(oppTeam.roster[n].gameStats.fgPr)
        orosterText[n][9].setText(oppTeam.roster[n].gameStats.thrM)
        orosterText[n][10].setText(oppTeam.roster[n].gameStats.thrA)
        orosterText[n][11].setText(oppTeam.roster[n].gameStats.thrPr)
        orosterText[n][12].setText(oppTeam.roster[n].gameStats.blck)
        orosterText[n][13].setText(oppTeam.roster[n].gameStats.stl)
        orosterText[n][14].setText(oppTeam.roster[n].gameStats.to)
        orosterText[n][15].setText(oppTeam.roster[n].gameStats.mins)
        n += 1


    n = 9
    orosterText[n][0].setText("Totals")
    orosterText[n][1].setText("N/A")
    orosterText[n][2].setText(oppTeam.ovr)
    orosterText[n][3].setText(round(oppTeam.gameStats.pts,1))
    orosterText[n][4].setText(round(oppTeam.gameStats.reb,1))
    orosterText[n][5].setText(round(oppTeam.gameStats.asst,1))
    orosterText[n][6].setText(round(oppTeam.gameStats.fgM,1))
    orosterText[n][7].setText(round(oppTeam.gameStats.fgA,1))
    if oppTeam.gameStats.fgA > 0:
        oppTeam.gameStats.fgPr = round(oppTeam.gameStats.fgM / oppTeam.gameStats.fgA,3)
    orosterText[n][8].setText(oppTeam.gameStats.fgPr)
    orosterText[n][9].setText(round(oppTeam.gameStats.thrM,1))
    orosterText[n][10].setText(round(oppTeam.gameStats.thrA,1))
    if oppTeam.gameStats.thrA > 0:
        oppTeam.gameStats.thrPr = round(oppTeam.gameStats.thrM / oppTeam.gameStats.thrA,3)
    orosterText[n][11].setText(oppTeam.gameStats.thrPr)
    orosterText[n][12].setText(round(oppTeam.gameStats.blck,1))
    orosterText[n][13].setText(round(oppTeam.gameStats.stl,1))
    orosterText[n][14].setText(round(oppTeam.gameStats.to,1))
    orosterText[n][15].setText("N/A")

    for item in orosterText[n]:
        item.setStyle("bold")
    
    expStGra.extend(orosterBoxHeader)
    expStGra.extend(orBoxHeadText)
    for item in orosterBox:
        expStGra.extend(item)
    for item in orosterText:
        expStGra.extend(item)
        
    scoreText = Text(Point(850,280),str(playerTeam.name + " " + str(playerTeam.gamePoints)))
    scoreText2 = Text(Point(850,300),str(oppTeam.name + " " + str(oppTeam.gamePoints)))
    scoreText.draw(win)
    expStGra.append(scoreText)
    scoreText2.draw(win)
    expStGra.append(scoreText2)
    team1Text = Text(Point(385,30),playerTeam.name)
    team2Text = Text(Point(385,300),oppTeam.name)
    team1Text.draw(win)
    team2Text.draw(win)
    expStGra.append(team1Text)
    expStGra.append(team2Text)
    

    backBox = Rectangle(Point(800,325),Point(900,355))
    backBox.draw(win)
    backText = Text(backBox.getCenter(),"Next")
    backText.setSize(10)
    backText.draw(win)
    expStGra.append(backBox)
    expStGra.append(backText)


    expStGra.append(expandedStatsBox)
    
    while True:
        mouse = win.getMouse()
        if inside(backBox,mouse):
            for item in expStGra:
                item.undraw()
            break

def stats(playerTeam,win):
    expStGra = []
    
    expandedStatsBox = Rectangle(Point(0,0),Point(1000,600))
    expandedStatsBox.setFill("burlywood3")
    expandedStatsBox.draw(win)
    
    
    depthChartText = ["G", "G","G/F","F/C","Flex","Bench","Bench","Bench","Bench","Res.","Res.","Res."]

    rosterText = []
    rosterBox = []
    rosterBoxHeader = []
    rBoxHeadText = []

    headerBox1 = Rectangle(Point(30,50),Point(70,70))
    rosterBoxHeader.append(headerBox1)
    headerBox2 = Rectangle(Point(70,50),Point(190,70))
    rosterBoxHeader.append(headerBox2)
    
    
    testText = Text(headerBox2.getCenter(),"Player Name")
    testText2 = Text(headerBox1.getCenter(),"Depth")
    rBoxHeadText.append(testText2)
    rBoxHeadText.append(testText)
    
    team1Text = Text(Point(395,30),"Season Per Game Stats")
    team1Text.draw(win)
    expStGra.append(team1Text)
    
    n = 0
    shortHead = ["Pos","Ovr","Pts","Reb","Asst","FGM","FGA","FG%",
                 "3PM","3PA","3P%","Blck","Stl","TO","Mins","GP"]
    
    while n < 16:
        rosterBoxHeader.append(Rectangle(Point(190+35*n,50),Point(225+35*n,70)))
        rBoxHeadText.append(Text(rosterBoxHeader[n+2].getCenter(),shortHead[n]))
        n+=1
    
    n = 1
    while n < 13:
        rosterBoxHeader.append(rosterBoxHeader[0].clone())
        rosterBoxHeader[n+17].move(0,20*n)
        rBoxHeadText.append(Text(rosterBoxHeader[n+17].getCenter(),depthChartText[n-1]))
        n += 1

    n = 0
    for item in rosterBoxHeader:
        item.draw(win)
        rBoxHeadText[n].setSize(10)
        rBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < 13:
        rosterText.append([])
        rosterBox.append([])
        i = 0
        for item in rosterBoxHeader[1:18]:
            rosterBox[n].append(item.clone())
            rosterBox[n][i].move(0,20*(n+1))
            rosterText[n].append(Text(rosterBox[n][i].getCenter(),""))
            rosterText[n][i].setSize(10)
            rosterBox[n][i].draw(win)
            rosterText[n][i].draw(win)
            i += 1
        n += 1
    n = 0
    while n < 12:
        if playerTeam.roster[n].stats.gp == 0:
            m = 1
        else:
            m = playerTeam.roster[n].stats.gp
        rosterText[n][0].setText(playerTeam.roster[n].name)
        rosterText[n][1].setText(playerTeam.roster[n].pos)
        rosterText[n][2].setText(playerTeam.roster[n].ovr)
        rosterText[n][3].setText(round(playerTeam.roster[n].stats.pts/m,1))
        rosterText[n][4].setText(round(playerTeam.roster[n].stats.reb/m,1))
        rosterText[n][5].setText(round(playerTeam.roster[n].stats.asst/m,1))
        rosterText[n][6].setText(round(playerTeam.roster[n].stats.fgM/m,1))
        rosterText[n][7].setText(round(playerTeam.roster[n].stats.fgA/m,1))
        if playerTeam.roster[n].stats.fgA > 0:
            playerTeam.roster[n].stats.fgPr = round(playerTeam.roster[n].stats.fgM / playerTeam.roster[n].stats.fgA,3)
        rosterText[n][8].setText(playerTeam.roster[n].stats.fgPr)
        rosterText[n][9].setText(round(playerTeam.roster[n].stats.thrM/m,1))
        rosterText[n][10].setText(round(playerTeam.roster[n].stats.thrA/m,1))
        if playerTeam.roster[n].stats.thrA > 0:
            playerTeam.roster[n].stats.thrPr = round(playerTeam.roster[n].stats.thrM / playerTeam.roster[n].stats.thrA,3)
        rosterText[n][11].setText(playerTeam.roster[n].stats.thrPr)
        rosterText[n][12].setText(round(playerTeam.roster[n].stats.blck/m,1))
        rosterText[n][13].setText(round(playerTeam.roster[n].stats.stl/m,1))
        rosterText[n][14].setText(round(playerTeam.roster[n].stats.to/m,1))
        rosterText[n][15].setText(round(playerTeam.roster[n].stats.mins/m,1))
        rosterText[n][16].setText(round(playerTeam.roster[n].stats.gp,1))
        n += 1

    expStGra.extend(rosterBoxHeader)
    expStGra.extend(rBoxHeadText)
    for item in rosterBox:
        expStGra.extend(item)
    for item in rosterText:
        expStGra.extend(item)

    backBox = Rectangle(Point(350,345),Point(450,375))
    backBox.draw(win)
    backText = Text(backBox.getCenter(),"Back")
    backText.setSize(10)
    backText.draw(win)
    expStGra.append(backBox)
    expStGra.append(backText)

    n = 12
    if playerTeam.stats.gp == 0:
            m = 1
    else:
        m = playerTeam.stats.gp
    rosterText[n][0].setText("Totals")
    rosterText[n][1].setText("N/A")
    rosterText[n][2].setText(playerTeam.ovr)
    rosterText[n][3].setText(round(playerTeam.stats.pts/m,1))
    rosterText[n][4].setText(round(playerTeam.stats.reb/m,1))
    rosterText[n][5].setText(round(playerTeam.stats.asst/m,1))
    rosterText[n][6].setText(round(playerTeam.stats.fgM/m,1))
    rosterText[n][7].setText(round(playerTeam.stats.fgA/m,1))
    if playerTeam.stats.fgA > 0:
        playerTeam.stats.fgPr = round(playerTeam.stats.fgM / playerTeam.stats.fgA,3)
    rosterText[n][8].setText(playerTeam.stats.fgPr)
    rosterText[n][9].setText(round(playerTeam.stats.thrM/m,1))
    rosterText[n][10].setText(round(playerTeam.stats.thrA/m,1))
    if playerTeam.stats.thrA > 0:
        playerTeam.stats.thrPr = round(playerTeam.stats.thrM / playerTeam.stats.thrA,3)
    rosterText[n][11].setText(playerTeam.stats.thrPr)
    rosterText[n][12].setText(round(playerTeam.stats.blck/m,1))
    rosterText[n][13].setText(round(playerTeam.stats.stl/m,1))
    rosterText[n][14].setText(round(playerTeam.stats.to/m,1))
    rosterText[n][15].setText("N/A")
    rosterText[n][16].setText(round(playerTeam.stats.gp,1))

    for item in rosterText[n]:
        item.setStyle("bold")
    
    expStGra.append(expandedStatsBox)
    
    while True:
        mouse = win.getMouse()
        if inside(backBox,mouse):
            for item in expStGra:
                item.undraw()
            break
def recruitPlayers(team,firstNames,lastNames):
    posList = []
    for player in team.roster:
        posList.append(player.pos)
    guards = freq(posList,"G")
    if guards < 2:
        for n in range(0,(2-guards)):
            team.roster.append(bias(team.prestige,"G",firstNames,lastNames,1))

    forwards = freq(posList,"F")
    centers = freq(posList,"C")

    # Come back to check if this is acceptable as a method of checking
    if forwards == 0 and guards < 3 and centers == 0:
        team.roster.append(bias(team.prestige,"F",firstNames,lastNames,1))

    while len(team.roster) < 12:
        team.roster.append(bias(team.prestige,"",firstNames,lastNames,1))

def grade(num):
    grades = ["F","D","C","B","A"]
    index = math.floor((num-50)/10)
    if index < 0:
        index = 0
    elif index > 4:
        index = 4
    return grades[index]

def fixRoster(roster,win,firstNames,lastNames):
    expStGra = []
    samplePlayer = bias(-50,"G",firstNames,lastNames,random.randint(1,4))
    samplePlayer.pot = random.randint(0,100)
    roster.append(samplePlayer)
    samplePlayer = bias(-50,"G",firstNames,lastNames,random.randint(1,4))
    samplePlayer.pot = random.randint(0,100)
    roster.append(samplePlayer)
    samplePlayer = bias(-50,"F",firstNames,lastNames,random.randint(1,4))
    samplePlayer.pot = random.randint(0,100)
    roster.append(samplePlayer)
    samplePlayer = bias(-50,"C",firstNames,lastNames,random.randint(1,4))
    samplePlayer.pot = random.randint(0,100)
    roster.append(samplePlayer)

    while len(roster) < 16:
        samplePlayer = bias(-50,"G",firstNames,lastNames,random.randint(1,4))
        samplePlayer.pot = random.randint(0,100)
        roster.append(samplePlayer)
    
    depthChartText = ["","","","","","","","","","","","","","","",""]

    rosterText = []
    rosterBox = []
    rosterBoxHeader = []
    rBoxHeadText = []

    headerBox1 = Rectangle(Point(207.5,50),Point(247.5,70))
    rosterBoxHeader.append(headerBox1)
    headerBox2 = Rectangle(Point(247.5,50),Point(367.5,70))
    rosterBoxHeader.append(headerBox2)
    
    
    testText = Text(headerBox2.getCenter(),"Player Name")
    testText2 = Text(headerBox1.getCenter(),"")
    rBoxHeadText.append(testText2)
    rBoxHeadText.append(testText)
    
    
    n = 0
    shortHead = ["Pos","Ovr","Yr","3pt","Reb","Ins","PerD","InD","Pass","Cont","Pot"]
    
    while n < 11:
        rosterBoxHeader.append(Rectangle(Point(367.5+35*n,50),Point(402.5+35*n,70)))
        rBoxHeadText.append(Text(rosterBoxHeader[n+2].getCenter(),shortHead[n]))
        n+=1
    
    n = 1
    while n < 13:
        rosterBoxHeader.append(rosterBoxHeader[0].clone())
        rosterBoxHeader[n+12].move(0,20*n)
        rBoxHeadText.append(Text(rosterBoxHeader[n+12].getCenter(),depthChartText[n-1]))
        n += 1

    n = 0
    for item in rosterBoxHeader:
        item.draw(win)
        rBoxHeadText[n].setSize(10)
        rBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < len(roster):
        rosterText.append([])
        rosterBox.append([])
        i = 0
        for item in rosterBoxHeader[1:13]:
            rosterBox[n].append(item.clone())
            rosterBox[n][i].move(0,20*(n+1))
            rosterText[n].append(Text(rosterBox[n][i].getCenter(),""))
            rosterText[n][i].setSize(10)
            rosterBox[n][i].draw(win)
            rosterText[n][i].draw(win)
            i += 1
        n += 1
    n = 0
    while n < len(roster):
        rosterText[n][0].setText(roster[n].name)
        rosterText[n][1].setText(roster[n].pos)
        rosterText[n][2].setText(roster[n].ovr)
        rosterText[n][3].setText(roster[n].year)
        rosterText[n][4].setText(roster[n].thrPt)
        rosterText[n][5].setText(roster[n].reb)
        rosterText[n][6].setText(roster[n].ins)
        rosterText[n][7].setText(roster[n].perD)
        rosterText[n][8].setText(roster[n].inD)
        rosterText[n][9].setText(roster[n].passing)
        rosterText[n][10].setText(roster[n].control)
        rosterText[n][11].setText(roster[n].pot)
        n += 1

    expStGra.extend(rosterBoxHeader)
    expStGra.extend(rBoxHeadText)
    for item in rosterBox:
        expStGra.extend(item)
    for item in rosterText:
        expStGra.extend(item)
        
    backBox = Rectangle(Point(850,325),Point(950,355))
    backBox.draw(win)
    backText = Text(backBox.getCenter(),"Confirm")
    backText.setSize(10)
    backText.draw(win)
    expStGra.append(backBox)
    expStGra.append(backText)
    removeText = Text(Point(500,20),"Click on the name of the players you want to remove " + str(len(roster) - 12) + " remaining.")
    removeText.draw(win)
    expStGra.append(removeText)

    newRoster = copy.copy(roster)
    
    while True:
        mouse = win.getMouse()

        newRosterP = []
        for item in newRoster:
            newRosterP.append(item.pos)
            
        guards = freq(newRosterP,"G")
        forwards = freq(newRosterP,"F")
        centers = freq(newRosterP,"C")

        if guards < 2:
            gNeed = (2 - guards)
        else:
            gNeed = 0
        if forwards + centers < 1:
            fcNeed = 1
        else:
            fcNeed = 0
        if guards < 3 and forwards < 1:
            gfNeed = 1
        else:
            gfNeed = 0
        needs = gNeed + fcNeed + gfNeed


        for i in range(0,len(rosterBox)):
            if inside(rosterBox[i][0],mouse):
                if roster[i] in newRoster:
                    rosterBox[i][0].setFill("red")
                    newRoster.remove(roster[i])
                else:
                    rosterBox[i][0].setFill("burlywood1")
                    newRoster.append(roster[i])
                removeText.setText("Click on the name of the players you want to remove " + str(len(newRoster) - 12) + " remaining.")

        if inside(backBox,mouse) and len(newRoster) - 12 == 0 and needs == 0:
            for item in expStGra:
                item.undraw()
            return newRoster

def playerRecruitment(team,win,firstNames,lastNames):
    graphicsList = []

    recruitablePlayers = []
    n = 0
    samplePlayer = bias(team.prestige,"G",firstNames,lastNames,1)
    recruitablePlayers.append(samplePlayer)
    samplePlayer = bias(team.prestige,"G",firstNames,lastNames,1)
    recruitablePlayers.append(samplePlayer)
    samplePlayer = bias(team.prestige,"F",firstNames,lastNames,1)
    recruitablePlayers.append(samplePlayer)
    samplePlayer = bias(team.prestige,"C",firstNames,lastNames,1)
    recruitablePlayers.append(samplePlayer)
    while n < 17:
        modifier = random.randint(-5,10)
        samplePlayer = bias(team.prestige + modifier,"",firstNames,lastNames,1)
        samplePlayer.pot = random.randint(40,100)
        recruitablePlayers.append(samplePlayer)
        n += 1

    
    
    boxes = []
    headers = ["Pos","thrPt","reb","ins","perD","inD","passing","control","pot","Cost"]
    num = 0
    for n in range(0,3):
        for i in range(0,7):
            attrList = []
            boxes.append(Rectangle(Point(300+100*i,0+200*n),Point(400+100*i,200+200*n)))
            boxes[num].draw(win)
            player = recruitablePlayers[num]
            attributes = [player.pos,player.thrPt,player.reb,player.ins,player.perD,player.inD,player.passing,player.control,player.pot]
            for b in range(0,11):
                attrList.append(Text(Point(boxes[num].getCenter().x,boxes[num].getCenter().y - 90 + b * 15 ),""))
                attrList[b].setSize(10)
                attrList[b].draw(win)
            attrList[0].setText(headers[0] + ": " + str(attributes[0]))
            attrList[0].setStyle("bold")
            costCalc = 0
            for b in range(1,9):
                attrGrade = grade(attributes[b])
                attrList[b].setText(headers[b] + ": " + attrGrade)
                if attrGrade == "A":
                    val = 75
                elif attrGrade == "B":
                    val = 50
                elif attrGrade == "C":
                    val = 25
                elif attrGrade == "D":
                    val = 15
                else:
                    val = 5

                if player.pos == "G":
                    if b == 1:
                        val = val * 3
                    elif b == 4:
                        val = val * 3
                    elif b == 6:
                        val = val * 2
                    elif b == 7:
                        val = val * 2

                elif player.pos == "F":
                    if b == 1:
                        val = val * 2
                    elif b == 2:
                        val = val * 2
                    elif b == 3:
                        val = val * 3
                    elif b == 5:
                        val = val * 2

                elif player.pos == "C":
                    if b == 2:
                        val = val * 3
                    elif b == 3:
                        val = val * 3
                    elif b == 5:
                        val = val * 3
                costCalc += val
            player.cost = round(costCalc * 0.8)
            attrList[10].setText(headers[9] + ": " + str(player.cost))
            num += 1
            graphicsList.extend(attrList)
    
    graphicsList.extend(boxes)
    recruitsBox = Rectangle(Point(300,0),Point(1000,600))
    recruitList = []
    recruitingPoints = round(400 + 800 * team.prestige / 100) + (100 * (12 - len(team.roster)))
    pointsText = Text(Point(150,30),"")
    pointsText.draw(win)
    graphicsList.append(pointsText)
    pointsText.setText("Points remaining: " + str(recruitingPoints) + "/" + str(recruitingPoints))
    availPoints = copy.copy(recruitingPoints)

    

    
    currentRoster = []
    for i in range(0,len(team.roster)):
        currentRoster.append(Text(Point(150,200 + 15 * i),""))
        currentRoster[i].setSize(10)
        currentRoster[i].setText(team.roster[i].name + " " + team.roster[i].pos + " " + str(team.roster[i].ovr) + " Upcoming Year: " + str(team.roster[i].year))
        currentRoster[i].draw(win)

    graphicsList.extend(currentRoster)
    confirmBox = Rectangle(Point(100,500),Point(200,550))
    confirmBox.draw(win)
    confirmText = Text(confirmBox.getCenter(),"Confirm")
    confirmText.draw(win)

    graphicsList.append(confirmText)
    graphicsList.append(confirmBox)

    while True:
        mouse = win.getMouse()
        if inside(recruitsBox,mouse):
            for i in range(0,21):
                if inside(boxes[i],mouse):
                    if recruitablePlayers[i] not in recruitList:
                        boxes[i].setFill("green yellow")
                        recruitList.append(recruitablePlayers[i])
                        availPoints -= recruitablePlayers[i].cost
                        pointsText.setText("Points remaining: " + str(availPoints) + "/" + str(recruitingPoints))
                    else:
                        boxes[i].setFill("burlywood1")
                        recruitList.remove(recruitablePlayers[i])
                        availPoints += recruitablePlayers[i].cost
                        pointsText.setText("Points remaining: " + str(availPoints) + "/" + str(recruitingPoints))
        elif inside(confirmBox,mouse) and availPoints >= 0:
            team.roster.extend(recruitList)
            break

    for item in graphicsList:
        item.undraw()

    
    # Acceptable combinations of players:
    # two guards, two forwards
    # two guards, a forward, a center
    # three guards, a forward
    # three guards, a center

    team.roster = fixRoster(team.roster,win,firstNames,lastNames)

def playerProgression(conferenceList):
    for conference in conferenceList:
        for team in conference:
            for player in team.roster:
                if player.year > 1:
                    progression = round(player.pot / 20)
                else:
                    progression = 0

                if player.pos == "G":
                    rebV = 0.1
                    thrPtV = 0.2
                    insV = 0.10
                    perDV = 0.17
                    inDV = 0.07
                    passingV = 0.19
                    controlV = 0.17

                    thrMod = 1
                    rebMod = -2
                    insMod = 0
                    perDMod = 0
                    inDMod = -2
                    passMod = 1
                    contMod = 0
                    
                elif player.pos == "F":
                    rebV = 0.16
                    thrPtV = 0.13
                    insV = 0.18
                    perDV = 0.16
                    inDV = 0.15
                    passingV = 0.12
                    controlV = 0.10

                    thrMod = 0
                    rebMod = 0
                    insMod = 0
                    perDMod = 0
                    inDMod = 0
                    passMod = -1
                    contMod = -1
                    
                else:
                    rebV = 0.24
                    thrPtV = 0.05
                    insV = 0.26
                    perDV = 0.1
                    inDV = 0.23
                    passingV = 0.05
                    controlV = 0.07

                    thrMod = -1
                    rebMod = 1
                    insMod = 0
                    perDMod = -1
                    inDMod = 1
                    passMod = -2
                    contMod = 0

                modList = [1,1,1,1,1,1,1]
                n = 0
                for mod in [thrMod,rebMod,insMod,perDMod,inDMod,passMod,contMod]:
                    difference = progression * 2 + mod
                    if difference <= 0 or progression == 0:
                        mod = 1
                        modList[n] = 0
                    n += 1    
                        
                if player.year > 1 and progression > 0:
                    player.thrPt += random.randint(0,2*progression+thrMod) * modList[0]
                    player.reb += random.randint(0,2*progression+rebMod) * modList[1]
                    player.ins += random.randint(0,2*progression+insMod)* modList[2]
                    player.perD += random.randint(0,2*progression+perDMod)* modList[3]
                    player.inD += random.randint(0,2*progression+inDMod)* modList[4]
                    player.passing += random.randint(0,2*progression+passMod)* modList[5]
                    player.control += random.randint(0,2*progression+contMod)* modList[6]
                
                player.ovr = round(player.thrPt * thrPtV + player.reb * rebV + player.ins * insV + player.perD * perDV + player.inD
                                   * inDV + player.passing * passingV + player.control * controlV)
def selectSystem(playerTeam,win):
    graphicsList = []
    coverBox = Rectangle(Point(0,0),Point(1000,600))
    coverBox.setFill("burlywood1")
    coverBox.draw(win)
    longRange = System(15,0,0,0,0,1,0,0,0,0,"Long Range")
    standard = System(0,0,0,0,0,1,0,0,0,0,"Standard")
    interior = System(-15,0,0,0,0,1,0,0,0,0,"Interior")
    PTS = System(0,5,0,0,0,1,0,0,-2,-3,"Play Through Star")
    defense = System(0,0,0,2,20,1.5,-4,-6,0,0,"Defense-Centric")
    systemList = [longRange,standard,interior,PTS,defense]
    systemTitle = Text(Point(500,30),("Selected System: " + playerTeam.system.name))
    systemTitle.setSize(15)
    graphicsList.append(systemTitle)
    buttonList = []
    systemDesc = Text(Point(500,100),"")
    graphicsList.append(systemDesc)
    systemDescList = ["Your team will shoot a lot more threes. Bad for teams with poor shooters.",
                      "The standard system, no modifiers to basic game simulation.",
                      "Your team will shoot far fewer threes. Bad for shooters, good if your team chucks it more than they should.",
                      "Your star player will get more opportunities per game at the cost of opportunities for your other starters \n and reduced efficiency from the star themselves.",
                      "Your team will play with an emphasis on defense at the cost of some offensive efficiency. \n Has increasing returns for good defensive teams, and may actually hurt bad defensive teams."]
    for item in systemList:
        if item.name == playerTeam.system.name:
            playerTeam.system = item
            break
    systemDesc.setText(systemDescList[systemList.index(playerTeam.system)])
    
    for i in range(0,5):
        buttonList.append(Rectangle(Point(25+200*i,300),Point(175+200*i,340)))
        graphicsList.append(Text(buttonList[i].getCenter(),systemList[i].name))

    graphicsList.extend(buttonList)
    backBox = Rectangle(Point(450,550),Point(550,580))
    backText = Text(backBox.getCenter(),"Back")
    graphicsList.append(backBox)
    graphicsList.append(backText)

    for item in graphicsList:
        item.draw(win)

    graphicsList.append(coverBox)
    while True:
        mouse = win.getMouse()
        if inside(backBox,mouse):
            for item in graphicsList:
                item.undraw()
            return
        for i in range(0,5):
            if inside(buttonList[i],mouse):
                playerTeam.system = systemList[i]
                systemTitle.setText("Selected System: " + playerTeam.system.name)
                systemDesc.setText(systemDescList[i])
                break
        
def teamRecords(playerTeam,win):
    coverBox = Rectangle(Point(0,0),Point(1000,600))
    coverBox.setFill("burlywood1")
    coverBox.draw(win)
    graphicsList = []
    # 8 different records, 125 wide each maybe 75 tall?
    title = Text(Point(500,30),"Team Records: Game")
    title.setSize(15)
    graphicsList.append(title)
    records = playerTeam.gameRecords
    recordsList = [records.pts,records.reb,records.asst,records.fgM,records.thrM,
                   records.blck,records.stl,records.to]
    srecords = playerTeam.seasonRecords
    srecordsList = [srecords.pts,srecords.reb,srecords.asst,srecords.fgM,srecords.thrM,
                   srecords.blck,srecords.stl,srecords.to]
    recordsNameList = ["Points","Rebounds","Assists","FG Made","3pt Made","Blocks","Steals","Turnovers"]
    for i in range(0,8):
        header = Text(Point(62.5+125*i,85),recordsNameList[i])
        header.setSize(10)
        graphicsList.append(header)
        for n in range(0,5):
            box = Rectangle(Point(0+125*i,100+50*n),Point(125+125*i,150+50*n))
            if recordsList[i][n][0] > 0:
                boxText = Text(box.getCenter(),(str(n+1) + ". " + recordsList[i][n][1] + ":\n" + str(recordsList[i][n][0])))
                boxText.setSize(9)
                graphicsList.append(boxText)
            graphicsList.append(box)
        box = Rectangle(Point(0+125*i,450),Point(125+125*i,500))
        header2 = Text(Point(62.5+125*i,435),recordsNameList[i])
        header2.setSize(10)
        graphicsList.append(header2)
        graphicsList.append(box)
        if srecordsList[i][0][0] > 0:
            boxText = Text(box.getCenter(),(srecordsList[i][0][1] + ":\n" + str(srecordsList[i][0][0])))
            boxText.setSize(9)
            graphicsList.append(boxText)

    title2 = Text(Point(500,380),"Team Records: Season")
    title2.setSize(15)
    graphicsList.append(title2)

    backBox = Rectangle(Point(412.5,540),Point(587.5,570))
    backText = Text(backBox.getCenter(),"Back")
    graphicsList.append(backBox)
    graphicsList.append(backText)

    for item in graphicsList:
        item.draw(win)

    while True:
        mouse = win.getMouse()
        if inside(backBox,mouse):
            for item in graphicsList:
                item.undraw()
            coverBox.undraw()
            return
def awards(conferenceList,playerConference,playerTeam,win,finalBool,awardsList):
    if finalBool == False:
        awardsList.sort(key = lambda x: (x.clout, x.ovr), reverse = True)
        for player in awardsList:
            player.finalClout = player.clout
    coverBox = Rectangle(Point(0,0),Point(1000,600))
    coverBox.setFill("burlywood1")
    coverBox.draw(win)
    top5 = awardsList[0:5]
    n = 0
    confTop5 = []
    for player in awardsList:
        if player.team.conf == playerTeam.conf:
            confTop5.append(player)
            n += 1
        if n == 5:
            break

    expStGra = []
    rosterText = []
    rosterBox = []
    rosterBoxHeader = []
    rBoxHeadText = []

    headerBox2 = Rectangle(Point(30,50),Point(150,70))
    rosterBoxHeader.append(headerBox2)
    
    
    testText = Text(headerBox2.getCenter(),"Player Name")
    rBoxHeadText.append(testText)
    
    title = Text(Point(500,30),"Player of the Year")
    title.draw(win)
    expStGra.append(title)
    
    n = 0
    shortHead = ["Pos","Ovr","Pts","Reb","Asst","FGM","FGA","FG%",
                 "3PM","3PA","3P%","Blck","Stl","TO","Votes"]
    
    while n < 15:
        rosterBoxHeader.append(Rectangle(Point(150+45*n,50),Point(195+45*n,70)))
        rBoxHeadText.append(Text(rosterBoxHeader[n+1].getCenter(),shortHead[n]))
        n+=1
    
    for i in range(0,6):
        newBox = Rectangle(Point(825,50+20*i),Point(975,70+20*i))
        if i - 1 < 0:
            newText = Text(newBox.getCenter(),"Team")
        else:
            newText = Text(newBox.getCenter(),top5[i-1].team.name)
        newText.setSize(10)
        newBox.draw(win)
        newText.draw(win)
        expStGra.append(newText)
        expStGra.append(newBox)
    n = 0
    for item in rosterBoxHeader:
        item.draw(win)
        rBoxHeadText[n].setSize(10)
        rBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < 5:
        rosterText.append([])
        rosterBox.append([])
        i = 0
        for item in rosterBoxHeader:
            rosterBox[n].append(item.clone())
            rosterBox[n][i].move(0,20*(n+1))
            rosterText[n].append(Text(rosterBox[n][i].getCenter(),""))
            rosterText[n][i].setSize(10)
            rosterBox[n][i].draw(win)
            rosterText[n][i].draw(win)
            i += 1
        n += 1
    n = 0
    while n < 5:
        if top5[n].stats.gp == 0:
            m = 1
        else:
            m = top5[n].stats.gp
        rosterText[n][0].setText(top5[n].name)
        rosterText[n][1].setText(top5[n].pos)
        rosterText[n][2].setText(top5[n].ovr)
        rosterText[n][3].setText(round(top5[n].stats.pts/m,1))
        rosterText[n][4].setText(round(top5[n].stats.reb/m,1))
        rosterText[n][5].setText(round(top5[n].stats.asst/m,1))
        rosterText[n][6].setText(round(top5[n].stats.fgM/m,1))
        rosterText[n][7].setText(round(top5[n].stats.fgA/m,1))
        if top5[n].stats.fgA > 0:
            top5[n].stats.fgPr = round(top5[n].stats.fgM / top5[n].stats.fgA,3)
        rosterText[n][8].setText(top5[n].stats.fgPr)
        rosterText[n][9].setText(round(top5[n].stats.thrM/m,1))
        rosterText[n][10].setText(round(top5[n].stats.thrA/m,1))
        if top5[n].stats.thrA > 0:
            top5[n].stats.thrPr = round(top5[n].stats.thrM / top5[n].stats.thrA,3)
        rosterText[n][11].setText(top5[n].stats.thrPr)
        rosterText[n][12].setText(round(top5[n].stats.blck/m,1))
        rosterText[n][13].setText(round(top5[n].stats.stl/m,1))
        rosterText[n][14].setText(round(top5[n].stats.to/m,1))
        rosterText[n][15].setText(round(top5[n].finalClout))
        n += 1

    expStGra.extend(rosterBoxHeader)
    expStGra.extend(rBoxHeadText)
    for item in rosterBox:
        expStGra.extend(item)
    for item in rosterText:
        expStGra.extend(item)

    backBox = Rectangle(Point(450,500),Point(550,530))
    backBox.draw(win)
    backText = Text(backBox.getCenter(),"Back")
    backText.setSize(10)
    backText.draw(win)
    expStGra.append(backBox)
    expStGra.append(backText)


    cRosterText = []
    cRosterBox = []
    cRosterBoxHeader = []
    crBoxHeadText = []

    cheaderBox2 = Rectangle(Point(30,300),Point(150,320))
    cRosterBoxHeader.append(cheaderBox2)
    
    
    ctestText = Text(cheaderBox2.getCenter(),"Player Name")
    crBoxHeadText.append(ctestText)
    
    ctitle = Text(Point(500,270),(playerTeam.conf + " Player of the Year"))
    ctitle.draw(win)
    expStGra.append(ctitle)
    
    n = 0
    
    while n < 15:
        cRosterBoxHeader.append(Rectangle(Point(150+45*n,300),Point(195+45*n,320)))
        crBoxHeadText.append(Text(cRosterBoxHeader[n+1].getCenter(),shortHead[n]))
        n+=1
    for i in range(0,6):
        newBox = Rectangle(Point(825,300+20*i),Point(975,320+20*i))
        if i - 1 < 0:
            newText = Text(newBox.getCenter(),"Team")
        else:
            newText = Text(newBox.getCenter(),confTop5[i-1].team.name)
        newText.setSize(10)
        newBox.draw(win)
        newText.draw(win)
        expStGra.append(newText)
        expStGra.append(newBox)
    n = 0
    for item in cRosterBoxHeader:
        item.draw(win)
        crBoxHeadText[n].setSize(10)
        crBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < 5:
        cRosterText.append([])
        cRosterBox.append([])
        i = 0
        for item in cRosterBoxHeader:
            cRosterBox[n].append(item.clone())
            cRosterBox[n][i].move(0,20*(n+1))
            cRosterText[n].append(Text(cRosterBox[n][i].getCenter(),""))
            cRosterText[n][i].setSize(10)
            cRosterBox[n][i].draw(win)
            cRosterText[n][i].draw(win)
            i += 1
        n += 1
    n = 0
    while n < 5:
        if confTop5[n].stats.gp == 0:
            m = 1
        else:
            m = confTop5[n].stats.gp
        cRosterText[n][0].setText(confTop5[n].name)
        cRosterText[n][1].setText(confTop5[n].pos)
        cRosterText[n][2].setText(confTop5[n].ovr)
        cRosterText[n][3].setText(round(confTop5[n].stats.pts/m,1))
        cRosterText[n][4].setText(round(confTop5[n].stats.reb/m,1))
        cRosterText[n][5].setText(round(confTop5[n].stats.asst/m,1))
        cRosterText[n][6].setText(round(confTop5[n].stats.fgM/m,1))
        cRosterText[n][7].setText(round(confTop5[n].stats.fgA/m,1))
        if confTop5[n].stats.fgA > 0:
            confTop5[n].stats.fgPr = round(confTop5[n].stats.fgM / confTop5[n].stats.fgA,3)
        cRosterText[n][8].setText(confTop5[n].stats.fgPr)
        cRosterText[n][9].setText(round(confTop5[n].stats.thrM/m,1))
        cRosterText[n][10].setText(round(confTop5[n].stats.thrA/m,1))
        if confTop5[n].stats.thrA > 0:
            confTop5[n].stats.thrPr = round(confTop5[n].stats.thrM / confTop5[n].stats.thrA,3)
        cRosterText[n][11].setText(confTop5[n].stats.thrPr)
        cRosterText[n][12].setText(round(confTop5[n].stats.blck/m,1))
        cRosterText[n][13].setText(round(confTop5[n].stats.stl/m,1))
        cRosterText[n][14].setText(round(confTop5[n].stats.to/m,1))
        cRosterText[n][15].setText(round(confTop5[n].finalClout))
        n += 1

    expStGra.extend(cRosterBoxHeader)
    expStGra.extend(crBoxHeadText)
    for item in cRosterBox:
        expStGra.extend(item)
    for item in cRosterText:
        expStGra.extend(item)
    
    while True:
        mouse = win.getMouse()
        if inside(backBox,mouse):
            for item in expStGra:
                item.undraw()
            coverBox.undraw()
            break
    
def showHistory(playerTeam,win):
    coverBox = Rectangle(Point(0,0),Point(1000,600))
    coverBox.setFill("burlywood1")
    coverBox.draw(win)
    graphicsList = []
    title = Text(Point(500,30),"Team History")
    graphicsList.append(title)
    pageList = [[]]
    onePage = len(playerTeam.history)
    previousBox = Rectangle(Point(10,550),Point(110,590))
    previousText = Text(previousBox.getCenter(),"Previous")
    graphicsList.append(previousBox)
    graphicsList.append(previousText)
    nextBox = previousBox.clone()
    nextBox.move(880,0)
    nextText = Text(nextBox.getCenter(),"Next")
    graphicsList.append(nextBox)
    graphicsList.append(nextText)
    backBox = previousBox.clone()
    backBox.move(440,0)
    backText = Text(backBox.getCenter(),"Exit")
    graphicsList.append(backBox)
    graphicsList.append(backText)

    for item in graphicsList:
        item.draw(win)
    
    x = 30 #Change this for size
    while True:
        if onePage - x > 0:
            pageList.append([])
            onePage -= x
        else:
            break
    team = playerTeam
    f = 0
    for i in range(0,len(pageList)):
        for m in range(0,3):
            for n in range(0,10):
                if f < len(playerTeam.history):
                    box = Rectangle(Point(0+n*100,50+150*m),Point(100+100*n,200+150*m))
                    if team.history[f].confFinish == 0:
                        confF = "Won " + playerTeam.conf
                    elif team.history[f].confFinish == 1:
                        confF = "2nd in " + playerTeam.conf
                    elif team.history[f].confFinish == 2:
                        confF = "3rd in " + playerTeam.conf
                    else:
                        confF = str(team.history[f].confFinish + 1) + "th in " + playerTeam.conf
                    text = str("Year " + str(team.history[f].year+1) + "\n" +
                               "Record: " + team.history[f].record + "\n" +
                               str(team.history[f].prestige) + " prestige\n" +
                               confF + "\n" +
                               str(team.history[f].seed) + " seed\n" +
                               team.history[f].tourneyExit)           
                    boxText = Text(box.getCenter(),text)
                    boxText.setSize(8)
                    pageList[i].append(box)
                    pageList[i].append(boxText)
                f += 1
    p = 0
    for item in pageList[p]:
        item.draw(win)
    while True:
        mouse = win.getMouse()
        if inside(previousBox,mouse):
            for item in pageList[p]:
                item.undraw()
            p = (p-1)%len(pageList)
            for item in pageList[p]:
                item.draw(win)
        elif inside(nextBox,mouse):
            for item in pageList[p]:
                item.undraw()
            p = (p+1)%len(pageList)
            for item in pageList[p]:
                item.draw(win)
        elif inside(backBox,mouse):
            for item in pageList[p]:
                item.undraw()
            for item in graphicsList:
                item.undraw()
            coverBox.undraw()
            return

def simThru(conferenceList,week,win,playerTeam,awardsBox,awardsText,oppRosterText,oppCorner,otherGames,weekText,
            playerConference,standingsText,standings,simThruBox):
    while week < 30:
        mouse = win.checkMouse()
        if mouse != None and inside(simThruBox,mouse):
            return (False,week)
        oppTeam = playerTeam.schedule[week]
        if week == 14: 
            awardsBox.draw(win)
            awardsText.draw(win)
        n = 0
        while n < 12:
            oppRosterText[n][0].setText(oppTeam.roster[n].name)
            oppRosterText[n][1].setText(oppTeam.roster[n].pos)
            oppRosterText[n][2].setText(oppTeam.roster[n].ovr)
            oppRosterText[n][3].setText(oppTeam.roster[n].year)
            n += 1
        oppCorner.setText(oppTeam.name + ", OVR: " + str(oppTeam.ovr))
        represented = []
        weekText.setText("Week " + str(week+1))
        havePlayed = []
        for conference in conferenceList:
            for team in conference:
                if team not in havePlayed:
                    simGame(team,team.schedule[week],playerTeam)
                    havePlayed.append(team)
                    havePlayed.append(team.schedule[week])
        represented = []
        
        n = 0
        for team in playerConference:
            if team not in represented:
                represented.append(team)
                represented.append(team.schedule[week])
                otherGames[n].setText(str(team.name + " " + str(team.gamePoints) + " " + team.schedule[week].name +
                                          " " + str(team.schedule[week].gamePoints)))
                n+=1
        if week > 8:
            for i in range(0,len(otherGames)):
                if i >= len(playerConference) / 2:
                    otherGames[i].setText("")
                
        for item in playerConference:
            if item.confWins > 0:
                item.confPct = item.confWins / (item.confWins+item.confLosses)
            item.wins = freq(item.record,1)
        confStandings = sorted(playerConference,key= lambda x: (x.confPct,x.confWins,x.wins),reverse = True)
        
        n = 0
        for item in confStandings:
            standings[n].setText(str(str(n+1) + ". " + item.name + " (" + str(item.confWins) + "-" + str(item.confLosses) + ") " + str(item.wins) + "-" + str(week-item.wins+1)))
            n += 1
        if week == 0:
            standingsText.setText("Conference Standings: (Conf Record) Overall Record")
        week += 1
    
    return (True,week)

def saveScreen(win):
    graphicsList = []
    title = Text(Point(500,30),"Select Save File")
    graphicsList.append(title)
    saveBox = []
    deleteBox = []
    deleteTextList = []
    for i in range(0,3):
        saveBox.append(Rectangle(Point(250,100+150*i),Point(650,200+150*i)))
        deleteBox.append(Rectangle(Point(650,100+150*i),Point(750,200+150*i)))
        deleteBox[i].setOutline("red")
        deleteText = Text(deleteBox[i].getCenter(),"Delete Save")
        deleteText.setSize(10)
        deleteText.setTextColor("red")
        deleteTextList.append(deleteText)
        graphicsList.append(deleteText)
        graphicsList.append(Text(saveBox[i].getCenter(),("Save " + str(i+1))))
    graphicsList.extend(saveBox)
    graphicsList.extend(deleteBox)
    quitBox = Rectangle(Point(450,530),Point(550,560))
    quitText = Text(quitBox.getCenter(),"Quit")

    graphicsList.append(quitBox)
    graphicsList.append(quitText)
    
    for item in graphicsList:
        item.draw(win)

    saveList = ["save1","save2","save3"]

    
    validMouse = False
    while validMouse == False:
        mouse = win.getMouse()
        for i in range(0,3):
            if inside(saveBox[i],mouse):
                fileName = saveList[i]
                validMouse = True
                break
            if inside(deleteBox[i],mouse):
                deleteTextList[i].setText("Confirm Delete?")
                mouse2 = win.getMouse()
                if inside(deleteBox[i],mouse2):
                    saveFile = shelve.open(saveList[i],flag = 'n')
                    saveFile['newFile'] = True
##                    del saveFile['playerTeam']
##                    del saveFile['year'] #= 0
##                    del saveFile['conferenceList'] #= []
##                    del saveFile['playerConference']# = []
                    saveFile.close()
                    deleteTextList[i].setText("Save Deleted")
                else:
                    deleteTextList[i].setText("Delete Save")
        if inside(quitBox,mouse):
            win.close()
            sys.exit()
    for item in graphicsList:
        item.undraw()

    return fileName
def instructions(win):
    coverBox = Rectangle(Point(0,0),Point(1000,600))
    coverBox.setFill("burlywood1")
    coverBox.draw(win)
    instr = Text(Point(500,300),"")
    instr.setText("Most of the gameplay is fairly intuitive in my opinion, so these are just a few pointers on the less intuitive gameplay mechanics.\n" +
                  "\n" +
                  "Roster adjustments: you can adjust your roster from the main screen by clicking on the names of two players whose roster positions \n" +
                  "you'd like to swap in succession, provided their positions meet the position requirements of the roster slots they are being\n" +
                  "swapped into (a starting lineup must be comprised of 2 G, 1 G/F, 1 C/F, and 1 flex position in which any positional player can be\n" +
                  "placed). The bench can be entirely flex players, but it is important to find balance to achieve success\n" +
                  'Star player: any of the five starters in your lineup may be designated as the "Star Player" of your team by clicking the empty box\n' +
                  'in the column next to their name, which will move the yellow "Star" designator to that position.\n' +
                  "A team's star player will play 36 minutes per game, other starters will play 28 mpg, the bench will play 13 mpg and reserves will play no minutes.\n \n" +
                  "Prestige vs. OVR: prestige (listed at the top of the main screen) is a measurement of cumulative team performance through the years\n" +
                  "and is gained by outperforming expectations and lost by falling short of them. Expectations are higher for teams of higher prestige\n" +
                  "particularly if they are higher comparatively than the rest of their conference."+ "\n OVR is a cumulative team rating for the current season based on roster composition.\n" +
                  "\n"+"Recruiting: each year based on team prestige and the number of players leaving, you get a certain number of recruiting points to   \n" +
                  "spend on recruits. These recruits' attribute ratings have been obfuscated into letter grades based on what range that rating is in.\n" +
                  "Recruiting points don't carry over from year to year, and player cost is calculated based on the grade and not the actual value of \n" +
                  "the players ratings, so it is possible to get a better player than what you paid for. There will always be at least 4 walk-ons\n"+
                  "and the number of walk-ons will always be generated to fill the roster to at least 16 players, at which point the game will prompt\n" +
                  "you to remove players from your roster to get down to 12 players, after which all non-freshmen will go through player progression\n" +
                  "\n" +
                  "Saving: The game auto saves at the beginning of every season.\n \n" + "Click anywhere to back out.")
    instr.setSize(11)
    instr.draw(win)
    win.getMouse()
    instr.undraw()
    coverBox.undraw()

def quitScreen(win):
    coverBox = Rectangle(Point(0,0),Point(1000,600))
    coverBox.setFill("burlywood1")
    graphicsList = []
    coverBox.draw(win)

    quitText = Text(Point(500,200),"Are you sure you want to quit? \n Progress is only saved at the beginning of a new season.")
    yesBox = Rectangle(Point(250,400),Point(400,440))
    yesText = Text(yesBox.getCenter(),"Yes")
    noBox = yesBox.clone()
    noBox.move(350,0)
    noText = Text(noBox.getCenter(),"No")
    graphicsList.extend([quitText,yesBox,yesText,noBox,noText])

    for item in graphicsList:
        item.draw(win)

    while True:
        mouse = win.getMouse()
        if inside(noBox,mouse):
            break
        elif inside(yesBox,mouse):
            win.close()
            sys.exit()

    for item in graphicsList:
        item.undraw()
    coverBox.undraw()
    
def main():
    sys.setrecursionlimit(100000)
    win = GraphWin("NCAA Coach", 1000, 600)
    win.setBackground("burlywood1")

    ball = Image(Point(500,340),"Basketball.png")
    ball.draw(win)
    title = Text(Point(500,30),"College Basketball Coach")
    title.setSize(20)
    title.setFace("times roman")
    subtitle = Text(Point(500,60),"a game by Noah Kuperberg")
    subtitle.draw(win)
    title.draw(win)
    clickText = Text(Point(900,580),"Click anywhere to continue")
    clickText.setSize(10)
    clickText.draw(win)
    
    
    win.getMouse()
    ball.undraw()
    title.undraw()
    subtitle.undraw()
    clickText.undraw()
    
    # Team Disribution
    f = open("teams.txt","r")
    n = 0
    num = 0
    currentConference = "AEC"
    conferenceList = [[]]
    while n < 350:
        teamName = f.readline().strip()
        teamPrestige = int(f.readline().strip())
        teamConference = f.readline().strip()
        f.readline()
        sampleTeam = Team(teamName,teamPrestige,teamConference,[],0)
        if teamConference != currentConference:
            conferenceList.append([])
            num += 1
            currentConference = teamConference
        conferenceList[num].append(sampleTeam)
        n+=1
    f.close()

    f = open("firstNames.txt","r")
    firstNames = []
    n = 0
    while n < 1006:
        firstNames.append(f.readline().strip())
        n += 1
    f.close()
    f = open("lastNames.txt","r")
    lastNames = []
    n = 0
    while n < 1002:
        lastNames.append(f.readline().strip())
        n+=1
    f.close()


    # Player Generation/Assignment
    for item in conferenceList:
        for team in item:
            n = 0
            samplePlayer = bias(team.prestige,"G",firstNames,lastNames,random.randint(1,4))
            team.roster.append(samplePlayer)
            samplePlayer = bias(team.prestige,"G",firstNames,lastNames,random.randint(1,4))
            team.roster.append(samplePlayer)
            samplePlayer = bias(team.prestige,"F",firstNames,lastNames,random.randint(1,4))
            team.roster.append(samplePlayer)
            samplePlayer = bias(team.prestige,"C",firstNames,lastNames,random.randint(1,4))
            team.roster.append(samplePlayer)
            while n < 8:
                samplePlayer = bias(team.prestige,"",firstNames,lastNames,random.randint(1,4))
                team.roster.append(samplePlayer)
                n += 1

    for item in conferenceList:
        for team in item:
            sortRoster = sorted(team.roster,key=operator.attrgetter('ovr'),reverse = True)
            team.roster.clear()
            n = 0
            i = 0
            while n < 2:
                if sortRoster[i].pos == "G":
                    n += 1
                    team.roster.append(sortRoster.pop(i))
                    i -= 1
                i += 1
            i = 0
            forward = False
            while forward == False:
                if sortRoster[i].pos == "G" or sortRoster[i].pos == "F":
                    forward = True
                    team.roster.append(sortRoster.pop(i))
                i += 1
            i = 0
            center = False
            while center == False:
                if sortRoster[i].pos == "F" or sortRoster[i].pos == "C":
                    center = True
                    team.roster.append(sortRoster.pop(i))
                i += 1
            team.roster.extend(sortRoster)
            team.starSlot = team.roster.index(max(team.roster,key=operator.attrgetter('ovr')))
                

    
    # FIRST YEAR
    # TEAM SELECTION

    year = 0
    
    # Load in save file here
    saveFileName = saveScreen(win)
    saveFile = shelve.open(saveFileName)
    
    newFile = saveFile['newFile']
    if newFile == True:
        playerTeam = conferenceSelect(conferenceList, win)
        saveFile['newFile'] = False
        
    elif newFile == False:
        playerTeam = saveFile['playerTeam']
        year = saveFile['year']
        conferenceList = saveFile['conferenceList']
        #playerConference = saveFile['playerConference']

    saveFile.close()
    
    
    playBox = Rectangle(Point(155,325),Point(265,355))
    playBox.draw(win)
    playText = Text(playBox.getCenter(),"Play Game")
    playText.setSize(10)
    playText.draw(win)

    quitBox = Rectangle(Point(900,555),Point(975,585))
    quitBox.setOutline("red")
    quitText = Text(quitBox.getCenter(),"Quit")
    quitText.setSize(10)
    quitText.setTextColor("red")
    quitBox.draw(win)
    quitText.draw(win)

    
    depthChartText = ["G", "G","G/F","F/C","Flex","Bench","Bench","Bench","Bench","Res.","Res.","Res."]

    rosterText = []
    rosterBox = []
    rosterBoxHeader = []
    rBoxHeadText = []

    headerBox1 = Rectangle(Point(30,50),Point(70,70))
    rosterBoxHeader.append(headerBox1)
    headerBox2 = Rectangle(Point(70,50),Point(195,70))
    rosterBoxHeader.append(headerBox2)
    
    testText = Text(headerBox2.getCenter(),"Player Name")
    testText2 = Text(headerBox1.getCenter(),"Depth")
    rBoxHeadText.append(testText2)
    rBoxHeadText.append(testText)
    n = 0
    shortHead = ["Pos","Ovr","Yr"]
    
    while n < 3:
        rosterBoxHeader.append(Rectangle(Point(195+30*n,50),Point(225+30*n,70)))
        rBoxHeadText.append(Text(rosterBoxHeader[n+2].getCenter(),shortHead[n]))
        n+=1
    
    n = 1
    while n < 13:
        rosterBoxHeader.append(rosterBoxHeader[0].clone())
        rosterBoxHeader[n+4].move(0,20*n)
        rBoxHeadText.append(Text(rosterBoxHeader[n+4].getCenter(),depthChartText[n-1]))
        n += 1

    n = 0
    for item in rosterBoxHeader:
        item.draw(win)
        rBoxHeadText[n].setSize(10)
        rBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < 12:
        rosterText.append([])
        rosterBox.append([])
        i = 0
        for item in rosterBoxHeader[1:5]:
            rosterBox[n].append(item.clone())
            rosterBox[n][i].move(0,20*(n+1))
            rosterText[n].append(Text(rosterBox[n][i].getCenter(),""))
            rosterText[n][i].setSize(10)
            rosterBox[n][i].draw(win)
            rosterText[n][i].draw(win)
            i += 1
        n += 1

    oppRosterText = []
    oppRosterBox = []
    oppRosterBoxHeader = []
    oRBoxHeadText = []

    oppHeaderBox1 = Rectangle(Point(700,50),Point(740,70))
    oppRosterBoxHeader.append(oppHeaderBox1)
    oppHeaderBox2 = Rectangle(Point(740,50),Point(195+670,70))
    oppRosterBoxHeader.append(oppHeaderBox2)
    
    oppTestText = Text(oppHeaderBox2.getCenter(),"Player Name")
    oppTestText2 = Text(oppHeaderBox1.getCenter(),"Depth")
    oRBoxHeadText.append(oppTestText2)
    oRBoxHeadText.append(oppTestText)
    n = 0
    
    while n < 3:
        oppRosterBoxHeader.append(Rectangle(Point(195+670+30*n,50),Point(225+670+30*n,70)))
        oRBoxHeadText.append(Text(oppRosterBoxHeader[n+2].getCenter(),shortHead[n]))
        n+=1
    
    n = 1
    while n < 13:
        oppRosterBoxHeader.append(oppRosterBoxHeader[0].clone())
        oppRosterBoxHeader[n+4].move(0,20*n)
        oRBoxHeadText.append(Text(oppRosterBoxHeader[n+4].getCenter(),depthChartText[n-1]))
        n += 1

    n = 0
    for item in oppRosterBoxHeader:
        item.draw(win)
        oRBoxHeadText[n].setSize(10)
        oRBoxHeadText[n].draw(win)
        n += 1
    n = 0
    num = 0
    while n < 12:
        oppRosterText.append([])
        oppRosterBox.append([])
        i = 0
        for item in oppRosterBoxHeader[1:5]:
            oppRosterBox[n].append(item.clone())
            oppRosterBox[n][i].move(0,20*(n+1))
            oppRosterText[n].append(Text(oppRosterBox[n][i].getCenter(),""))
            oppRosterText[n][i].setSize(10)
            oppRosterBox[n][i].draw(win)
            oppRosterText[n][i].draw(win)
            i += 1
        n += 1

    
    upperCorner = Text(Point(150,30),"")
    upperCorner.draw(win)
    oppCorner = Text(Point(150+680,30),"")
    oppCorner.draw(win)

    otherGames = []
    n = 0
    while n < 32:
        otherGames.append(Text(Point(500,70+n*15),""))
        otherGames[n].setSize(10)
        otherGames[n].draw(win)
        n += 1
    weekText = Text(Point(500,50),"")
    weekText.draw(win)

    standings = []
    n = 0
    while n < 15:
        standings.append(Text(Point(500,350+n*15),""))
        standings[n].setSize(10)
        standings[n].draw(win)
        n += 1
    standingsText = Text(Point(500,330),"")
    standingsText.draw(win)

    statsBox = Rectangle(Point(155,360),Point(265,390))
    statsBox.draw(win)
    statsBoxText = Text(statsBox.getCenter(),"Stats")
    statsBoxText.setSize(10)
    statsBoxText.draw(win)

    oppStatsBox = Rectangle(Point(782,320),Point(892,350))
    oppStatsBox.draw(win)
    oppStatsBoxText = Text(oppStatsBox.getCenter(),"Opponent Stats")
    oppStatsBoxText.setSize(10)
    oppStatsBoxText.draw(win)

    expandBox = Rectangle(Point(50,325),Point(150,355))
    expandBox.draw(win)
    expandText = Text(expandBox.getCenter(),"Expand")
    expandText.setSize(10)
    expandText.draw(win)

    scheduleBox = Rectangle(Point(50,360),Point(150,390))
    scheduleBox.draw(win)
    scheduleBoxText = Text(scheduleBox.getCenter(),"Schedule")
    scheduleBoxText.setSize(10)
    scheduleBoxText.draw(win)

    selectSystemBox = scheduleBox.clone()
    selectSystemBox.move(0,35)
    selectSystemBox.draw(win)
    selectSystemText = Text(selectSystemBox.getCenter(),"Coach System")
    selectSystemText.setSize(10)
    selectSystemText.draw(win)

    recordsBox = statsBox.clone()
    recordsBox.move(0,35)
    recordsBox.draw(win)
    recordsText = Text(recordsBox.getCenter(),"Team Records")
    recordsText.setSize(10)
    recordsText.draw(win)

    awardsBox = recordsBox.clone()
    awardsBox.move(0,35)
    awardsText = Text(awardsBox.getCenter(),"Award Races")
    awardsText.setSize(10)

    historyBox = selectSystemBox.clone()
    historyBox.move(0,35)
    historyBox.draw(win)
    historyText = Text(historyBox.getCenter(),"Team History")
    historyText.setSize(10)
    historyText.draw(win)
    
    x = playerTeam.starSlot
    rosterBorder = Rectangle(rosterBox[0][0].getP1(),rosterBox[11][3].getP2())
    starCol = []
    starText = ""
    num = 0
    while num < 5:
        starCol.append(Rectangle(Point(rosterBorder.getP2().x,rosterBorder.getP1().y+20*num),
                                 Point(rosterBorder.getP2().x + 40,rosterBorder.getP1().y+20*(num+1))))
        starCol[num].draw(win)
        if num == x:
            starText = Text(starCol[num].getCenter(),"Star")
            starCol[num].setFill("yellow")
            starText.setSize(10)
            starText.draw(win)
        num += 1
    starColBorder = Rectangle(starCol[0].getP1(),starCol[4].getP2())
    lowerCorner = Text(Point(70,575),"")
    lowerCorner.draw(win)
    simThruBox = Rectangle(Point(680,555),Point(880,585))
    simThruText = Text(simThruBox.getCenter(),"Sim to end of regular season")
    simThruText.setSize(9)

    instructionsBox = Rectangle(Point(150,560),Point(250,590))
    instructionsText = Text(instructionsBox.getCenter(),"Tips")
    instructionsText.setSize(10)
    instructionsBox.draw(win)
    instructionsText.draw(win)

    ## EVERY YEAR LOOP SHOULD START HERE
    while True:

        if newFile == True:
            scheduleBuild(conferenceList)

        
        
        simThruBox.draw(win)
        simThruText.draw(win)
        teamHistory = History()
        awardsList = []
        for conference in conferenceList:
            for team in conference:
                for player in team.roster:
                    player.team = team
                    awardsList.append(player)
        
        x = playerTeam.starSlot
        for item in starCol:
            if starCol.index(item) == x:
                starCol[playerTeam.starSlot].setFill("burlywood1")
                newInd = starCol.index(item)
                starCol[newInd].setFill("yellow")
                starText.undraw()
                starText = Text(starCol[x].getCenter(),"Star")
                starText.setSize(10)
                starText.draw(win)
                if newFile == True:
                    playerTeam.starSlot = newInd
            else:
                item.setFill("burlywood1")
                
        week = 0 # Test Adjustable
        weekTest = 14 # Adjustable for testing, should be 14

        
        
        n = 0
        while n < 12:
            rosterText[n][0].setText(playerTeam.roster[n].name)
            rosterText[n][1].setText(playerTeam.roster[n].pos)
            rosterText[n][2].setText(playerTeam.roster[n].ovr)
            rosterText[n][3].setText(playerTeam.roster[n].year)
            n += 1

        
        if newFile == True:
            for conference in conferenceList:
                for team in conference:
                    powerList = []
                    for player in team.roster[0:9]:
                        powerList.append(player.ovr)
                    team.ovr = round(statistics.mean(powerList))

        upCTxt = str(playerTeam.name)+ " Year " + str(str(year+1)+",") + " Prestige " + str(playerTeam.prestige)
        upperCorner.setText(upCTxt)
        lowerCorner.setText("Team OVR: " + str(playerTeam.ovr))
        # Generates expected win %
        expectedWins = 0
        yearPrestige = 0
        for game in playerTeam.schedule:
            if game.prestige < playerTeam.prestige:
                expectedWins += 0.5
            if game.ovr < playerTeam.ovr:
                expectedWins += 0.5
        if expectedWins < 10:
            expectedWins = 10
        elif expectedWins > 25:
            expectedWins = 25
        expectedWins = round(expectedWins)

        
        

        endSeason = False

        newFile = True
        saveFile = shelve.open(saveFileName,flag = 'n')
        saveFile['newFile'] = False
        saveFile['year'] = year
        saveFile['conferenceList'] = conferenceList

        for item in conferenceList:
            for team in item:
                if team.name == playerTeam.name:
                    playerTeam = team

        playerConference = []
        for conference in conferenceList:
            if playerTeam in conference:
                playerConference = conference
                break

        saveFile['playerTeam'] = playerTeam
        saveFile['playerConference'] = playerConference
        
        saveFile.close()
        
        # Week to week
        while week < 30:
            oppTeam = playerTeam.schedule[week]
            
            if week == weekTest: 
                awardsBox.draw(win)
                awardsText.draw(win)
            n = 0
            while n < 12:
                oppRosterText[n][0].setText(oppTeam.roster[n].name)
                oppRosterText[n][1].setText(oppTeam.roster[n].pos)
                oppRosterText[n][2].setText(oppTeam.roster[n].ovr)
                oppRosterText[n][3].setText(oppTeam.roster[n].year)
                n += 1
            oppCorner.setText(oppTeam.name + ", OVR: " + str(oppTeam.ovr))
            represented = []
            for item in otherGames:
                item.setText("")
            n = 0
            weekText.setText("Week " + str(week+1))
            for team in playerConference:
                if team not in represented:
                    represented.append(team)
                    represented.append(team.schedule[week])
                    otherGames[n].setText(str(team.name + " vs. " + team.schedule[week].name))
                    n+=1
            
            havePlayed = []    
            validBox = False
            while validBox == False:
                mouse = win.getMouse()
                if inside(rosterBorder,mouse):
                    switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
                elif inside(expandBox,mouse):
                    expandRoster(playerTeam.roster,win)
                elif inside(scheduleBox,mouse):
                    showSchedule(playerTeam,win)
                elif inside(starColBorder,mouse):
                    changeStar(playerTeam,starCol,starText,mouse,win)
                elif inside(statsBox,mouse):
                    stats(playerTeam,win)
                elif inside(oppStatsBox,mouse):
                    stats(oppTeam,win)
                elif inside (quitBox,mouse):
                    quitScreen(win)
                elif inside(recordsBox,mouse):
                    teamRecords(playerTeam,win)
                elif inside(selectSystemBox,mouse):
                    selectSystem(playerTeam,win)
                elif week >= weekTest and inside(awardsBox,mouse):
                    awards(conferenceList,playerConference,playerTeam,win,False,awardsList)
                elif inside(historyBox,mouse):
                    showHistory(playerTeam,win)
                elif inside(instructionsBox,mouse):
                    instructions(win)
                elif inside(simThruBox,mouse):
                    simThruText.setText("Pause Simulation")
                    endSeason, week = simThru(conferenceList,week,win,playerTeam,awardsBox,awardsText,oppRosterText,oppCorner,otherGames,weekText,
                                              playerConference,standingsText,standings,simThruBox)
                    if endSeason == False:
                        simThruText.setText("Simulate to end of season")
                        playText.setText("Next Week")
                        week -= 1
                    break
                elif inside(playBox,mouse):
                    for conference in conferenceList:
                        for team in conference:
                            if team not in havePlayed:
                                simGame(team,team.schedule[week],playerTeam)
                                havePlayed.append(team)
                                havePlayed.append(team.schedule[week])

                    validBox = True
                    boxScore(playerTeam,oppTeam,win)
                    playText.setText("Next Week")

                    represented = []
                    
                    n = 0
                    for team in playerConference:
                        if team not in represented:
                            represented.append(team)
                            represented.append(team.schedule[week])
                            otherGames[n].setText(str(team.name + " " + str(team.gamePoints) + " " + team.schedule[week].name +
                                                      " " + str(team.schedule[week].gamePoints)))
                            n+=1
                    
            if endSeason == True:
                break
            for item in playerConference:
                if item.confWins > 0:
                    item.confPct = item.confWins / (item.confWins+item.confLosses)
                item.wins = freq(item.record,1)
            confStandings = sorted(playerConference,key= lambda x: (x.confPct,x.confWins,x.wins),reverse = True)
            n = 0
            for item in confStandings:
                standings[n].setText(str(str(n+1) + ". " + item.name + " (" + str(item.confWins) + "-" + str(item.confLosses) + ") " + str(item.wins) + "-" + str(week-item.wins+1)))
                n += 1
            if week == 0:
                standingsText.setText("Conference Standings: (Conf Record) Overall Record")
            validBox = False
            while validBox == False:
                mouse = win.getMouse()
                if inside(rosterBorder,mouse):
                    switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
                elif inside(expandBox,mouse):
                    expandRoster(playerTeam.roster,win)
                elif inside(scheduleBox,mouse):
                    showSchedule(playerTeam,win)
                elif inside(starColBorder,mouse):
                    changeStar(playerTeam,starCol,starText,mouse,win)
                elif inside(statsBox,mouse):
                    stats(playerTeam,win)
                elif inside(oppStatsBox,mouse):
                    stats(oppTeam,win)
                elif inside (quitBox,mouse):
                    quitScreen(win)
                elif inside(selectSystemBox,mouse):
                    selectSystem(playerTeam,win)
                elif inside(recordsBox,mouse):
                    teamRecords(playerTeam,win)
                elif inside(historyBox,mouse):
                    showHistory(playerTeam,win)
                elif week >= weekTest and inside(awardsBox,mouse):
                    awards(conferenceList,playerConference,playerTeam,win,False,awardsList)
                elif inside(instructionsBox,mouse):
                    instructions(win)
                elif inside(simThruBox,mouse):
                    playText.setText("Play Games")
                    simThruText.setText("Pause Simulation")
                    week += 1
                    endSeason, week = simThru(conferenceList,week,win,playerTeam,awardsBox,awardsText,oppRosterText,oppCorner,otherGames,weekText,
                                              playerConference,standingsText,standings,simThruBox)
                    if endSeason == False:
                        simThruText.setText("Simulate to end of season")
                        week -= 1
                    break
                elif inside(playBox,mouse):
                    validBox = True
                    playText.setText("Play Game")
            if endSeason == True:
                break
            week += 1

        simThruText.setText("Simulate to end of season")
        simThruBox.undraw()
        simThruText.undraw()
        week = 30
        confStandings = sorted(playerConference,key= lambda x: (x.confPct, x.confWins, x.wins),reverse = True)
        
        # Prestige for winning regular season conference title
        if playerTeam == confStandings[0]:
            yearPrestige += 3

        teamHistory.confFinish = confStandings.index(playerTeam)
        teamHistory.year = year
        teamHistory.prestige = playerTeam.prestige
        
        confTournament = []
        y = 0
        for conference in conferenceList:
            confStandings = sorted(conference,key= lambda x: (x.confPct, x.confWins, x.wins),reverse = True)
            confTournament.append([])
            while len(confStandings) < 16:
                confStandings.append(Team("bye",0,"",[],0))
            for n in range(0,8):
                team = confStandings[n]
                oppTeam = confStandings[len(confStandings)-(n+1)]
                confTournament[y].extend([team,oppTeam])
            y += 1

        # Calculate regular season prestige gain
        if playerTeam.wins > expectedWins + 2:
            yearPrestige += ((playerTeam.wins - (expectedWins + 2)) * 1)
        elif playerTeam.wins < expectedWins - 3:
            yearPrestige += ((playerTeam.wins - (expectedWins - 3) ) * 1)

        # Calculate Team Single Season Records:
        for player in playerTeam.roster:
            if player.stats.pts > playerTeam.seasonRecords.pts[0][0]:
                playerTeam.seasonRecords.pts[0] = [player.stats.pts,player.name]
            if player.stats.reb > playerTeam.seasonRecords.reb[0][0]:
                playerTeam.seasonRecords.reb[0] = [player.stats.reb,player.name]
            if player.stats.thrM > playerTeam.seasonRecords.thrM[0][0]:
                playerTeam.seasonRecords.thrM[0] = [player.stats.thrM,player.name]
            if player.stats.to > playerTeam.seasonRecords.to[0][0]:
                playerTeam.seasonRecords.to[0] = [player.stats.to,player.name]
            if player.stats.fgM > playerTeam.seasonRecords.fgM[0][0]:
                playerTeam.seasonRecords.fgM[0] = [player.stats.fgM,player.name]
            if player.stats.asst > playerTeam.seasonRecords.asst[0][0]:
                playerTeam.seasonRecords.asst[0] = [player.stats.asst,player.name]
            if player.stats.blck > playerTeam.seasonRecords.blck[0][0]:
                playerTeam.seasonRecords.blck[0] = [player.stats.blck,player.name]
            if player.stats.stl > playerTeam.seasonRecords.stl[0][0]:
                playerTeam.seasonRecords.stl[0] = [player.stats.stl,player.name]

        awards(conferenceList,playerConference,playerTeam,win,False,awardsList)
        awardsText.setText("Award Winners")

        for conference in conferenceList:
            for team in conference:
                team.tourneyPoints += team.prestige
                team.tourneyPoints += ((team.ovr - 77) * 20)
                team.tourneyPoints = team.tourneyPoints * 1.5
        
        # Begin Conference Tournaments
        for w in range(0,4):
            if w > 0:
                y = 0
                for conference in confTournament:
                    confStandings = []
                    for n in range(0,int(len(conference)/2)):
                        team = conference[n]
                        oppTeam = conference[len(conference)-(n+1)]
                        confStandings.extend([team,oppTeam])
                    confTournament[y] = confStandings
                    y += 1
            for conference in confTournament:
                for n in range(0,len(conference),2):
                    team = conference[n]
                    oppTeam = conference[n+1]
                    team.schedule.append(oppTeam)
                    oppTeam.schedule.append(team)

            if len(playerTeam.schedule) == week + 1:
                oppTeam = playerTeam.schedule[week]
            else:
                oppTeam = Team("bye",0,"",[],0)
            if oppTeam.name != "bye":
                n = 0
                while n < 12:
                    oppRosterText[n][0].setText(oppTeam.roster[n].name)
                    oppRosterText[n][1].setText(oppTeam.roster[n].pos)
                    oppRosterText[n][2].setText(oppTeam.roster[n].ovr)
                    oppRosterText[n][3].setText(oppTeam.roster[n].year)
                    n += 1
            else:
                n = 0
                while n < 12:
                    oppRosterText[n][0].setText("")
                    oppRosterText[n][1].setText("")
                    oppRosterText[n][2].setText("")
                    oppRosterText[n][3].setText("")
                    n += 1
            oppCorner.setText(oppTeam.name + ", OVR: " + str(oppTeam.ovr))
            represented = []
            for item in otherGames:
                item.setText("")
            n = 0
            weekText.setText("Conference Tournament")
            for team in confTournament[conferenceList.index(playerConference)][0:len(conference):2]:
                if team.name != "bye":
                    represented.append(team)
                    represented.append(team.schedule[week])
                    otherGames[n].setText(str(team.name + " vs. " + team.schedule[week].name))
                n+=1

            validBox = False
            while validBox == False:
                mouse = win.getMouse()
                if inside(rosterBorder,mouse):
                    switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
                elif inside(expandBox,mouse):
                    expandRoster(playerTeam.roster,win)
                elif inside(scheduleBox,mouse):
                    showSchedule(playerTeam,win)
                elif inside(starColBorder,mouse):
                    changeStar(playerTeam,starCol,starText,mouse,win)
                elif inside(statsBox,mouse):
                    stats(playerTeam,win)
                elif inside(oppStatsBox,mouse) and oppTeam.name != "bye":
                    stats(oppTeam,win)
                elif inside (quitBox,mouse):
                    quitScreen(win)
                elif inside(historyBox,mouse):
                    showHistory(playerTeam,win)
                elif inside(selectSystemBox,mouse):
                    selectSystem(playerTeam,win)
                elif inside(recordsBox,mouse):
                    teamRecords(playerTeam,win)
                elif inside(instructionsBox,mouse):
                    instructions(win)
                elif inside(awardsBox,mouse):
                    awards(conferenceList,playerConference,playerTeam,win,True,awardsList)
                elif inside(playBox,mouse):
                    for conference in confTournament:
                        loserTeams = []
                        for n in range(0,len(conference),2):
                            team = conference[n]
                            oppTeam = conference[n+1]
                            if oppTeam.name == "bye":
                                loserTeams.append(oppTeam)
                            else:
                                simGame(team,oppTeam,playerTeam)
                                if team.gamePoints < oppTeam.gamePoints:
                                    loserTeams.append(team)
                                else:
                                    loserTeams.append(oppTeam)
                        for item in loserTeams:
                            conference.remove(item)
                    validBox = True
                    represented = []
                    for item in otherGames:
                                item.setText("")        
                    n = 0
                    for team in playerConference:
                        if team not in represented and len(team.schedule) == week +1 and team.schedule[week].name != "bye":
                            represented.append(team)
                            represented.append(team.schedule[week])
                            otherGames[n].setText(str(team.name + " " + str(team.gamePoints) + " " + team.schedule[week].name +
                                                      " " + str(team.schedule[week].gamePoints)))
                            n+=1


                    if len(playerTeam.schedule) == week + 1:
                        oppTeam = playerTeam.schedule[week]
                    else:
                        oppTeam = Team("bye",0,"",[],0)
                        
                    if oppTeam.name != "bye":
                        boxScore(playerTeam,oppTeam,win)
                    playText.setText("Next Week")
                    week += 1

            validBox = False
            while validBox == False:
                mouse = win.getMouse()
                if inside(rosterBorder,mouse):
                    switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
                elif inside(expandBox,mouse):
                    expandRoster(playerTeam.roster,win)
                elif inside(scheduleBox,mouse):
                    showSchedule(playerTeam,win)
                elif inside(starColBorder,mouse):
                    changeStar(playerTeam,starCol,starText,mouse,win)
                elif inside(statsBox,mouse):
                    stats(playerTeam,win)
                elif inside(oppStatsBox,mouse) and oppTeam.name != "bye":
                    stats(oppTeam,win)
                elif inside (quitBox,mouse):
                    quitScreen(win)
                elif inside(historyBox,mouse):
                    showHistory(playerTeam,win)
                elif inside(selectSystemBox,mouse):
                    selectSystem(playerTeam,win)
                elif inside(recordsBox,mouse):
                    teamRecords(playerTeam,win)
                elif inside(instructionsBox,mouse):
                    instructions(win)
                elif inside(awardsBox,mouse):
                    awards(conferenceList,playerConference,playerTeam,win,True,awardsList)
                elif inside(playBox,mouse):
                    validBox = True
                    playText.setText("Play Game")
                    

        playText.setText("Next")
        tournamentWinners = []
        for item in confTournament:
            tournamentWinners.append(item[0])

        weekText.setText("Tournament Winners")

        # Prestige Gain for winning conference tournament:
        if playerTeam in tournamentWinners:
            yearPrestige += 2
        
        for n in range(0,32):
            otherGames[n].setText(tournamentWinners[n].name)

        for item in standings:
            item.setText("")

        standingsText.setText("")

        validBox = False
        while validBox == False:
            mouse = win.getMouse()
            if inside(rosterBorder,mouse):
                switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
            elif inside(expandBox,mouse):
                expandRoster(playerTeam.roster,win)
            elif inside(scheduleBox,mouse):
                showSchedule(playerTeam,win)
            elif inside(starColBorder,mouse):
                changeStar(playerTeam,starCol,starText,mouse,win)
            elif inside(statsBox,mouse):
                stats(playerTeam,win)
            elif inside(oppStatsBox,mouse) and oppTeam.name != "bye":
                stats(oppTeam,win)
            elif inside (quitBox,mouse):
                quitScreen(win)
            elif inside(historyBox,mouse):
                showHistory(playerTeam,win)
            elif inside(recordsBox,mouse):
                teamRecords(playerTeam,win)
            elif inside(selectSystemBox,mouse):
                selectSystem(playerTeam,win)
            elif inside(instructionsBox,mouse):
                instructions(win)
            elif inside(awardsBox,mouse):
                awards(conferenceList,playerConference,playerTeam,win,True,awardsList)
            elif inside(playBox,mouse):
                validBox = True

        for item in otherGames:
            item.setText("")

        allTeams = []
        for conference in conferenceList:
            for team in conference:
                
                if team not in tournamentWinners:
                    allTeams.append(team)
        rankings = sorted(allTeams, key = lambda x: (x.tourneyPoints, x.wins, x.prestige, x.ovr), reverse = True)[:32]

        for item in tournamentWinners:
            rankings.append(item)

        
        
        rankings.sort(key = lambda x: (x.tourneyPoints, x.wins, x.prestige, x.ovr), reverse = True)

        for n in range(0,32):
            otherGames[n].setText(str(math.ceil((n+1)/4.0)) + ". " + rankings[n].name + "       " + str(math.ceil((n+33)/4.0)) + ". " + rankings[n+32].name)

        weekText.setText("NCAA Tourney Selections")

        for n in range(0,64):
            rankings[n].seed = str(math.ceil((n+1)/4.0))

        # prestige gain for making tournament
        if playerTeam in rankings:
            yearPrestige += 2
            teamHistory.tourneyExit = "Round of 64"
            teamHistory.seed = playerTeam.seed
        else:
            teamHistory.tourneyExit = "DNQ"
            teamHistory.seed = "N/A"
        
        validBox = False
        while validBox == False:
            mouse = win.getMouse()
            if inside(rosterBorder,mouse):
                switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
            elif inside(expandBox,mouse):
                expandRoster(playerTeam.roster,win)
            elif inside(scheduleBox,mouse):
                showSchedule(playerTeam,win)
            elif inside(starColBorder,mouse):
                changeStar(playerTeam,starCol,starText,mouse,win)
            elif inside(statsBox,mouse):
                stats(playerTeam,win)
            elif inside(oppStatsBox,mouse) and oppTeam.name != "bye":
                stats(oppTeam,win)
            elif inside (quitBox,mouse):
                quitScreen(win)
            elif inside(historyBox,mouse):
                showHistory(playerTeam,win)
            elif inside(selectSystemBox,mouse):
                selectSystem(playerTeam,win)
            elif inside(recordsBox,mouse):
                teamRecords(playerTeam,win)
            elif inside(instructionsBox,mouse):
                instructions(win)
            elif inside(awardsBox,mouse):
                awards(conferenceList,playerConference,playerTeam,win,True,awardsList)
            elif inside(playBox,mouse):
                validBox = True
                playText.setText("Play Game")

        for item in rankings:
            x = len(item.schedule)
            if x < 34:
                for n in range(0,(34-x)):
                    item.schedule.append("")

        weekText.setText("NCAA Tournament")

        # NCAA TOURNAMENT
        week = 34
        for w in range(0,6):
            playText.setText("Play Games")
            confStandings = []
            for n in range(0,int(len(rankings)/2)):
                team = rankings[n]
                oppTeam = rankings[len(rankings)-(n+1)]
                confStandings.extend([team,oppTeam])
            rankings = confStandings

            for n in range(0,len(rankings),2):
                team = rankings[n]
                oppTeam = rankings[n+1]
                team.schedule.append(oppTeam)
                oppTeam.schedule.append(team)

            if len(playerTeam.schedule) == week + 1:
                oppTeam = playerTeam.schedule[week]
            else:
                oppTeam = Team("Out",0,"",[],0)

            if oppTeam.name != "Out":
                n = 0
                while n < 12:
                    oppRosterText[n][0].setText(oppTeam.roster[n].name)
                    oppRosterText[n][1].setText(oppTeam.roster[n].pos)
                    oppRosterText[n][2].setText(oppTeam.roster[n].ovr)
                    oppRosterText[n][3].setText(oppTeam.roster[n].year)
                    n += 1
            else:
                n = 0
                while n < 12:
                    oppRosterText[n][0].setText("")
                    oppRosterText[n][1].setText("")
                    oppRosterText[n][2].setText("")
                    oppRosterText[n][3].setText("")
                    n += 1

            oppCorner.setText(oppTeam.name + ", OVR: " + str(oppTeam.ovr))
            for item in otherGames:
                        item.setText("")
            n = 0
            for team in rankings[0:len(rankings):2]:
                otherGames[n].setText(str(team.seed + ". " + team.name + " vs. " + team.schedule[week].seed + ". " + team.schedule[week].name))
                n+=1

            validBox = False
            while validBox == False:
                mouse = win.getMouse()
                if inside(rosterBorder,mouse):
                    switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
                elif inside(expandBox,mouse):
                    expandRoster(playerTeam.roster,win)
                elif inside(scheduleBox,mouse):
                    showSchedule(playerTeam,win)
                elif inside(starColBorder,mouse):
                    changeStar(playerTeam,starCol,starText,mouse,win)
                elif inside(statsBox,mouse):
                    stats(playerTeam,win)
                elif inside(oppStatsBox,mouse) and oppTeam.name != "Out":
                    stats(oppTeam,win)
                elif inside (quitBox,mouse):
                    quitScreen(win)
                elif inside(historyBox,mouse):
                    showHistory(playerTeam,win)
                elif inside(selectSystemBox,mouse):
                    selectSystem(playerTeam,win)
                elif inside(recordsBox,mouse):
                    teamRecords(playerTeam,win)
                elif inside(awardsBox,mouse):
                    awards(conferenceList,playerConference,playerTeam,win,True,awardsList)
                elif inside(instructionsBox,mouse):
                    instructions(win)
                elif inside(playBox,mouse):
                    loserTeams = []
                    for n in range(0,len(rankings),2):
                        team = rankings[n]
                        oppTeam = rankings[n+1]
                        simGame(team,oppTeam,playerTeam)
                        if team.gamePoints < oppTeam.gamePoints:
                            loserTeams.append(team)
                        else:
                            loserTeams.append(oppTeam)
                    for item in loserTeams:
                        rankings.remove(item)
                    validBox = True

                    represented = []
                    for item in otherGames:
                                item.setText("")        
                    n = 0
                    for team in rankings:
                        if team not in represented and len(team.schedule) == week +1 and team.schedule[week].name != "bye":
                            represented.append(team)
                            represented.append(team.schedule[week])
                            otherGames[n].setText(str(team.name + " " + str(team.gamePoints) + " " + team.schedule[week].name +
                                                      " " + str(team.schedule[week].gamePoints)))
                            n+=1

            if len(playerTeam.schedule) == week + 1:
                oppTeam = playerTeam.schedule[week]
            else:
                oppTeam = Team("Out",0,"",[],0)
                
            if oppTeam.name != "Out":
                boxScore(playerTeam,oppTeam,win)
            playText.setText("Next Week")

            # Calculating prestige gain for each round

            if playerTeam in rankings:
                if w == 0:
                    yearPrestige += 1
                    teamHistory.tourneyExit = "Round of 32"
                elif w == 1:
                    yearPrestige += 1
                    teamHistory.tourneyExit = "Sweet 16"
                elif w == 2:
                    yearPrestige += 2
                    teamHistory.tourneyExit = "Elite 8"
                elif w == 3:
                    yearPrestige += 5
                    teamHistory.tourneyExit = "Final 4"
                elif w == 4:
                    yearPrestige += 2
                    teamHistory.tourneyExit = "National Runner-Up"
                elif w == 5:
                    yearPrestige += 8
                    teamHistory.tourneyExit = "National Champions"


            validBox = False
            while validBox == False:
                mouse = win.getMouse()
                if inside(rosterBorder,mouse):
                    switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
                elif inside(expandBox,mouse):
                    expandRoster(playerTeam.roster,win)
                elif inside(scheduleBox,mouse):
                    showSchedule(playerTeam,win)
                elif inside(starColBorder,mouse):
                    changeStar(playerTeam,starCol,starText,mouse,win)
                elif inside(statsBox,mouse):
                    stats(playerTeam,win)
                elif inside (quitBox,mouse):
                    quitScreen(win)
                elif inside(selectSystemBox,mouse):
                    selectSystem(playerTeam,win)
                elif inside(recordsBox,mouse):
                    teamRecords(playerTeam,win)
                elif inside(historyBox,mouse):
                    showHistory(playerTeam,win)
                elif inside(instructionsBox,mouse):
                    instructions(win)
                elif inside(oppStatsBox,mouse) and oppTeam.name != "Out":
                    stats(oppTeam,win)
                elif inside(awardsBox,mouse):
                    awards(conferenceList,playerConference,playerTeam,win,True,awardsList)
                elif inside(playBox,mouse):
                    validBox = True

            week += 1
        playText.setText("Next")
        weekText.setText(rankings[0].name + " Won the National Championship")
        
        validBox = False
        while validBox == False:
            mouse = win.getMouse()
            if inside(rosterBorder,mouse):
                switchPlayers(rosterBox,mouse,playerTeam,rosterText,win)
            elif inside(expandBox,mouse):
                expandRoster(playerTeam.roster,win)
            elif inside(scheduleBox,mouse):
                showSchedule(playerTeam,win)
            elif inside(starColBorder,mouse):
                changeStar(playerTeam,starCol,starText,mouse,win)
            elif inside(statsBox,mouse):
                stats(playerTeam,win)
            elif inside (quitBox,mouse):
                quitScreen(win)
            elif inside(recordsBox,mouse):
                teamRecords(playerTeam,win)
            elif inside(awardsBox,mouse):
                awards(conferenceList,playerConference,playerTeam,win,True,awardsList)
            elif inside(selectSystemBox,mouse):
                selectSystem(playerTeam,win)
            elif inside(historyBox,mouse):
                showHistory(playerTeam,win)
            elif inside(instructionsBox,mouse):
                instructions(win)
            elif inside(playBox,mouse):
                validBox = True

        for item in otherGames:
            item.setText("")

        # insert here
        playerWins = freq(playerTeam.record,1)
        playerLosses = freq(playerTeam.record,0)
        teamHistory.record = (str(playerWins)+"-"+str(playerLosses))
        playerTeam.history.append(teamHistory)
        
        leavingList = []

        for conference in conferenceList:
            for team in conference:
                teamLeaving = []
                for player in team.roster:
                    if player.year == 4:
                        teamLeaving.append(player)
                    elif player.ovr > 80 and random.randint(0,100) < 10 * (player.ovr - 80):
                        teamLeaving.append(player)
                if team == playerTeam:
                    leavingList = teamLeaving
                for item in teamLeaving:
                    team.roster.remove(item)

        weekText.setText("Players Leaving")

        n = 0
        for item in leavingList:
            if item.year == 4:
                reason = "Graduated"
                grad = "Senior"
            else:
                if item.year == 3:
                    grad = "Junior"
                elif item.year == 2:
                    grad = "Sophmore"
                else:
                    grad = "Freshman"
                reason = "Left for Draft"
                
            otherGames[n].setText(str(item.name + ", " + item.pos + " " + str(item.ovr) + " " + grad + ", " + reason))
            n += 1

        otherGames[n+2].setText("Click anywhere to continue")

        win.getMouse()

        playerTeam.prestige += yearPrestige
        if playerTeam.prestige > 100:
            playerTeam.prestige = 100
        elif playerTeam.prestige < 0:
            playerTeam.prestige = 0

        for conference in conferenceList:
            for team in conference:
                for player in team.roster:
                    player.year += 1
                if team is not playerTeam:
                    prestigeModifier = random.randint(-1,1)
                    team.prestige += prestigeModifier
                    if team.prestige > 100:
                        team.prestige = 100
                    elif team.prestige < 0:
                        team.prestige = 0
                    recruitPlayers(team,firstNames,lastNames)

        coverBox = Rectangle(Point(0,0),Point(1000,600))
        coverBox.setFill("burlywood1")
        coverBox.draw(win)

        prestigeText = Text(Point(500,200),"")
        prestigeText.draw(win)
        
        if yearPrestige > 0:
            prestigeText.setText(str("You exceeded expectations and gained " + str(yearPrestige) + " prestige. Click to continue."))
        elif yearPrestige < 0:
            prestigeText.setText(str("You fell short of expectations and lost " + str(abs(yearPrestige)) + " prestige. Click to continue."))
        else:
            prestigeText.setText("You did about as expected and neither gained nor lost prestige this season. Click to continue.")

        win.getMouse()

        prestigeText.undraw()

        playerRecruitment(playerTeam,win,firstNames,lastNames)

        playerProgression(conferenceList)

        for item in conferenceList:
            for team in item:
                sortRoster = sorted(team.roster,key=operator.attrgetter('ovr'),reverse = True)
                team.roster.clear()
                n = 0
                i = 0
                while n < 2:
                    if sortRoster[i].pos == "G":
                        n += 1
                        team.roster.append(sortRoster.pop(i))
                        i -= 1
                    i += 1
                i = 0
                forward = False
                while forward == False:
                    if sortRoster[i].pos == "G" or sortRoster[i].pos == "F":
                        forward = True
                        team.roster.append(sortRoster.pop(i))
                    i += 1
                i = 0
                center = False
                while center == False:
                    if sortRoster[i].pos == "F" or sortRoster[i].pos == "C":
                        center = True
                        team.roster.append(sortRoster.pop(i))
                    i += 1
                team.roster.extend(sortRoster)
                team.starSlot = team.roster.index(max(team.roster,key=operator.attrgetter('ovr')))
        year += 1
        coverBox.undraw()
        playText.setText("Play Games")
        #Zeroing everything
        awardsBox.undraw()
        awardsText.undraw()
        awardsText.setText("Award Races")
        for conference in conferenceList:
            for team in conference:
                team.schedule = []
                team.record = []
                team.confWins = 0
                team.confLosses = 0
                team.confPct = 0
                team.wins = 0
                team.seed = 0
                team.tourneyPoints = 0
                team.stats.reb = 0
                team.stats.pts = 0
                team.stats.thrA = 0
                team.stats.thrM = 0
                team.stats.fgA = 0
                team.stats.fgM = 0
                team.stats.to = 0
                team.stats.asst = 0
                team.stats.blck = 0
                team.stats.stl = 0
                team.stats.thrPr = 0
                team.stats.fgPr = 0
                team.stats.mins = 0
                team.stats.gp = 0
                for player in team.roster:
                    player.stats.reb = 0
                    player.stats.pts = 0
                    player.stats.thrA = 0
                    player.stats.thrM = 0
                    player.stats.fgA = 0
                    player.stats.fgM = 0
                    player.stats.to = 0
                    player.stats.asst = 0
                    player.stats.blck = 0
                    player.stats.stl = 0
                    player.stats.thrPr = 0
                    player.stats.fgPr = 0
                    player.stats.mins = 0
                    player.stats.gp = 0
                    player.gameStats.reb = 0
                    player.gameStats.pts = 0
                    player.gameStats.thrA = 0
                    player.gameStats.thrM = 0
                    player.gameStats.fgA = 0
                    player.gameStats.fgM = 0
                    player.gameStats.to = 0
                    player.gameStats.asst = 0
                    player.gameStats.blck = 0
                    player.gameStats.stl = 0
                    player.gameStats.thrPr = 0
                    player.gameStats.fgPr = 0
                    player.gameStats.mins = 0
                    player.gameStats.gp = 0
                    player.clout = 0

        

       

    
main()
