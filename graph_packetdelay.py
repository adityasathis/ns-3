import matplotlib.pyplot as plt
import csv
import numpy as np

def smooth_data(y, window_size=501):
    """
    Applies a moving average filter to smooth the data.
    
    Args:
        y (list or np.array): The data to be smoothed.
        window_size (int): The window size for the moving average filter.
    
    Returns:
        np.array: The smoothed data.
    """
    # Convert to a NumPy array if necessary
    y = np.array(y)
    
    # Pad the data with zeros at the beginning and end
    padded_y = np.pad(y, (window_size//2, window_size//2), mode='edge')
    
    # Apply the moving average filter
    smoothed_y = np.convolve(padded_y, np.ones(window_size)/window_size, mode='valid')
    
    return smoothed_y

def plot_hol_packet_delay(file_path, window_size=400):
    # Read the CSV file
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        filtered_rows = []
        for row in reader:
            if row:
                if row[0] == 'Access Delay':
                    if int(row[1]) == 1:
                        filtered_rows.append(row)
                # if row[0] == 'HOL Packet Delay':
                #     filtered_rows.append(row)
        # filtered_rows = [row for row in reader if row and row[0] == 'HOL Packet Delay']

    # print(filtered_rows)

    # Extract the relevant columns for plotting
    x = [float(row[-2].strip("ns")) / 1e6 for row in filtered_rows]  # Convert to milliseconds
    y = [float(row[-1].strip("ns")) for row in filtered_rows]  # Convert to milliseconds

    # Calculate the moving average over the last 'window_size' entries
    moving_avg = []
    for i in range(len(y)):
        if i < window_size:
            window_values = y[:i+1]  # Use all available values up to i
        else:
            window_values = y[i-window_size+1:i+1]  # Use only the last 'window_size' values
        moving_avg.append(sum(window_values) / len(window_values))  # Average of the window

    smoothed_moving_avg = smooth_data(moving_avg, window_size=100000)

    # Read the energy data
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        energy_rows = [row for row in reader if row and row[0] == 'EnergyDetect']

    energy_x = [float(row[-2].strip("ns")) / 1e6 for row in energy_rows]  # Convert to milliseconds
    energy_y = [1000 if float(row[-1]) > 1e-8 else 0 for row in energy_rows]  # Assume energy is in W
    # energy_y = [float(row[-1]) for row in energy_rows]

    # Set up the plot
    fig, ax1 = plt.subplots()

    # Plot the HOL Packet Delay data
    ax1.plot(x, moving_avg, marker='o', markersize=3, label='HOL Packet Delay (us)', color='tab:blue')
    ax1.set_xlabel('Observation Time (ms)')
    ax1.set_ylabel('HOL Packet Delay (us)')
    ax1.set_title('HOL Packet Delay (us) vs Time (ms)')

    # Add shaded regions for Wi-Fi OFF and ON periods
    # ax1.axvspan(0, 10000, color='yellow', alpha=0.3, label='Wi-Fi OFF')  # 0 to 10 seconds: Wi-Fi OFF
    # ax1.axvspan(10000, 20000, color='blue', alpha=0.3, label='Wi-Fi ON')  # 10 to 20 seconds: Wi-Fi ON
    # ax1.axvspan(20000, 30000, color='yellow', alpha=0.3, label='Wi-Fi OFF')  # 20 to 30 seconds: Wi-Fi OFF
    # ax1.legend(loc='upper left')

    # Create a secondary y-axis to plot the energy data
    ax2 = ax1.twinx()
    ax2.plot(energy_x, energy_y, label='Coexistence Period', color='tab:red', alpha=0.2)
    # ax2.set_ylabel('Energy (W)')
    ax2.set_yticklabels([])
    ax2.legend(loc='upper right')

    # Show the plot
    plt.show()

# Specify the path to your CSV file
file_path = 'output2.csv'
plot_hol_packet_delay(file_path, 2000)