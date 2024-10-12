import numpy as np
import matplotlib.pyplot as plt

# Parameters
Nx, Ny = 100, 100   # Grid size
Db = 10             # Diffusion coefficient for biomass
Dn = 10             # Initial diffusion coefficient for nutrients
zeta = 0.5          # Conversion rate
lambda1, lambda2 = 0.95, 0.01
n0 = 1           # Critical value for mobile biomass
Dt = 0.01           # Time step

# Initial conditions
b_n = np.zeros((Nx, Ny))  # Non-insulated biomass
b_i = np.zeros((Nx, Ny))  # Insulated biomass
n = np.zeros((Nx, Ny))    # Mobile biomass
s = np.ones((Nx, Ny))     # Substrate (nutrient)

# Start with a small amount of fungus in the center
b_n[Nx//2, Ny//2] = 1.0

# Simulation loop
for t in range(1000):  # Run for 1000 time steps
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
    
    # Visualization (every 100 time steps)
    if t % 100 == 0:
        plt.imshow(n, cmap='hot')
        plt.title(f'Time step: {t}')
        plt.colorbar(label='Mobile Biomass')
        plt.show()
