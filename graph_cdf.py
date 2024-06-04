import numpy as np
import matplotlib.pyplot as plt

# Parse the log data and extract access delay values for NR-U and Wi-Fi transmissions
def parse_log_data(log_file):
    nr_u_transmissions = []
    wifi_transmissions = []

    with open(log_file, 'r') as file:
        for line in file:
            if line.startswith("Access Delay"):
                parts = line.strip().split(',')
                time = float(parts[2].rstrip('ns')) / 1e9  # Convert ns to seconds
                access_delay = float(parts[3].rstrip('ns')) / 1e9  # Convert ns to seconds
                
                if 0 <= time < 10 or 20 <= time < 30:
                    nr_u_transmissions.append(access_delay)
                elif 10 <= time < 20:
                    wifi_transmissions.append(access_delay)

    return nr_u_transmissions, wifi_transmissions

# Calculate CDF
def calculate_cdf(data):
    sorted_data = np.sort(data)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    return sorted_data, cdf

# Plot CDF
def plot_cdf(sorted_data, cdf, label):
    plt.plot(sorted_data, cdf, label=label)

# Main function
def main():
    log_file = 'output'  # Update with your log file name
    nr_u_transmissions, wifi_transmissions = parse_log_data(log_file)

    # Calculate CDF for NR-U transmissions during different time intervals
    sorted_nr_u, cdf_nr_u = calculate_cdf(nr_u_transmissions)

    # Plot NR-U and Wi-Fi CDFs in the same graph
    plt.figure(figsize=(10, 6))
    plot_cdf(sorted_nr_u, cdf_nr_u, label='NR-U Transmissions (0-10 and 20-30 seconds)')
    if wifi_transmissions:
        sorted_wifi, cdf_wifi = calculate_cdf(wifi_transmissions)
        plot_cdf(sorted_wifi, cdf_wifi, label='Wi-Fi Transmissions (10-20 seconds)')
    plt.xlabel('Access Delay (seconds)')
    plt.ylabel('CDF')
    plt.title('Access Delay CDF for NR-U and Wi-Fi Transmissions')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
