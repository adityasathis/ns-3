import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from scipy import stats

# Function to calculate QoS metrics from multiple files and calculate confidence intervals
def calculate_qos_metrics(file_paths):
    qos_delays = []
    qos_throughputs = []

    for file_path in file_paths:
        achieved_delays = 0
        achieved_throughputs = 0

        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            
            for row in csv_reader:
                if row[0] == 'OUTPUT':
                    delay_indicator = int(row[-1])
                    throughput_indicator = int(row[-2])
                    
                    if delay_indicator in [0, 1]:
                        qos_delays.append(delay_indicator)
                    if throughput_indicator in [0, 1]:
                        qos_throughputs.append(throughput_indicator)
                    if delay_indicator == 1:
                        achieved_delays += 1
                    if throughput_indicator == 1:
                        achieved_throughputs += 1

        QoSGuaranteesThroughput = achieved_throughputs / len(qos_throughputs) * 100 if len(qos_throughputs) > 0 else 0
        QoSGuaranteesDelays = achieved_delays / len(qos_delays) * 100 if len(qos_delays) > 0 else 0

    return QoSGuaranteesThroughput, QoSGuaranteesDelays, stats.sem(qos_throughputs) * stats.t.ppf((1 + 0.95) / 2, len(qos_throughputs) - 1), stats.sem(qos_delays) * stats.t.ppf((1 + 0.95) / 2, len(qos_delays) - 1)

# List of user terminals to consider
user_terminals = [4, 5, 6, 7, 8, 9, 10]
capc_configs = [0, 1]
num_runs = 5

# Initialize lists to store results
throughput_guarantees = {capc: [] for capc in capc_configs}
delay_guarantees = {capc: [] for capc in capc_configs}
throughput_ci = {capc: [] for capc in capc_configs}
delay_ci = {capc: [] for capc in capc_configs}

# Iterate over each user terminal and calculate QoS metrics for multiple runs
for ut in user_terminals:
    for capc in capc_configs:
        file_paths = [f'nru-csv/changeuts-gnb6-ap0-ut{ut}-ratio1111-numerology0-bandwidth20-capc{capc}-simtime1-run{i}.csv' for i in range(num_runs)]
        throughputs = []
        delays = []
        for file_path in file_paths:
            throughput, delay, throughput_error, delay_error = calculate_qos_metrics(file_path)
            throughputs.append(throughput)
            delays.append(delay)
        throughput_guarantees[capc].append(np.mean(throughputs))
        delay_guarantees[capc].append(np.mean(delays))
        throughput_ci[capc].append(throughput_error)
        delay_ci[capc].append(delay_error)

# Plotting the results
x = np.arange(len(user_terminals))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot for Throughput Guarantees vs User Terminals
ax[0].bar(x - width/2, throughput_guarantees[0], width, yerr=throughput_ci[0], label='Static CAPC')
ax[0].bar(x + width/2, throughput_guarantees[1], width, yerr=throughput_ci[1], label='Proposed Dynamic CAPC')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[0].set_xlabel('User Terminals Per gNB')
ax[0].set_ylabel('Percenteage of User Reaching Throughput Guarantees %')
ax[0].set_title('Throughput Guarantees vs User Terminals')
ax[0].set_xticks(x)
ax[0].set_xticklabels(user_terminals)
ax[0].legend()
ax[0].grid(True)

# Plot for Delay Guarantees vs User Terminals
ax[1].bar(x - width/2, delay_guarantees[0], width, yerr=delay_ci[0], label='Static CAPC')
ax[1].bar(x + width/2, delay_guarantees[1], width, yerr=delay_ci[1], label='Proposed Dynamic CAPC')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[1].set_xlabel('User Terminals Per gNB')
ax[1].set_ylabel('Delay Guarantees')
ax[1].set_title('Delay Guarantees vs User Terminals')
ax[1].set_xticks(x)
ax[1].set_xticklabels(user_terminals)
ax[1].legend()
ax[1].grid(True)

# Show the plots
plt.tight_layout()
plt.show()