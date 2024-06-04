import matplotlib.pyplot as plt

# Function to parse the log file and extract active and busy periods
def parse_log_file(file_path):
    active_periods = []
    busy_periods = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("ActiveGraph"):
                _, start, duration = line.split(',')
                start_time = float(start.strip().strip('+ns')) / 1e9  # Convert to seconds
                duration_time = float(duration.strip().strip('ns')) / 1e9  # Convert to seconds
                active_periods.append((start_time, duration_time))
            elif line.startswith("BusyGraph"):
                _, start, duration = line.split(',')
                start_time = float(start.strip().strip('+ns')) / 1e9  # Convert to seconds
                duration_time = float(duration.strip().strip('ns')) / 1e9  # Convert to seconds
                busy_periods.append((start_time, duration_time))

    return active_periods, busy_periods

# File path to the output log file
file_path = 'output'

# Parse the log file
active_periods, busy_periods = parse_log_file(file_path)

# Plotting the data
fig, ax = plt.subplots()

# Plot active periods
for start, duration in active_periods:
    ax.broken_barh([(start, duration)], (10, 20), facecolors='green', linewidth=5)

# Plot busy periods
for start, duration in busy_periods:
    ax.broken_barh([(start, duration)], (10, 20), facecolors='red', linewidth=5)

# Formatting the plot
ax.set_ylim(5, 35)
ax.set_xlim(0, 10)
ax.set_xlabel('Time (seconds)', fontsize=16)  # Set font size for x-axis label
ax.set_ylabel('Status', fontsize=16)  # Set font size for y-axis label
ax.set_yticks([15, 25])
ax.set_yticklabels(['Active', 'Busy'], fontsize=14)  # Set font size for y-axis tick labels
ax.grid(True)

# Set font size for title
ax.set_title('Active and Busy Periods in LAA and Wi-Fi Coexistence Experiment', fontsize=18)

# Set font size for all other text (e.g., legend)
plt.rcParams.update({'font.size': 14})

plt.show()