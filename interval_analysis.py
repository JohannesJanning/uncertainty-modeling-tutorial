import matplotlib.pyplot as plt
import os

# Create figures directory
if not os.path.exists('figures'):
    os.makedirs('figures')

# 1. Define the Data with labels A-F
# Structure: "Label": [min, max, "Full Name Reference"]
data = {
    "(A)": [60.0, 93.2, "Abdelbaky et al."],
    "(B)": [60.0, 150.0, "Amarakoon et al."],
    "(C)": [120.5, 172.9, "André & Hajek"],
    "(D)": [170.5, 170.5, "Liberacki et al."],
    "(E)": [115.0, 115.0, "Pollet et al."],
    "(F)": [72.9, 72.9, "Pontika et al."]
}

# 2. Perform Interval Analysis
all_min = min(val[0] for val in data.values())
all_max = max(val[1] for val in data.values())

# --- FIGURE 1: ---
plt.figure(figsize=(9, 5))
labels = list(data.keys())
y_pos = range(len(labels))

# Plot individual studies (A-F)
for i, label in enumerate(labels):
    bounds = data[label][:2]
    if bounds[0] == bounds[1]:
        plt.plot(bounds[0], i, 'ko', markersize=7) # Scalar
    else:
        plt.plot(bounds, [i, i], 'b|-', linewidth=2, markersize=8) # Range

# Plot the Resulting Union at the bottom
plt.axvspan(all_min, all_max, color='gray', alpha=0.1)
plt.plot([all_min, all_max], [-1, -1], 'r|-', linewidth=3, markersize=10)

plt.yticks(list(y_pos) + [-1], labels + ["Union Result"])
plt.xlabel('GWP (kg $CO_2$e/kWh)')
plt.title('Figure 1: Interval Analysis')
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('figures/Figure_1_interval.png', dpi=300)

plt.show()

print(f"Success! Figures saved in /figures/")
print(f"Interval: [{all_min}, {all_max}]")