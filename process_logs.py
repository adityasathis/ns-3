import os
import subprocess
import sys
import time

gnbChannelAccessManager = sys.argv[1]
varyDevice = sys.argv[2]

# # Functions Models
# mcot = a + b*x

# # Definitions for the CAPC Values
# Capc0Mcot = {2, 3, 4, 5, 6, 7, 8, 10}
# Capc0CWMin = {1, 3, 5, 7, 15}
# Capc0CWMax = {7, 15, 63, 1023}
# Capc0Defer = {25, 34, 43, 52, 61, 70, 79}

# Capc1Mcot = {2, 3, 4, 5, 6, 7, 8, 10}
# Capc1CWMin = {1, 3, 5, 7, 15}
# Capc1CWMax = {7, 15, 63, 1023}
# Capc1Defer = {25, 34, 43, 52, 61, 70, 79}

# Capc2Mcot = {2, 3, 4, 5, 6, 7, 8, 10}
# Capc2CWMin = {1, 3, 5, 7, 15}
# Capc2CWMax = {7, 15, 63, 1023}
# Capc2Defer = {25, 34, 43, 52, 61, 70, 79}

# Capc3Mcot = {2, 3, 4, 5, 6, 7, 8, 10}
# Capc3CWMin = {1, 3, 5, 7, 15}
# Capc3CWMax = {7, 15, 63, 1023}
# Capc3Defer = {25, 34, 43, 52, 61, 70, 79}

Capc0Configuration = "{5, 3, 7, 2ms, 25us, ACK_ANY}"
Capc1Configuration = "{5, 7, 15, 3ms, 25us, ACK_ANY}"
Capc2Configuration = "{5, 15, 63, 10ms, 43us, ACK_ANY}"
Capc3Configuration = "{5, 15, 1023, 10ms,79us, ACK_ANY}"

technologySelection = {0, 1, 2}  # 0: Only NR-U, 1: Only Wi-Fi, 2: NR-u and Wi-Fi

numGnbs = {1, 2, 3, 4, 5, 6}
numAps = {1, 2, 3, 4, 5, 6}
numUesPerGnb = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
numStasPerAp = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

trafficRatios = {"1:1:1:1", "2:1:1:1", "1:2:1:1", "1:1:2:1", "1:1:1:2"}

subcarrierSpacing = {0, 1, 2} # 0: 15 khz, 2: 60 Khz --> Limit for sub-7 GHz

runId = 0

file_path = "/home/aditya/Repositories/ns-3/contrib/nr-u/examples/cci-nr-wifi-qos.cc"

# Modify the channel access manager for the gNB first
line_number = 264
new_line_content = f'  std::string gnbCamType = "{gnbChannelAccessManager}";'
with open(file_path, 'r') as file:
    lines = file.readlines()
lines[line_number - 1] = new_line_content + '\n'
with open(file_path, 'w') as file:
    file.writelines(lines)

