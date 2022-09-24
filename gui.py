from cgitb import text
import tkinter as tk
from tkmacosx import Button
import tkinter.ttk as ttk
import numpy as np

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
        tk.Frame.__init__(self, master)
        master.title("Blockudoku create blocks") #Controls the window title.
        self.pack()

        self.createWidgets()


    def createWidgets(self):

        self.optionsFrame = tk.Frame(self)
        self.optionsFrame.pack()

        labelText=tk.StringVar()
        labelText.set("Enter number of rows")
        labelDir=tk.Label(self.optionsFrame, textvariable=labelText, height=4)
        labelDir.grid(row=0,column=0)
        
        self.rows_var=tk.IntVar(None, 2)
        rows_entry=tk.Entry(self.optionsFrame,textvariable=self.rows_var,width=50)
        rows_entry.grid(row=0,column=1)

        labelText=tk.StringVar()
        labelText.set("Enter number of columns")
        labelDir=tk.Label(self.optionsFrame, textvariable=labelText, height=4)
        labelDir.grid(row=1,column=0)

        self.columns_var=tk.IntVar(None,2)
        columns_entry=tk.Entry(self.optionsFrame,textvariable=self.columns_var,width=50)
        columns_entry.grid(row=1,column=1)
        
        grid_button = Button(self.optionsFrame, text="Create grid!", command = lambda : self.create_grid())
        grid_button.grid(row=2,column=1)


    def create_grid(self):        
        self.buttonsFrame = tk.Frame(self)
        self.buttonsFrame.pack()

        self.rows_num = self.rows_var.get()
        self.cols_num =self.columns_var.get()

        order = list(range( self.rows_num* self.cols_num))
        self.grid_buttons = []
        self.active_buttons = np.zeros((self.rows_num, self.cols_num))

        for i in order:
            button = GridButton(self.buttonsFrame, app=self, text =str(i), order=i)
            button.grid(row = i // self.cols_num, column = i % self.cols_num)
            self.grid_buttons.append(button)

        submit_grid_button = Button(self.buttonsFrame,text="Submit",command= lambda : self.submit_grid())
        submit_grid_button.grid(row=self.rows_num,column=self.cols_num)


    def submit_grid(self):
        print(repr(self.active_buttons))

def main():
    window = tk.Tk()
    app = Application(master=window)

    app.mainloop()

if __name__ == "__main__":
    main()