from cgitb import text
from symbol import while_stmt
from time import sleep
import tkinter as tk
from typing import List
from tkmacosx import Button
import tkinter.ttk as ttk
import numpy as np
from blocks import blocks
from solver import one_round, pick_multiple_blocks

NUM_COLS = 9
NUM_ROWS = 9
SIZE = 32


def start_simulation(app, chosen_blocks: List[List[int]], map:List[List[int]], one_step: bool=False):
    """Does one best step

    Args:
        app (_type_): Application reference
        chosen_blocks (List[List[int]]): blocks picked for this run
        map (List[List[int]]): map of this run
    """
    print("Start!")
    print(chosen_blocks)

    counter = 0
    while (True):
        print(f"Step:   {counter}")
        counter +=1

        app.master.update()

        best_map = one_round(map,chosen_blocks)
        if best_map:
            best_map = best_map[0][1]
        
        else:
            print("Map is full 😥")
            break

        app.map_array = best_map.map
        map = app.map_array

        
        app.create_steps_view(best_map.steps)
        app.create_map()

        if one_step:
            break
        
        app.chosen_blocks = pick_multiple_blocks()
        chosen_blocks = app.chosen_blocks
        app.create_block_choice()
        sleep(0.3)
        
        

class GridButton(Button):
    def __init__(self, master=None, app=None, order= None, cnf=..., **kw):
        self.app = app
        self.order = order
        self.isActive = False
        super().__init__(master, cnf, command= lambda : self.button_action(self.order),activebackground="blue",**kw)
    
    def button_action(self, button):
        self.isActive = not self.isActive
        self.app.active_buttons[self.order // self.app.cols_num][self.order % self.app.cols_num] = self.isActive
        color = "red" if self.isActive else "white"
        self.configure(bg=color)

class Application(tk.Frame):
    def __init__(self, master: None) -> None:
        tk.Frame.__init__(self, master, width=500,height=500)
        master.title("Blockudoku Simulator") #Controls the window title.
        self.pack()

        self.columns = NUM_COLS
        self.rows = NUM_ROWS
        self.color1 = "white"
        self.color2 = "blue"

        self.map_array = np.zeros((9,9),dtype=int)

        self.map_frame = tk.Frame(self, width=500,height=500,bg="yellow")
        self.map_frame.pack(side='top')

        self.blocks_frame = tk.Frame(self, width=1000, height=500,bg="orange")
        self.blocks_frame.pack(side='top')

        self.chosen_blocks_frame = tk.Frame(self, width=1000, height=500,bg="green")
        self.chosen_blocks_frame.pack(side='top')

        self.chosen_blocks = []

        self.steps_frame = tk.Frame(self, width=1000, height=500,bg="blue")
        self.steps_frame.pack(side='top')

        self.create_map()
        self.create_possible_blocks()
        self.create_block_choice()


    def create_map(self):
        self.reset_frame(self.map_frame)

        canvas_width = NUM_COLS * SIZE
        canvas_height = NUM_ROWS * SIZE

        canvas = tk.Canvas(self.map_frame, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
    
        self.create_grid_canvas(SIZE,canvas,self.map_array)


    def create_possible_blocks(self):
        self.reset_frame(self.blocks_frame)

        for block in blocks:
            block_size_x = block.shape[1] # num cols of block
            block_size_y = block.shape[0] # num rows of block

            canvas_width = block_size_x * (SIZE // 2)
            canvas_height = block_size_y * (SIZE // 2)

            canvas = tk.Canvas(self.blocks_frame, borderwidth=0, highlightthickness=0,
                                    width=canvas_width, height=canvas_height, background="bisque")

            canvas.bind("<Button-1>", lambda event, b=block :self.choose_block(b))                                    
            canvas.pack(side='left', fill="both", expand=True, padx=2, pady=2)
            self.create_grid_canvas(SIZE//2,canvas,block)


    def create_block_choice(self):
        self.reset_frame(self.chosen_blocks_frame)
        
        choices_frame = tk.Frame(self.chosen_blocks_frame)
        choices_frame.pack(side='top')

        for idx in range(len(self.chosen_blocks)):

            block = self.chosen_blocks[idx]
            block_size_x = block.shape[1] # num cols of block
            block_size_y = block.shape[0] # num rows of block

            canvas_width = block_size_x * (SIZE)
            canvas_height = block_size_y * (SIZE)

            canvas = tk.Canvas(choices_frame, borderwidth=0, highlightthickness=0,
                                    width=canvas_width, height=canvas_height, background="bisque")

            canvas.bind("<Button-1>", lambda event, i=idx :self.rotate_chosen_block(i))                                    
            canvas.pack(side='left', fill="both", expand=True, padx=2, pady=2)
            self.create_grid_canvas(SIZE,canvas,block)

        button_frame = tk.Frame(self.chosen_blocks_frame)
        button_frame.pack(side='top')
        refresh_button = Button(self.chosen_blocks_frame,text="New choice", 
                                command= lambda : self.reset_chosen() )
        refresh_button.pack(side="bottom")

        start_button = Button(self.chosen_blocks_frame,text="Start", 
                                command= lambda a=self, chosen=self.chosen_blocks, map=self.map_array: start_simulation(a,chosen,map))
        start_button.pack(side="bottom")


    def create_steps_view(self, steps):
        self.reset_frame(self.steps_frame)
        
        for idx in range(len(steps)):

            block = steps[idx]
            block_size_x = block.shape[1] # num cols of block
            block_size_y = block.shape[0] # num rows of block

            canvas_width = block_size_x * (SIZE)
            canvas_height = block_size_y * (SIZE)

            canvas = tk.Canvas(self.steps_frame, borderwidth=0, highlightthickness=0,
                                    width=canvas_width, height=canvas_height, background="bisque")
                                    
            canvas.pack(side='left', fill="both", expand=True, padx=2, pady=2)
            self.create_grid_canvas(SIZE,canvas,block)


    def create_grid_canvas(self,grid_size,canvas, block_array):    
        rows = block_array.shape[0]
        columns = block_array.shape[1]

        size = grid_size
        canvas.delete("square")
        for row in range(rows):
            for col in range(columns):
                x1 = (col * size)
                y1 = (row * size)
                x2 = x1 + size
                y2 = y1 + size

                w_color = "white"
                if ((row // 3 != 1) and (col // 3 != 1)) \
                    or ((row // 3 == 1) and (col // 3 == 1)):
                    w_color = "gray80"

                color = 'blue' if block_array[row][col] == 1 else w_color

                canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")


    def reset_chosen(self):
        self.chosen_blocks = []
        self.create_block_choice()

    def rotate_chosen_block(self,idx):
        self.chosen_blocks[idx] = np.rot90(self.chosen_blocks[idx],k=1)
        self.create_block_choice()


    def choose_block(self,block):
        print(f"Clicked block: {block}" )
        self.chosen_blocks.append(block)
        print(self.chosen_blocks)
        self.create_block_choice()


    def reset_frame(self,frame):
        for child in frame.winfo_children():
            child.destroy()


    def submit_grid(self):
        print(repr(self.active_buttons))


def main():
    window = tk.Tk()
    app = Application(master=window)

    app.mainloop()

if __name__ == "__main__":
    main()