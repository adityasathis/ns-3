# import subprocess
# import itertools

# numBs = [(6, 0), (3, 3)]
# numUtsPerBs = [4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50]
# trafficRatios = ["1:1:1:1", "2:1:1:1", "1:2:1:1", "1:1:2:1", "1:1:1:2"]
# numerology = [0, 1, 2]
# bandwidth = [20e6, 40e6, 80e6]
# enableCapcScheduler = [0, 1]
# simTime = 10
# runs = 5

# # Experiment 1: Homogeneous NR-U
# # Variations (1.1): Changing UtsPerBs
# # Variations (1.2): Changing Traffic Ratios
# # Variations (1.3): Bandwidth
# # Variations (1.4): Numerology
# variation = "uts"
# ratio = "1:1:1:1"
# num = 1
# bw = 20e6
# simTime = 10
# for uts in numUtsPerBs:
#   for numGnbs, numAps in numBs:
#     for capc in enableCapcScheduler:
#       for run in range(runs):
#         command = [
#           "./ns3", "run",
#           f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#           f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#           f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
#         ]
        
#         log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
        
#         print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#               f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
#               f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}")
        
#         with open(log_file, "w") as f:
#           subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

# variation = "ratios"
# numGnbs = 6
# numAps  = 0
# uts = 10
# num = 0
# bw = 20e6
# simTime = 10
# for ratio in trafficRatios:
#   for capc in enableCapcScheduler:
#     for run in range(runs):
#       command = [
#         "./ns3", "run",
#         f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#         f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
#       ]
      
#       log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
      
#       print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#             f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
#             f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}")
      
#       with open(log_file, "w") as f:
#         subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

# variation = "bandwidth"
# numGnbs = 6
# numAps  = 0
# uts = 10
# num = 0
# ratio = "1:1:1:1"
# simTime = 10
# for bw in bandwidth:
#   for capc in enableCapcScheduler:
#     for run in range(runs):
#       command = [
#         "./ns3", "run",
#         f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#         f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
#       ]
      
#       log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
      
#       print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#             f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
#             f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}")
      
#       with open(log_file, "w") as f:
#         subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

# variation = "numerology"
# numGnbs = 6
# numAps  = 0
# uts = 10
# num = 0
# ratio = "1:1:1:1"
# simTime = 10
# for bw in bandwidth:
#   for capc in enableCapcScheduler:
#     for run in range(runs):
#       command = [
#         "./ns3", "run",
#         f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#         f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
#       ]
      
#       log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
      
#       print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#             f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
#             f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}")
      
#       with open(log_file, "w") as f:
#         subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

# # for bs in numBs:
# #     for uts in numUtsPerBs:
# #         for ratio in trafficRatios:
# #             for num in numerology:
# #                 for bw in bandwidth:
# #                     for capc in enableCapcScheduler:
# #                       numGnbs, numAps = bs
# #                       # Construct the command
# #                       command = [
# #                         "./ns3", "run",
# #                         f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
# #                         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
# #                         f"--enableCapcScheduler={capc} --simTime={simTime}"
# #                       ]
                      
# #                       log_file = f"nru-logs/gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}.log"
                      
# #                       print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
# #                             f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
# #                             f"--enableCapcScheduler={capc} --simTime={simTime}")
                      
# #                       with open(log_file, "w") as f:
# #                         subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

import subprocess
import itertools
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

def run_experiment(command, log_file):
    with open(log_file, "w") as f:
        subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
    return log_file

numBs = [(6, 0), (3, 3)]
numUtsPerBs = [4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50]
trafficRatios = ["1:1:1:1", "2:1:1:1", "1:2:1:1", "1:1:2:1", "1:1:1:2"]
numerology = [0, 1, 2]
bandwidth = [20e6, 40e6, 80e6]
enableCapcScheduler = [0, 1]
simTime = 10
runs = 5

def generate_commands():
    commands = []

    # Experiment 1: Homogeneous NR-U
    # Variations (1.1): Changing UtsPerBs
    variation = "uts"
    ratio = "1:1:1:1"
    num = 1
    bw = 20e6
    for uts in numUtsPerBs:
        for numGnbs, numAps in numBs:
            for capc in enableCapcScheduler:
                for run in range(runs):
                    command = [
                        "./ns3", "run",
                        f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
                        f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
                        f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
                    ]
                    
                    log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
                    commands.append((command, log_file))

    # Variations (1.2): Changing Traffic Ratios
    variation = "ratios"
    numGnbs = 6
    numAps = 0
    uts = 10
    num = 0
    bw = 20e6
    for ratio in trafficRatios:
        for capc in enableCapcScheduler:
            for run in range(runs):
                command = [
                    "./ns3", "run",
                    f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
                    f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
                    f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
                ]
                
                log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
                commands.append((command, log_file))

    # Variations (1.3): Bandwidth
    variation = "bandwidth"
    numGnbs = 6
    numAps = 0
    uts = 10
    num = 0
    ratio = "1:1:1:1"
    for bw in bandwidth:
        for capc in enableCapcScheduler:
            for run in range(runs):
                command = [
                    "./ns3", "run",
                    f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
                    f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
                    f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
                ]
                
                log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
                commands.append((command, log_file))

    # Variations (1.4): Numerology
    variation = "numerology"
    numGnbs = 6
    numAps = 0
    uts = 10
    ratio = "1:1:1:1"
    for num in numerology:
        for bw in bandwidth:
            for capc in enableCapcScheduler:
                for run in range(runs):
                    command = [
                        "./ns3", "run",
                        f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
                        f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
                        f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
                    ]
                    
                    log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
                    commands.append((command, log_file))

    return commands

num_cores = os.cpu_count()
max_workers = num_cores  # Set max_workers to the number of CPU cores

commands = generate_commands()  # Assuming this function is defined as in previous examples

# Run commands in parallel
with ProcessPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(run_experiment, cmd, log) for cmd, log in commands]
    for future in as_completed(futures):
        log_file = future.result()
        print(f"Completed: {log_file}")