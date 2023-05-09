import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
import os 
import numpy as np

# Set font and figure size
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 6)})

cwd = os.getcwd()
print(cwd)

df = pd.read_csv('assembler_dataset.csv')
print(df.head())

est = df['estimated HR']
true = df['HR from pulse oximeter']
print(est)
print(true)

# Calculate differences between true and estimated values
diff = true - est

# Calculate mean and standard deviation of differences
mean_diff = np.mean(diff)
std_diff = np.std(diff)

# Plot scatter plot
plt.scatter(est, true, alpha=0.5, color='white', edgecolor='blue')
plt.xlabel('Estimated HR')
plt.ylabel('HR from Pulse Oximeter')
plt.title('Scatter Plot between Estimated HR and HR from Pulse Oximeter')

# Plot line y=x
min_val = min(min(est), min(true))
max_val = max(max(est), max(true))
plt.plot([min_val, max_val], [min_val, max_val], color='red')

# Create Bland-Altman plot                  
f, ax = plt.subplots(1, figsize=(12, 6))
sm.graphics.mean_diff_plot(est, true, ax=ax)
plt.xlabel('Mean of Estimated HR and HR from Pulse Oximeter')
plt.ylabel('Difference of Estimated HR and HR from Pulse Oximeter')
plt.title('Bland-Altman Plot between Estimated HR and HR from Pulse Oximeter')

# Add MAD to Bland-Altman plot
# Calculate mean absolute difference (MAD)
mad = np.mean(np.abs(diff))
print(f"MAD = {mad}")
print(std_diff)

# Add MAD to Bland-Altman plot
plt.axhline(mean_diff + mad, color='black', linestyle='--')
plt.axhline(mean_diff - mad, color='black', linestyle='--')
plt.text(max_val + 1, mean_diff, f'Mean diff: {mean_diff:.2f}\nMAD: {mad:.2f}', va='center')

# Add distribution plot of absolute difference
sns.displot(np.abs(diff), kde=True, color='blue', height=5, aspect=2)
plt.xlabel('Absolute difference between true and estimated HR')
plt.ylabel('Density')
plt.title('Distribution of Absolute Difference between True and Estimated HR')

# Display plots
plt.tight_layout()
plt.show()
