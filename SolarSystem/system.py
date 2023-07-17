import tkinter as tk
import numpy as np
from PIL import ImageTk,Image 
import time

#x,y in millions of km
#velocity in km/s
#radius in 1000km
#mass in kg

screen_size  = [1500, 1000]
zoom = 100

class Planet:

    def __init__(self, canvas, x, y, velocity, radius, mass, color, personal_display_size, immovable=False):
        self.display_size = personal_display_size*zoom
        self.canvas = canvas
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius
        self.mass = mass
        self.color = color
        self.immovable = immovable
        self.planet = None
        self.draw()
    
    def draw(self):
        if self.planet:
            self.canvas.delete(self.planet)
        self.planet = self.canvas.create_oval(zoom*self.x-self.display_size*self.radius, zoom*self.y-self.display_size*self.radius,
                zoom*self.x+self.display_size*self.radius, zoom*self.y+self.display_size*self.radius, fill=self.color)
    
    


class Win:
    
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=screen_size[0], height=screen_size[1], bg="black")
        self.canvas.pack()
        self.planets = []
        self.time_step=10**2
        self.populate()
        self.simulate()

    def populate(self):
        #x,y in millions of km
        #velocity in km/s
        #radius in 1000km
        #mass in kg

        # self.planets.append(Planet(self.canvas, x=10, y=10, velocity=(0,0), radius=696.340, mass=1.989*10**30 , color="yellow", personal_display_size=10**-2))
        # self.planets.append(Planet(self.canvas, x=40, y=40, velocity=(0,0), radius=6.371, mass=5.972*10**24 , color="blue", personal_display_size=10**-1))
        # self.planets.append(Planet(self.canvas, x=42, y=42, velocity=(0,0), radius=1.736, mass=7.346*10**22 , color="gray", personal_display_size=10**-1))
        
        # self.planets.append(Planet(self.canvas, x=40, y=40, velocity=(0,0), radius=6.371, mass=5.972*10**24 , color="blue", personal_display_size=10**-1,immovable=True))
        # self.planets.append(Planet(self.canvas, x=40, y=50, velocity=(0.2,0), radius=6.371, mass=5.972*10**24 , color="blue", personal_display_size=10**-1))
        # self.planets.append(Planet(self.canvas, x=40, y=60, velocity=(-0.1,0), radius=6.371, mass=5.972*10**24 , color="blue", personal_display_size=10**-1))

        self.planets.append(Planet(self.canvas, x=5, y=5, velocity=(0,0), radius=6.371, mass=5.972*10**24 , color="blue", personal_display_size=10**-1.5,immovable=True))
        self.planets.append(Planet(self.canvas, x=5, y=5.3844, velocity=(1.02,0), radius=1.737, mass=7.3*10**22 , color="grey", personal_display_size=10**-1.5,immovable=False))

    
    def simulate(self):

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
                    print(distance)
                    acceleration = (K * other_planet.mass / distance**2)/1000 # m/s -> km/s
                    planet.velocity = (planet.velocity[0]-self.time_step*acceleration * Dx / distance, planet.velocity[1]-self.time_step* acceleration * Dy / distance)
        

        """Calculate positions"""
        counter=0
        for planet in self.planets:
            if planet.immovable:
                continue
            counter+=1
            # velocity is in km/s
            # planet.x is in M km
            planet.x += planet.velocity[0]*(self.time_step/10**6)
            planet.y += planet.velocity[1]*(self.time_step/10**6)
            if counter == 1:
                pass
                # print(planet.velocity[0]*(self.time_step/10**6))
                # print(planet.velocity[1]*(self.time_step/10**6))
                # print(planet.x)
                # print(planet.y)
                # print("")
            planet.draw()
        self.canvas.after(1, self.simulate)

root = tk.Tk()
root.geometry(f"{screen_size[0]}x{screen_size[1]}+10+10")
root.configure(bg="#FFFFFF")
Win(root)

root.mainloop()
