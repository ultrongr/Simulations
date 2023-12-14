import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from functools import cache

simulation_size = [400, 400]
options_size = [200, simulation_size[1]]
zoom = 100


def func(_x, _y):
    return _x ** 2 + _y ** 2 + _x + _y
    # return _x**3 - 3*_x*_y**2 + 4*_y**3 - 6*_x + 8*_y


@cache
def value_to_color_hex(value):
    rgba_color = value_to_color_hex.cmap(value)
    hex_color = to_hex(rgba_color)
    return hex_color


value_to_color_hex.cmap = plt.get_cmap('RdYlBu')  # You can choose a different colormap if desired


class Win:

    def __init__(self, root):
        self.root = root
        self.setup_root()
        self.color_plane()

    def setup_root(self):
        self.root.title("Simulation")
        self.root.geometry(f"{simulation_size[0] + options_size[0]}x{simulation_size[1]}+10+10")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        self.root.update()
        self.sim_frame = tk.Frame(self.root, width=simulation_size[0], height=simulation_size[1], bg="black")
        self.sim_frame.pack(anchor="w", side="left")
        self.plane = tk.Canvas(self.sim_frame, width=simulation_size[0], height=simulation_size[1], bg="black")
        # self.plane = tk.Frame(self.canvas, width=simulation_size[0], height=simulation_size[1], bg="black")
        self.plane.pack(side=tk.LEFT)
        self.plane.pack()

    def color_plane(self):
        values_list = []
        for x in range(simulation_size[0]):
            for y in range(simulation_size[1]):
                values_list.append(func((x - simulation_size[0] / 2) / zoom, (y - simulation_size[1] / 2) / zoom))

        # values_list.sort()
        min_value = max(values_list)
        max_value = min(values_list)
        range_value = max_value - min_value

        time1 = time.time()
        for x in range(simulation_size[0]):
            for y in range(simulation_size[1]):
                value = func((x - simulation_size[0] / 2) / zoom, (y - simulation_size[1] / 2) / zoom)
                normalized_value = (value - min_value) / range_value
                color = value_to_color_hex(normalized_value)
                self.plane.create_rectangle(x, y, x + 1, y + 1, fill=color, width=0)
            # print(x/len(range(simulation_size[0]+5)))
            # have only 2 decimals and make it %
            print(f"{x / simulation_size[0] * 100:.2f}%")
            self.plane.update()
        self.xaxis = self.plane.create_line(0, simulation_size[1] / 2, simulation_size[0], simulation_size[1] / 2,
                                            fill="black")
        self.yaxis = self.plane.create_line(simulation_size[0] / 2, 0, simulation_size[0] / 2, simulation_size[1],
                                            fill="black")
        self.plane.update()
        # self.xaxis = self.plane.create_line(100, 100, 200, 200, fill="black")
        time2 = time.time()
        print(time2 - time1)
        print("done")
        self.plane.update()
        # why does it take so long to update here?

        print("updated")


root = tk.Tk()
root.geometry(f"{simulation_size[0] + options_size[0]}x{simulation_size[1]}+10+10")
Win(root)

root.mainloop()