import subprocess
import itertools

numBs = [(6, 0), (3, 3)]
numUtsPerBs = [4, 5, 6, 7, 8, 9, 10, 15, 20]
trafficRatios = ["1:1:1:1", "2:1:1:1", "1:2:1:1", "1:1:2:1", "1:1:1:2"]
numerology = [0, 1, 2]
bandwidth = [20e6, 40e6, 80e6]
enableCapcScheduler = [0, 1]
simTime = 1
runs = 5

# Experiment 1: Homogeneous NR-U
# Variations (1.1): Changing UtsPerBs
# Variations (1.2): Changing Traffic Ratios
# Variations (1.3): Bandwidth
# Variations (1.4): Numerology
variation = "uts"
ratio = "1:1:1:1"
num = 1
bw = 40e6
simTime = 1
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
        
        print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
              f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
              f"--enableCapcScheduler={capc} --simTime={simTime} --runId={run}")
        
        with open(log_file, "w") as f:
          subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

# variation = "ratios"
# numGnbs = 6
# numAps  = 0
# uts = 10
# num = 0
# bw = 20e6
# simTime = 1
# for ratio in trafficRatios:
#   for capc in enableCapcScheduler:
#     command = [
#       "./ns3", "run",
#       f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#       f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#       f"--enableCapcScheduler={capc} --simTime={simTime}"
#     ]
    
#     log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}.log"
    
#     print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#           f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
#           f"--enableCapcScheduler={capc} --simTime={simTime}")
    
#     with open(log_file, "w") as f:
#       subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

# variation = "bandwidth"
# numGnbs = 6
# numAps  = 0
# uts = 10
# num = 0
# ratio = "1:1:2:1"
# simTime = 1
# for bw in bandwidth:
#   for capc in enableCapcScheduler:
#     command = [
#       "./ns3", "run",
#       f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#       f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#       f"--enableCapcScheduler={capc} --simTime={simTime}"
#     ]
    
#     log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}.log"
    
#     print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#           f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
#           f"--enableCapcScheduler={capc} --simTime={simTime}")
    
#     with open(log_file, "w") as f:
#       subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

# variation = "bandwidth"
# numGnbs = 6
# numAps  = 0
# uts = 10
# num = 0
# ratio = "1:1:2:1"
# simTime = 1
# for bw in bandwidth:
#   for capc in enableCapcScheduler:
#     command = [
#       "./ns3", "run",
#       f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#       f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#       f"--enableCapcScheduler={capc} --simTime={simTime}"
#     ]
    
#     log_file = f"nru-logs/change{variation}-gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}.log"
    
#     print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#           f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
#           f"--enableCapcScheduler={capc} --simTime={simTime}")
    
#     with open(log_file, "w") as f:
#       subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

# for bs in numBs:
#     for uts in numUtsPerBs:
#         for ratio in trafficRatios:
#             for num in numerology:
#                 for bw in bandwidth:
#                     for capc in enableCapcScheduler:
#                       numGnbs, numAps = bs
#                       # Construct the command
#                       command = [
#                         "./ns3", "run",
#                         f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#                         f"--trafficRatio={ratio} --numerology={num} --bandwidth={bw} "
#                         f"--enableCapcScheduler={capc} --simTime={simTime}"
#                       ]
                      
#                       log_file = f"nru-logs/gnb{numGnbs}-ap{numAps}-ut{uts}-ratio{ratio.replace(':', '')}-numerology{num}-bandwidth{int(bw/1e6)}-capc{capc}-simtime{simTime}.log"
                      
#                       print(f"nru_wifi_qos --numGnbs={numGnbs} --numAps={numAps} --numUtsPerBs={uts} "
#                             f"--trafficRatios={ratio} --numerology={num} --bandwidth={bw} "
#                             f"--enableCapcScheduler={capc} --simTime={simTime}")
                      
#                       with open(log_file, "w") as f:
#                         subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)
