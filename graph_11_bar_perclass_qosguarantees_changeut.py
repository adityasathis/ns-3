import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from scipy import stats

# Function to calculate QoS metrics from multiple files and calculate confidence intervals
def calculate_qos_metrics(file_path):
    guaranteedTput0 = []
    guaranteedTput1 = []
    guaranteedTput2 = []
    
    guaranteedDelay0 = []
    guaranteedDelay1 = []
    guaranteedDelay2 = []
    
    achievedDelay0 = []
    achievedDelay1 = []
    achievedDelay2 = []
    achievedDelay3 = []
    
    achievedTput0 = []
    achievedTput1 = []
    achievedTput2 = []
    achievedTput3 = []

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            if (row[0] == 'OUTPUT'):
                if ((float(row[2]) == 3e7) and (float(row[3]) == 5)):
                    achievedTput0.append(float(row[6]))
                    guaranteedTput0.append(float(row[2])/1e6)
                    
                    # Add delay only if it is not-zero
                    if (float(row[7]) != 0):
                        achievedDelay0.append(float(row[7]))
                        guaranteedDelay0.append(10)

                if ((float(row[2]) == 5e6) and (float(row[3]) == 150)):
                    achievedTput1.append(float(row[6]))
                    guaranteedTput1.append(float(row[2])/1e6)
                    
                    # Add delay only if it is not-zero
                    if (float(row[7]) != 0):
                        achievedDelay1.append(float(row[7]))
                        guaranteedDelay1.append(float(row[3]))
                        
                if ((float(row[2]) == 5e6) and (float(row[3]) == 300)):
                    achievedTput2.append(float(row[6]))
                    guaranteedTput2.append(float(row[2])/1e6)
                    
                    # Add delay only if it is not-zero
                    if (float(row[7]) != 0):
                        achievedDelay2.append(float(row[7]))
                        guaranteedDelay2.append(float(row[3]))
                        
                if ((float(row[2]) == 5e6) and (float(row[3]) == 300)):
                    achievedTput3.append(float(row[6]))
                    
                    # Add delay only if it is not-zero
                    if (float(row[7]) != 0):
                        achievedDelay3.append(float(row[7]))

    print(f"Average Delay0: {achievedDelay0}")
    print(f"QoS Delay0: {guaranteedDelay0}")
    
    print(f"Average Delay1: {achievedDelay1}")
    print(f"QoS Delay1: {guaranteedDelay1}")

    print(f"Average Delay2: {achievedDelay2}")
    print(f"QoS Delay2: {guaranteedDelay2}")

    AverageThroughput0 = np.where(np.array(achievedTput0) / np.array(guaranteedTput0) < 1, 0, 1)
    AverageDelay0 = np.where(np.array(guaranteedDelay0) / np.array(achievedDelay0) < 1, 0, 1)
    AverageThroughput1 = np.where(np.array(achievedTput1) / np.array(guaranteedTput1) < 1, 0, 1)
    AverageDelay1 = np.where(np.array(guaranteedDelay1) / np.array(achievedDelay1) < 1, 0, 1)
    AverageThroughput2 = np.where(np.array(achievedTput2) / np.array(guaranteedTput2) < 1, 0, 1)
    AverageDelay2 = np.where(np.array(guaranteedDelay2) / np.array(achievedDelay2) < 1, 0, 1)
    # AverageThroughput3 = np.array(achievedTput3)
    # AverageDelay3 = np.array(achievedDelay3)

    return AverageThroughput0, AverageThroughput1, AverageThroughput2, AverageDelay0, AverageDelay1, AverageDelay2

# List of user terminals to consider
user_terminals = [4, 8, 12]
xlabels = ['24', '48', '72']
capc_configs = [0, 1, 2]
num_runs = 1
trafficModel = 0
num = 2
bw = 40
simTime = 50

