# This script repeatedly tests DH + TensorFlow for segfaults

# Imports
import subprocess
from subprocess import TimeoutExpired
import signal
import time
import sys
import os

# Globals
cwd = os.getcwd()
reports_folder = "reports/"

# Function Definitions
def start_docker(folder_path, run_num):
    docker_process = subprocess.Popen("docker-compose up server > " + folder_path + "run_number" + str(run_num) + ".txt", \
        stdout = subprocess.PIPE, \
        shell = True, \
        preexec_fn = os.setsid)

    return docker_process
   
def stop_docker(process):
    subprocess.Popen("docker-compose down server", \
        stdout = subprocess.PIPE, 
        shell = True, 
        preexec_fn = os.setsid).wait()

def check_logfile(path, n, n_s, n_f):
    tensorflow_substring = "Epoch 100/100"
    f = open(path + "run_number" + str(n) + ".txt", "r")
    lines = f.readlines()
    f.close()
    return [idx for idx, line in enumerate(lines) if tensorflow_substring in line]
     

# The Main Function
def main():
    num_successes = 0
    num_fails = 0
    global reports_folder
    # Build just once
    os.system('docker-compose build')
    for run_number in range(10):
        with start_docker(reports_folder, run_number) as process:
          try:
            process.wait(60)
          except TimeoutExpired:
            stop_docker(start_pid)
          success = check_logfile(reports_folder, run_number, num_successes, num_fails)
          if success:
            num_successes = num_successes + 1
          else:
            num_fails = num_fails + 1
    print("Number of successes: " + str(num_successes))
    print("Number of failures: " + str(num_fails))

if __name__ == "__main__":
    main()
