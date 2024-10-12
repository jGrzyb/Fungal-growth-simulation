import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Parameters
w, h = 500, 500  # Grid size
S0 = 2.0  # Initial substrate concentration
n_spores = 5  # Number of spores
ktip_1 = 1  # Initial tip extension rate
ktip_2 = 2  # Difference between max extension rate and ktip_1
Kt = 0.05  # Time to reach half of max extension rate
Ks = 0.2  # Substrate concentration to reach half of max growth level
q = 0.15  # Branching probability
M = 100000  # Max number of hyphae
N = 5000  # Max number of steps

# Initialize grid
substrate = np.full((w, h), S0)
biomass = np.zeros((w, h))

# Initialize spores
spores = [(random.randint(0, w-1), random.randint(0, h-1)) for _ in range(n_spores)]
hyphae = [{'x': x, 'y': y, 'theta': random.uniform(0, 2*np.pi), 'length': 0} for x, y in spores]

# Growth function
def grow(hypha, substrate):
    x0, y0 = hypha['x'], hypha['y']
    theta = hypha['theta']
    length = hypha['length']
    S = substrate[int(x0), int(y0)]
    rtip_i = (ktip_1 + ktip_2 * length / (length + Kt)) * (S / (S + Ks))
    x1 = x0 + rtip_i * np.cos(theta)
    y1 = y0 + rtip_i * np.sin(theta)
    return x1, y1, rtip_i

# Initialize the figure and axis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
im1 = ax1.imshow(substrate, cmap='hot', origin='lower', vmin=0, vmax=S0)
im2 = ax2.imshow(biomass, cmap='Greens', origin='lower', vmin=0, vmax=S0)
ax1.set_title('Substrate Concentration')
ax2.set_title('Biomass Density')

# Update function for animation
def update(frame):
    global hyphae, substrate, biomass
    new_hyphae = []
    for hypha in hyphae:
        x, y, rtip_i = grow(hypha, substrate)
        if 0 <= x < w and 0 <= y < h and substrate[int(x), int(y)] > 0:
            hypha['x'], hypha['y'] = x, y
            hypha['length'] += rtip_i
            substrate[int(x), int(y)] -= rtip_i
            biomass[int(x), int(y)] += rtip_i
            if random.random() < q and len(hyphae) + len(new_hyphae) < M:
                new_hyphae.append({'x': x, 'y': y, 'theta': random.uniform(0, 2*np.pi), 'length': 0})
    hyphae.extend(new_hyphae)
    im1.set_data(substrate)
    im2.set_data(biomass)
    if np.sum(substrate) == 0:
        ani.event_source.stop()
    return im1, im2

# Create the animation
ani = FuncAnimation(fig, update, frames=range(N), blit=False, interval=100, repeat=False)

# Display the animation
plt.show()