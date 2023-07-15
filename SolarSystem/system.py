import tkinter as tk
import numpy as np
from PIL import ImageTk,Image 
import time

#x,y in millions of km
#velocity in km/s
#radius in 1000km
#mass in kg

screen_size  = [1000, 700]
zoom = 10

class Planet:

    def __init__(self, canvas, x, y, velocity, radius, mass, color, personal_display_size):
        self.display_size = personal_display_size*zoom
        self.canvas = canvas
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.mass = mass
        self.color = color
        self.planet = None
        self.draw()
    
    def draw(self):
        self.planet = self.canvas.create_oval(zoom*self.x-self.display_size*self.radius, zoom*self.y-self.display_size*self.radius,
                zoom*self.x+self.display_size*self.radius, zoom*self.y+self.display_size*self.radius, fill=self.color)
    
    


class Win:
    
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=screen_size[0], height=screen_size[1], bg="black")
        self.canvas.pack()
        self.planets = []
        self.populate()

    def populate(self):
        self.planets.append(Planet(self.canvas, x=10, y=10, velocity=(0,0), radius=696.340, mass=1.989*10**30 , color="yellow", personal_display_size=10**-2))
        self.planets.append(Planet(self.canvas, x=40, y=40, velocity=(0,0), radius=6.371, mass=5.972*10**24 , color="blue", personal_display_size=10**-1))
        self.planets.append(Planet(self.canvas, x=42, y=42, velocity=(0,0), radius=1.736, mass=7.346*10**22 , color="gray", personal_display_size=10**-1))

root = tk.Tk()
root.geometry(f"{screen_size[0]}x{screen_size[1]}+10+10")
root.configure(bg="#FFFFFF")
Win(root)

root.mainloop()
