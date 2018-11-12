import random
import time
from math import *
from threading import *
from tkinter import *
from tkinter import messagebox
from ClassFractalPoint import Point
from ClassFractalLine import Line

root = Tk()
root.resizable(False, False)
root.geometry("1270x900+0+20")

listOfPoints = []
listOfLines = []
listOfLinesMain = []
tmpListOfLinesMain = []
iterationCurrent = 1
generatorLength = 0
#############################
points = StringVar()
points.set('7')
fieldPoints = Entry(root, textvariable=points)
fieldPoints.place(x=20, y=450, width=100, height=20)

iterations = StringVar()
iterations.set('6')
fieldIterations = Entry(root, textvariable=iterations)
fieldIterations.place(x=140, y=450, width=100, height=20)

shapes = StringVar()
shapes.set('1')
fieldShapes = Entry(root, textvariable=shapes)
fieldShapes.place(x=140, y=410, width=100, height=20)

labelPoints = Label(root, text="numberOfPoints")
labelPoints.place(x=20, y=430, width=100, height=20)

labelShapes = Label(root, text="Shapes")
labelShapes.place(x=140, y=390, width=100, height=20)

labelIterations = Label(root, text="Iterations")
labelIterations.place(x=140, y=430, width=100, height=20)

generatorField = Canvas(root, bg="white")
generatorField.place(x=20, y=480, width=400, height=400)

mainField = Canvas(root, bg="white")
mainField.place(x=440, y=20, width=800, height=800)


#############################
def clear():
    global listOfLinesMain
    global tmpListOfLinesMain
    global iterationCurrent
    for line in listOfLinesMain:
        line.erase(mainField)
    for line in tmpListOfLinesMain:
        line.erase(mainField)
    listOfLinesMain = []
    tmpListOfLinesMain = []
    iterationCurrent = 1


def startGenerator():
    global listOfPoints
    global listOfLines
    if listOfPoints:
        for point in listOfPoints:
            point.erase(generatorField)
        listOfPoints = []
    if listOfLines:
        for line in listOfLines:
            line.erase(generatorField)
        listOfLines = []
    try:
        amountOfPoints = int(fieldPoints.get())
    except ValueError:
        messagebox.showinfo('Oops', 'amountOfPoints value not int')
        fieldPoints.delete(0, END)
        fieldPoints.insert(0, 0)
    for i in range(1, amountOfPoints + 1):
        listOfPoints.append(
            Point([10 + 380 * (i - 1) / (amountOfPoints - 1), 200],
                  generatorField.create_oval(0, 0, 0, 0), i, True))
        listOfPoints[i - 1].erase(generatorField)
        listOfPoints[i - 1].paint(generatorField)
    for i in range(1, amountOfPoints):
        x1 = listOfPoints[i - 1].getCoords()[0]
        y1 = listOfPoints[i - 1].getCoords()[1]
        x2 = listOfPoints[i].getCoords()[0]
        y2 = listOfPoints[i].getCoords()[1]
        listOfLines.append(
            Line([x1, y1, x2, y2], generatorField.create_line(0, 0, 0, 0), i))
        listOfLines[i - 1].erase(generatorField)
        listOfLines[i - 1].paint(generatorField)


def holdAndCalc():
    global listOfPoints
    global listOfLines
    global generatorLength
    dx = listOfPoints[0].getCoords()[0] - listOfPoints[-1].getCoords()[0]
    dy = listOfPoints[0].getCoords()[1] - listOfPoints[-1].getCoords()[1]
    l = ((dx) ** 2 + (dy) ** 2) ** (1 / 2)
    generatorLength = l
    cosA = -dx / l
    sinA = dy / l
    generatorDirection = [cosA, sinA]
    i = 0
    if listOfLines[0] == listOfLines[-1]:
        listOfLines[0].setDirection(generatorDirection)
    else:
        for line in listOfLines:
            dx = line.getCoords()[0] - line.getCoords()[2]
            dy = line.getCoords()[1] - line.getCoords()[3]
            l = ((dx) ** 2 + (dy) ** 2) ** (1 / 2)
            tmpX = -cosA * dx / l + sinA * dy / l
            tmpY = sinA * dx / l + cosA * dy / l
            line.setDirection([tmpX, tmpY])
            i = i + 1


