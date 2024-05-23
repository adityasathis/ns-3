import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import glob
matplotlib.use('TkAgg')  # or another interactive backend

# Function to calculate QoS metrics from a given file
def calculate_qos_metrics(file_path, type):
    qos_delays = 0
    qos_throughputs = 0
    achieved_delays = 0
    achieved_throughputs = 0

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            if row[0] == 'OUTPUT':
                if row[1] == type:
                    delay_indicator = int(row[-1])
                    throughput_indicator = int(row[-2])
                    
                    if delay_indicator in [0, 1]:
                        qos_delays += 1
                    if throughput_indicator in [0, 1]:
                        qos_throughputs += 1
                    if delay_indicator == 1:
                        achieved_delays += 1
                    if throughput_indicator == 1:
                        achieved_throughputs += 1

    QoSGuaranteesThroughput = achieved_throughputs / qos_throughputs * 100 if qos_throughputs > 0 else 0
    QoSGuaranteesDelays = achieved_delays / qos_delays * 100 if qos_delays > 0 else 0

    return QoSGuaranteesThroughput, QoSGuaranteesDelays

def calculate_sum_throughput(file_path, type):
    count = 0
    average_throughput = 0
    average_delay = 0

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        
        for row in csv_reader:
            if row[0] == 'OUTPUT':
                if row[1] == type:
                    count = count + 1

                    average_throughput = average_throughput + float(row[2])
                    average_delay = average_delay + float(row[3])

    average_throughput = average_throughput / count
    average_delay = average_delay / count

    return average_throughput, average_delay


# # Define input and output directories
# input_dir = 'nru-logs/'
# output_dir = 'nru-csv/'

# # Ensure the output directory exists
# os.makedirs(output_dir, exist_ok=True)

# # Get all .log files from the input directory
# log_files = glob.glob(os.path.join(input_dir, '*.log'))

# for log_file in log_files:
#     with open(log_file, 'r') as file:
#         lines = file.readlines()
    
#     output_lines = []
#     for line in lines:
#         if line.startswith('OUTPUT'):
#             columns = line.strip().split(',')
#             if columns[-1] != '3':
#                 output_lines.append(line)
    
#     # Define the output file name
#     output_file = os.path.join(output_dir, os.path.basename(log_file).replace('.log', '.csv'))
    
#     with open(output_file, 'w') as file:
#         file.writelines(output_lines)
    
#     print(f"Filtered lines from {log_file} have been saved to {output_file}")

# List of user terminals to consider
user_terminals = [4, 5, 6, 7]
capc_configs = [0, 1]

# Initialize lists to store results
# throughput_guarantees_nru = {capc: [] for capc in capc_configs}
# delay_guarantees_nru = {capc: [] for capc in capc_configs}
# throughput_guarantees_wifi = {capc: [] for capc in capc_configs}
# delay_guarantees_wifi = {capc: [] for capc in capc_configs}
average_throughput_nru = {capc: [] for capc in capc_configs}
average_throughput_wifi = {capc: [] for capc in capc_configs}
average_delay_nru = {capc: [] for capc in capc_configs}
average_delay_wifi = {capc: [] for capc in capc_configs}

# Iterate over each user terminal and calculate QoS metrics
variation = "uts"
for ut in user_terminals:
  for capc in capc_configs:
    file_path = f'nru-csv/change{variation}-gnb3-ap3-ut{ut}-ratio1111-numerology1-bandwidth40-capc{capc}-simtime1.csv'
    throughput, delay = calculate_sum_throughput(file_path, "wifi")
    average_throughput_wifi[capc].append(throughput)
    average_delay_wifi[capc].append(delay)
    throughput, delay = calculate_sum_throughput(file_path, "nru")
    average_throughput_nru[capc].append(throughput)
    average_delay_nru[capc].append(delay)

# Plotting the results
x = np.arange(len(user_terminals))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot for Throughput Guarantees vs User Terminals
rects1 = ax[0].bar(x - 1.5 * width, average_throughput_wifi[0], width, label='Static CAPC - Wi-Fi', color='blue')
rects2 = ax[0].bar(x - 0.5 * width, average_throughput_nru[0], width, label='Static CAPC - NR-U', color='green')
rects3 = ax[0].bar(x + 0.5 * width, average_throughput_wifi[1], width, label='Proposed Dynamic CAPC - Wi-Fi', color='red')
rects4 = ax[0].bar(x + 1.5 * width, average_throughput_nru[1], width, label='Proposed Dynamic CAPC - NR-U', color='yellow')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax[0].set_xlabel('User Terminals Per gNB')
ax[0].set_ylabel('Average Throughput (Mbps)')
ax[0].set_title('Average Throughput (Mbps) vs User Terminals')
ax[0].set_xticks(x)
ax[0].set_xticklabels(user_terminals)
ax[0].legend()
ax[0].grid(True)

# Plot for Delay Guarantees vs User Terminals
rects5 = ax[1].bar(x - 1.5 * width, average_delay_wifi[0], width, label='Static CAPC - Wi-Fi', color='blue')
rects6 = ax[1].bar(x - 0.5 * width, average_delay_nru[0], width, label='Static CAPC - NR-U', color='green')
rects7 = ax[1].bar(x + 0.5 * width, average_delay_wifi[1], width, label='Dynamic CAPC - Wi-Fi', color='red')
rects8 = ax[1].bar(x + 1.5 * width, average_delay_nru[1], width, label='Dynamic CAPC - NR-U', color='yellow')

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