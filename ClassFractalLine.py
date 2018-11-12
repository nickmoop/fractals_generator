class Line():
    def __init__(
            self, coordsNew=[0, 0, 0, 0], itemNew='', numberNew=0,
            colorNew='black', directionNew=[0, 0]
    ):
        self.coords = coordsNew
        self.item = itemNew
        self.number = numberNew
        self.color = colorNew
        self.direction = directionNew

    def getCoords(self):
        return (self.coords)

    def getItem(self):
        return (self.item)

    def getNumber(self):
        return (self.number)

    def getColor(self):
        return (self.color)

    def getDirection(self):
        return (self.direction)

    def setCoords(self, coordsNew):
        self.coords = coordsNew

    def setItem(self, itemNew):
        self.item = itemNew

    def setNumber(self, numberNew):
        self.number = numberNew

    def setColor(self, colorNew):
        self.color = colorNew

    def setDirection(self, directionNew):
        self.direction = directionNew

    def paint(self, field):
        x1 = self.getCoords()[0]
        y1 = self.getCoords()[1]
        x2 = self.getCoords()[2]
        y2 = self.getCoords()[3]
        color = self.getColor()
        item = field.create_line(x1, y1, x2, y2, fill=color)
        self.setItem(item)

    def paintDash(self, field):
        x1 = self.getCoords()[0]
        y1 = self.getCoords()[1]
        x2 = self.getCoords()[2]
        y2 = self.getCoords()[3]
        color = self.getColor()
        item = field.create_line(x1, y1, x2, y2, fill=color, dash=(10, 10))
        self.setItem(item)

    def erase(self, field):
        field.delete(self.getItem())

    def info(self):
        print('XY=', self.coords, 'itm=', self.item)
