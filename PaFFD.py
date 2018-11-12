import urllib
from urllib.request import urlopen
import datetime
from tkinter import *
from tkinter import messagebox
import pytz
from math import *
from ClassPaFFD import Day

root=Tk()
root.resizable(False,False)
root.geometry("1270x900+0+20")

list_of_days=[]
list_of_axle=[]
list_of_lines=[]
site='http://www.gismeteo.ru/diary'
city=4225					#калининград
########################################
year=StringVar()
year.set(datetime.datetime.now().year)
field_year=Entry(root,textvariable=year)
field_year.place(x=20,y=20,width=100,height=20)

month=StringVar()
month.set(datetime.datetime.now().month)
field_month=Entry(root,textvariable=month)
field_month.place(x=20,y=40,width=100,height=20)

date=StringVar()
date.set(datetime.datetime.now().day)
field_date=Entry(root,textvariable=date)
field_date.place(x=20,y=60,width=100,height=20)

interval=StringVar()
interval.set('30')
field_interval=Entry(root,textvariable=interval)
field_interval.place(x=20,y=80,width=100,height=20)

term=StringVar()
term.set('1')
field_term=Entry(root,textvariable=term)
field_term.place(x=20,y=100,width=100,height=20)

label_year=Label(root,text="Year")
label_year.place(x=100,y=20,width=80,height=20)

label_month=Label(root,text="Month")
label_month.place(x=100,y=40,width=80,height=20)

label_date=Label(root,text="Date")
label_date.place(x=100,y=60,width=80,height=20)

label_interval=Label(root,text="Interval[day]")
label_interval.place(x=100,y=80,width=80,height=20)

label_term=Label(root,text="Term[30days]")
label_term.place(x=100,y=100,width=80,height=20)

graph_field=Canvas(root,bg="white")
graph_field.place(x=240,y=20,width=800,height=400)
########################################
def getNumber(string):
	digit=''.join(element for element in string if element.isdigit())
	if digit:
		if '-' not in string:
			return int(digit)
		else:
			return (0-int(digit))
	else:
		pass

def calcDates():#			NEED CHANGE!!!!
	global site
	global city
	now_date=datetime.datetime.now()
	start_date=now_date+datetime.timedelta(-30)
	if now_date.year-start_date.year==0:
		if now_date.month-start_date.month==0:
			print(0)
			month=now_date.month
			year=now_date.year
			page=getPage(site,city,year,month)
			formatPage(page,year,month)
		elif now_date.month-start_date.month==1:
			print(1)
			month=start_date.month
			year=start_date.year
			page=getPage(site,city,year,month)
			formatPage(page,year,month)
			month=now_date.month
			year=now_date.year
			page=getPage(site,city,year,month)
			formatPage(page,year,month)
		elif now_date.month-start_date.month==2:
			print(2)
		else:
			print('Error in calcDates.dMonth>2')
	else:
		print('Error in calcDates.dYear>0')

def getPage(site,city,year,month):
	url=str(str(site)+'/'+str(city)+'/'+str(year)+'/'+str(month)+'/')
	page=urlopen(url).read().decode()
	return(page)

def formatPage(page,year,month):
	global list_of_days
	index_start=page.find('<tr align="center">')
	index_finish=page.find('</tbody>')
	page=page[index_start+20:index_finish]
	page=page.replace('br','')
	page=page.replace('tr','')
	page=page.replace('<','')
	page=page.replace('>','')
	page=page.replace('/','')
	page=page.replace('\n','')
	page=page.replace('\t','')
	page=page.replace('\r','')
	page=page.split('td')
	for value in page:
		if 'img' in value:
			page.remove(value)
	page=str(page)
	page=page.replace("'",'')
	page=page.replace(',','')
	page=page.replace('[','')
	page=page.replace(']','')
	page=page.replace('"','')
	page=page.replace('align=center','')
	page=page.split()
	TMPLIST=[]
	for value in page:
		value_final=getNumber(str(value))
		if value_final or value_final==0:
			TMPLIST.append(value_final)
		else:
			pass
	i_max=len(TMPLIST)/5
	i=0
	while i<i_max:
		date=TMPLIST[i*5]
		temperature=[TMPLIST[i*5+1],TMPLIST[i*5+3]]
		pressure=[TMPLIST[i*5+2],TMPLIST[i*5+4]]
		day=Day(year,month,date,temperature,pressure)
		list_of_days.append(day)
		i=i+1

