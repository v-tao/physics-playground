import arcade
import math
import time

S_WIDTH = S_HEIGHT = 600

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
        return (x,y, vx_final, vy_final)

def to_pixels(x, pixels_per_meter):
        return x * pixels_per_meter

class Projectile(arcade.Sprite):
    def __init__(self, img, size, s_x, s_y):
        super().__init__(img, size)
        self.set_position(s_x, s_y)
        self.stopped = True
        self.v0 = 0
        self.theta0 = 0
        self.start_time = 0

    def get_time(self):
        return time.time() - self.start_time

    def on_update(self, dt):
        t = self.get_time()
        (x, y, vx, vy) = kinematics_2d(self.theta0, self.v0, t)
        dx = vx * dt
        dy = vy * dt
        #magic number shh dont tell anyone
        self.center_x += to_pixels(dx, 20)
        self.center_y += to_pixels(dy, 20)

class Target(arcade.Sprite):
    def __init__(self, img, size, s_x, s_y):
        super().__init__(img, size)
        self.set_position(s_x, s_y)
        self.v0 = 0
        self.theta0 = 0
        self.start_time = 0

class Game(arcade.Window):

    def __init__(self, width, height, pixels_per_meter=20):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.proj_list = None
        self.proj = None
        self.target_list = None
        self.target = None
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
        self.game_over = False
        self.game_won = False

    def setup(self):
        self.proj_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.proj = Projectile("shrek.png", 0.25,  100, 100)
        self.target = Target("fiona.jpeg", 0.3, 500, 500)
        self.proj_list.append(self.proj)
        self.target_list.append(self.target)
        self.game_over = False
        self.game_won = False
        #self.started = True
        #self.start_time = time.time()

    def on_draw(self):
        arcade.start_render()
        self.proj_list.draw()
        self.target_list.draw()
        if not self.launched:
            self.draw_vector(self.proj.center_x, self.proj.center_y, self.mouse_x, self.mouse_y, (255, 0, 0), "m/s")
        if self.game_over:
            self.end_message()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.launched or button is not arcade.MOUSE_BUTTON_LEFT:
            return
        v0 = (1/self.pixels_per_meter) * math.sqrt((x-self.proj.center_x)**2 + (y-self.proj.center_y)**2)
        theta = self.get_angle(self.proj.center_x, self.proj.center_y, x, y)
        
        self.proj.v0 = v0
        self.proj.theta0 = theta
        self.proj.stopped = False
        self.proj.start_time = time.time()
        self.launched = True
        self.started = True

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
        arcade.draw_text(theta_label, s_x, s_y - (self.proj.height/2) - t_height, (0, 0, 0), t_height, width=200, align="center", anchor_x="center", anchor_y="center")
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

    def end_message(self):
        if self.game_won:
            arcade.draw_text("YOU SAVED FIONA POGGERS",
                        S_WIDTH/2, S_HEIGHT/2, arcade.color.GREEN, 30, width=S_WIDTH, align="center",
                        anchor_x="center", anchor_y="center")
        else:
            arcade.draw_text("GET OUT OF MY SWAMP",
                        S_WIDTH/2, S_HEIGHT/2, arcade.color.RED, 30, width=S_WIDTH, align="center",
                        anchor_x="center", anchor_y="center")

    def update(self, dt):
        if self.started:
            if not self.proj.stopped:
                self.proj_list.on_update()
                if arcade.check_for_collision(self.proj, self.target):
                    self.game_won = True
                    self.game_over = True
                    self.proj.stopped = True
                elif self.proj.center_y <=  self.proj.height/2:
                    self.proj.center_y = self.proj.height/2
                    self.proj.stopped = True
                    self.game_over = True
                elif self.proj.center_x > S_WIDTH:
                    self.game_over = True

def main():
    game = Game(S_WIDTH, S_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
