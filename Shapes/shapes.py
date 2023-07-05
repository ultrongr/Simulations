import tkinter as tk
from math import sqrt
import math
import numpy as np

size = 350
offset = [425, 425]
np.random.seed(0)

c1 = 0.25*(sqrt(5)-1)
c2 = 0.25*(sqrt(5)+1)
s1 = 0.25*(sqrt(10+2*sqrt(5)))
s2 = 0.25*(sqrt(10-2*sqrt(5)))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Win:

    def __init__(self, root):
        self.board = tk.Canvas(root, width=1200, height=800, bg="white")
        self.board.pack()

        """Hexagon"""
        ideal_shape_points = [Point(1, 0), Point(0.5, sqrt(3) / 2), Point(-0.5, sqrt(3) / 2), Point(-1, 0),
                                Point(-0.5, -sqrt(3) / 2), Point(0.5, -sqrt(3) / 2)]
        
        """Square"""
        # ideal_shape_points = [Point(-1, -1), Point(1, -1), Point(1, 1), Point(-1, 1)] 
        
        """Triangle"""
        # ideal_shape_points = [Point(0, -1), Point(1, 1), Point(-1, 1)]

        """Pentagon"""
        # ideal_shape_points = [Point(0, 1), Point(s1, c1), Point(s2, -c2), Point(-s2, -c2), Point(-s1, c1)]

        self.shape_points = []
        for point in ideal_shape_points:
            self.shape_points.append(Point(size * point.x + offset[0], size * point.y + offset[1]))
        for ind, point in enumerate(self.shape_points):
            next_point = self.shape_points[ind + 1 if ind + 1 < len(self.shape_points) else 0]
            self.board.create_line(point.x, point.y, next_point.x,  next_point.y)
            # board.crea
        for i in self.shape_points:
            print(i.x, i.y)
        self.point  = self.shape_points[0]
        # self.point = Point(offset[0], offset[1])
        self.simulate()

    

    def simulate(self):
        self.board.create_oval(self.point.x-1, self.point.y-1, self.point.x+1, self.point.y+1, width = 0, fill="black")
        
        random_point = self.shape_points[np.random.randint(0, len(self.shape_points))]
        distance = [random_point.x - self.point.x, random_point.y - self.point.y]
        self.point = Point(self.point.x + 2*distance[0]/3, self.point.y + 2*distance[1]/3)
        self.board.after(1, self.simulate)

root = tk.Tk()
root.geometry("1200x900+10+10")
root.configure(bg="#96DFCE")
Win(root)

root.mainloop()