# Initialize lists to store results
throughput_guarantees0 = {capc: [] for capc in capc_configs}
throughput_guarantees1 = {capc: [] for capc in capc_configs}
throughput_guarantees2 = {capc: [] for capc in capc_configs}
throughput_guarantees3 = {capc: [] for capc in capc_configs}
delay_guarantees0 = {capc: [] for capc in capc_configs}
delay_guarantees1 = {capc: [] for capc in capc_configs}
delay_guarantees2 = {capc: [] for capc in capc_configs}
delay_guarantees3 = {capc: [] for capc in capc_configs}
throughput_ci0 = {capc: [] for capc in capc_configs}
throughput_ci1 = {capc: [] for capc in capc_configs}
throughput_ci2 = {capc: [] for capc in capc_configs}
throughput_ci3 = {capc: [] for capc in capc_configs}
delay_ci0 = {capc: [] for capc in capc_configs}
delay_ci1 = {capc: [] for capc in capc_configs}
delay_ci2 = {capc: [] for capc in capc_configs}
delay_ci3 = {capc: [] for capc in capc_configs}

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

        file_paths = [f'nru-csv/ip/changeuts-gnb6-ap0-ut{ut}-ratio1111-numerology{num}-bandwidth{bw}-scheduler{scheduler}-lcScheduler{lcScheduler}-trafficModel{trafficModel}-capc{capc}-simtime{simTime}-run{i}.csv' for i in range(num_runs)]
        throughputs0 = []
        throughputs1 = []
        throughputs2 = []
        throughputs3 = []
        delays0 = []
        delays1 = []
        delays2 = []
        delays3 = []
        print(file_paths)
        print("-----")
        for file_path in file_paths:
            throughput0, throughput1, throughput2, delay0, delay1, delay2 = calculate_qos_metrics(file_path)
            throughputs0.extend(throughput0)
            throughputs1.extend(throughput1)
            throughputs2.extend(throughput2)
            # throughputs3.extend(throughput3)
            
            delays0.extend(delay0)
            delays1.extend(delay1)
            delays2.extend(delay2)
            # delays3.extend(delay3)
            
        throughput_guarantees0[mode].append(np.mean(throughputs0) * 100)
        throughput_guarantees1[mode].append(np.mean(throughputs1) * 100)
        throughput_guarantees2[mode].append(np.mean(throughputs2) * 100)
        # throughput_guarantees3[mode].append(np.mean(throughputs3))
        
        delay_guarantees0[mode].append(np.mean(delays0) * 100)
        delay_guarantees1[mode].append(np.mean(delays1) * 100)
        delay_guarantees2[mode].append(np.mean(delays2) * 100)
        # delay_guarantees3[mode].append(np.mean(delays3))
        
        throughput_ci0[mode].append(stats.sem(throughputs0) * stats.t.ppf((1 + 0.95) / 2, len(throughputs0) - 1))
        throughput_ci1[mode].append(stats.sem(throughputs1) * stats.t.ppf((1 + 0.95) / 2, len(throughputs1) - 1))
        throughput_ci2[mode].append(stats.sem(throughputs2) * stats.t.ppf((1 + 0.95) / 2, len(throughputs2) - 1))
        # throughput_ci3[mode].append(stats.sem(throughputs3) * stats.t.ppf((1 + 0.95) / 2, len(throughputs3) - 1))
        
        delay_ci0[mode].append(stats.sem(delays0) * stats.t.ppf((1 + 0.95) / 2, len(delays0) - 1))
        delay_ci1[mode].append(stats.sem(delays1) * stats.t.ppf((1 + 0.95) / 2, len(delays1) - 1))
        delay_ci2[mode].append(stats.sem(delays2) * stats.t.ppf((1 + 0.95) / 2, len(delays2) - 1))
        # delay_ci3[mode].append(stats.sem(delays3) * stats.t.ppf((1 + 0.95) / 2, len(delays3) - 1))
        # Let us check if this ppf command is correct.

# Plotting the results

