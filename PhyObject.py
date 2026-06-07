# class PhyObject:
#     def __init__(self, mass: float, x: float, y : float, Vx: float, Vy: float):
#         self.mass = mass
#         self.x = x
#         self.y = y
#         self.Vx = Vx
#         self.Vy = Vy
#
#     def getMass(self):
#         return self.mass
#
#     def __setstate__(self, new_mass: float):
#         self.mass = new_mass
#
#     def getVx(self):
#         return self.Vx
#
#     def getVy(self):
#         return self.Vy
#
#     def setVx(self, new_Vx: float):
#         self.Vx = new_Vx
#
#     def setVy(self, new_Vy: float):
#         self.Vy = new_Vy
#
#     def setX(self, new_x: float):
#         self.x = new_x
#
#     def setY(self, new_y: float):
#         self.y = new_y
#
#     def getX(self):
#         return self.x
#
#     def getY(self):
#         return self.y

class PhyObject:

    def __init__(
            self,
            mass: float,
            x: float,
            y: float,
            Vx: float,
            Vy: float,
            density: float = 1.0,
            obj_type: str = "meteor"
    ):

        self.mass = mass

        self.x = x
        self.y = y

        self.Vx = Vx
        self.Vy = Vy

        self.density = density

        # "sun", "earth", "meteor"
        self.obj_type = obj_type

    # ==================================
    # Масса
    # ==================================

    def getMass(self):
        return self.mass

    def setMass(self, new_mass):
        self.mass = new_mass

    # ==================================
    # Координаты
    # ==================================

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, new_x):
        self.x = new_x

    def setY(self, new_y):
        self.y = new_y

    # ==================================
    # Скорости
    # ==================================

    def getVx(self):
        return self.Vx

    def getVy(self):
        return self.Vy

    def setVx(self, new_vx):
        self.Vx = new_vx

    def setVy(self, new_vy):
        self.Vy = new_vy

    # ==================================
    # Плотность
    # ==================================

    def getDensity(self):
        return self.density

    def setDensity(self, density):
        self.density = density

    # ==================================
    # Тип объекта
    # ==================================

    def getType(self):
        return self.obj_type

    # ==================================
    # Геометрия
    # ==================================

    def getVolume(self):

        return self.mass / self.density

    def getRadius(self):

        volume = self.getVolume()

        return volume ** (1 / 3)