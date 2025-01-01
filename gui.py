import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
from PIL import Image, ImageTk
from io import BytesIO
from fractal_noise import get_fractal_noise
from simulation import Grid, Hyphae  

def run_simulation():
    try:
        size = int(size_var.get())
        num_hyphae = int(hyphae_count_var.get())
        forward_prob = float(forward_prob_var.get())
        side_prob = float(side_prob_var.get())
        greed = float(greed_var.get())
        move_prob_lower = float(move_prob_lower_var.get())
        creation_cost = float(creation_cost_var.get())
        
        
        hyphaes = [Hyphae(forward_probability=forward_prob, side_probability=side_prob,
                          greed=greed, move_probab_lower=move_prob_lower,
                          creation_cost=creation_cost) for _ in range(num_hyphae)]
        
        
        grid = Grid(size=size, hyphaes=hyphaes)
        grid.run(50)  
        grid.generate_gifs(filename="simulation_output") 
        
        
        with open("fungus_simulation_output.gif", 'rb') as f:
            image_bytes = f.read()
            data_stream = BytesIO(image_bytes)
            pil_image = Image.open(data_stream)
            tk_image = ImageTk.PhotoImage(pil_image)
            display_label.config(image=tk_image)
            display_label.image = tk_image 
        
    except Exception as e:
        messagebox.showerror("Simulation Error", str(e))

def save_configuration():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as file:
            data = f"{size_var.get()},{hyphae_count_var.get()},{forward_prob_var.get()},{side_prob_var.get()},"
            data += f"{greed_var.get()},{move_prob_lower_var.get()},{creation_cost_var.get()}"
            file.write(data)

def load_configuration():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            params = file.read().split(',')
            size_var.set(params[0])
            hyphae_count_var.set(params[1])
            forward_prob_var.set(params[2])
            side_prob_var.set(params[3])
            greed_var.set(params[4])
            move_prob_lower_var.set(params[5])
            creation_cost_var.set(params[6])

root = tk.Tk()
root.title("Fungal Growth Simulation GUI")

# Entry variables
size_var = tk.StringVar(value='100')
hyphae_count_var = tk.StringVar(value='1')
forward_prob_var = tk.StringVar(value='0.5')
side_prob_var = tk.StringVar(value='0.25')
greed_var = tk.StringVar(value='0.01')
move_prob_lower_var = tk.StringVar(value='0.8')
creation_cost_var = tk.StringVar(value='0.01')


entries = [
    ("Grid Size", size_var),
    ("Number of Hyphae", hyphae_count_var),
    ("Forward Probability", forward_prob_var),
    ("Side Probability", side_prob_var),
    ("Greed", greed_var),
    ("Move Probability Lower Bound", move_prob_lower_var),
    ("Creation Cost", creation_cost_var)
]

for label, var in entries:
    tk.Label(root, text=label).pack()
    entry = tk.Entry(root, textvariable=var)
    entry.pack()

# Buttons
run_button = tk.Button(root, text="Run Simulation", command=run_simulation)
run_button.pack()
save_button = tk.Button(root, text="Save Configuration", command=save_configuration)
save_button.pack()
load_button = tk.Button(root, text="Load Configuration", command=load_configuration)
load_button.pack()


display_label = tk.Label(root)
display_label.pack()

root.mainloop()


