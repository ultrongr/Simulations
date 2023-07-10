import tkinter as tk
import numpy as np
from PIL import ImageTk,Image 
import time
from playsound import playsound
import threading
import os

size  = [1000, 700]
np.random.seed(123)

class Player:
    def __init__(self, coords, type):
        self.size = 20
        self.step = 3
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        # self.color = color
        self.shape  = None
        self.type = type
        self.img=None
        
        self.img=None
    
    def draw(self, board):
        if self.img:   
            board.delete(self.img)
        self.img = ImageTk.PhotoImage(Image.open(f"{self.type}.png"))
        board.create_image(self.x,self.y, anchor='nw', image=self.img)
        board.pack()
    
    def move(self, win):
        
        
        win.matrix[int(self.x), int(self.y)] = "0"

        if not np.random.randint(0, 3):
            """Avoid enemies"""
            closest_enemy = None
            closest_distance = 100000
            for enemy in win.lists[win.loses[self.type]]:
                if closest_distance>self.distance(enemy):
                    closest_distance = self.distance(enemy)
                    closest_enemy = enemy
            if closest_enemy and closest_distance>0:            
                max_distance = max(abs(closest_enemy.x-self.x), abs(closest_enemy.y-self.y))
                self.direction = [-(closest_enemy.x-self.x)/max_distance, -(closest_enemy.y-self.y)/max_distance]
                self.x += self.direction[0]*self.step
                self.y += self.direction[1]*self.step

        else:
            """Hunt and kill"""
            closest_pray = None
            closest_distance = 100000
            for pray in win.lists[win.wins[self.type]]:
                if closest_distance>self.distance(pray):
                    closest_distance = self.distance(pray)
                    closest_pray = pray
            if closest_pray:
                max_distance = max(abs(closest_pray.x-self.x), abs(closest_pray.y-self.y))
                self.direction = [(closest_pray.x-self.x)/max_distance, (closest_pray.y-self.y)/max_distance]
                self.x += self.direction[0]*self.step
                self.y += self.direction[1]*self.step




        
        """Random walk"""
        # direction = np.random.randint(-1, 2, size = 2)
        # self.x += direction[0]*self.step
        # self.y += direction[1]*self.step



        if self.x<self.size:
            self.x=self.size
        if self.x>size[0]-self.size:
            self.x=size[0]-self.size
        if self.y<self.size:
            self.y=self.size
        if self.y>size[1]-self.size:
            self.y = size[1]-self.size
        self.coords = [self.x, self.y]

        win.matrix[int(self.x), int(self.y)] = self.type
        self.draw(win.board)

    def distance(self, enemy):
        return abs(self.x-enemy.x)+abs(self.y-enemy.y)

class Win:

    def __init__(self, root):
        self.board = tk.Canvas(root, width=size[0], height=size[1], bg="white")
        self.matrix = np.ndarray(size, dtype=str)
        self.matrix.fill("0")
        self.players=[]
        self.types= ["rock",  "scissors", "paper"]
        self.lists={"rock":[], "scissors":[], "paper":[]}
        self.wins = {"rock":"scissors", "scissors":"paper", "paper":"rock"}
        self.loses = {"rock":"paper", "scissors":"rock", "paper":"scissors"}
        self.steps=0
        self.radius = 20

        self.board.pack()
        
        self.populate()
        
    
    def populate(self):
        for i in range(100,size[0]-1, 100):
            for j in range(100, size[1]-1, 100):
                type = np.random.choice(self.types)
                self.players.append(Player([i, j], type))
                self.lists[type].append(self.players[-1])
        self.step()
    
    def step(self):
        self.steps+=1
        if not self.steps%10:
            self.board.delete("all")
            self.start_time = time.time()
        for player in self.players:
            player.move(self)
        self.check()
        self.board.after(50, self.step)

    def paper_sound(self):
        fileName = "paper"
        fileExtension = "mp3"
        fullPath = fr"{os.getcwd()}\{fileName}.{fileExtension}".replace("\\", "/")
        playsound(fullPath, block = True)
    
    def rock_sound(self):
        fileName = "rock"
        fileExtension = "mp3"
        fullPath = fr"{os.getcwd()}\{fileName}.{fileExtension}".replace("\\", "/")
        playsound(fullPath, block = True)

    def scissors_sound(self):
        fileName = "scissors"
        fileExtension = "mp3"
        fullPath = fr"{os.getcwd()}\{fileName}.{fileExtension}".replace("\\", "/")
        playsound(fullPath, block = True)
    
    def check(self):
        sounds = {"rock":self.rock_sound, "paper":self.paper_sound, "scissors":self.scissors_sound}
        for type in self.types:
            for player in self.lists[type]:
                for enemy in self.lists[self.loses[type]]:
                    if player.distance(enemy)<=self.radius:                        
                        t = threading.Thread(target=sounds[enemy.type])
                        t.start()

                        self.lists[type].remove(player)
                        self.lists[enemy.type].append(player)
                        player.type = enemy.type
                        player.draw(self.board)
                        break

        return


root = tk.Tk()
root.geometry("1200x900+10+10")
root.configure(bg="#96DFCE")
Win(root)

root.mainloop()
