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
                if (float(row[2]) != 0.0):
                    guaranteed_throughputs.append(float(row[2])/1e6)
                    achieved_throughputs.append(float(row[4]))
                
                if (float(row[3]) != 0.0):
                    guaranteed_delays.append(float(row[3]))
                    achieved_delay_value = float(row[5]) if float(row[5]) != 0.0 else 1e-9
                    achieved_delays.append(achieved_delay_value)

    QoSGuaranteesThroughput = np.where(np.array(achieved_throughputs) / np.array(guaranteed_throughputs) < 1, 0, 1)
    QoSGuaranteesDelays = np.where(np.array(guaranteed_delays) / np.array(achieved_delays) < 1, 0, 1)

    return QoSGuaranteesThroughput*100, QoSGuaranteesDelays*100

# List of user terminals to consider
user_terminals = [4, 8, 12]
capc_configs = [0, 1, 2]
num_runs = 1
trafficModel = 0

# Initialize lists to store results
throughput_guarantees = {capc: [] for capc in capc_configs}
delay_guarantees = {capc: [] for capc in capc_configs}
throughput_ci = {capc: [] for capc in capc_configs}
delay_ci = {capc: [] for capc in capc_configs}

# Iterate over each user terminal and calculate QoS metrics for multiple runs
for ut in user_terminals:
    for mode in capc_configs:
        if mode == 0:
            capc = 0
            scheduler = "PF"
            lcScheduler = 0
        elif mode == 1:
            capc = 0
            scheduler = "Qos"
            lcScheduler = 1
        else:
            capc = 1
            scheduler = "Qos"
            lcScheduler = 1

        file_paths = [f'nru-csv/ip/changeuts-gnb6-ap0-ut{ut}-ratio1111-numerology1-bandwidth40-scheduler{scheduler}-lcScheduler{lcScheduler}-trafficModel{trafficModel}-capc{capc}-simtime5-run{i}.csv' for i in range(num_runs)]
        throughputs = []
        delays = []
        print(file_paths)
        print("-----")
        for file_path in file_paths:
            throughput, delay = calculate_qos_metrics(file_path)
            throughputs.extend(throughput)
            delays.extend(delay)
        throughput_guarantees[mode].append(np.mean(throughputs))
        delay_guarantees[mode].append(np.mean(delays))
        throughput_ci[mode].append(stats.sem(throughputs) * stats.t.ppf((1 + 0.95) / 2, len(throughputs) - 1))
        delay_ci[mode].append(stats.sem(delays) * stats.t.ppf((1 + 0.95) / 2, len(delays) - 1))
        # Let us check if this ppf command is correct.

# Plotting the results
x = np.arange(len(user_terminals))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot for Throughput Guarantees vs User Terminals
print(len(throughput_guarantees[0]), len(throughput_ci[0]))
ax[0].bar(x - width, throughput_guarantees[0], width, yerr=throughput_ci[0], label='Static CAPC with RR Scheduler')
ax[0].bar(x, throughput_guarantees[1], width, yerr=throughput_ci[1], label='Static CAPC with QoS Scheduler')
ax[0].bar(x + width, throughput_guarantees[2], width, yerr=throughput_ci[2], label='Decoupled CAPC with QoS Scheduler')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[0].set_xlabel('User Terminals Per gNB')
ax[0].set_ylabel('Percenteage of User Reaching Throughput Guarantees %')
ax[0].set_title('Throughput Guarantees vs User Terminals')
ax[0].set_xticks(x)
ax[0].set_xticklabels(user_terminals)
ax[0].legend()
ax[0].grid(True)

# Plot for Delay Guarantees vs User Terminals
ax[1].bar(x - width, delay_guarantees[0], width, yerr=delay_ci[0], label='Static CAPC with RR Scheduler')
ax[1].bar(x,         delay_guarantees[1], width, yerr=delay_ci[1], label='Static CAPC with QoS Scheduler')
ax[1].bar(x + width, delay_guarantees[2], width, yerr=delay_ci[2], label='Decoupled CAPC')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[1].set_xlabel('User Terminals Per gNB')
ax[1].set_ylabel('QoS PDB Guarantees (%)')
ax[1].set_title('QoS PDB Guarantees (%) vs User Terminals')
ax[1].set_xticks(x)
ax[1].set_xticklabels(user_terminals)
ax[1].legend()
ax[1].grid(True)

# Show the plots
plt.tight_layout()
plt.show()

# x = np.arange(len(user_terminals))  # the label locations

# fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# # Plot for Throughput Guarantees vs User Terminals
# ax[0].errorbar(x, throughput_guarantees[0], yerr=throughput_ci[0], fmt='-o', label='Static CAPC')
# ax[0].errorbar(x, throughput_guarantees[1], yerr=throughput_ci[1], fmt='-o', label='Proposed Dynamic CAPC')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax[0].set_xlabel('User Terminals Per gNB')
# ax[0].set_ylabel('Percentage of Users Reaching Throughput Guarantees %')
# ax[0].set_title('Throughput Guarantees vs User Terminals')
# ax[0].set_xticks(x)
# ax[0].set_xticklabels(user_terminals)
# ax[0].legend()
# ax[0].grid(True)

# # Plot for Delay Guarantees vs User Terminals
# ax[1].errorbar(x, delay_guarantees[0], yerr=delay_ci[0], fmt='-o', label='Static CAPC')
# ax[1].errorbar(x, delay_guarantees[1], yerr=delay_ci[1], fmt='-o', label='Proposed Dynamic CAPC')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax[1].set_xlabel('User Terminals Per gNB')
# ax[1].set_ylabel('Delay Guarantees')
# ax[1].set_title('Delay Guarantees vs User Terminals')
# ax[1].set_xticks(x)
# ax[1].set_xticklabels(user_terminals)
# ax[1].legend()
# ax[1].grid(True)

# # Show the plots
# plt.tight_layout()
# plt.show()
