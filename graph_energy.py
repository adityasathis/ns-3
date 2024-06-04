import matplotlib.pyplot as plt
import pandas as pd

# Define the path to the 'output' file
file_path = 'output_energy'

def parse_output(file_path):
    """
    Parse the output file to extract timestamps and dBM values.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('EnergyDetect'):
                parts = line.split(',')
                timestamp_ns = float(parts[1].strip('+').strip('ns'))
                dbm = float(parts[2])
                data.append((timestamp_ns, dbm))
    return pd.DataFrame(data, columns=['timestamp_ns', 'dbm'])

# Parse the output file
data = parse_output(file_path)

# Convert timestamps from nanoseconds to seconds
data['timestamp_s'] = data['timestamp_ns'] / 1e9

# Plot the dBM power over time
plt.figure(figsize=(10, 6))
plt.plot(data['timestamp_s'], data['dbm'], marker='o', linestyle='-', color='b', label='dBM Power')
plt.xlabel('Time (s)')
plt.ylabel('dBM Power')
plt.title('dBM Power Over Time')
plt.legend()
plt.grid(True)
plt.show()