import math
import subprocess
import itertools
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

envVars = os.environ.copy()
# envVars["NS_LOG"] = "NrGnbPhy:NrMacSchedulerNs3"

def run_experiment(command, log_file):
    with open(log_file, "w") as f:
        subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, env=envVars)
    return log_file

numBs = [(6, 0), (3, 3)]
numUtsPerBs = [4, 8, 12]
#numUtsPerBs = [16]
trafficRatios = ["1:1:1:1", "2:1:1:1", "1:2:1:1", "1:1:2:1", "1:1:1:2"]
numerology = [0, 1, 2]
bandwidth = [20e6, 40e6, 80e6]
enableCapcScheduler = [0, 1, 2]
simTime = 10
runs = 10

def generate_commands():
    commands = {run: [] for run in range(runs)}

    # Experiment 1: Homogeneous NR-U
    # Variations (1.1): Changing UtsPerBs
    variation = "uts"
    ratio = "1:1:1:1"
    num = 2
    bw = 80e6
    trafficModel = 0
    numBs = [(6,0)]
    enableOfdma = 1

    for run in range(runs):
        for numGnbs, numAps in numBs:
            for uts in numUtsPerBs:
                for mode in enableCapcScheduler:
                    if mode == 0:
                        capc = 0
                        scheduler = "PF"
                        lcScheduler = 0
                    elif mode == 1:
                        capc = 0
                        scheduler = "Qos"
                        lcScheduler = 0
                    else:
                        capc = 1
                        scheduler = "Qos"
                        lcScheduler = 0

                    command = [
                        "./ns3", "run", 
                        f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
                        f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
                        f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run} --scheduler={scheduler} --lcScheduler={lcScheduler} --trafficModel={trafficModel} --enableOfdma={enableOfdma}"
                    ]
                    
                    log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-scheduler{scheduler}-lcScheduler{lcScheduler}-trafficModel{trafficModel}-capc{capc}-simtime{simTime}-run{run}.log"
                    commands[run].append((command, log_file))
    return commands

num_cores = math.floor(os.cpu_count() / (0.5))
max_workers = num_cores  # Set max_workers to the number of CPU cores

commands_by_run = generate_commands()  # Group commands by run

for run in range(runs):
    commands = commands_by_run[run]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_experiment, cmd, log) for cmd, log in commands]
        num_commands = len(commands)
        completed_count = 0
                    
        for future in as_completed(futures):
            log_file = future.result()
            completed_count += 1
            print(f"Completed [{completed_count}/{num_commands}] for run {run}: {log_file}")

# Run commands in parallel
#with ProcessPoolExecutor(max_workers=max_workers) as executor:
#    futures = [executor.submit(run_experiment, cmd, log) for cmd, log in commands]
#    num_commands = len(commands)
#    for future in as_completed(futures):
#        log_file = future.result()
#        print(f"Completed: {log_file}")


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
#           f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#           f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#           f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
#         ]
        
#         log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
        
#         print(f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
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
#         f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#         f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
#       ]
      
#       log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
      
#       print(f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
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
#         f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#         f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
#       ]
      
#       log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
      
#       print(f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
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
#         f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#         f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}"
#       ]
      
#       log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}-run{run}.log"
      
#       print(f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
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
# #                         f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
# #                         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
# #                         f"--enableCapcScheduler={capc} --simTime={simTime}"
# #                       ]
                      
# #                       log_file = f"nru-logs/gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}.log"
                      
# #                       print(f"nru-wifi-qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
# #                             f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
# #                             f"--enableCapcScheduler={capc} --simTime={simTime}")
                      
# #                       with open(log_file, "w") as f:
# #                         subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
