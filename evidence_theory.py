import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure directory exists
if not os.path.exists('figures'):
    os.makedirs('figures')

# 1. Data from literature (6 sources)
# Basic Belief Assignment (BBA): We assign equal mass m = 1/6 to each study.
data = [
    {"name": "André & Hajek", "bounds": (120.5, 172.9)},
    {"name": "Liberacki et al.", "bounds": (170.5, 170.5)},
    {"name": "Pollet et al.", "bounds": (115.0, 115.0)},
    {"name": "Pontika/Dai", "bounds": (72.9, 72.9)},
    {"name": "Abdelbaky et al.", "bounds": (60.0, 93.2)},
    {"name": "Amarakoon et al.", "bounds": (60.0, 150.0)}
]

n = len(data)
mass = 1.0 / n  

# 2. Evaluation
x_vals = np.linspace(40, 200, 2000)
bel_vals = []
pl_vals = []

for x in x_vals:
    bel = 0
    pl = 0
    for d in data:
        low, high = d["bounds"]
        # Belief (Bel): Cumulative mass of evidence strictly supporting [GWP <= x]
        # This only happens if the ENTIRE interval is below x.
        if high <= x:
            bel += mass
        
        # Plausibility (Pl): Cumulative mass of evidence that DOES NOT contradict [GWP <= x]
        # This happens if at least part of the interval (the lower bound) is below x.
        if low <= x:
            pl += mass
            
    bel_vals.append(bel)
    pl_vals.append(pl)

# 3. Visualization
plt.figure(figsize=(10, 6))

# Plotting the P-Box bounds
plt.step(x_vals, pl_vals, label='Cumulative Plausibility Function (CPF) - Upper Bound', 
         where='post', color='blue', linewidth=2.5)
plt.step(x_vals, bel_vals, label='Cumulative Belief Function (CBF) - Lower Bound', 
         where='post', color='red', linewidth=2.5)

# Shading the area of "Ignorance"
plt.fill_between(x_vals, bel_vals, pl_vals, step='post', color='gray', alpha=0.2, 
                 label='Epistemic Uncertainty (Ignorance)')

# Formatting
plt.xlabel('Battery GWP [$kg CO_2e / kWh$]', fontsize=12)
plt.ylabel('Belief / Plausibility', fontsize=12)
plt.title('Figure 4: Evidence Theory Probability Box (P-Box)', fontsize=14)
plt.grid(True, which='both', linestyle=':', alpha=0.6)
plt.legend(loc='lower right', fontsize=10)
plt.ylim(0, 1.05)
plt.xlim(50, 185)

plt.tight_layout()
plt.savefig('figures/Figure_4_evidence.png', dpi=300)
plt.show()

# Terminal Output for GitHub logic check
print(f"Evidence Theory Model Complete.")
print(f"At GWP=100: Bel={np.interp(100, x_vals, bel_vals):.2f}, Pl={np.interp(100, x_vals, pl_vals):.2f}")