import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from scipy import stats

# Function to calculate QoS metrics from multiple files and calculate confidence intervals
def calculate_qos_metrics(file_path):
    guaranteed_throughputs = []
    guaranteed_delays = []
    achieved_delays = []
    achieved_throughputs = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            if row[0] == 'OUTPUT':
                achieved_throughputs.append(float(row[4]))
                achieved_delays.append(float(row[5]))

    AverageThroughput = np.array(achieved_throughputs)
    AverageDelay = np.array(achieved_delays)

    return AverageThroughput, AverageDelay

# List of user terminals to consider
user_terminals = [4, 5] #, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50]
capc_configs = [0, 1]
num_runs = 25
trafficModel = 1

# Initialize lists to store results
throughput_guarantees = {capc: [] for capc in capc_configs}
delay_guarantees = {capc: [] for capc in capc_configs}
throughput_ci = {capc: [] for capc in capc_configs}
delay_ci = {capc: [] for capc in capc_configs}

# Iterate over each user terminal and calculate QoS metrics for multiple runs
for ut in user_terminals:
    for capc in capc_configs:
        if capc == 0:
            scheduler = "PF"
            lcScheduler = 0
        else:
            scheduler = "Qos"
            lcScheduler = 1
        file_paths = [f'nru-csv/ip/changeuts-gnb6-ap0-ut{ut}-ratio1111-numerology1-bandwidth20-scheduler{scheduler}-lcScheduler{lcScheduler}-trafficModel{trafficModel}-capc{capc}-simtime5-run{i}.csv' for i in range(num_runs)]
        throughputs = []
        delays = []
        for file_path in file_paths:
            throughput, delay = calculate_qos_metrics(file_path)
            throughputs.extend(throughput)
            delays.extend(delay)
        throughput_guarantees[capc].append(np.mean(throughputs))
        delay_guarantees[capc].append(np.mean(delays))
        throughput_ci[capc].append(stats.sem(throughputs) * stats.t.ppf((1 + 0.95) / 2, len(throughputs) - 1))
        delay_ci[capc].append(stats.sem(delays) * stats.t.ppf((1 + 0.95) / 2, len(delays) - 1))
        # Let us check if this ppf command is correct.

# Plotting the results
x = np.arange(len(user_terminals))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot for Throughput Guarantees vs User Terminals
ax[0].bar(x - width/2, throughput_guarantees[0], width, yerr=throughput_ci[0], label='Static CAPC')
ax[0].bar(x + width/2, throughput_guarantees[1], width, yerr=throughput_ci[1], label='Proposed Dynamic CAPC')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[0].set_xlabel('User Terminals Per gNB')
ax[0].set_ylabel('Average Throughput (Mbps)')
ax[0].set_title('Average Throughput (Mbps) of All Devices in Scenario vs User Terminals')
ax[0].set_xticks(x)
ax[0].set_xticklabels(user_terminals)
ax[0].legend()
ax[0].grid(True)

# Plot for Delay Guarantees vs User Terminals
ax[1].bar(x - width/2, delay_guarantees[0], width, yerr=delay_ci[0], label='Static CAPC')
ax[1].bar(x + width/2, delay_guarantees[1], width, yerr=delay_ci[1], label='Proposed Dynamic CAPC')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[1].set_xlabel('User Terminals Per gNB')
ax[1].set_ylabel('Average Delay (ms)')
ax[1].set_title('Average Delay (ms) vs User Terminals')
ax[1].set_xticks(x)
ax[1].set_xticklabels(user_terminals)
ax[1].legend()
ax[1].grid(True)

# Show the plots
plt.tight_layout()
plt.show()