import tkinter as tk
import numpy as np
from PIL import ImageTk,Image 
import time

#x,y in millions of km
#velocity in km/s
#radius in 1000km
#mass in kg

# screen_size  = [2700, 1050]
screen_size  = [1500, 880]
zoom = 2
class Planet:

    def __init__(self, canvas, x, y, velocity, radius, mass, color, personal_display_size, immovable=False):
        self.display_size = personal_display_size
        self.canvas = canvas
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.mass = mass
        self.color = color
        self.immovable = immovable
        self.planet = None
        self.name = None
        self.draw()
    
    def draw(self):
        if self.planet:
            self.canvas.delete(self.planet)
        display_size = self.display_size*zoom
        self.planet = self.canvas.create_oval(zoom*self.x-display_size*self.radius, zoom*self.y-display_size*self.radius,
                zoom*self.x+display_size*self.radius, zoom*self.y+display_size*self.radius, fill=self.color)
    
    


class Win:
    
    def __init__(self, root):
        self.root = root
        self.setup_root()
        self.canvas = tk.Canvas(self.root, width=screen_size[0], height=screen_size[1], bg="black")
        self.canvas.pack()
        # self.canvas.bind("<space>", self.click)
        self.previous_drag = (0,0)
        self.planets = []
        self.time_step=10**2.5
        self.locked = False
        self.locked_on = 0
        self.populate()
        self.time=0
        self.simulate()

    def populate(self):
        #x,y in millions of km
        #velocity in km/s
        #radius in 1000km
        #mass in kg


        spawn_offset =[180, 180]
        sun = Planet(self.canvas, x=0+spawn_offset[0], y=0+spawn_offset[1], velocity=(0,0), radius=696.340, mass=1.989*10**30 , color="yellow", personal_display_size=10**-2, immovable=True)
        earth = Planet(self.canvas, x=147+spawn_offset[0], y=0+spawn_offset[1], velocity=(0,30.3), radius=6.371, mass=5.972*10**24 , color="blue", personal_display_size=10**-2,immovable=False)
        moon = Planet(self.canvas, x=147.360+spawn_offset[0], y=0+spawn_offset[1], velocity=(0,30.3+1.082), radius=1.737, mass=7.3*10**22 , color="grey", personal_display_size=10**-2,immovable=False)

        self.planets.append(sun)
        self.planets.append(earth)
        self.planets.append(moon)
        sun.name = "Sun"
        earth.name = "Earth"
        moon.name = "Moon"

        self.locked=False
        self.locked_on=0
    
    def simulate(self):

        if self.locked:
            locked_cords = [self.planets[self.locked_on].x, self.planets[self.locked_on].y]
            screen_center = [screen_size[0]/2, screen_size[1]/2]
            offset = [screen_center[0]-locked_cords[0]*zoom, screen_center[1]-locked_cords[1]*zoom]

            for planet in self.planets:
                planet.x += offset[0]/zoom
                planet.y += offset[1]/zoom
                planet.draw()
        

        """Calculate velocities"""
        for planet in self.planets:
            if planet.immovable:
                continue
            for other_planet in self.planets:
                if planet != other_planet:
                    Dx = (planet.x - other_planet.x)*10**9 #M km -> m
                    Dy = (planet.y - other_planet.y)*10**9 #M km -> m
                    other_m = other_planet.mass # kg -> kg
                    K = 6.67408*10**-11
                    distance = (Dx**2 + Dy**2)**0.5
                    # if distance < 140318173421:
                    #     print(distance, planet.x, planet.y, zoom)

                    acceleration = (K * other_planet.mass / distance**2)/1000 # m/s^2 -> km/s^2
                    # if planet.name == "Moon" and other_planet.name == "Earth":
                    #     print("Moon, earth:", acceleration)
                    # if planet.name == "Moon" and other_planet.name == "Sun":
                    #     print("Moon,   sun:", acceleration)
                    planet.velocity = (planet.velocity[0]-self.time_step*acceleration * Dx / distance, planet.velocity[1]-self.time_step* acceleration * Dy / distance)

        

        """Calculate positions"""
        for planet in self.planets:
            if planet.immovable:
                planet.draw()
                continue
            # velocity is in km/s
            # planet.x is in M km
            planet.x += planet.velocity[0]*(self.time_step/10**6)
            planet.y += planet.velocity[1]*(self.time_step/10**6)

            planet.draw()
        self.time = self.time_step + self.time
        # print(self.time/(24*3600))
        self.canvas.after(1, self.simulate)


    def setup_root(self):
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<MouseWheel>", self.wheel)
        self.root.bind("<Key>", self.keypress)
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<Button-1>", self.click)
    
    def click(self, event):
        self.previous_drag = (event.x, event.y)
    
    def drag(self, event):
        if self.locked:
            return
        if self.previous_drag==(0,0):
            self.previous_drag = (event.x, event.y)        
        offset = [event.x-self.previous_drag[0], event.y-self.previous_drag[1]]
        self.previous_drag = (event.x, event.y)
        for planet in self.planets:
            planet.x += offset[0]/zoom
            planet.y += offset[1]/zoom
            planet.draw()
    
    def keypress(self, event):
        if self.locked:
            return
        offset =[0,0]
        moving = { "w": [0, 1], "a": [1,0], "s": [0,-1], "d": [-1,0] }
        offset = moving.get(event.char, [0,0])
        if not offset:
            return
        moving_step  = 1
        for planet in self.planets:
            planet.x += moving_step * offset[0] 
            planet.y += moving_step * offset[1]
            planet.draw()

    def wheel(self, event):
        global zoom
        old_zoom = zoom
        zoom+=0.1*zoom*event.delta/120

        
        if self.locked:
            locked_cords = [self.planets[self.locked_on].x, self.planets[self.locked_on].y]
            screen_center = [screen_size[0]/2, screen_size[1]/2]  
            offset = [screen_center[0]-locked_cords[0]*zoom, screen_center[1]-locked_cords[1]*zoom]
        else:
            locked_cords= [event.x/old_zoom, event.y/old_zoom]
            offset = [event.x-locked_cords[0]*zoom, event.y-locked_cords[1]*zoom]      

        
        for planet in self.planets:
            planet.x += offset[0]/zoom
            planet.y += offset[1]/zoom
            planet.draw()

root = tk.Tk()
root.geometry(f"{screen_size[0]}x{screen_size[1]}+10+10")
root.configure(bg="#FFFFFF")
Win(root)

root.mainloop()
