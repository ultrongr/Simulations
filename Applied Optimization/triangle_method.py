import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from functools import cache
from PIL import Image
import math

simulation_size = [500, 500]
options_size = [200, simulation_size[1]]
zoom = 100
a = 30

@cache
def hex_to_rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

@cache
def func(_x, _y):
    return _x ** 2 + _y ** 2 + _x + _y
    # return _x**3 - 3*_x*_y**2 + 4*_y**3 - 6*_x + 8*_y


@cache
def value_to_color_hex(value):
    rgba_color = value_to_color_hex.cmap(value)
    hex_color = to_hex(rgba_color)
    return hex_color


value_to_color_hex.cmap = plt.get_cmap('RdYlBu')  # You can choose a different colormap if desired

class Point:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.cords=(x,y)
        
        

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2=p2
        
        

class Triangle:
    def __init__(self, canvas, points):
        self.canvas = canvas
        self.points = points
        self.triangle = self.canvas.create_polygon(self.points,  fill=None,outline="black", width =1 )
        self.canvas.update()
        self.past_positions={((self.points[0], self.points[1]), (self.points[2], self.points[3]), (self.points[4], self.points[5]))}
        return

    def move():
        return

class Win:

    def __init__(self, root):
        self.root = root
        self.heatmap = None
        self.setup_root()
        self.color_plane()
        self.create_triangle()

    def setup_root(self):
        self.root.title("Simulation")
        self.root.geometry(f"{simulation_size[0] + options_size[0]}x{simulation_size[1]}+10+10")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        self.root.update()
        self.sim_frame = tk.Frame(self.root, width=simulation_size[0], height=simulation_size[1], bg="black")
        self.sim_frame.pack(anchor="w", side="left")
        self.sim_frame.pack()
        self.plane = tk.Canvas(self.sim_frame, width=simulation_size[0], height=simulation_size[1], bg="black")
        self.plane.pack()

    def color_plane(self):
        if not self.heatmap:
            values_list = []
            for x in range(simulation_size[0]):
                for y in range(simulation_size[1]):
                    values_list.append(func((x - simulation_size[0] / 2) / zoom, (y - simulation_size[1] / 2) / zoom))

            # values_list.sort()
            min_value = min(values_list)
            max_value = max(values_list)
            range_value = max_value - min_value

            width, height= simulation_size
            img = Image.new('RGB', (width, height), "black")
            pixels = img.load()
            for x in range(width):
                for y in range(height):
                    value = func((x - simulation_size[0] / 2) / zoom, (y - simulation_size[1] / 2) / zoom)
                    normalized_value = 1-(value - min_value) / range_value # to reverse the color map
                    color = value_to_color_hex(normalized_value)[1:]
                    pixels[x, y] = hex_to_rgb(color)

            pixels = img.load()
            img.save('values.png')
        t1 = time.time()
        self.heatmap = tk.PhotoImage(file="values.png")
        self.image = self.plane.create_image(0, 0, anchor=tk.NW, image=self.heatmap)
        self.plane.update()
        self.xaxis = self.plane.create_line(0, simulation_size[1] / 2, simulation_size[0], simulation_size[1] / 2,
                                            fill="black")
        self.yaxis = self.plane.create_line(simulation_size[0] / 2, 0, simulation_size[0] / 2, simulation_size[1],
                                            fill="black")
        print(time.time()-t1)
        print("done")


        return

    def create_triangle(self):
        self.triangle = Triangle(self.plane, [0, 0, 0+a, 0, 0.5*a , math.sqrt(3)/2*a])
        return

root = tk.Tk()
root.geometry(f"{simulation_size[0] + options_size[0]}x{simulation_size[1]}+10+10")
w=Win(root)

root.mainloop()