x = np.arange(len(xlabels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots(3, 1, figsize=(14, 6))

# Plot for Throughput Guarantees vs User Terminals
# ax[0,0].bar(x - width, throughput_guarantees0[0], width, yerr=throughput_ci0[0], label='Static CAPC with RR Scheduler')
# ax[0,0].bar(x, throughput_guarantees0[1], width, yerr=throughput_ci0[1], label='Static CAPC with QoS Scheduler')
# ax[0,0].bar(x + width, throughput_guarantees0[2], width, yerr=throughput_ci0[2], label='Decoupled CAPC')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax[0,0].set_xlabel('User Terminals Per gNB')
# ax[0,0].set_ylabel('Throughput (Mbps)')
# ax[0,0].set_title('Throughput (Mbps) vs User Terminals')
# ax[0,0].set_xticks(x)
# ax[0,0].set_xticklabels(xlabels)
# ax[0,0].legend()
# ax[0,0].grid(True)

# Plot for Delay Guarantees vs User Terminals
ax[0].bar(x - width/2, delay_guarantees0[0], width, label='Static CAPC with RR Scheduler')
# ax[0].bar(x,         delay_guarantees0[1], width, label='Static CAPC with QoS Scheduler')
ax[0].bar(x + width/2, delay_guarantees0[2], width, label='Decoupled CAPC')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[0].set_xlabel('Total User Terminals in Scenario')
ax[0].set_ylabel('QoS Guarantees (%)')
ax[0].set_title('QoS Guarantees (%) vs User Terminals - (PDB: 5ms)')
ax[0].set_xticks(x)
ax[0].set_xticklabels(xlabels)
ax[0].legend()
ax[0].grid(True)

################################################################################

# Plot for Throughput Guarantees vs User Terminals
# ax[1,0].bar(x - width, throughput_guarantees1[0], width, yerr=throughput_ci1[0], label='Static CAPC with RR Scheduler')
# ax[1,0].bar(x, throughput_guarantees1[1], width, yerr=throughput_ci1[1], label='Static CAPC with QoS Scheduler')
# ax[1,0].bar(x + width, throughput_guarantees1[2], width, yerr=throughput_ci1[2], label='Decoupled CAPC')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax[1,0].set_xlabel('User Terminals Per gNB')
# ax[1,0].set_ylabel('Throughput (Mbps)')
# ax[1,0].set_title('Throughput (Mbps) vs User Terminals')
# ax[1,0].set_xticks(x)
# ax[1,0].set_xticklabels(xlabels)
# ax[1,0].legend()
# ax[1,0].grid(True)

# Plot for Delay Guarantees vs User Terminals
ax[1].bar(x - width/2, delay_guarantees1[0], width, label='Static CAPC with RR Scheduler')
# ax[1].bar(x,         delay_guarantees1[1], width, label='Static CAPC with QoS Scheduler')
ax[1].bar(x + width/2, delay_guarantees1[2], width, label='Decoupled CAPC')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[1].set_xlabel('Total User Terminals in Scenario')
ax[1].set_ylabel('QoS Guarantees (%)')
ax[1].set_title('QoS Guarantees (%) vs User Terminals - (PDB: 150ms)')
ax[1].set_xticks(x)
ax[1].set_xticklabels(xlabels)
ax[1].legend()
ax[1].grid(True)

################################################################################

# Plot for Throughput Guarantees vs User Terminals
# ax[2,0].bar(x - width, throughput_guarantees2[0], width, yerr=throughput_ci2[0], label='Static CAPC with RR Scheduler')
# ax[2,0].bar(x, throughput_guarantees2[1], width, yerr=throughput_ci2[1], label='Static CAPC with QoS Scheduler')
# ax[2,0].bar(x + width, throughput_guarantees2[2], width, yerr=throughput_ci2[2], label='Decoupled CAPC')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax[2,0].set_xlabel('User Terminals Per gNB')
# ax[2,0].set_ylabel('Throughput (Mbps)')
# ax[2,0].set_title('Throughput (Mbps) vs User Terminals')
# ax[2,0].set_xticks(x)
# ax[2,0].set_xticklabels(xlabels)
# ax[2,0].legend()
# ax[2,0].grid(True)

# Plot for Delay Guarantees vs User Terminals
ax[2].bar(x - width/2, delay_guarantees2[0], width, label='Static CAPC with RR Scheduler')
# ax[2].bar(x,         delay_guarantees2[1], width, label='Static CAPC with QoS Scheduler')
ax[2].bar(x + width/2, delay_guarantees2[2], width, label='Decoupled CAPC')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[2].set_xlabel('Total User Terminals in Scenario')
ax[2].set_ylabel('QoS Guarantees (%)')
ax[2].set_title('QoS Guarantees (%) vs User Terminals - (PDB: 300ms)')
ax[2].set_xticks(x)
ax[2].set_xticklabels(xlabels)
ax[2].legend()
ax[2].grid(True)

###############################################################################

# Plot for Throughput Guarantees vs User Terminals
# ax[3,0].bar(x - width, throughput_guarantees3[0], width, yerr=throughput_ci3[0], label='Static CAPC with RR Scheduler')
# ax[3,0].bar(x, throughput_guarantees3[1], width, yerr=throughput_ci3[1], label='Static CAPC with QoS Scheduler')
# ax[3,0].bar(x + width, throughput_guarantees3[2], width, yerr=throughput_ci3[2], label='Decoupled CAPC')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax[3,0].set_xlabel('User Terminals Per gNB')
# ax[3,0].set_ylabel('Throughput (Mbps)')
# ax[3,0].set_title('Throughput (Mbps) vs User Terminals')
# ax[3,0].set_xticks(x)
# ax[3,0].set_xticklabels(xlabels)
# ax[3,0].legend()
# ax[3,0].grid(True)

# # Plot for Delay Guarantees vs User Terminals
# ax[3,1].bar(x - width, delay_guarantees3[0], width, label='Static CAPC with RR Scheduler')
# ax[3,1].bar(x,         delay_guarantees3[1], width, label='Static CAPC with QoS Scheduler')
# ax[3,1].bar(x + width, delay_guarantees3[2], width, label='Decoupled CAPC')

# # Add some text for labels, title and custom x-axis tick labels, etc.
# ax[3,1].set_xlabel('User Terminals Per gNB')
# ax[3,1].set_ylabel('Average Delay (ms)')
# ax[3,1].set_title('Average Delay (ms) vs User Terminals')
# ax[3,1].set_xticks(x)
# ax[3,1].set_xticklabels(xlabels)
# ax[3,1].legend()
# ax[3,1].grid(True)

################################################################################

# Show the plots
plt.tight_layout()
plt.show()
