#на входе 2 файла тхт, отдельно х, отдельно у.в каждом по 21 элементу(пока так для проверки)
#программа запускается, рисует график и всё.больше(пока) ни на что не способна
import math
from tkinter import *

root=Tk()
root.resizable(False,False)
root.geometry("856x912+0+20")
######									PAINT FIELD
mainField=Canvas(root,bg='white')
mainField.place(x=50,y=50,width=600,height=600)
######									
fileToRead=open('inputY.txt')
tmpY=fileToRead.read().splitlines()
fileToRead=open('inputX.txt')
tmpX=fileToRead.read().splitlines()
lengthX=len(tmpX)
lengthY=len(tmpY)
listX=[]
listY=[]
listAverageValueFirst=[]
listAverageValueSecond=[]
listAverageValueThird=[]
listAverageValueFourth=[]
listAverageValueFifth=[]
listAverageValueSixth=[]
xStep=[0,0,0]
length=[0,0,0,0,0,0,0]

if lengthX!=lengthY:
	print("lengthX!=lengthY")
else:	
	for i in range(0,lengthX):
		listX.append(float(tmpX[i]))
		listY.append(float(tmpY[i]))
######									AVERAGING START!!!!
def averagingFirst(listY):
	global listAverageValueFirst
	length=len(listY)
	for i in range(1,length):
		listAverageValueFirst.append((listY[i-1]+listY[i])/2)

def averagingSecond(listY):
	global listAverageValueSecond
	length=math.ceil(len(listY)/2)
	for i in range(1,length):
		listAverageValueSecond.append((listY[2*i-2]+listY[2*i-1])/2)

def averagingThird(listY):
	global listAverageValueThird
	length=math.ceil(len(listY)/2)
	for i in range(1,length):
		listAverageValueThird.append((listY[2*i-1]+listY[2*i])/2)

def averagingFourth(listY):
	global listAverageValueFourth
	length=math.ceil(len(listY)/3)
	for i in range(1,length):
		listAverageValueFourth.append((listY[3*i-3]+listY[3*i-2]+listY[3*i-1])/3)

def averagingFifth(listY):
	global listAverageValueFifth
	length=math.ceil(len(listY)/3)
	for i in range(1,length):
		listAverageValueFifth.append((listY[3*i-2]+listY[3*i-1]+listY[3*i])/3)

def averagingSixth(listY):
	global listAverageValueSixth
	length=math.ceil(len(listY)/3)
	for i in range(1,length):
		listAverageValueSixth.append((listY[3*i-1]+listY[3*i]+listY[3*i+1])/3)
######									AVERAGING FINISH!!!!
def findAllXStep(listX):				#stupid func name??
	global xStep1
	global xStep2
	global xStep3
	xStep[0]=listX[::]
	xStep[1]=listX[::2]
	xStep[2]=listX[::3]
	xStep[0].pop()
	xStep[1].pop()
	xStep[2].pop()

def findLength(listX,listY):
	length=len(listX)
	lineLength=0
	for i in range(1,length):
		#listLineLength.append(((listX[i]-listX[i-1])**2+(listY[i]-listY[i-1])**2)**(1/2))
		lineLength=((listX[i]-listX[i-1])**2+(listY[i]-listY[i-1])**2)**(1/2)+lineLength
	return(lineLength)
######									MAIN PROGRAMM START!!!!
averagingFirst(listY)
averagingSecond(listY)
averagingThird(listY)
averagingFourth(listY)
averagingFifth(listY)
averagingSixth(listY)

findAllXStep(listX)

length[0]=findLength(listX,listY)
length[1]=findLength(xStep[0],listAverageValueFirst)
length[2]=findLength(xStep[1],listAverageValueSecond)
length[3]=findLength(xStep[1],listAverageValueThird)
length[4]=findLength(xStep[2],listAverageValueFourth)
length[5]=findLength(xStep[2],listAverageValueFifth)
length[6]=findLength(xStep[2],listAverageValueSixth)
maxY=max(length)
minY=min(length)
maxX=len(xStep[0])
minX=len(xStep[2])
lenY=maxY-minY
lenX=maxX-minX
######									MAIN PROGRAMM FINISH!!!!
######									CREATE GRAPH START!!!!
for i in range(0,11):
	lineGridX=mainField.create_line(0,i*60,600,i*60,fill='black')
	lineGridY=mainField.create_line(i*60,0,i*60,600,fill='black')
	textX=str(round(lenX/10*i+minX,1))
	axleX=Label(root,text=textX)
	axleX.place(x=59*i+30,y=660,width=50,height=40)
	textY=str(round(lenY/10*i+minY,1))
	axleY=Label(root,text=textY)
	axleY.place(x=0,y=595-59*i+30,width=50,height=40)

#print(len(xStep[0]),length[0],'\n',len(xStep[0]),length[1],'\n',len(xStep[1]),length[2],'\n',len(xStep[1]),length[3],'\n',len(xStep[2]),length[4],'\n',len(xStep[2]),length[5],'\n',len(xStep[2]),length[6],'\n')

#print(lenX,lenY)

y1=600-(length[1]-minY)/lenY*600
y0=600-(length[0]-minY)/lenY*600
x1=(len(xStep[0])-minX)/lenX*600
x0=(len(xStep[0])-minX)/lenX*600
line=mainField.create_line(x0,y0,x1,y1,fill='red')
#print(x0,x1,y0,y1)
y1=600-(length[2]-minY)/lenY*600
y0=600-(length[1]-minY)/lenY*600
x1=(len(xStep[1])-minX)/lenX*600
x0=(len(xStep[0])-minX)/lenX*600
line=mainField.create_line(x0,y0,x1,y1,fill='red')
#print(x0,x1,y0,y1)
y1=600-(length[3]-minY)/lenY*600
y0=600-(length[2]-minY)/lenY*600
x1=(len(xStep[1])-minX)/lenX*600
x0=(len(xStep[1])-minX)/lenX*600
line=mainField.create_line(x0,y0,x1,y1,fill='red')
#print(x0,x1,y0,y1)
y1=600-(length[4]-minY)/lenY*600
y0=600-(length[3]-minY)/lenY*600
x1=(len(xStep[2])-minX)/lenX*600
x0=(len(xStep[1])-minX)/lenX*600
line=mainField.create_line(x0,y0,x1,y1,fill='red')
#print(x0,x1,y0,y1)
y1=600-(length[5]-minY)/lenY*600
y0=600-(length[4]-minY)/lenY*600
x1=(len(xStep[2])-minX)/lenX*600
x0=(len(xStep[2])-minX)/lenX*600
line=mainField.create_line(x0,y0,x1,y1,fill='red')
#print(x0,x1,y0,y1)
y1=600-(length[6]-minY)/lenY*600
y0=600-(length[5]-minY)/lenY*600
x1=(len(xStep[2])-minX)/lenX*600
x0=(len(xStep[2])-minX)/lenX*600
line=mainField.create_line(x0,y0,x1,y1,fill='red')
#print(x0,x1,y0,y1)

######									CREATE GRAPH FINISH!!!!
root.mainloop()
