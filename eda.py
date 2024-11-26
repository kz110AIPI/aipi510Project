import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Load the datasets
non_progressing_df = pd.read_csv('non_progressing_subset.csv')
progressing_df = pd.read_csv('progressing_subset.csv')

# Define CpG sites
cpg_sites = ['cg12374721', 'cg18081940', 'cg04475027']

# Extract relevant CpG sites and add a group column
non_progressing_cpg = non_progressing_df[cpg_sites].copy()
non_progressing_cpg['Group'] = 'Non-Progressing'

progressing_cpg = progressing_df[cpg_sites].copy()
progressing_cpg['Group'] = 'Progressing'

# Combine the two datasets for visualization
combined_df = pd.concat([non_progressing_cpg, progressing_cpg])

# Create boxplots for each CpG site
for cpg in cpg_sites:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Group', y=cpg, data=combined_df, palette="Set2")
    plt.title(f"Comparison of {cpg} Between Progressing and Non-Progressing Samples")
    plt.ylabel("Methylation Level")
    plt.xlabel("Group")
    plt.show()

# Perform t-tests for each CpG site and store the results
results = []
for cpg in cpg_sites:
    t_stat, p_val = ttest_ind(non_progressing_df[cpg], progressing_df[cpg], nan_policy='omit')
    results.append({'CpG Site': cpg, 'T-Statistic': t_stat, 'P-Value': p_val})

# Convert results to a DataFrame and save as CSV
results_df = pd.DataFrame(results)
results_df.to_csv('cpg_sites_statistical_results.csv', index=False)

# Print results
print(results_df)
