import arcade
import math
import time

S_WIDTH = S_HEIGHT = 600

class Ball:
    def __init__(self, s_x, s_y, r, clr):
        self.start_x = s_x
        self.start_y = s_y
        self.x = s_x
        self.y = s_y
        self.r = r
        self.color = clr
        self.stopped = True
        self.v0 = 0
        self.theta0 = 0

class Game(arcade.Window):

    def __init__(self, width, height, pixels_per_meter=20):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.shapes = []
        self.proj = None
        self.started = False
        self.start_time = 0
        self.pixels_per_meter = pixels_per_meter
        #fullscreen, totally did not copy and paste from docs
        # width, height = self.get_size()
        # self.set_viewport(0, width, 0, height)
        # self.set_fullscreen(True),
        self.mouse_x = 0
        self.mouse_y = 0
        self.launched = False

    def setup(self):
        self.shapes = []
        proj = Ball(100, 100, 10, (0, 0, 0))
        self.shapes.append(proj)
        self.proj = proj
        #self.started = True
        #self.start_time = time.time()

    def on_draw(self):
        arcade.start_render()

        for s in self.shapes:
            arcade.draw_circle_filled(s.x, s.y, s.r, s.color)
            
        if not self.launched:
            self.draw_vector(self.proj.x, self.proj.y, self.mouse_x, self.mouse_y, (255, 0, 0), "m/s")

    def to_pixels(self, x):
        return x * self.pixels_per_meter

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.launched or button is not arcade.MOUSE_BUTTON_LEFT:
            return
        v0 = (1/self.pixels_per_meter) * math.sqrt((x-self.proj.x)**2 + (y-self.proj.y)**2)
        theta = self.get_angle(self.proj.x, self.proj.y, x, y)
        
        self.proj.v0 = v0
        self.proj.theta0 = theta
        self.proj.stopped = False
        self.launched = True
        self.started = True
        self.start_time = time.time()

    def draw_vector(self, s_x, s_y, e_x, e_y, color, units, scale=None):
        if scale is None:
            scale = 1/self.pixels_per_meter
        arcade.draw_line(s_x, s_y, e_x, e_y, color, 3)

        #Finding label
        label_num = round(scale * math.sqrt((e_x-s_x)**2 + (e_y-s_y)**2), 2)
        label = str(label_num) + " " + units
        
        #Drawing label
        theta = self.get_angle(s_x, s_y, e_x, e_y)
        #Vector math to make text appear above line instead of in it
        #There is almost certainly a better way to do this
        mid = ((s_x+e_x)/2, (s_y+e_y)/2)
        mid_x = (s_x+e_x)/2
        mid_y = (s_y+e_y)/2
        t_height = 14
        v = [e_y-s_y,s_x-e_x]
        mag = math.sqrt(v[0]**2+v[1]**2)
        u = [i/mag for i in v]
        t_x, t_y = mid_x - t_height*u[0], mid_y - t_height*u[1]
        arcade.draw_text(label, t_x, t_y, (0, 0, 0), t_height, width=200, align="center", anchor_x="center", anchor_y="center", rotation=theta)

        #Arrow head
        ll = [e_x-s_x, e_y-s_y]
        mag_ll = math.sqrt(ll[0]**2+ll[1]**2)
        u_ll = [i/mag_ll for i in ll]

        s = 5
        p1x, p1y = e_x + s*u[0], e_y + s*u[1]
        p2x, p2y = e_x - s*u[0], e_y - s*u[1]
        p3x, p3y = e_x + 2*s*u_ll[0], e_y + 2*s*u_ll[1]
        arcade.draw_triangle_filled(p1x, p1y, p2x, p2y, p3x, p3y, color)

        #Angle
        theta_label = str(round(theta, 2)) + u'\N{DEGREE SIGN}'
        arcade.draw_text(theta_label, s_x, s_y - self.proj.r - t_height, (0, 0, 0), t_height, width=200, align="center", anchor_x="center", anchor_y="center")
        return (label_num, theta)


    def get_angle(self, s_x, s_y, e_x, e_y):
        if e_x == s_x:
            if e_y > s_y:
                theta = 90
            else:
                theta = -90
        else:
            t = math.degrees(math.atan((e_y-s_y)/(e_x-s_x)))
            if e_x < s_x:
                theta = 180 + t
            elif e_y < s_y:
                theta = 360 + t
            else:
                theta = t
        return theta

    def update(self, dt):
        if self.started:
            t = self.get_time()
            for shape in self.shapes:
                if shape.stopped:
                    continue
                (x, y, vx, vy) = self.kinematics_2d(self.proj.theta0, self.proj.v0, t)
                dx = vx * dt
                dy = vy * dt
                shape.x += self.to_pixels(dx)
                shape.y += self.to_pixels(dy)
                if shape.y <= shape.r:
                    shape.y = shape.r
                    shape.stopped = True
                
    
    def draw_circle(self, x, y):
        r = 50
        return arcade.draw_circle_filled(x, y, r, (0, 0, 0))

    
    def kinematics_2d(self, theta, v_initial, t, g=-9.813):
        theta = theta * (math.pi/180)
        vx_initial = v_initial*math.cos(theta)
        vy_initial = v_initial*math.sin(theta)
        x = vx_initial*t
        y = vy_initial*t+0.5*g*(t**2)
        vx_final = vx_initial
        vy_final = vy_initial + g*t
        if y < 0:
            y = 0
        return (x,y, vx_final, vy_final)

    def get_time(self):
        return time.time() - self.start_time


def main():
    game = Game(S_WIDTH, S_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
