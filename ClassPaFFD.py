class Day():
	
	def __init__(self,year_new=0,month_new=0,date_new=0,temperature_new=[0,0],pressure_new=[0,0],temperature_fractal_new=[0,0],pressure_fractal_new=[0,0]):
		self.year=year_new
		self.month=month_new
		self.date=date_new
		self.temperature=temperature_new
		self.pressure=pressure_new
		self.temperature_fractal=temperature_fractal_new
		self.pressure_fractal=pressure_fractal_new

	def getYear(self):
		return(self.year)

	def getMonth(self):
		return(self.month)

	def getDate(self):
		return(self.date)

	def getTemperature(self):
		return(self.temperature)

	def getPressure(self):
		return(self.pressure)

	def getTemperatureFractal(self):
		return(self.temperature_fractal)

	def getPressureFractal(self):
		return(self.pressure_fractal)

	def setYear(self,year_new):
		self.year=year_new

	def setMonth(self,month_new):
		self.month=month_new

	def setDate(self,date_new):
		self.date=date_new

	def setTemperature(self,temperature_new):
		self.temperature=temperature_new

	def setPressure(self,pressure_new):		
		self.pressure=pressure_new

	def setTemperatureFractal(self,temperature_fractal_new,param):
		if param=='day':
			self.temperature_fractal[0]=temperature_fractal_new
			#print('add',temperature_fractal_new)
		if param=='night':
			self.temperature_fractal[1]=temperature_fractal_new
			#print('add',temperature_fractal_new)

	def setPressureFractal(self,pressure_fractal_new,param):
		if param=='day':
			self.pressure_fractal[0]=pressure_fractal_new
		if param=='night':
			self.pressure_fractal[1]=pressure_fractal_new

	def info(self):
		print('date=',self.year,':',self.month,':',self.date,'temperature(d/n)=',self.temperature[0],'/', self.temperature[1],'pressure(d/n)=',self.pressure[0],'/',self.pressure[1])

if __name__=='__main__':
	day1=Day(2015,2,1,[3,4],[500,600])
	day1.info()
