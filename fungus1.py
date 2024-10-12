import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters (assuming these are defined somewhere in your code)
Nx, Ny = 100, 100  # Grid size
Dt = 0.01  # Time step
Db = 1.0  # Diffusion coefficient for biomass
Dn = 1.0  # Diffusion coefficient for nutrients
zeta = 0.1  # Conversion rate
lambda1 = 0.1  # Uptake efficiency for non-insulated biomass
lambda2 = 0.1  # Uptake efficiency for insulated biomass
n0 = 0.5  # Critical value for mobile biomass

# Initialize arrays
b_n = np.zeros((Nx, Ny))
b_i = np.zeros((Nx, Ny))
n = np.zeros((Nx, Ny))
s = np.ones((Nx, Ny))

# Start with a small amount of fungus in the center
b_n[Nx//2, Ny//2] = 1.0

# Initialize the figure and axis
fig, ax = plt.subplots()
cax = ax.imshow(n, cmap='hot', vmin=0, vmax=1)
cbar = fig.colorbar(cax, label='Mobile Biomass')

def update(t):
    global b_n, b_i, n, s, Dn
    step_skip = 100
    for i in range(step_skip):

        # Compute Laplacians (discretized diffusion)
        laplacian_b_n = np.roll(b_n, 1, axis=0) + np.roll(b_n, -1, axis=0) + \
                        np.roll(b_n, 1, axis=1) + np.roll(b_n, -1, axis=1) - 4 * b_n
        
        laplacian_n = np.roll(n, 1, axis=0) + np.roll(n, -1, axis=0) + \
                    np.roll(n, 1, axis=1) + np.roll(n, -1, axis=1) - 4 * n

        # Update equations
        b_i += Dt * (zeta * Db * laplacian_b_n)
        b_n += Dt * ((1 - zeta) * Db * laplacian_b_n)
        n += Dt * (Dn * laplacian_n + s * (lambda1 * b_n + lambda2 * b_i))
        s -= Dt * (lambda1 * b_n + lambda2 * b_i) * s

        # Apply threshold for mobile biomass
        Dn = np.where(n > n0, 10**-7 * Db, Dn)

        # Clamp values to ensure non-negative concentrations
        n = np.clip(n, 0, 1)
        b_i = np.clip(n, 0, 1)

    result = n
    # Update the image data
    cax.set_array(result)
    cax.set_clim(vmin=np.min(result), vmax=np.max(result))  # Update color limits
    cbar.update_normal(cax)  # Update colorbar
    ax.set_title(f'Time step: {t*step_skip}')
    return cax,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(0, 201, 1), blit=False, interval=10, repeat=False)
# Display the animation
plt.show()