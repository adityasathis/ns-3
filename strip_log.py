# Open the original log file for reading
with open('output_6', 'r') as original_file:
    # Open a new log file for writing
    with open('output6.csv', 'w') as filtered_file:
        # Iterate through each line in the original log file
        for line in original_file:
            # Check if the line contains ActiveGraph or BusyGraph
            if 'ActiveGraph' in line:
                # Write the line to the filtered log file
                filtered_file.write(line)
            if 'BusyGraph' in line:
                # Write the line to the filtered log file
                filtered_file.write(line)
            if 'Access Delay' in line:
                # Write the line to the filtered log file
                filtered_file.write(line)
            if 'HOL Packet Delay' in line:
                # Write the line to the filtered log file
                filtered_file.write(line)
            if 'EnergyDetect' in line:
                # Write the line to the filtered log file
                filtered_file.write(line)