def iterate():
    global iterationCurrent
    global listOfLinesMain
    global tmpListOfLinesMain
    try:
        iterationMax = int(fieldIterations.get())
    except ValueError:
        messagebox.showinfo('Oops', 'iterations value not int')
        fieldIterations.delete(0, END)
        fieldIterations.insert(0, 0)
    holdAndCalc()
    if iterationCurrent <= iterationMax:
        for lineMain in listOfLinesMain:
            dx = lineMain.getCoords()[0] - lineMain.getCoords()[2]
            dy = lineMain.getCoords()[1] - lineMain.getCoords()[3]
            l = ((dx) ** 2 + (dy) ** 2) ** (1 / 2)
            directionX = -dx / l
            directionY = dy / l
            lineMain.setDirection([directionX, directionY])
            changeLine(lineMain)
            lineMain.erase(mainField)
        iterationCurrent = iterationCurrent + 1
        listOfLinesMain = tmpListOfLinesMain[:]
        tmpListOfLinesMain = []
    else:
        messagebox.showinfo('Oops', 'iterationCurrent > iterationMax')


def changeLine(lineMain):
    global listOfPoints
    global listOfLines
    global generatorLength
    global tmpListOfLinesMain
    dx = lineMain.getCoords()[0] - lineMain.getCoords()[2]
    dy = lineMain.getCoords()[1] - lineMain.getCoords()[3]
    l = (dx ** 2 + dy ** 2) ** (1 / 2)
    sizeKoeff = l / generatorLength
    x0 = listOfLines[0].getCoords()[0]
    y0 = listOfLines[0].getCoords()[1]
    for line in listOfLines:
        dirX = line.getDirection()[0]
        dirY = line.getDirection()[1]
        dx = line.getCoords()[0] - line.getCoords()[2]
        dy = line.getCoords()[1] - line.getCoords()[3]
        l = (dx ** 2 + dy ** 2) ** (1 / 2)
        cosA = lineMain.getDirection()[0]
        sinA = lineMain.getDirection()[1]
        tmpX = cosA * dirX - sinA * dirY
        tmpY = sinA * dirX + cosA * dirY
        l = l * sizeKoeff
        if line.getNumber() == 1:
            x1 = line.getCoords()[0] - x0 + lineMain.getCoords()[0]
            y1 = line.getCoords()[1] - y0 + lineMain.getCoords()[1]
            x2 = x1 + l * tmpX
            y2 = y1 - l * tmpY
        else:
            x1 = tmpListOfLinesMain[-1].getCoords()[2]
            y1 = tmpListOfLinesMain[-1].getCoords()[3]
            x2 = x1 + l * tmpX
            y2 = y1 - l * tmpY
        tmpListOfLinesMain.append(
            Line([x1, y1, x2, y2], mainField.create_line(x1, y1, x2, y2), 0,
                 'black', [tmpX, tmpY]))


#############################
def clickGeneratorLeft(event):
    global listOfPoints
    global listOfLines
    clickX = event.x
    clickY = event.y
    for point in listOfPoints:
        pointX = point.getCoords()[0]
        pointY = point.getCoords()[1]
        distance = ((pointX - clickX) ** 2 + (pointY - clickY) ** 2) ** (1 / 2)
        if distance < 5:
            point.erase(generatorField)
            point.setColor('red')
            point.paint(generatorField)
            for line in listOfLines:
                if line.getNumber() == point.getNumber() - 1:
                    line.erase(generatorField)
                    line.setColor('red')
                    line.paint(generatorField)
                if line.getNumber() == point.getNumber():
                    line.erase(generatorField)
                    line.setColor('red')
                    line.paint(generatorField)
            break


