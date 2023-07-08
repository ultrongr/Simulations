import tkinter as tk
import numpy as np
from PIL import ImageTk,Image 

size  = [1000, 700]
np.random.seed(123)

class Player:
    def __init__(self, coords, color):
        self.coords = coords
        self.x = coords[0]
        self.y = coords[1]
        self.color = color
        self.shape  = None
        self.size = 10
        self.step = 10
        self.img=None
    
    def draw(self, board):
        if self.img:   
            board.delete(self.img)
        self.img = ImageTk.PhotoImage(Image.open("scissors.png"))
        board.create_image(self.x,self.y, anchor='nw', image=self.img)
        # self.shape = board.create_oval(self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size, width = 0, fill=self.color)
        board.pack()
    
    def move(self, matrix, board):
        
        
        matrix[int(self.x), int(self.y)] = "0"
        
        direction = np.random.randint(-1, 2, size = (2))
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

        matrix[int(self.x), int(self.y)] = self.color
        self.draw(board)
        # self.shape = board.create_oval(self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size, width = 0, fill=self.color)
        # board.after(3000, self.move, matrix, board)


class Win:

    def __init__(self, root):
        self.board = tk.Canvas(root, width=size[0], height=size[1], bg="white")
        self.matrix = np.ndarray(size, dtype=str)
        self.matrix.fill("0")
        self.players=[]
        # img = tk.PhotoImage(file="ball.ppm")      
        # self.board.create_image(200,200, anchor="nw", image=img)  
        
        # img = ImageTk.PhotoImage(Image.open("ball.jpg"))  
        # self.board.create_image(20, 20, anchor="nw", image=img) 
        
        # img = ImageTk.PhotoImage(Image.open("scissors.png"))
        # self.board.create_image(5,5, anchor='nw', image=img)
        # self.board.image = img
        self.board.pack()
        
        self.populate()
        
    
    def populate(self):
        colors = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "black"]
        for i in range(100,size[0]-1, 100):
            for j in range(100, size[1]-1, 100):
                self.players.append(Player([i, j], np.random.choice(colors)))
        
        self.step()
    
    def step(self):
        for player in self.players:
            player.move(self.matrix, self.board)
        self.board.after(1, self.step)

root = tk.Tk()
root.geometry("1200x900+10+10")
root.configure(bg="#96DFCE")
Win(root)

root.mainloop()