import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

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
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(np.arange(Nx), np.arange(Ny))
cax = ax.plot_surface(X, Y, n, cmap='hot')

def update(t):
    global b_n, b_i, n, s, Dn
    step_skip = 50
    for i in range(step_skip):

        # Compute Laplacians (discretized diffusion)
        laplacian_b_n = np.roll(b_n, 1, axis=0) + np.roll(b_n, -1, axis=0) + \
                        np.roll(b_n, 1, axis=1) + np.roll(b_n, -1, axis=1) - 4 * b_n
        
        laplacian_n = np.roll(n, 1, axis=0) + np.roll(n, -1, axis=0) + \
                    np.roll(n, 1, axis=1) + np.roll(n, -1, axis=1) - 4 * n

        # Update equations
        delta_b_i = Dt * (zeta * Db * laplacian_b_n)
        delta_b_n = Dt * ((1 - zeta) * Db * laplacian_b_n)
        
        b_i += delta_b_i
        b_n += delta_b_n - delta_b_i  # Ensure conservation of total biomass

        n += Dt * (Dn * laplacian_n + s * (lambda1 * b_n + lambda2 * b_i))
        s -= Dt * (lambda1 * b_n + lambda2 * b_i) * s

        # Apply threshold for mobile biomass
        Dn = np.where(n > n0, 10**-7 * Db, Dn)

        # Clamp values to ensure non-negative concentrations
        n = np.clip(n, 0, 1)
        b_i = np.clip(b_i, 0, 1)
        b_n = np.clip(b_n, 0, 1)

    # Update the surface plot
    ax.clear()
    ax.plot_surface(X, Y, n, cmap='hot')
    ax.set_zlim(np.min(n), np.max(n))  # Set z-axis limits
    ax.set_title(f'Time step: {t*step_skip}')
    return ax,

# Create the animation
ani = FuncAnimation(fig, update, frames=range(0, 201, 1), blit=False, interval=10, repeat=False)

# Display the animation
plt.show()