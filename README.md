# DMR-Database-Python-Tool
DMR Database Python Tool

This script is designed to download a CSV file from a specified URL, process the data,
and convert it into various formats suitable for different radio databases. It can also
clean up the downloaded files and display the current count of entries in the CSV file.

Features:
- Download the CSV file with a custom progress bar.
- Count entries in the downloaded CSV file and compare with the previous count.
- Process the CSV file into different formats for various radio databases.
- Clean up all downloaded files and count.txt.
- Perform all operations sequentially with a single command.

Required Python Modules:
- requests: For downloading the CSV file.
- csv: For reading and counting entries in the CSV file.
- os: For file operations like checking if files exist.
- sys: For command-line argument handling and displaying the progress bar.
- shutil: For copying files.

Application Information:
Name: DMR Database Python Tool
Version: v0.1
Author: PD2EMC aka Einstein with help of ChatGPT