def start():
	global site
	global city
	global list_of_days
	clear()
	year=int(field_year.get())
	month=int(field_month.get())
	day=int(field_date.get())
	date_finish=datetime.datetime.strptime(str(month)+' '+str(day)+' '+str(year)+' 11:00','%m %d %Y %H:%M')
	term=int(field_term.get())
	date_start=date_finish+datetime.timedelta(-30*term)
	flag=True
	year=date_start.year
	month=date_start.month
	while date_finish.year!=year:
		while month<=12:
			page=getPage(site,city,year,month)
			formatPage(page,year,month)
			month=month+1
		month=1
		year=year+1
	while date_finish.month>=month:
		page=getPage(site,city,year,month)
		formatPage(page,year,month)
		month=month+1
	f=open('test.txt','w')
	for day in list_of_days:
		date=str(day.getYear())+' '+str(day.getMonth())+' '+str(day.getDate())
		temperature=str(day.getTemperature()[0])+' '+str(day.getTemperature()[1])
		pressure=str(day.getPressure()[0])+' '+str(day.getPressure()[1])
		string=date+' '+temperature+' '+pressure+'\n'
		f.write(string)
	f.close()
	makeAxles()

def getDataFromFile():
	global list_of_days
	clear()
	year=int(field_year.get())
	month=int(field_month.get())
	day=int(field_date.get())
	date_finish=datetime.datetime.strptime(str(month)+' '+str(day)+' '+str(year)+' 11:00','%m %d %Y %H:%M')
	term=int(field_term.get())
	date_start=date_finish+datetime.timedelta(-30*term)
	flag=True
	year=date_start.year
	month=date_start.month
	f=open('test.txt','r')
	for line in f:
		year=int(line.split()[0])
		month=int(line.split()[1])
		date=int(line.split()[2])
		temperature=[int(line.split()[3]),int(line.split()[4])]
		pressure=[int(line.split()[5]),int(line.split()[6])]
		day=Day(year,month,date,temperature,pressure)
		list_of_days.append(day)
	f.close()
	makeAxles()

def clear():
	global list_of_days
	global list_of_axle
	global list_of_lines
	for label in list_of_axle:
		label=Label(root,text='')
		label.place(x=0,y=0,width=0,height=0)
	for line in list_of_lines:
		graph_field.delete(line)
	list_of_lines=[]
	list_of_axle=[]
	#list_of_days=[]

def makeAxles():
	global list_of_days
	global list_of_axle
	list_of_day_temperature=[]
	list_of_night_temperature=[]
	list_of_day_pressure=[]
	list_of_night_pressure=[]
	for day in list_of_days:			
		list_of_day_temperature.append(day.getTemperature()[0])
		list_of_night_temperature.append(day.getTemperature()[1])
		list_of_day_pressure.append(day.getPressure()[0])
		list_of_night_pressure.append(day.getPressure()[1])
	day_step=len(list_of_days)/15
	day_temperature_step=(max(list_of_day_temperature)-min(list_of_day_temperature))/15
	night_temperature_step=(max(list_of_night_temperature)-min(list_of_night_temperature))/15
	day_pressure_step=(max(list_of_day_pressure)-min(list_of_day_pressure))/15
	night_pressure_step=(max(list_of_night_pressure)-min(list_of_night_pressure))/15
	for i in range(0,15):
		k=int(i*day_step)
		axle_time_title=str(list_of_days[k].getDate())+'.'+str(list_of_days[k].getMonth())
		label_axle_time=Label(root,text=axle_time_title)
		label_axle_time.place(x=240+800/15*i,y=420,width=30,height=20)
		day_temperature=str(round(min(list_of_day_temperature)+day_temperature_step*i,1))
		night_temperature=str(round(min(list_of_night_temperature)+night_temperature_step*i,1))
		day_pressure=str(round(min(list_of_day_pressure)+day_pressure_step*i,1))
		night_pressure=str(round(min(list_of_night_pressure)+night_pressure_step*i,1))
		axle_function_title=str(day_temperature+' '+night_temperature+' '+day_pressure+' '+night_pressure)
		label_axle_function=Label(root,text=axle_function_title)
		label_axle_function.place(x=1040,y=400-400/15*i,width=150,height=20)
		list_of_axle.append(label_axle_time)
		list_of_axle.append(label_axle_function)

