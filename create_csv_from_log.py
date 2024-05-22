import os
import glob

# Define input and output directories
input_dir = 'nru-logs/'
output_dir = 'nru-csv/'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get all .log files from the input directory
log_files = glob.glob(os.path.join(input_dir, '*.log'))

for log_file in log_files:
    with open(log_file, 'r') as file:
        lines = file.readlines()
    
    output_lines = []
    for line in lines:
        if line.startswith('OUTPUT'):
            columns = line.strip().split(',')
            if columns[-1] != '3':
                output_lines.append(line)
    
    # Define the output file name
    output_file = os.path.join(output_dir, os.path.basename(log_file).replace('.log', '.csv'))
    
    with open(output_file, 'w') as file:
        file.writelines(output_lines)
    
    print(f"Filtered lines from {log_file} have been saved to {output_file}")