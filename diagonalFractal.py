import random
import time
from math import *
from threading import *
from tkinter import *
from tkinter import messagebox
from ClassFractalPoint import Point
from ClassFractalLine import Line

root=Tk()
root.resizable(False,False)
root.geometry("1270x950+0+20")

listOfLines=[]
#############################
sizeX=StringVar()
sizeX.set('800')
fieldSizeX=Entry(root,textvariable=sizeX)
fieldSizeX.place(x=20,y=40,width=100,height=20)

sizeY=StringVar()
sizeY.set('900')
fieldSizeY=Entry(root,textvariable=sizeY)
fieldSizeY.place(x=20,y=80,width=100,height=20)

iterations=StringVar()
iterations.set('100')
fieldIterations=Entry(root,textvariable=iterations)
fieldIterations.place(x=20,y=120,width=100,height=20)

labelSizeX=Label(root,text="size X")
labelSizeX.place(x=20,y=20,width=100,height=20)

labelSizeY=Label(root,text="size Y")
labelSizeY.place(x=20,y=60,width=100,height=20)

labelIterations=Label(root,text="iterations")
labelIterations.place(x=20,y=100,width=100,height=20)

mainField=Canvas(root,bg="white")
#mainField.place(x=440,y=20,width=0,height=0)
#############################
def clear():
	global mainField
	global listOfLines
	mainField.place(x=440,y=20,width=0,height=0)
	for line in listOfLines:
		line.erase(mainField)
	listOfLines=[]

def startGeneration():
	global mainField
	clear()
	size=[0,0]
	try:
		size[0]=int(sizeX.get())
		if size[0]>1100 or size[0]<100:
			messagebox.showinfo('Oops','sizeX value must be in 100...1100 interval')
			size[0]=100
			fieldSizeX.delete(0,END)
			fieldSizeX.insert(0,100)
	except ValueError:
		messagebox.showinfo('Oops','sizeX value not int')
		fieldSizeX.delete(0,END)
		fieldSizeX.insert(0,100)
	try:
		size[1]=int(sizeY.get())
		if size[1]>900 or size[1]<100:
			messagebox.showinfo('Oops','sizeY value must be in 100...900 interval')
			size[1]=100
			fieldSizeY.delete(0,END)
			fieldSizeY.insert(0,100)
	except ValueError:
		messagebox.showinfo('Oops','sizeY value not int')
		fieldSizeY.delete(0,END)
		fieldSizeY.insert(0,100)
	try:
		iteration=int(iterations.get())
	except ValueError:
		messagebox.showinfo('Oops','sizeY value not int')
		fieldSizeY.delete(0,END)
		fieldSizeY.insert(0,100)
	mainField.place(x=140,y=20,width=size[0],height=size[1])
	makeDashedDiagonal(size[0],size[1],iteration)

def makeDashedDiagonal(sizeX,sizeY,iteration):
	global listOfLines
	x1=0
	y1=0
	x2=min(sizeX,sizeY)
	y2=min(sizeX,sizeY)
	listOfLines.append(Line([x1,y1,x2,y2],mainField.create_line(x1,y1,x2,y2,dash=(10,10)),0))
	listOfLines[-1].setDirection([(2**(1/2)/2),-(2**(1/2)/2)])
	l=((x1-x2)**(2)+(y1-y2)**(2))**(1/2)
	k=0
	while True:
		x1=listOfLines[-1].getCoords()[2]
		y1=listOfLines[-1].getCoords()[3]
		dirX=listOfLines[-1].getDirection()[0]
		dirY=listOfLines[-1].getDirection()[1]
		i=0
		number=listOfLines[-1].getNumber()+1
		listOfLines.append(Line([x1,y1,0,0],mainField.create_line(x1,y1,0,0,dash=(10,10)),number))
		listOfLines[-1].setDirection([dirX,dirY])
		while True:
			i+=1
			x2=x1+dirX*i
			y2=y1+dirY*i
			if refractionCheck(x2,y2,sizeX,sizeY,listOfLines[-1])[0]:
				#dx=refractionCheck(x2,y2,sizeX,sizeY,listOfLines[-1])[1][0]
				#dy=refractionCheck(x2,y2,sizeX,sizeY,listOfLines[-1])[1][1]
				listOfLines[-1].erase(mainField)
				listOfLines[-1].setCoords([x1,y1,x2-dirX,y2-dirY])
				listOfLines[-1].paintDash(mainField)
				break
		k+=1
		if k==iteration:				
			break

def refractionCheck(xNew,yNew,sizeX,sizeY,line):
	flag=False
	dx=0
	dy=0
	if xNew>sizeX:
		#print(0)
		dx=xNew-sizeX
		flag=True
		line.setDirection([-line.getDirection()[0],line.getDirection()[1]])
	if xNew<0:
		#print(1)
		dx=xNew
		flag=True
		line.setDirection([-line.getDirection()[0],line.getDirection()[1]])
	if yNew>sizeY:
		#print(2)
		dy=yNew-sizeY
		flag=True
		line.setDirection([line.getDirection()[0],-line.getDirection()[1]])
	if yNew<0:
		#print(3)
		dy=yNew
		flag=True
		line.setDirection([line.getDirection()[0],-line.getDirection()[1]])
	return(flag,[dx,dy])
#############################
buttonStartGeneration=Button(root,text="StartGeneration",command=startGeneration)
buttonStartGeneration.place(x=20,y=160,width=100,height=20)

buttonClear=Button(root,text="Clear",command=clear)
buttonClear.place(x=20,y=140,width=100,height=20)
#############################
root.mainloop()
