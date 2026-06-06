from PhyObject import *

class PhysicsEngine:
    gravity = 9.81

    def __init__(self):
        self.gravity = True

    def simulate_on_time(self, phy_objects: list[PhyObject], dt: float):
        for phy_obj in phy_objects:
            ax = 0
            ay = 0

            if (self.gravity):
                ay += PhysicsEngine.gravity

            phy_obj.setX(phy_obj.getVx() * dt + (ax * (dt**2)) / 2)
            phy_obj.setY(phy_obj.getVy() * dt + (ay * (dt**2)) / 2)

            phy_obj.setVx(phy_obj.getVx() + ax * dt)
            phy_obj.setVy(phy_obj.getVy() + ay * dt)