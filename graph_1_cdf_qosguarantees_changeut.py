import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Step 1: Read and Filter Log Files
def read_and_filter_logs(log_dir):
    data = []
    for filename in os.listdir(log_dir):
        if filename.endswith(".log"):
            with open(os.path.join(log_dir, filename), 'r') as file:
                for line in file:
                    if line.startswith("OUTPUT"):
                        parts = line.strip().split(',')
                        if parts[1] == "nru" and float(parts[2]) > 0:
                            data.append([filename] + parts)
    return pd.DataFrame(data, columns=["filename", "type", "flow_type", "guaranteed_throughput", "guaranteed_delay", "achieved_throughput", "achieved_delay"])

log_dir = 'path_to_log_files'
df = read_and_filter_logs(log_dir)

# Step 2: Parse Data
df['guaranteed_throughput'] = pd.to_numeric(df['guaranteed_throughput'])
df['guaranteed_delay'] = pd.to_numeric(df['guaranteed_delay'])
df['achieved_throughput'] = pd.to_numeric(df['achieved_throughput'])
df['achieved_delay'] = pd.to_numeric(df['achieved_delay'])

# Step 3: Aggregate Data
def extract_identifiers(filename):
    parts = filename.split('-')
    num_uts = int(parts[2][3:])
    capc = int(parts[6][4:])
    run = int(parts[8][3:].replace(".log", ""))
    return num_uts, capc, run

df['num_uts'], df['capc'], df['run'] = zip(*df['filename'].apply(extract_identifiers))

# Group by identifiers and calculate mean and 95% CI
grouped = df.groupby(['num_uts', 'capc', 'flow_type', 'guaranteed_throughput', 'guaranteed_delay'])

mean_df = grouped.mean().reset_index()
std_df = grouped.std().reset_index()

mean_df['achieved_throughput_upper'] = mean_df['achieved_throughput'] + 1.96 * (std_df['achieved_throughput'] / np.sqrt(5))
mean_df['achieved_throughput_lower'] = mean_df['achieved_throughput'] - 1.96 * (std_df['achieved_throughput'] / np.sqrt(5))

mean_df['achieved_delay_upper'] = mean_df['achieved_delay'] + 1.96 * (std_df['achieved_delay'] / np.sqrt(5))
mean_df['achieved_delay_lower'] = mean_df['achieved_delay'] - 1.96 * (std_df['achieved_delay'] / np.sqrt(5))

# Step 4: Calculate Ratios
mean_df['throughput_ratio'] = mean_df['achieved_throughput'] / mean_df['guaranteed_throughput']
mean_df['delay_ratio'] = mean_df['guaranteed_delay'] / mean_df['achieved_delay']

# Step 5: Generate CDF Plots
def plot_cdf(data, column, title, xlabel, filename):
    sorted_data = np.sort(data)
    yvals = np.arange(1, len(sorted_data)+1) / float(len(sorted_data))

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_data, yvals, marker='.', linestyle='none')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('CDF')
    plt.grid(True)
    plt.savefig(filename)
    plt.show()

# Plotting CDF for throughput guarantees
plot_cdf(mean_df['throughput_ratio'], 'throughput_ratio', 'CDF of Throughput Guarantees', 'Throughput Ratio', 'throughput_cdf.png')

# Plotting CDF for delay guarantees
plot_cdf(mean_df['delay_ratio'], 'delay_ratio', 'CDF of Delay Guarantees', 'Delay Ratio', 'delay_cdf.png')