if gnbChannelAccessManager == "ns3::NrCat4LbtAccessManager":
    # If we are operating with Cat4, then we only need to change the CAPC2 values
    if varyDevice == "ue":
        total_experiments = 1
        total_tests = len(numUes) * len(Capc2Mcot) * len(Capc2CWMin) * len(Capc2CWMax)
        print("Running a total of ", total_experiments, " experiments with ", total_tests, "test cases")
        for ue in numUesPerGnb:
            print("Selecting ", ue, " ues for this run")
            for mcot in Capc2Mcot:
                print("Selecting ", mcot, "ms as mcot for this run")
                for cwMin in Capc2CWMin:
                    print("Selecting ", cwMin, " as cwMin for this run")
                    for cwMax in Capc2CWMax:
                        # If CW Max needs to be greater than CWmin
                        if cwMin >= cwMax:
                            continue

                        print("Selecting ", cwMax, " as cwMax for this run")
                        for defer in Capc2Defer:
                            print("Selecting ", defer, "us as defer for this run")
                            gnb = 3
                            line_number = 218
                            new_line_content = f'  uint32_t numGnbs = {gnb};'
                            with open(file_path, 'r') as file:
                                lines = file.readlines()
                                lines[line_number - 1] = new_line_content + '\n'

                            with open(file_path, 'w') as file:
                                file.writelines(lines)

                            # ue = 15
                            line_number = 219
                            new_line_content = f'  uint32_t numUesPerGnb = {ue};'
                            with open(file_path, 'r') as file:
                                lines = file.readlines()

                            lines[line_number - 1] = new_line_content + '\n'

                            with open(file_path, 'w') as file:
                                file.writelines(lines) 

                            ap = 3
                            line_number = 220
                            new_line_content = f'  uint32_t numAps = {ap};'
                            with open(file_path, 'r') as file:
                                lines = file.readlines()

                            lines[line_number - 1] = new_line_content + '\n'

                            with open(file_path, 'w') as file:
                                file.writelines(lines) 

                            sta = 15
                            line_number = 221
                            new_line_content = f'  uint32_t numStasPerAp = {sta};'
                            with open(file_path, 'r') as file:
                                lines = file.readlines()

                            lines[line_number - 1] = new_line_content + '\n'

                            with open(file_path, 'w') as file:
                                file.writelines(lines) 

                            # Given the values for the LBT parameters, let run the experiment to figure out the behavior of the gNB.
                            # Change the defer duration
                            line_number = 273
                            new_line_content = f'Time capc2Defer = MicroSeconds({defer});'
                            with open(file_path, 'r') as file:
                                lines = file.readlines()

                            lines[line_number - 1] = new_line_content + '\n'

                            with open(file_path, 'w') as file:
                                file.writelines(lines)

                            # Change the MCOT
                            line_number = 277
                            new_line_content = f'  Time capc2Mcot  = MilliSeconds({mcot});'
                            with open(file_path, 'r') as file:
                                lines = file.readlines()

                            lines[line_number - 1] = new_line_content + '\n'

                            with open(file_path, 'w') as file:
                                file.writelines(lines)

                            # Change the CWMin
                            line_number = 281
                            new_line_content = f'  uint32_t capc2CwMin = {cwMin};'
                            with open(file_path, 'r') as file:
                                lines = file.readlines()

                            lines[line_number - 1] = new_line_content + '\n'

                            with open(file_path, 'w') as file:
                                file.writelines(lines)


                            # Change the CWMin
                            line_number = 285
                            new_line_content = f'  uint32_t capc2CwMax = {cwMax};'
                            with open(file_path, 'r') as file:
                                lines = file.readlines()

                            lines[line_number - 1] = new_line_content + '\n'

                            with open(file_path, 'w') as file:
                                file.writelines(lines)

                            # Now we can run the experiment
                            start_time = time.time()
                            output_filename = f"output_{gnbChannelAccessManager}_defer{defer}_mcot{mcot}_cwmin{cwMin}_cwmax{cwMax}.txt"
                            with open(output_filename, 'w') as output_file:
                                subprocess.run(["./ns3", "run", "cci-nr-wifi-qos"], stdout=output_file, stderr=output_file)
                            end_time = time.time()
                            print("Completed experiment ", experiment,"/",total_experiments," and test ",test,"/",total_tests," in ",format(end_time - start_time))
    elif varyDevice == "gnb":
        print("Not supported")
    elif varyDevice == "ap":
        print("Not supported")
    elif varyDevice == "sta":
        print("Not supported")
    else:
        print("Invalid option to vary")
elif gnbChannelAccessManager == "ns3::NrCat4CapcLbtAccessManager":
    if varyDevice == "ue":
        print("Not supported")
    elif varyDevice == "gnb":
        print("Not supported")
    elif varyDevice == "ap":
        print("Not supported")
    elif varyDevice == "sta":
        print("Not supported")
    else:
        print("Invalid option to vary")