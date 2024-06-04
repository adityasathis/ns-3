import csv
import re
import matplotlib.pyplot as plt

# Initialize dictionaries to store durations for ActiveGraph and BusyGraph lines
active_max_duration = {}
busy_max_duration = {}

# Read the log file line by line
with open('output_1', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) < 3:
            continue  # Skip lines that don't have enough columns
        if row[0] == 'ActiveGraph':
            start_time, duration = map(lambda x: float(x.strip('ns')), row[1:])
            if start_time in active_max_duration:
                active_max_duration[start_time] = max(active_max_duration[start_time], duration)
            else:
                active_max_duration[start_time] = duration
        elif row[0] == 'BusyGraph':
            start_time, duration = map(lambda x: float(x.strip('ns')), row[1:])
            if start_time in busy_max_duration:
                busy_max_duration[start_time] = max(busy_max_duration[start_time], duration)
            else:
                busy_max_duration[start_time] = duration

# Sum up durations for ActiveGraph and BusyGraph lines that remain
active_sum = sum(active_max_duration.values())
busy_sum = sum(busy_max_duration.values())

# # Calculate total duration based on the last entry of ActiveGraph or BusyGraph
last_active_time = max(int(start) for start in active_max_duration.keys()) if active_max_duration else 0
last_busy_time = max(int(start) for start in busy_max_duration.keys()) if busy_max_duration else 0
total_duration = max(last_active_time, last_busy_time) + max(active_max_duration[last_active_time], busy_max_duration[last_busy_time])

# # Calculate idle duration
idle_duration = total_duration - (active_sum + busy_sum)

print(idle_duration, active_sum, busy_sum)

# # Create pie chart
labels = ['Occupying', 'Channel Busy', 'Channel Idle']
sizes = [active_sum, busy_sum, idle_duration]
colors = ['lightblue', 'lightgreen', 'lightcoral']
explode = (0.1, 0, 0)  # explode the 1st slice

plt.figure(figsize=(8, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Channel Utilization')
plt.show()



# import csv
# import re
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# # Initialize dictionaries to store durations for ActiveGraph and BusyGraph lines
# active_max_duration = {}
# busy_max_duration = {}

# # Initialize figure and axes
# fig, ax = plt.subplots()

# def animate(i):
#     # Clear previous plot
#     ax.clear()

#     # Read the log file line by line
#     with open('output_1', 'r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if len(row) < 3:
#                 continue  # Skip lines that don't have enough columns
#             if row[0] == 'ActiveGraph':
#                 start_time, duration = map(lambda x: float(x.strip('ns')), row[1:])
#                 if start_time in active_max_duration:
#                     active_max_duration[start_time] = max(active_max_duration[start_time], duration)
#                 else:
#                     active_max_duration[start_time] = duration
#             elif row[0] == 'BusyGraph':
#                 start_time, duration = map(lambda x: float(x.strip('ns')), row[1:])
#                 if start_time in busy_max_duration:
#                     busy_max_duration[start_time] = max(busy_max_duration[start_time], duration)
#                 else:
#                     busy_max_duration[start_time] = duration

#     # Sum up durations for ActiveGraph and BusyGraph lines that remain
#     active_sum = sum(active_max_duration.values())
#     busy_sum = sum(busy_max_duration.values())

#     # Calculate total duration based on the last entry of ActiveGraph or BusyGraph
#     last_active_time = max(int(start) for start in active_max_duration.keys()) if active_max_duration else 0
#     last_busy_time = max(int(start) for start in busy_max_duration.keys()) if busy_max_duration else 0
#     total_duration = max(last_active_time + active_max_duration[last_active_time], last_busy_time + busy_max_duration[last_busy_time])

#     # Calculate idle duration
#     idle_duration = total_duration - (active_sum + busy_sum)

#     # Print the current state
#     print(idle_duration, active_sum, busy_sum)

#     # Create pie chart
#     labels = ['Active', 'Busy', 'Idle']
#     sizes = [active_sum, busy_sum, idle_duration]
#     colors = ['lightblue', 'lightgreen', 'lightcoral']
#     explode = (0.1, 0, 0)  # explode the 1st slice

#     ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
#     ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     ax.set_title('Active, Busy, and Idle Durations')

# # Create animation
# ani = animation.FuncAnimation(fig, animate, interval=1000)

# plt.show()