def makeGraphTDay():
	global list_of_days
	global list_of_lines
	step_x=800/(len(list_of_days))
	list_of_day_temperature=[]
	for day in list_of_days:
		list_of_day_temperature.append(day.getTemperature()[0])
	TMP=max(list_of_day_temperature)-min(list_of_day_temperature)
	for day in list_of_days:	
		try:
			x1=step_x*list_of_days.index(day)
			y1=400-(day.getTemperature()[0]-min(list_of_day_temperature)+0.0001)/TMP*400
			x2=step_x*(list_of_days.index(day)+1)
			y2=400-(list_of_days[list_of_days.index(day)+1].getTemperature()[0]-min(list_of_day_temperature)+0.0001)/TMP*400
			line=graph_field.create_line(x1,y1,x2,y2,fill='red')
			list_of_lines.append(line)
		except:
			pass

def makeGraphFDTDay():
	global list_of_days
	global list_of_lines
	interval=int(field_interval.get())
	list_of_squares=[]
	list_of_day_temperature_fractal=[]
	for i in range(0,len(list_of_days)):
		try:
			list_of_squares.append(abs(list_of_days[i].getTemperature()[0]-list_of_days[i+1].getTemperature()[0]))
		except:
			pass
			#print('Error in makeGraphFDTDay().End of list')
	for i in range(0,len(list_of_squares)-interval+1):
		summ=0
		for j in range(0,interval):
			summ=summ+list_of_squares[i+j]
		#list_of_days[interval+i].setTemperatureFractal(log(summ),'day')
		list_of_day_temperature_fractal.append(log(summ))
	for i in range(0,len(list_of_day_temperature_fractal)-1):
		fractal_dimension=(list_of_day_temperature_fractal[i+1]-list_of_day_temperature_fractal[i])/(log(interval+i+1)-log(interval+i))
		list_of_days[interval+i].setTemperatureFractal(fractal_dimension,'day')
	step_x=800/(len(list_of_days))
	step_y_fractal=400/(max(list_of_day_temperature_fractal))
	for i in range(0,len(list_of_day_temperature_fractal)):
		try:
			x1=step_x*(i+interval)
			y1=600-step_y_fractal*list_of_day_temperature_fractal[i]
			x2=step_x*(i+interval+1)
			y2=600-step_y_fractal*list_of_day_temperature_fractal[i+1]
			line=graph_field.create_line(x1,y1,x2,y2,fill='blue')
			list_of_lines.append(line)
		except:
			pass
	

def makeGraphTNight():
	global list_of_days
	global list_of_lines
	step_x=800/(len(list_of_days))
	list_of_night_temperature=[]
	for day in list_of_days:
		list_of_night_temperature.append(day.getTemperature()[1])
	TMP=max(list_of_night_temperature)-min(list_of_night_temperature)
	for day in list_of_days:	
		try:
			x1=step_x*list_of_days.index(day)
			y1=400-(day.getTemperature()[1]-min(list_of_night_temperature)+0.0001)/TMP*400
			x2=step_x*(list_of_days.index(day)+1)
			y2=400-(list_of_days[list_of_days.index(day)+1].getTemperature()[1]-min(list_of_night_temperature)+0.0001)/TMP*400
			line=graph_field.create_line(x1,y1,x2,y2,fill='blue')
			list_of_lines.append(line)
		except:
			pass