def clickGeneratornRight(event):
    global listOfPoints
    global listOfLines
    for point in listOfPoints:
        if point.getColor() == 'red':
            point.erase(generatorField)
            point.setColor('black')
            point.paint(generatorField)
            for line in listOfLines:
                if line.getNumber() == point.getNumber() - 1:
                    line.erase(generatorField)
                    line.setColor('black')
                    line.paint(generatorField)
                if line.getNumber() == point.getNumber():
                    line.erase(generatorField)
                    line.setColor('black')
                    line.paint(generatorField)
            holdAndCalc()
            break


def motionGenerator(event):
    global listOfPoints
    global listOfLines
    for point in listOfPoints:
        if point.getColor() == 'red':
            point.erase(generatorField)
            point.setCoords([event.x, event.y])
            point.paint(generatorField)
            point.getNumber()
            for line in listOfLines:
                if line.getNumber() == point.getNumber() - 1:
                    line.erase(generatorField)
                    x1 = line.getCoords()[0]
                    y1 = line.getCoords()[1]
                    x2 = event.x
                    y2 = event.y
                    line.setCoords([x1, y1, x2, y2])
                    line.paint(generatorField)
                if line.getNumber() == point.getNumber():
                    line.erase(generatorField)
                    x1 = event.x
                    y1 = event.y
                    x2 = line.getCoords()[2]
                    y2 = line.getCoords()[3]
                    line.setCoords([x1, y1, x2, y2])
                    line.paint(generatorField)


def MakeObject():
    global listOfLinesMain
    clear()
    try:
        shapesCurrent = int(fieldShapes.get())
    except ValueError:
        messagebox.showinfo('Oops', 'shapes value not int')
        fieldIterations.delete(0, END)
        fieldIterations.insert(0, 0)
    if shapesCurrent == 1:
        # print('shapesCurrent 1:',shapesCurrent)
        listOfLinesMain.append(
            Line([50, 400, 750, 400], mainField.create_line(50, 400, 750, 400),
                 1))
    elif shapesCurrent != 2:
        r = 180
        a = r * 2 * tan(pi / shapesCurrent)
        if a > 451:
            a = 450
        angle = 2 * pi / shapesCurrent
        x1 = 400 - a / 2
        y1 = 400 - 110
        x2 = 400 + a / 2
        y2 = 400 - 110
        listOfLinesMain.append(
            Line([x1, y1, x2, y2], mainField.create_line(x1, y1, x2, y2), 0))
        for i in range(1, shapesCurrent):
            dirX = cos(angle * i)
            dirY = sin(angle * i)
            x1 = listOfLinesMain[-1].getCoords()[2]
            y1 = listOfLinesMain[-1].getCoords()[3]
            x2 = x1 + a * dirX
            y2 = y1 + a * dirY
            listOfLinesMain.append(
                Line([x1, y1, x2, y2], mainField.create_line(x1, y1, x2, y2),
                     i))
    else:
        messagebox.showinfo('Oops', 'shapes value == 2')


#############################
generatorField.bind('<Motion>', motionGenerator)
generatorField.bind('<Button-1>', clickGeneratorLeft)
generatorField.bind('<Button-3>', clickGeneratornRight)
#############################
buttonMakeObject = Button(root, text="Make Fig.", command=MakeObject)
buttonMakeObject.place(x=260, y=410, width=100, height=20)

buttonGenerator = Button(root, text="Show generator", command=startGenerator)
buttonGenerator.place(x=260, y=450, width=100, height=20)

buttonStartGeneration = Button(root, text="OK, iterate it!", command=iterate)
buttonStartGeneration.place(x=440, y=830, width=120, height=20)

buttonClear = Button(root, text="Clear", command=clear)
buttonClear.place(x=580, y=830, width=100, height=20)
#############################
root.mainloop()
