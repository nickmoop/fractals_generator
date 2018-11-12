class Point():

	def __init__(self,coordsNew=[0,0],itemNew='',numberNew=0,checkNew=True,colorNew='black'):
		self.coords=coordsNew
		self.item=itemNew
		self.number=numberNew
		self.check=checkNew
		self.color=colorNew

	def getCoords(self):
		return(self.coords)

	def getItem(self):
		return(self.item)

	def getNumber(self):
		return(self.number)
	
	def getCheck(self):
		return(self.check)

	def getColor(self):
		return(self.color)

	def setCoords(self,coordsNew):
		self.coords=coordsNew

	def setItem(self,itemNew):
		self.item=itemNew

	def setNumber(self,numberNew):
		self.number=numberNew

	def setCheck(self,moveNew):
		self.check=checkNew

	def setColor(self,colorNew):		
		self.color=colorNew

	def paint(self,field):
		x=self.getCoords()[0]
		y=self.getCoords()[1]
		color=self.getColor()
		item=field.create_oval(x-5,y-5,x+5,y+5,fill=color,outline=color)
		self.setItem(item)

	def erase(self,field):
		field.delete(self.getItem())

	def info(self):
		print('XY=',self.coords,'itm=',self.item)