def makeGraphPDay():
	global list_of_days
	global list_of_lines
	step_x=800/(len(list_of_days))
	list_of_day_pressure=[]
	for day in list_of_days:
		list_of_day_pressure.append(day.getPressure()[0])
	TMP=max(list_of_day_pressure)-min(list_of_day_pressure)
	for day in list_of_days:	
		try:
			x1=step_x*list_of_days.index(day)
			y1=400-(day.getPressure()[0]-min(list_of_day_pressure)+0.0001)/TMP*400
			x2=step_x*(list_of_days.index(day)+1)
			y2=400-(list_of_days[list_of_days.index(day)+1].getPressure()[0]-min(list_of_day_pressure)+0.0001)/TMP*400
			line=graph_field.create_line(x1,y1,x2,y2,fill='red')
			list_of_lines.append(line)
		except:
			pass

def makeGraphPNight():
	global list_of_days
	global list_of_lines
	step_x=800/(len(list_of_days))
	list_of_night_pressure=[]
	for day in list_of_days:
		list_of_night_pressure.append(day.getPressure()[1])
	TMP=max(list_of_night_pressure)-min(list_of_night_pressure)
	for day in list_of_days:	
		try:
			x1=step_x*list_of_days.index(day)
			y1=400-(day.getPressure()[1]-min(list_of_night_pressure)+0.0001)/TMP*400
			x2=step_x*(list_of_days.index(day)+1)
			y2=400-(list_of_days[list_of_days.index(day)+1].getPressure()[1]-min(list_of_night_pressure)+0.0001)/TMP*400
			line=graph_field.create_line(x1,y1,x2,y2,fill='blue')
			list_of_lines.append(line)
		except:
			pass

def makeGraphFDTNight():
	global list_of_days
	global list_of_lines
	interval=int(field_interval.get())
	list_of_squares=[]
	list_of_night_temperature_fractal=[]
	for i in range(0,len(list_of_days)):
		try:
			list_of_squares.append(abs(list_of_days[i].getTemperature()[1]-list_of_days[i+1].getTemperature()[1]))
		except:
			pass
	for i in range(0,len(list_of_squares)-interval+1):
		summ=0
		for j in range(0,interval):
			summ=summ+list_of_squares[i+j]
		list_of_night_temperature_fractal.append(log(summ))
	for i in range(0,len(list_of_night_temperature_fractal)-1):
		fractal_dimension=(list_of_night_temperature_fractal[i+1]-list_of_night_temperature_fractal[i])/(log(interval+i+1)-log(interval+i))
		list_of_days[interval+i].setTemperatureFractal(fractal_dimension,'night')
	step_x=800/(len(list_of_days))
	step_y_fractal=400/(max(list_of_night_temperature_fractal))
	for i in range(0,len(list_of_night_temperature_fractal)):
		try:
			x1=step_x*(i+interval)
			y1=600-step_y_fractal*list_of_night_temperature_fractal[i]
			x2=step_x*(i+interval+1)
			y2=600-step_y_fractal*list_of_night_temperature_fractal[i+1]
			line=graph_field.create_line(x1,y1,x2,y2,fill='red')
			list_of_lines.append(line)
		except:
			pass

