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
       
        hyphaes = []
        for hyphae_frame in hyphae_frames:
            fp = float(hyphae_frame.vars['fp_var'].get())
            sp = float(hyphae_frame.vars['sp_var'].get())
            greed = float(hyphae_frame.vars['greed_var'].get())
            mpl = float(hyphae_frame.vars['mpl_var'].get())
            cc = float(hyphae_frame.vars['cc_var'].get())
            direction = int(hyphae_frame.vars['direction_var'].get())
            hyphaes.append(Hyphae(forward_probability=fp, side_probability=sp, greed=greed,
                                  move_probab_lower=mpl, creation_cost=cc, direction=direction))

        grid = Grid(size=size, hyphaes=hyphaes)
        grid.run(50)  # You can make the number of steps a GUI parameter too
        grid.generate_gifs(filename="simulation_output")

        # Display the first GIF
        display_gif("fungus_simulation_output.gif")
        
    except Exception as e:
        messagebox.showerror("Simulation Error", str(e))

def display_gif(path):
    img = Image.open(path)
    frame = ImageTk.PhotoImage(img)
    display_label.config(image=frame)
    display_label.image = frame  # Keep a reference

def add_hyphae():
    # Frame for one hyphae's settings
    frame = tk.Frame(root)
    frame.pack()

   
    fp_var = tk.StringVar(value='0.5')
    sp_var = tk.StringVar(value='0.25')
    greed_var = tk.StringVar(value='0.01')
    mpl_var = tk.StringVar(value='0.8')
    cc_var = tk.StringVar(value='0.01')
    direction_var = tk.StringVar(value='0')

   
    labels = ['Forward Prob.', 'Side Prob.', 'Greed', 'Move Prob Lower', 'Creation Cost', 'Direction']
    vars = [fp_var, sp_var, greed_var, mpl_var, cc_var, direction_var]
    for label, var in zip(labels, vars):
        tk.Label(frame, text=label).pack(side='left')
        tk.Entry(frame, textvariable=var).pack(side='left')
    
   
    frame.vars = {
        'fp_var': fp_var, 'sp_var': sp_var, 'greed_var': greed_var, 
        'mpl_var': mpl_var, 'cc_var': cc_var, 'direction_var': direction_var
    }
    print(frame.vars)
    hyphae_frames.append(frame)


def on_closing():
    root.destroy()


root = tk.Tk()
root.title("Fungal Growth Simulation GUI")
root.protocol("WM_DELETE_WINDOW", on_closing)

size_var = tk.StringVar(value='100')

hyphae_frames = []

tk.Label(root, text="Grid Size").pack()
tk.Entry(root, textvariable=size_var).pack()

tk.Button(root, text="Add Hyphae", command=add_hyphae).pack()

tk.Button(root, text="Run Simulation", command=run_simulation).pack()

# Label for displaying the GIF
display_label = tk.Label(root)
display_label.pack()

root.mainloop()

