import os
import shutil
import subprocess
import glob

try:
    # Run the dmr-database.py script and show live output
    result = subprocess.run(["python", "dmr-database.py", "-a"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error while running dmr-database.py: {e}")
    raise

# Define source and destination directories
src_dir = "/usr/src/app"
dest_dir = os.path.join(src_dir, "output")

# Ensure the destination directory exists
os.makedirs(dest_dir, exist_ok=True)

# Define files to exclude
excluded_files = ["citys_nl.csv", "user_ext.csv"]

# Copy all .csv and .bin files to the output directory, excluding specific files
for file_pattern in ["*.csv", "*.bin", "*.dat"]:
    for file_path in glob.glob(os.path.join(src_dir, file_pattern)):
        if os.path.basename(file_path) not in excluded_files:
            shutil.copy(file_path, dest_dir)
            print(f"File {file_path} copied to {dest_dir}")
