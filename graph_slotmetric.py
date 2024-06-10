import matplotlib.pyplot as plt
import csv
from collections import defaultdict

# Initialize a dictionary to store counts of TTIs per priority class for each gNB
gnb_data = defaultdict(lambda: defaultdict(int))

# Read and parse the log file
with open('output_backoffdelay.log', 'r') as file:
    for line in file:
        if line.startswith("SlotAllocation"):
            # Parse the CSV line
            parts = line.strip().split(',')
            if len(parts) == 4:
                metric_type, gnb_id, tti_index, priority_class = parts
                # Convert values to appropriate types
                tti_index = int(tti_index)
                priority_class = int(priority_class)
                # Update the count for the gNB and priority class
                gnb_data[gnb_id][priority_class] += 1

# Prepare data for plotting
gnb_list = list(gnb_data.keys())
priority_classes = range(5)  # Priority classes from 0 to 4

# Create subplots for each gNB in a 2x3 grid
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))

# Flatten the axes array for easy iteration
axes = axes.flatten()

for ax, gnb_id in zip(axes, gnb_list):
    # Get the total number of TTIs for the current gNB
    total_ttis = sum(gnb_data[gnb_id].values())
    # Calculate the proportions of TTIs for each priority class
    proportions = [gnb_data[gnb_id][pc] / total_ttis for pc in priority_classes]
    
    # Plot the proportions as a pie chart
    ax.pie(proportions, labels=[f'Priority {pc}' for pc in priority_classes], autopct='%1.1f%%')
    ax.set_title(f'Proportion of TTIs Allocated to Each Priority Class for gNB {gnb_id}')

# Remove any empty subplots if gNBs are less than 6
for i in range(len(gnb_list), len(axes)):
    fig.delaxes(axes[i])

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()
