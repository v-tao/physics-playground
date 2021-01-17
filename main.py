import math
#input angle, velocity, and time output position
def kinematics_2d(theta, v_initial, t, g=-9.813):
    theta = theta * (math.pi/180)
    vx_initial = v_initial*math.cos(theta)
    vy_initial = v_initial*math.sin(theta)
    x = vx_initial*t
    y = vy_initial*t+0.5*g*(t**2)
    vx_final = vx_initial
    vy_final = vy_initial + g*t
    if y < 0:
        y = 0
    print("Displacement: " + str((x, y)))
    print("Final Velocity: " + str((vx_final, vy_final)))
    return (x,y, vx_final, vy_final)

kinematics_2d(60, 30, 3)
