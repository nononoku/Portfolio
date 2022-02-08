# wordle.py
"""Python graphics-based clone of Wordle by Josh Wardle

Written by Noah Kuperberg 2/7/2022"""

from graphics import *
import random
import time


WIN = GraphWin("Wordle", 600, 625)

def inside(rectangle,point):
    x1 = rectangle.getP1().x
    x2 = rectangle.getP2().x
    y1 = rectangle.getP1().y
    y2 = rectangle.getP2().y
    if (x1 < point.x and x2 > point.x and y1 < point.y and y2 > point.y):
        return True

def main():
    word = ""
    words = []
    with open("words.txt") as w:
        words = w.readlines()
        word = random.choice(words)
        word = word.strip().upper()   
    for wo in words:
        wo = wo.strip()

    # Set letter boxes
    letterBoxes = []
    for n in range(6):
        row = []
        for i in range(5):
            box = Rectangle(Point(135 + i * 70, 30 + n * 90),
                            Point(185 + i * 70, 100 + n * 90))
            box.draw(WIN)
            letter = Text(box.getCenter(),"")
            letter.setSize(35)
            letter.draw(WIN)
            row.append((letter,box))
        letterBoxes.append(row)

    for n, row in enumerate(letterBoxes):
        index = 0
        guessWord = ""
        while True:
            key = WIN.getKey()
            if key.isalpha() and len(key) == 1 and index < 5:
                key = key.upper()
                guessWord += key
                row[index][0].setText(key)
                index += 1
            elif index and key == "BackSpace":
                index -= 1
                row[index][0].setText("")
                guessWord = guessWord[:-1]
            elif (index == 5 and key == "Return"):
                break
        guessedLetters = ""
        for i, char in enumerate(guessWord):
            if char == word[i]:
                guessedLetters += char
        for i, char in enumerate(guessWord):
            time.sleep(0.1)
            if char == word[i]:
                letterBoxes[n][i][1].setFill("green")
                letterBoxes[n][i][0].setTextColor("white")
            elif (char in word and
                  (guessedLetters.count(char) < word.count(char))):
                letterBoxes[n][i][1].setFill("gold")
                letterBoxes[n][i][0].setTextColor("white")
                guessedLetters += char
            else:
                letterBoxes[n][i][1].setFill("gray")
                letterBoxes[n][i][0].setTextColor("white")
        if guessWord == word:
            break
    print(word)

main()
