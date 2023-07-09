import tkinter as tk
import numpy as np
from PIL import ImageTk,Image 
import time

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
        
        
        # win.matrix[int(self.x), int(self.y)] = "0"
        
        direction = np.random.randint(-1, 2, size = 2)
        self.x += direction[0]*self.step
        self.y += direction[1]*self.step
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
        # type1 = "rock"
        # type2="paper"
        # self.players.append(Player([100, 100], type1))
        # self.lists[type1].append(self.players[-1])
        # self.players.append(Player([110, 100], type2))
        # self.lists[type2].append(self.players[-1])
        self.step()
    
    def step(self):
        # print(len(self.players))
        self.steps+=1
        if not self.steps%10:
            self.board.delete("all")
            # print("deleted")
            # start_time = time.time()
            self.start_time = time.time()
        for player in self.players:
            player.move(self)
        # if not self.steps%10:
            # print(time.time()-start_time)
        self.check()
        self.board.after(50, self.step)
    
    def check(self):
        for type in self.types:
            for player in self.lists[type]:
                for enemy in self.lists[self.loses[type]]:
                    if player.distance(enemy)<=self.radius:
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