def makeGraphStraightLine():
	global list_of_lines
	interval=int(field_interval.get())
	list_of_squares=[]
	list_of_values=[]
	list_of_values_fractal=[]
	for i in range(0,100):
		list_of_values.append(i)
	for i in range(0,len(list_of_values)):
		try:
			list_of_squares.append(abs(list_of_values[i]-list_of_values[i+1]))
		except:
			pass
	for i in range(0,len(list_of_squares)-interval+1):
		summ=0
		for j in range(0,interval):
			summ=summ+list_of_squares[i+j]
		list_of_values_fractal.append(log(summ))
	for i in range(0,len(list_of_values_fractal)-1):
		fractal_dimension=(list_of_values_fractal[i+1]-list_of_values_fractal[i])/(log(interval+i+1)-log(interval+i))
		print(fractal_dimension)
	step_x=800/(len(list_of_values))
	step_y=400/(len(list_of_values))
	step_y_fractal=400/(max(list_of_values_fractal))
	for value in list_of_values:
		try:
			x1=step_x*list_of_values.index(value)
			y1=400-step_y*list_of_values.index(value)
			x2=step_x*(list_of_values.index(value)+1)
			y2=400-step_y*(list_of_values.index(value)+1)
			line=graph_field.create_line(x1,y1,x2,y2,fill='red')
			list_of_lines.append(line)
			if list_of_values.index(value)>=interval:
				y1=700-step_y_fractal*list_of_values_fractal[(list_of_values.index(value)-interval)]
				y2=700-step_y_fractal*list_of_values_fractal[(list_of_values.index(value)+1-interval)]
				line=graph_field.create_line(x1,y1,x2,y2,fill='red')
				list_of_lines.append(line)
		except:
			pass

def makeGraphParaLine():
	global list_of_lines
	interval=int(field_interval.get())
	list_of_squares=[]
	list_of_values=[]
	list_of_values_fractal=[]
	for i in range(-100,100):
		list_of_values.append(5*i*i+3*i)
	#print(list_of_values)
	for i in range(0,len(list_of_values)):
		try:
			list_of_squares.append(abs(list_of_values[i]-list_of_values[i+1]))
		except:
			pass
	#print(list_of_squares)
	for i in range(0,len(list_of_squares)-interval+1):
		summ=0
		for j in range(0,interval):
			summ=summ+list_of_squares[i+j]
		list_of_values_fractal.append(log(summ))
	#print(list_of_values_fractal)
	for i in range(0,len(list_of_values_fractal)-1):
		try:
			#sin=list_of_values_fractal[i+1]-list_of_values_fractal[i]
			#cos=log((i+1)*interval)-log(i*interval)
			#print("cos=",cos,"sin=",sin)
			logNTmp=list_of_values_fractal[i]
			logDeltaTmp=1/log(i*interval)
			#fractal_dimension=sin/cos
			fractal_dimension=logNTmp/logDeltaTmp
			print(fractal_dimension)
		except:
			pass
			#print("k=",k)
	step_x=800/(len(list_of_values))
	step_y=400/(max(list_of_values))
	step_y_fractal=400/(max(list_of_values_fractal))
	for value in list_of_values:
		try:
			x1=step_x*list_of_values.index(value)
			y1=400-step_y*value
			x2=step_x*(list_of_values.index(value)+1)
			y2=400-step_y*list_of_values[(list_of_values.index(value)+1)]
			line=graph_field.create_line(x1,y1,x2,y2,fill='green')
			list_of_lines.append(line)
			if list_of_values.index(value)>=interval:
				y1=500-step_y_fractal*list_of_values_fractal[(list_of_values.index(value)-interval)]
				y2=500-step_y_fractal*list_of_values_fractal[(list_of_values.index(value)+1-interval)]
				line=graph_field.create_line(x1,y1,x2,y2,fill='green')
				list_of_lines.append(line)
		except:
			pass

def makeGraphFDPDay():
	global list_of_days
	global list_of_lines
	interval=int(field_interval.get())
	list_of_squares=[]
	list_of_day_pressure_fractal=[]
	for i in range(0,len(list_of_days)):
		try:
			list_of_squares.append(abs(list_of_days[i].getPressure()[0]-list_of_days[i+1].getPressure()[0]))
		except:
			pass
	for i in range(0,len(list_of_squares)-interval+1):
		summ=0
		for j in range(0,interval):
			summ=summ+list_of_squares[i+j]
		list_of_day_pressure_fractal.append(log(summ))
	for i in range(0,len(list_of_day_pressure_fractal)-1):
		fractal_dimension=(list_of_day_pressure_fractal[i+1]-list_of_day_pressure_fractal[i])/(log(interval+i+1)-log(interval+i))
		list_of_days[interval+i].setPressureFractal(fractal_dimension,'day')
	step_x=800/(len(list_of_days))
	step_y_fractal=400/(max(list_of_day_pressure_fractal))
	for i in range(0,len(list_of_day_pressure_fractal)):
		try:
			x1=step_x*(i+interval)
			y1=600-step_y_fractal*list_of_day_pressure_fractal[i]
			x2=step_x*(i+interval+1)
			y2=600-step_y_fractal*list_of_day_pressure_fractal[i+1]
			line=graph_field.create_line(x1,y1,x2,y2,fill='blue')
			list_of_lines.append(line)
		except:
			pass

