import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import random

# Parameters
G = 1.0  # Growth step size
branching_probability = 0.1  # Probability of branching
n_spores = 10  # Number of spores
N = 55  # Number of steps

# Initialize spores
spores = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n_spores)]
angles = [random.uniform(0, 2 * np.pi) for _ in range(n_spores)]
tips = spores.copy()
hyphae = []

# Initialize the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_title('Fungal Growth Simulation (2D)')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')

# Initialize LineCollection
line_segments = []
line_collection = LineCollection(line_segments, colors='k')
ax.add_collection(line_collection)

# Growth function
def grow(tip, angle):
    dx = G * np.cos(angle)
    dy = G * np.sin(angle)
    new_tip = [tip[0] + dx, tip[1] + dy]
    return new_tip

# Update function for animation
def update(frame):
    global tips, angles, hyphae, line_segments
    new_tips = []
    new_angles = []
    for i, tip in enumerate(tips):
        angle = angles[i]
        new_tip = grow(tip, angle)
        
        # Store the new tip position
        hyphae.append((tip, new_tip))  # Record the hyphal segment
        new_tips.append(new_tip)
        new_angles.append(angle)  # Keep the same direction
        
        # Check for branching
        if random.random() < branching_probability:
            # Create a new branch with a random new direction
            new_branch_angle = angle + np.random.uniform(0, 2 * np.pi)
            new_angles.append(new_branch_angle)
            new_tips.append(new_tip)  # Branch starts from the same point
    
    tips = new_tips
    angles = new_angles
    
    # Update the line segments for hyphae
    new_segments = [[start, end] for start, end in hyphae[len(line_segments):]]
    line_segments.extend(new_segments)
    line_collection.set_segments(line_segments)
    ax.set_title("Fungal Growth Simulation (2D) " + str(frame) + " iteration " + str(len(tips)) + " tips")
    
    return line_collection,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(N), blit=True, interval=100, repeat=False)

# Display the animation
plt.show()