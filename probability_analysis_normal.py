import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# Ensure directory exists
if not os.path.exists('figures'):
    os.makedirs('figures')

# 1. Data Definitions
data = {
    "(A)": [60.0, 93.2], "(B)": [60.0, 150.0], "(C)": [120.5, 172.9],
    "(D)": [170.5, 170.5], "(E)": [115.0, 115.0], "(F)": [72.9, 72.9]
}

means, sigmas = [], []
for bounds in data.values():
    low, high = bounds
    if low == high:
        mu = low
        sigma = 0.05 * mu 
    else:
        mu = (low + high) / 2
        sigma = (high - low) / (2 * 1.96)
    means.append(mu)
    sigmas.append(sigma)

# 2. Mixture Statistics Calculation
mix_mean = np.mean(means)
mix_var = np.mean(np.square(sigmas) + np.square(means)) - np.square(mix_mean)
mix_sd = np.sqrt(mix_var)

# 3. Generate CDF
x_eval = np.linspace(0, 250, 2000)
cdf_total = np.zeros_like(x_eval)
for m, s in zip(means, sigmas):
    cdf_total += norm.cdf(x_eval, loc=m, scale=s) / len(means)

# 4. Extract Confidence Intervals (Quantiles)
# Using np.interp to find where CDF hits 0.025 and 0.975
ci_lower = np.interp(0.025, cdf_total, x_eval)
ci_upper = np.interp(0.975, cdf_total, x_eval)

# --- TERMINAL OUTPUT ---
print("-" * 30)
print("PROBABILISTIC MODEL RESULTS")
print("-" * 30)
print(f"Aggregated Mean: {mix_mean:>10.2f} kg CO2e/kWh")
print(f"Aggregated SD:   {mix_sd:>10.2f} kg CO2e/kWh")
print(f"95% CI Lower:    {ci_lower:>10.2f} kg CO2e/kWh")
print(f"95% CI Upper:    {ci_upper:>10.2f} kg CO2e/kWh")
print("-" * 30)

# 5. Plotting
plt.figure(figsize=(10, 6))
plt.plot(x_eval, cdf_total, color='darkblue', linewidth=3, label='Aggregated Probabilistic Model')

# Vertical lines for Mean and CI
plt.axvline(mix_mean, color='orange', linestyle='--', linewidth=2, label=f'Mean: {mix_mean:.1f}')
plt.axvline(ci_lower, color='red', linestyle=':', linewidth=1.5, label=f'95% CI: [{ci_lower:.1f}, {ci_upper:.1f}]')
plt.axvline(ci_upper, color='red', linestyle=':', linewidth=1.5)

# Shading for Mean ± 1 SD
plt.axvspan(mix_mean - mix_sd, mix_mean + mix_sd, color='orange', alpha=0.1, label='1 SD Range')

# Formatting
plt.title('Figure 2: Probabilistic Model with Normal Distributions', fontsize=14)
plt.xlabel('GWP (kg $CO_2$e/kWh)', fontsize=12)
plt.ylabel('Cumulative Probability $P(X \leq x)$', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower right')
plt.xlim(50, 200)
plt.ylim(0, 1.05)

plt.tight_layout()
plt.savefig('figures/Figure_2_normal.png', dpi=300)
plt.show()