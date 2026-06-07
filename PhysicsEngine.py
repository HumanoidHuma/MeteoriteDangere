# class PhysicsEngine:
#     gravity = 9.81
#
#     earth_son_mass = 333000
#     earth_son_v = 109
#
#
#     def __init__(self):
#         self.gravity = True
#
#     def simulate_on_time(self, phy_objects: list[PhyObject], dt: float):
#         for phy_obj in phy_objects:
#             ax = 0
#             ay = 0
#
#             if (self.gravity):
#                 ay += PhysicsEngine.gravity
#
#             phy_obj.setX(phy_obj.getX() + phy_obj.getVx() * dt + (ax * (dt**2)) / 2)
#             phy_obj.setY(phy_obj.getY() + phy_obj.getVy() * dt + (ay * (dt**2)) / 2)
#
#             phy_obj.setVx(phy_obj.getVx() + ax * dt)
#             phy_obj.setVy(phy_obj.getVy() + ay * dt)






#
#
from PhyObject import *
import math


class PhysicsEngine:

    G = 1.0

    earth_son_mass = 333000

    def simulate_on_time(self,
                         phy_objects: list[PhyObject],
                         dt: float):

        accelerations = []

        # ------------------------------------
        # вычисляем ускорения
        # ------------------------------------

        for obj in phy_objects:

            ax = 0.0
            ay = 0.0

            for other in phy_objects:

                if obj is other:
                    continue

                dx = other.getX() - obj.getX()
                dy = other.getY() - obj.getY()

                r2 = dx * dx + dy * dy

                if r2 < 0.0001:
                    continue

                r = math.sqrt(r2)

                a = PhysicsEngine.G * other.getMass() / r2

                ax += a * dx / r
                ay += a * dy / r

            accelerations.append((ax, ay))

        # ------------------------------------
        # обновляем скорости
        # ------------------------------------

        for i in range(len(phy_objects)):

            obj = phy_objects[i]

            ax, ay = accelerations[i]

            obj.setVx(
                obj.getVx() + ax * dt
            )

            obj.setVy(
                obj.getVy() + ay * dt
            )

        # ------------------------------------
        # обновляем координаты
        # ------------------------------------

        for obj in phy_objects:

            obj.setX(
                obj.getX() + obj.getVx() * dt
            )

            obj.setY(
                obj.getY() + obj.getVy() * dt
            )




