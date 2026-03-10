import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure directory exists
if not os.path.exists('figures'):
    os.makedirs('figures')

# 1. Define the Data (A-F)
data = {
    "(A)": [60.0, 93.2],
    "(B)": [60.0, 150.0],
    "(C)": [120.5, 172.9],
    "(D)": [170.5, 170.5],
    "(E)": [115.0, 115.0],
    "(F)": [72.9, 72.9]
}

# 2. Generate the CDF
# We assume a Uniform Distribution within each range for the probabilistic approach
x_eval = np.linspace(50, 185, 1000)
cdf_total = np.zeros_like(x_eval)

for bounds in data.values():
    low, high = bounds
    if low == high:
        # Scalar: Step function at the specific value
        cdf_i = np.where(x_eval >= low, 1.0, 0.0)
    else:
        # Range: Linear ramp (Uniform CDF) from 0 to 1
        cdf_i = np.clip((x_eval - low) / (high - low), 0, 1)
    
    cdf_total += cdf_i

# Average the 6 distributions
cdf_total /= len(data)

# 2. Statistics for Mixture of Uniforms
means = [np.mean(b) for b in data.values()]
variances = [((b[1]-b[0])**2 / 12) if b[1] != b[0] else 0 for b in data.values()]

mix_mean = np.mean(means)
# Variance of mixture = average(variances + means^2) - mean(means)^2
mix_var = np.mean(np.array(variances) + np.array(means)**2) - mix_mean**2
mix_sd = np.sqrt(mix_var)

# 3. CDF Quantiles (using interpolation from your x_eval and cdf_total)
ci_lower = np.interp(0.025, cdf_total, x_eval)
ci_upper = np.interp(0.975, cdf_total, x_eval)

# 4. Plotting
plt.figure(figsize=(10, 6))

# Plot the main CDF curve
plt.plot(x_eval, cdf_total, color='darkgreen', linewidth=3, label='Aggregated CDF (A-F)')

# Markers for the individual source locations for clarity
for label, bounds in data.items():
    plt.axvline(bounds[0], color='gray', linestyle=':', alpha=0.3)
    if bounds[0] != bounds[1]:
        plt.axvline(bounds[1], color='gray', linestyle=':', alpha=0.3)

# Formatting
plt.title('Figure 3: Probabilistic Model with Uniform Distributions', fontsize=14)
plt.xlabel('GWP (kg $CO_2$e/kWh)', fontsize=12)
plt.ylabel('Cumulative Distribution Function (CDF) $P(X \leq x)$', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.ylim(0, 1.05)
plt.xlim(50, 185)
plt.legend(loc='lower right')

plt.tight_layout()
plt.savefig('figures/Figure_3_uniform.png', dpi=300)
plt.show()

print(f"Mean: {mix_mean:.2f} | SD: {mix_sd:.2f}")
print(f"95% CI: [{ci_lower:.2f}, {ci_upper:.2f}]")