import tkinter as tk
import math

simulation_size = (800, 600)

frames = 200

G = 3e-2

rate = [-1, 1, 0]
after_image_color = "#FF0000"
after_image_pos = [0, 0]

edges = {
    (255, 0, 0): [-1, 1, 0],
    (0, 255, 0): [0, -1, 1],
    (0, 0, 255): [1, 1, -1],
    (255, 255, 0): [0, -1, 1],
    (255, 0, 255): [-1, 1, 0],
    (0, 255, 255): [0, -1, -1],
    (0, 0, 0): [1, 0, 0]
}


class Circle:

    def __init__(self, canvas, x, y, r, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.shape = self.canvas.create_oval(x - r, y - r, x + r, y + r, outline=color, fill='black', width=1)


class Ball:

    def __init__(self, canvas, x, y, r, color, vx, vy):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy
        self.shape = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color)

    def speed_after_bounce(self, circle):
        v = 1.05 * (self.vx ** 2 + self.vy ** 2) ** 0.5
        v_angle = math.atan2(self.vy, self.vx)

        r_angle = math.atan2(self.y - circle.y, self.x - circle.x)

        a = v_angle - (r_angle - math.pi / 2)
        new_angle = r_angle - math.pi / 2 - a
        self.vx = v * math.cos(new_angle)
        self.vy = v * math.sin(new_angle)


class Win:

    def __init__(self, root):
        self.root = root
        self.setup_root()
        self.create_circle()
        self.create_balls()

        self.update()

    def setup_root(self):
        self.sim_frame = tk.Frame(self.root, width=simulation_size[0], height=simulation_size[1], bg="black")
        self.sim_frame.pack(anchor="w", side="left")
        self.canvas = tk.Canvas(self.sim_frame, width=simulation_size[0], height=simulation_size[1], bg="black")

    def create_circle(self):
        x, y = simulation_size[0] / 2, simulation_size[1] / 2
        r = 200
        self.circle = Circle(self.canvas, x, y, r, "white")
        self.canvas.pack()

    def create_balls(self):
        x, y = simulation_size[0] / 2, simulation_size[1] / 2
        vx, vy = -1., 1.
        r = 10
        color = "red"

        self.ball = Ball(self.canvas, x, y, r, color, vx, vy)
        self.canvas.tag_raise(self.ball)
        self.canvas.tag_raise(self.ball)
        self.canvas.tag_raise(self.ball)
        self.canvas.pack()

    def create_after_image(self):

        global after_image_color
        global rate

        r = int(after_image_color[1:3], 16)
        g = int(after_image_color[3:5], 16)
        b = int(after_image_color[5:], 16)
        r += rate[0]
        g += rate[1]
        b += rate[2]

        if (r, g, b) in edges:
            rate = edges[(r, g, b)]
        r = "0" * (2 - len(hex(r)[2:])) + hex(r)[2:]
        g = "0" * (2 - len(hex(g)[2:])) + hex(g)[2:]
        b = "0" * (2 - len(hex(b)[2:])) + hex(b)[2:]

        after_image_color = "#" + r + g + b
        after_image = self.canvas.create_oval(self.ball.x - 10, self.ball.y - 10, self.ball.x + 10,
                                              self.ball.y + 10, fill=after_image_color)
        self.canvas.itemconfig(self.ball.shape, fill=after_image_color)
        after_image_pos[0] = self.ball.x
        after_image_pos[1] = self.ball.y

    def update(self):
        self.canvas.after(int(1000 / frames), self.update)

        self.ball.vy += G

        # Check for collision with circle
        dx = self.circle.x - self.ball.x
        dy = self.circle.y - self.ball.y
        if (dx ** 2 + dy ** 2) ** 0.5 >= self.circle.r - self.ball.r:
            self.create_after_image()
            self.ball.speed_after_bounce(self.circle)

        self.ball.x += self.ball.vx
        self.ball.y += self.ball.vy

        # Create afterimage
        after_image_created = False
        if (after_image_pos[0] - self.ball.x) ** 2 + (after_image_pos[1] - self.ball.y) ** 2 > 15 ** 2:
            after_image_created = True
            self.create_after_image()

        self.canvas.move(self.ball.shape, self.ball.vx, self.ball.vy)
        if after_image_created:
            self.canvas.tag_raise(self.ball.shape)


root = tk.Tk()
root.geometry(f"{simulation_size[0]}x{simulation_size[1]}+10+10")
Win(root)

root.mainloop()
