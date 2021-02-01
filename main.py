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
        self.stopped = False

class Game(arcade.Window):

    def __init__(self, width, height, pixels_per_meter=20):
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.WHITE)
        self.shapes = []
        self.started = False
        self.t = 0
        self.pixels_per_meter = pixels_per_meter
        #fullscreen, totally did not copy and paste from docs
        # width, height = self.get_size()
        # self.set_viewport(0, width, 0, height)
        # self.set_fullscreen(True),

    def setup(self):
        self.shapes = []
        self.shapes.append(Ball(100, 100, 10, (0, 0, 0)))
        self.started = True
        self.start_time = time.time()

    def on_draw(self):
        arcade.start_render()

        for s in self.shapes:
            arcade.draw_circle_filled(s.x, s.y, s.r, s.color)

    def to_pixels(self, x):
        return x * self.pixels_per_meter

    def update(self, dt):
        if self.started:
            t = self.get_time()
            for shape in self.shapes:
                if shape.stopped:
                    continue
                (x, y, vx, vy) = self.kinematics_2d(0, 4, t)
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
