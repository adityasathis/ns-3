import os
import glob

# Define input and output directories
input_dir = 'nru-logs/'
output_dir = 'nru-csv/'
output_dir_ip = 'nru-csv/ip/'
output_dir_slotdelay = 'nru-csv/slotdelay/'
output_dir_lbtcycle = 'nru-csv/lbtcycle/'
output_dir_backoffdelay = 'nru-csv/backoffdelay'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_dir_ip, exist_ok=True)
os.makedirs(output_dir_slotdelay, exist_ok=True)
os.makedirs(output_dir_lbtcycle, exist_ok=True)
os.makedirs(output_dir_backoffdelay, exist_ok=True)

log_files = glob.glob(os.path.join(input_dir, '*.log'))

# Getting all the final throughput and delay logs
for log_file in log_files:
    with open(log_file, 'r') as file:
        lines = file.readlines()
    
    output_lines = []
    for line in lines:
        if line.startswith('OUTPUT'):
            columns = line.strip().split(',')
            if (columns[1] == "nru"):
                output_lines.append(line)
    
    # Define the output file name
    output_file = os.path.join(output_dir_ip, os.path.basename(log_file).replace('.log', '.csv'))
    
    with open(output_file, 'w') as file:
        file.writelines(output_lines)
    
    print(f"Filtered lines from {log_file} have been saved to {output_file}")
    
# Getting all the slot delay logs
for log_file in log_files:
    with open(log_file, 'r') as file:
        lines = file.readlines()
    
    output_lines = []
    for line in lines:
        if line.startswith('SlotAllocation'):
            output_lines.append(line)
    
    # Define the output file name
    output_file = os.path.join(output_dir_slotdelay, os.path.basename(log_file).replace('.log', '.csv'))
    
    with open(output_file, 'w') as file:
        file.writelines(output_lines)
    
    print(f"Filtered lines from {log_file} have been saved to {output_file}")

# Getting all the access delay logs
for log_file in log_files:
    with open(log_file, 'r') as file:
        lines = file.readlines()
    
    output_lines = []
    for line in lines:
        if line.startswith('AverageBackoffDelay'):
            output_lines.append(line)
    
    # Define the output file name
    output_file = os.path.join(output_dir_backoffdelay, os.path.basename(log_file).replace('.log', '.csv'))
    
    with open(output_file, 'w') as file:
        file.writelines(output_lines)
    
    print(f"Filtered lines from {log_file} have been saved to {output_file}")
    
# Getting all the LBT cycle logs
for log_file in log_files:
    with open(log_file, 'r') as file:
        lines = file.readlines()
    
    output_lines = []
    for line in lines:
        if line.startswith('LbtCycle'):
            output_lines.append(line)
    
    # Define the output file name
    output_file = os.path.join(output_dir_lbtcycle, os.path.basename(log_file).replace('.log', '.csv'))
    
    with open(output_file, 'w') as file:
        file.writelines(output_lines)
    
    print(f"Filtered lines from {log_file} have been saved to {output_file}")