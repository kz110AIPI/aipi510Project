from statsmodels.stats.power import TTestIndPower

# Parameters
effect_size = 0.5    # assumed medium effect size
alpha = 0.05         # significance level
power = 0.8          # power level

# Create an instance of the power analysis object
analysis = TTestIndPower()

# Calculate the required sample size
sample_size = analysis.solve_power(effect_size=effect_size, power=power, alpha=alpha, alternative='two-sided')
print("Required sample size per group:", sample_size)
