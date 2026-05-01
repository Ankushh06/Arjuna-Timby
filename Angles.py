import math

class turret:
    def __init__(self, obj_x, obj_y, obj_z):
        self.obj_x = obj_x
        self.obj_y = obj_y
        self.obj_z = obj_z

    def offsets(self, offs_x=0, offs_y=0, offs_z=0):
        self.offs_x = offs_x
        self.offs_y = offs_y
        self.offs_z = offs_z

    def getAngles(self):
        self.z_fromTurret = self.obj_z - self.offs_z

        if self.z_fromTurret == 0:
            self.z_fromTurret = 0.1

        # X axis
        if self.obj_x >= 0:
            x = abs(self.obj_x) + self.offs_x
            theta_x = 90 + math.degrees(math.atan2(x, self.z_fromTurret))
        else:
            x = max(0.1, abs(self.obj_x) - self.offs_x)
            theta_x = 90 - math.degrees(math.atan2(x, self.z_fromTurret))

        # Y axis
        if self.obj_y >= 0:
            y = max(0.1, abs(self.obj_y) - self.offs_y)
            theta_y = 90 - math.degrees(math.atan2(y, self.z_fromTurret))
        else:
            y = abs(self.obj_y) + self.offs_y
            theta_y = 90 + math.degrees(math.atan2(y, self.z_fromTurret))

        self.theta_x = theta_x
        self.theta_y = theta_y

    def getTheta_x(self):
        return self.theta_x

    def getTheta_y(self):
        return self.theta_y