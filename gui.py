import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from simulation import Grid, Hyphae

def run_simulation():
    try:
        size = int(size_var.get())
        substrate_mean = float(substrate_mean_var.get())
        translocation_cost = float(translocation_cost_var.get())
        step_count = int(step_count_var.get())
        filepath = filepath_var.get()

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

        grid = Grid(size=size, hyphaes=hyphaes, substrate_mean=substrate_mean, translocation_cost=translocation_cost)
        grid.run(step_count)  
        grid.generate_gifs(interval=50, gap=1, filename=filepath)

        display_gif(f"{filepath}_fungus.gif", fungus_label)
        display_gif(f"{filepath}_substrate.gif", substrate_label)
        
    except Exception as e:
        messagebox.showerror("Simulation Error", str(e))

def display_gif(path, label):
    img = Image.open(path)
    img.seek(0)  # Rewind to the first frame
    frame = ImageTk.PhotoImage(img)
    label.config(image=frame)
    label.image = frame  # Keep a reference
    animate_gif(img, label)

def animate_gif(img, label, frame=0):
    try:
        img.seek(frame)
        next_frame = ImageTk.PhotoImage(img)
        label.config(image=next_frame)
        label.image = next_frame
        frame += 1
        root.after(50, animate_gif, img, label, frame)
    except EOFError:
        animate_gif(img, label, 0)  # Repeat the animation

def add_hyphae():
    frame = tk.Frame(hyphae_frame)
    frame.pack()

    fp_var = tk.StringVar(value='0.5')
    sp_var = tk.StringVar(value='0.25')
    greed_var = tk.StringVar(value='0.01')
    mpl_var = tk.StringVar(value='0.8')
    cc_var = tk.StringVar(value='0.01')
    direction_var = tk.StringVar(value='0')

    labels = ['Forward Prob.', 'Side Prob.', 'Substrate consumption', 'Move Prob Lower', 'Creation Cost', 'Direction']
    vars = [fp_var, sp_var, greed_var, mpl_var, cc_var, direction_var]
    for label, var in zip(labels, vars):
        tk.Label(frame, text=label).pack(side='left')
        tk.Entry(frame, textvariable=var).pack(side='left')
    
    frame.vars = {
        'fp_var': fp_var, 'sp_var': sp_var, 'greed_var': greed_var, 
        'mpl_var': mpl_var, 'cc_var': cc_var, 'direction_var': direction_var
    }
    hyphae_frames.append(frame)

def on_closing():
    root.destroy()

root = tk.Tk()
root.title("Fungal Growth Simulation GUI")
root.protocol("WM_DELETE_WINDOW", on_closing)

size_var = tk.StringVar(value='100')
substrate_mean_var = tk.StringVar(value='0.5')
translocation_cost_var = tk.StringVar(value='0.01')
step_count_var = tk.StringVar(value='50')
filepath_var = tk.StringVar(value='simulation_output')

hyphae_frames = []

# Main frame
main_frame = tk.Frame(root)
main_frame.pack()

# Parameters frame
params_frame = tk.Frame(main_frame)
params_frame.pack()

tk.Label(params_frame, text="Grid Size").pack()
tk.Entry(params_frame, textvariable=size_var).pack()
tk.Label(params_frame, text="Avarage substrate amount").pack()
tk.Entry(params_frame, textvariable=substrate_mean_var).pack()
tk.Label(params_frame, text="Substrate transport cost").pack()
tk.Entry(params_frame, textvariable=translocation_cost_var).pack()
tk.Label(params_frame, text="Number of steps").pack()
tk.Entry(params_frame, textvariable=step_count_var).pack()
tk.Label(params_frame, text="Name of simulation").pack()
tk.Entry(params_frame, textvariable=filepath_var).pack()

# Hyphae frame
hyphae_frame = tk.Frame(main_frame)
hyphae_frame.pack()

tk.Button(main_frame, text="Add Hyphae", command=add_hyphae).pack()

# Run simulation button
tk.Button(main_frame, text="Run Simulation", command=run_simulation).pack()

# Create a frame to hold the two labels
image_frame = tk.Frame(main_frame)
image_frame.pack()

# Create two labels for displaying the images
fungus_label = tk.Label(image_frame)
fungus_label.pack(side='left')

substrate_label = tk.Label(image_frame)
substrate_label.pack(side='left')

add_hyphae()

root.mainloop()