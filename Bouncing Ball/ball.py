import tkinter as tk
import time
import math

simulation_size = (800, 600)

g=1e-4
after_image = "pink"
after_image_pos = [0,0]

class Circle:

    def __init__(self, canvas, x, y, r, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.shape = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, fill='black', width=1)

class Ball:

    def __init__(self, canvas, x, y, r, color, vx, vy):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy
        self.shape = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill = color)

    def speed_after_bounce(self, circle):
        v =1.1*(self.vx**2 + self.vy**2)**0.5
        v_angle = math.atan2(self.vy, self.vx)

        r_angle = math.atan2(self.y - circle.y, self.x - circle.x)
        
        a = v_angle-(r_angle-math.pi/2)
        new_angle = r_angle-math.pi/2-a
        new_tan = math.tan(new_angle)
        # vx = v / (1 + new_tan**2)**0.5
        # vy = vx*new_tan
        self.vx = v*math.cos(new_angle)
        self.vy = v*math.sin(new_angle)
        # print(self.vx, self.vy, a, new_angle, new_tan) 
        # print the above but say what each variable is 
        


        # c = r_angle - v_angle
        # a = math.pi - c
        # new_angle = v_angle - 2*a
        # new_tan = math.tan(new_angle)

        # self.vx = v / (1 + new_tan**2)**0.5
        # self.vy = self.vx*new_tan
        # print(self.vx, self.vy)
        

class Win:

    def __init__(self, root):
        self.root = root
        self.setup_root()
        self.create_circle()
        self.create_balls()

        self.update()

    def setup_root(self):
        self.sim_frame = tk.Frame(self.root, width=simulation_size[0], height=simulation_size[1], bg="black")
        self.sim_frame.pack(anchor = "w", side = "left")
        self.canvas = tk.Canvas(self.sim_frame, width=simulation_size[0], height=simulation_size[1], bg="black")
        # self.canvas.bind("<Escape>", lambda e: self.root.destroy())
        # self.canvas.bind("<MouseWheel>", self.wheel)
        # self.canvas.bind("<Key>", self.keypress)
        # self.canvas.bind("<B1-Motion>", self.drag)
        # self.canvas.bind("<Button-1>", self.click)
        # self.canvas.focus_set()

        # self.options_frame = tk.Frame(self.root, width=options_size[0], height=options_size[1], bg="gray")
        # self.options_frame.pack(anchor = "nw", side="left")

    def create_circle(self):
        x, y = simulation_size[0]/2, simulation_size[1]/2
        r=200
        self.circle = Circle(self.canvas, x, y, r, "white")
        self.canvas.pack()
    
    def create_balls(self):
        x, y = simulation_size[0]/2, simulation_size[1]/2
        # x+=100
        vx, vy = -0.02, 0.02
        r = 10
        color = "red"
        
        self.ball = Ball(self.canvas, x, y, r, color, vx, vy)
        self.canvas.tag_raise(self.ball)
        self.canvas.tag_raise(self.ball)
        self.canvas.tag_raise(self.ball)
        self.canvas.pack()
    
    def update(self):
        self.ball.vy += g

        ### Check for collision with circle
        dx = self.circle.x - self.ball.x
        dy = self.circle.y - self.ball.y
        if (dx**2 + dy**2)**0.5 >= self.circle.r-self.ball.r:
            self.ball.speed_after_bounce(self.circle)
        self.ball.x += self.ball.vx
        self.ball.y += self.ball.vy
        if (after_image_pos[0]-self.ball.x)**2 + (after_image_pos[1]-self.ball.y)**2 > 10**2:
            # self.canvas.delete("after_image")
            self.canvas.create_oval(self.ball.x-10, self.ball.y-10, self.ball.x+10, self.ball.y+10, fill=after_image)
            after_image_pos[0] = self.ball.x
            after_image_pos[1] = self.ball.y
        self.canvas.move(self.ball.shape, self.ball.vx, self.ball.vy)

        self.canvas.after(1, self.update)
        


root = tk.Tk()
root.geometry(f"{simulation_size[0]}x{simulation_size[1]}+10+10")
Win(root)

root.mainloop()
