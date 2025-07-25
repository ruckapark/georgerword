import tkinter as tk

class ArrowwordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arrowword")
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack()
        self.create_grid()

    def create_grid(self):
        for i in range(8):
            for j in range(8):
                entry = tk.Entry(self.grid_frame, width=4, justify='center', state='disabled')
                entry.grid(row=i, column=j)

    def run(self):
        self.root.mainloop()
