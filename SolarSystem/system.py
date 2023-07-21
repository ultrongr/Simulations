import tkinter as tk
import time

#x,y in millions of km
#velocity in km/s
#radius in 1000km
#mass in kg

simulation_size  = [1500, 880]
options_size = [200, 880]
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


        self.canvas.pack()
        self.previous_drag = (0,0)
        self.planets = []
        self.time_step=10**3
        self.populate()
        self.setup_options()
        self.time=0
        self.counter = 0
        self.simulate()

    def populate(self):
        #x,y in millions of km
        #velocity in km/s
        #radius in 1000km
        #mass in kg


        spawn_offset =[180, 180]
        scale = -2
        sun = Planet(self.canvas, x=0+spawn_offset[0], y=0+spawn_offset[1], velocity=(0,0), radius=696.340, mass=1.989*10**30 , color="yellow", personal_display_size=10**scale, immovable=True)
        mercury = Planet(self.canvas, x=46+spawn_offset[0], y=0+spawn_offset[1], velocity=(0,58.97), radius=2.439, mass=3.301*10**23 , color="brown", personal_display_size=10**scale ,immovable=False)
        venus = Planet(self.canvas, x=107.480+spawn_offset[0], y=0+spawn_offset[1], velocity=(0,35.26), radius=6.051, mass=4.867*10**24 , color="orange", personal_display_size=10**scale ,immovable=False)
        earth = Planet(self.canvas, x=147.095+spawn_offset[0], y=0+spawn_offset[1], velocity=(0,30.3), radius=6.371, mass=5.972*10**24 , color="blue", personal_display_size=10**scale ,immovable=False)
        moon = Planet(self.canvas, x=147.095+0.363+spawn_offset[0], y=0+spawn_offset[1], velocity=(0,30.3+1.082), radius=1.738, mass=7.346*10**22 , color="grey", personal_display_size=10**scale ,immovable=False)
        
        

        self.planets.append(sun)
        self.planets.append(mercury)
        self.planets.append(venus)
        self.planets.append(earth)
        self.planets.append(moon)
        
        
        sun.name = "Sun"
        earth.name = "Earth"
        moon.name = "Moon"
        venus.name = "Venus"
        mercury.name = "Mercury"

        self.locked=False
    
    def simulate(self):

        if self.locked:
            locked_cords = [self.planets[self.locked_on].x, self.planets[self.locked_on].y]
            screen_center = [simulation_size[0]/2, simulation_size[1]/2]
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
                if planet == other_planet:
                    continue
                
                Dx = (planet.x - other_planet.x)*10**9 #M km -> m
                Dy = (planet.y - other_planet.y)*10**9 #M km -> m
                other_m = other_planet.mass # kg -> kg
                K = 6.67408*10**-11
                distance = (Dx**2 + Dy**2)**0.5

                acceleration = (K * other_planet.mass / distance**2)/1000 # m/s^2 -> km/s^2
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
        text = f"Time: {self.time/(3600*24):.1f} days"
        padd =22-len(text) 
        self.days_label.config(text=f"Time: {padd*' '}{self.time/(3600*24):.1f} days")
        self.canvas.after(1, self.simulate)

    def update_options(self):
        self.time_step = float(self.time_step_box.get())
        for planet in self.planets:
            planet.display_size = float(planet.size_box.get())
        self.canvas.focus_set()

    def setup_root(self):
        self.sim_frame = tk.Frame(self.root, width=simulation_size[0], height=simulation_size[1], bg="black")
        self.sim_frame.pack(anchor = "w", side = "left")
        self.canvas = tk.Canvas(self.sim_frame, width=simulation_size[0], height=simulation_size[1], bg="black")
        self.canvas.bind("<Escape>", lambda e: self.root.destroy())
        self.canvas.bind("<MouseWheel>", self.wheel)
        self.canvas.bind("<Key>", self.keypress)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.focus_set()

        self.options_frame = tk.Frame(self.root, width=options_size[0], height=options_size[1], bg="gray")
        self.options_frame.pack(anchor = "nw", side="left")
        
    def setup_options(self):
        self.days_frame = tk.Frame(self.options_frame, width=options_size[0], height=100, bg="gray")
        self.days_frame.pack(anchor="nw", side="top", fill = "x")
        self.days_label = tk.Label(self.days_frame, text="Time: 0", font=("Arial", 15))
        self.days_label.pack(anchor="nw", side="top", expand = True, fill = "x")

        self.time_step_frame = tk.Frame(self.options_frame, width=options_size[0], height=100, bg="gray")
        self.time_step_frame.pack(anchor="nw", side="top", fill = "x")
        self.time_step_button = tk.Button(self.time_step_frame, text="Time step:", font=("Arial", 13), height=1, command=lambda: self.update_options())
        self.time_step_button.pack(anchor="nw", side="left", expand = False, fill = "x")

        self.time_step_box = tk.Entry(self.time_step_frame, font = ("Arial", 19))
        self.time_step_box.insert(0, f"{self.time_step}")
        self.time_step_box.pack(anchor="nw", side="right", expand = True, fill = "x")

        self.sizes_frame = tk.Frame(self.options_frame, width=options_size[0], height=100, bg="#F0F0F0")
        self.sizes_frame.pack(anchor="nw", side="top", fill = "x")
        self.sizes_label = tk.Label(self.sizes_frame, text=f"\n\nSizes:", font=("Arial", 18))
        self.sizes_label.grid(row=0,columnspan = 2, sticky = "nw")
        for planet in self.planets:
            planet.size_frame = tk.Frame(self.sizes_frame, width=options_size[0], height=100, bg="#F0F0F0")
            planet.size_frame.grid(row=self.planets.index(planet)+1, columnspan=2, sticky = "n")
            planet.size_button = tk.Button(planet.size_frame, text=f"{planet.name}", font=("Arial", 12), height=1, command=lambda: self.update_options())
            planet.size_button.pack(anchor="nw", side="left", expand = False, fill = "x")
            planet.size_box = tk.Entry(planet.size_frame, font = ("Arial", 19))
            planet.size_box.insert(0, f"{planet.display_size}")
            planet.size_box.pack(anchor="ne", side="right", expand = True, fill = "x")


        self.planet_buttons_frame = tk.Frame(self.options_frame, width=options_size[0], height=len(self.planets)*25, bg="gray")
        self.planet_buttons_frame.pack(anchor="nw", side="top", fill = "x")
        self.locked_on_label = tk.Label(self.planet_buttons_frame, text=f"\n\nLocked on:{18*' '}", font=("Arial", 15))
        self.locked_on_label.grid(row=0, sticky = "n")
        self.planet_buttons = []
        for planet in self.planets:
            self.planet_buttons.append(tk.Button(self.planet_buttons_frame, text=planet.name, font = ("Arial", 15), command=lambda planet=planet: self.lock(planet)))
            self.planet_buttons[-1].grid(row = self.planets.index(planet)+1, sticky="nsew")
        self.unlock_button = tk.Button(self.planet_buttons_frame, text="(Unlock)", font = ("Arial", 15), command=lambda: self.unlock())
        self.unlock_button.grid(row = len(self.planets)+1, sticky="nsew")
 
    def lock(self, planet):
        self.locked=True
        self.locked_on = self.planets.index(planet)
        self.days_label.config(text=f"Time: {self.time}")
        self.canvas.focus_set()
    
    def unlock(self):
        self.locked=False

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
            screen_center = [simulation_size[0]/2, simulation_size[1]/2]  
            offset = [screen_center[0]-locked_cords[0]*zoom, screen_center[1]-locked_cords[1]*zoom]
        else:
            locked_cords= [event.x/old_zoom, event.y/old_zoom]
            offset = [event.x-locked_cords[0]*zoom, event.y-locked_cords[1]*zoom]      

        
        for planet in self.planets:
            planet.x += offset[0]/zoom
            planet.y += offset[1]/zoom
            planet.draw()

root = tk.Tk()
root.geometry(f"{simulation_size[0]+options_size[0]}x{simulation_size[1]}+10+10")
Win(root)

root.mainloop()
