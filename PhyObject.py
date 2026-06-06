class PhyObject:
    def __init__(self, mass: float, x: float, y : float, Vx: float, Vy: float):
        self.mass = mass
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy

    def getMass(self):
        return self.mass

    def __setstate__(self, new_mass: float):
        self.mass = new_mass

    def getVx(self):
        return self.Vx

    def getVy(self):
        return self.Vy

    def setVx(self, new_Vx: float):
        self.Vx = new_Vx

    def setVy(self, new_Vy: float):
        self.Vy = new_Vy

    def setX(self, new_x: float):
        self.x = new_x

    def setY(self, new_y: float):
        self.y = new_y

    def getX(self):
        return self.x

    def getY(self):
        return self.y