import math
#input angle, velocity, and time output position
def kinematics_2d(theta, v, t, g=-9.813):
    theta = theta * (math.pi/180)
    x = v*math.cos(theta)*t
    y = v*math.sin(theta)*t+0.5*g*(t**2)
    print(x,y)
    return (x,y)

kinematics_2d(60, 30, 3)