def makeGraphFDPNight():
	global list_of_days
	global list_of_lines
	interval=int(field_interval.get())
	list_of_squares=[]
	list_of_night_pressure_fractal=[]
	for i in range(0,len(list_of_days)):
		try:
			list_of_squares.append(abs(list_of_days[i].getPressure()[1]-list_of_days[i+1].getPressure()[1]))
		except:
			pass
	for i in range(0,len(list_of_squares)-interval+1):
		summ=0
		for j in range(0,interval):
			summ=summ+list_of_squares[i+j]
		list_of_night_pressure_fractal.append(log(summ))
	for i in range(0,len(list_of_night_pressure_fractal)-1):
		fractal_dimension=(list_of_night_pressure_fractal[i+1]-list_of_night_pressure_fractal[i])/(log(interval+i+1)-log(interval+i))
		list_of_days[interval+i].setPressureFractal(fractal_dimension,'night')
	step_x=800/(len(list_of_days))
	step_y_fractal=400/(max(list_of_night_pressure_fractal))
	for i in range(0,len(list_of_night_pressure_fractal)):
		try:
			x1=step_x*(i+interval)
			y1=600-step_y_fractal*list_of_night_pressure_fractal[i]
			x2=step_x*(i+interval+1)
			y2=600-step_y_fractal*list_of_night_pressure_fractal[i+1]
			line=graph_field.create_line(x1,y1,x2,y2,fill='red')
			list_of_lines.append(line)
		except:
			pass
########################################
button_start=Button(root,text="Start",command=start)
button_start.place(x=20,y=120,width=80,height=20)

button_clear=Button(root,text="Clear",command=clear)
button_clear.place(x=20,y=140,width=80,height=20)

button_make_graph=Button(root,text="T.Day",command=makeGraphTDay)
button_make_graph.place(x=20,y=160,width=80,height=20)

button_make_graph=Button(root,text="T.Night",command=makeGraphTNight)
button_make_graph.place(x=20,y=180,width=80,height=20)

button_make_graph=Button(root,text="P.Day",command=makeGraphPDay)
button_make_graph.place(x=20,y=200,width=80,height=20)

button_make_graph=Button(root,text="P.Night",command=makeGraphPNight)
button_make_graph.place(x=20,y=220,width=80,height=20)

button_from_file=Button(root,text="From file",command=getDataFromFile)
button_from_file.place(x=20,y=240,width=80,height=20)

button_start=Button(root,text="Str.line",command=makeGraphStraightLine)
button_start.place(x=100,y=120,width=80,height=20)

button_clear=Button(root,text="Para.line",command=makeGraphParaLine)
button_clear.place(x=100,y=140,width=80,height=20)

button_make_graph=Button(root,text="F.D.T.Day",command=makeGraphFDTDay)
button_make_graph.place(x=100,y=160,width=80,height=20)

button_make_graph=Button(root,text="F.D.T.Night",command=makeGraphFDTNight)
button_make_graph.place(x=100,y=180,width=80,height=20)

button_make_graph=Button(root,text="F.D.P.Day",command=makeGraphFDPDay)
button_make_graph.place(x=100,y=200,width=80,height=20)

button_make_graph=Button(root,text="F.D.P.Night",command=makeGraphFDPNight)
button_make_graph.place(x=100,y=220,width=80,height=20)
########################################
root.mainloop()
