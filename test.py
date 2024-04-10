import subprocess
import time
import matplotlib.pyplot as plt
import os
import shutil

def clear_cache():
    cache_dir = utils.cache_dir()  # Retrieve the cache directory path from the utils module
    try:
        # Check if the cache directory exists
        if os.path.exists(cache_dir):
            # Recursively delete the directory contents
            shutil.rmtree(cache_dir)
            print(f"Cache directory '{cache_dir}' cleared.")
        else:
            print(f"Cache directory '{cache_dir}' does not exist.")
    except Exception as e:
        print(f"Failed to clear cache directory '{cache_dir}': {e}")

data_dir = "/data"
plot_filename = os.path.join(data_dir, "execution_time_by_num_workers.png")
os.makedirs(data_dir, exist_ok=True)

# Configuration for benchmarking
num_workers_options = [2, 4, 8, 16]
execution_times = []

# Parameters for the command
bulkdata = "BILLSTATUS"
congress = "118"

# Loop through each num_workers option to run the script and measure execution time
for num_workers in num_workers_options:
    clear_cache()

    command = [
        "usc-run", "govinfo",
        "--bulkdata={}".format(bulkdata),
        "--congress={}".format(congress),
        "--workers={}".format(num_workers)
    ]

    # Measure start time
    start_time = time.time()
    
    print(f"Running {command}")
    # Execute the command
    result = subprocess.run(command, capture_output=True)
    
    # Check for errors
    if result.returncode != 0:
        print(f"Error executing {' '.join(command)}: {result.stderr}")
        continue
    
    # Measure end time
    end_time = time.time()
    
    # Calculate execution time and store it
    execution_times.append(end_time - start_time)
    
    # Optional: Print execution time for this run
    print(f"Execution time with {num_workers} workers: {end_time - start_time:.2f} seconds")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(num_workers_options, execution_times, marker='o', linestyle='-')
plt.title('Execution Time by Number of Workers')
plt.xlabel('Number of Workers')
plt.ylabel('Execution Time (seconds)')
plt.xticks(num_workers_options)
plt.grid(True)
plt.show()

plt.savefig(plot_filename)
