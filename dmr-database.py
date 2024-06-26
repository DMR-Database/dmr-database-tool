#!/usr/bin/python3
import requests
import csv
import os
import sys
import hashlib
import time

# Application information
APP_NAME = "DMR Database Tool"
APP_VERSION = "v0.1"
APP_MAKER = "PD2EMC aka Einstein with help of my friend ChatGPT"

# URL of the CSV file
url = 'https://radioid.net/static/user.csv'

# Filenames
csv_filename = 'user.csv'
userat_filename = 'userat.csv'
userhd_filename = 'userhd.csv'
usermd2017_filename = 'usermd2017.csv'
userbin_filename = 'user.bin'
usrbin_filename = 'usr.bin'
pistar_filename = 'DMRIds.dat'
count_filename = 'count.txt'
md5_filename = 'user.md5'

# Function to display progress bar
def show_progress_bar(downloaded, total_size, bar_length=50):
    progress = downloaded / total_size
    block = int(bar_length * progress)
    bar = "#" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\r[{bar}] {progress * 100:.2f}%")
    sys.stdout.flush()

# Function to calculate MD5 hash of a file
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Function to download the CSV file and handle count checking
def download_csv():
    start_time = time.time()
    # Step 1: Download the CSV file with a custom progress bar
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    block_size = 1024  # 1 KB

    with open(csv_filename, 'wb') as file:
        for data in response.iter_content(block_size):
            downloaded += len(data)
            file.write(data)
            show_progress_bar(downloaded, total_size)

    print()  # Move to the next line after the progress bar completes

    if total_size != 0 and downloaded != total_size:
        print('Failed to download the CSV file completely.')
        exit(1)

    # Step 2: Calculate the MD5 hash of the downloaded CSV file
    new_md5 = calculate_md5(csv_filename)

    # Step 3: Check if users.md5 exists and read the old MD5 hash
    old_md5 = None
    if os.path.exists(md5_filename):
        with open(md5_filename, 'r') as file:
            old_md5 = file.read().strip()

    # Step 4: Compare MD5 hashes and decide action
    if old_md5 is not None and old_md5 == new_md5:
        print('The file has not changed.')
        print(f'Old MD5: {old_md5}')
        print(f'New MD5: {new_md5}')
    else:
        with open(md5_filename, 'w') as file:
            file.write(new_md5)

        # Count the entries in the downloaded CSV file
        entry_count = count_entries()
        with open(count_filename, 'w') as file:
            file.write(str(entry_count))

        print(f'Download completed. The count of entries is {entry_count}.')
        print(f'New MD5 hash: {new_md5}')
        if old_md5:
            print(f'Old MD5 hash: {old_md5}')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Function to count entries in user.csv
def count_entries():
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        entry_count = sum(1 for row in reader) - 1  # Subtracting 1 to exclude header row
    return entry_count

# Function to process user.csv to userat.csv for Anytone Mobile Radio database
def process_to_userat():
    start_time = time.time()
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        with open(csv_filename, 'r') as infile, open(userat_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = ['No.', 'Radio ID', 'Callsign', 'Name', 'City', 'State', 'Country', 'Remarks', 'Call Type', 'Call Alert']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, row in enumerate(reader, start=1):
                name = row['FIRST_NAME'].split()[0] if row['FIRST_NAME'].strip() else ''  # Use only the first name
                writer.writerow({
                    'No.': i,
                    'Radio ID': row['RADIO_ID'],
                    'Callsign': row['CALLSIGN'],
                    'Name': name,
                    'City': row['CITY'],
                    'State': row['STATE'],
                    'Country': row['COUNTRY'],
                    'Remarks': '',
                    'Call Type': 'Private Call',
                    'Call Alert': 'None'
                })
        print(f"Processed {csv_filename} to {userat_filename}")

    else:
        print(f"Failed to process {csv_filename} to {userat_filename}.")
        exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Function to process user.csv to userhd.csv for Ailunce HD1 database
def process_to_userhd():
    start_time = time.time()
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        with open(csv_filename, 'r') as infile, open(userhd_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = ['No.', 'Radio ID', 'Callsign', 'Name', 'City', 'State', 'Country']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, row in enumerate(reader, start=1):
                name = row['FIRST_NAME'].split()[0] if row['FIRST_NAME'].strip() else ''  # Use only the first name
                writer.writerow({
                    'No.': i,
                    'Radio ID': row['RADIO_ID'],
                    'Callsign': row['CALLSIGN'],
                    'Name': name,
                    'City': row['CITY'],
                    'State': row['STATE'],
                    'Country': row['COUNTRY']
                })
        print(f"Processed {csv_filename} to {userhd_filename}")

    else:
        print(f"Failed to process {csv_filename} to {userhd_filename}.")
        exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Function to process user.csv to usermd2017.csv for Tytera MD2017 database
def process_to_usermd2017():
    start_time = time.time()
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        with open(csv_filename, 'r') as infile, open(usermd2017_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = ['No.', 'Radio ID', 'Callsign', 'Name', 'City', 'State', 'Country']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, row in enumerate(reader, start=1):
                name = row['FIRST_NAME'].split()[0] if row['FIRST_NAME'].strip() else ''  # Use only the first name
                writer.writerow({
                    'No.': i,
                    'Radio ID': row['RADIO_ID'],
                    'Callsign': row['CALLSIGN'],
                    'Name': name,
                    'City': row['CITY'],
                    'State': row['STATE'],
                    'Country': row['COUNTRY']
                })
        print(f"Processed {csv_filename} to {usermd2017_filename}")

    else:
        print(f"Failed to process {csv_filename} to {usermd2017_filename}.")
        exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Function to process user.csv to user.bin for Tytera MD380/390 database
def process_to_userbin():
    start_time = time.time()
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        with open(csv_filename, 'r') as infile, open(userbin_filename, 'wb') as outfile:
            reader = csv.DictReader(infile)
            for row in reader:
                name = row['FIRST_NAME'].split()[0] if row['FIRST_NAME'].strip() else ''  # Use only the first name
                data = f"{row['RADIO_ID']}\t{row['CALLSIGN']}\t{name}\t{row['CITY']}\t{row['STATE']}\t{row['COUNTRY']}\n"
                outfile.write(data.encode('utf-8'))
        print(f"Processed {csv_filename} to {userbin_filename}")

    else:
        print(f"Failed to process {csv_filename} to {userbin_filename}.")
        exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Function to process user.csv to usr.bin for Pi-Star SSH Helper database
def process_to_usrbin():
    start_time = time.time()
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        with open(csv_filename, 'r') as infile, open(usrbin_filename, 'wb') as outfile:
            reader = csv.DictReader(infile)
            for row in reader:
                name = row['FIRST_NAME'].split()[0] if row['FIRST_NAME'].strip() else ''  # Use only the first name
                data = f"{row['RADIO_ID']}\t{row['CALLSIGN']}\t{name}\t{row['CITY']}\t{row['STATE']}\t{row['COUNTRY']}\n"
                outfile.write(data.encode('utf-8'))
        print(f"Processed {csv_filename} to {usrbin_filename}")

    else:
        print(f"Failed to process {csv_filename} to {usrbin_filename}.")
        exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Function to process user.csv to DMRIds.dat for Pi-Star database
def process_to_pistar():
    start_time = time.time()
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        with open(csv_filename, 'r') as infile, open(pistar_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            for row in reader:
                name = row['FIRST_NAME'].split()[0] if row['FIRST_NAME'].strip() else ''  # Use only the first name
                outfile.write(f"{row['RADIO_ID']}\t{row['CALLSIGN']}\t{name}\n")
        print(f"Processed {csv_filename} to {pistar_filename}")

    else:
        print(f"Failed to process {csv_filename} to {pistar_filename}.")
        exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

# Function to clean up downloaded files
def clean_downloads():
    files_to_delete = [csv_filename, userat_filename, userhd_filename, usermd2017_filename,
                       userbin_filename, usrbin_filename, pistar_filename, count_filename, md5_filename]

    for filename in files_to_delete:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Deleted {filename}")
        else:
            print(f"{filename} not found.")

# Function to display help information
def display_help():
    print(f"=== {APP_NAME} ===")
    print(f"Version: {APP_VERSION}")
    print(f"Made by: {APP_MAKER}\n")
    print("Options:")
    print("-a : Clean all, then download, and process to all destinations.")
    print("-d : Download the CSV file.")
    print("-c : Clean all downloaded files and count.txt.")
    print("-h : Display this help message.\n")
    print("Processing Options:")
    print("-userat : Process user.csv to userat.csv for Anytone Mobile Radio database.")
    print("-userhd : Process user.csv to userhd.csv for Ailunce HD1 database.")
    print("-usermd2017 : Process user.csv to usermd2017.csv for Tytera MD2017 database.")
    print("-userbin : Process user.csv to user.bin for Tytera MD380/390 database.")
    print("-usrbin : Process user.csv to usr.bin for Pi-Star SSH Helper database.")
    print("-pistar : Process user.csv to DMRIds.dat for Pi-Star database.")

# Main function to handle user input
if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        display_help()
        exit(1)

    option = sys.argv[1]

    if option == "-d":
        download_csv()
    elif option == "-userat":
        process_to_userat()
    elif option == "-userhd":
        process_to_userhd()
    elif option == "-usermd2017":
        process_to_usermd2017()
    elif option == "-userbin":
        process_to_userbin()
    elif option == "-usrbin":
        process_to_usrbin()
    elif option == "-pistar":
        process_to_pistar()
    elif option == "-c":
        clean_downloads()
    elif option == "-a":
        clean_downloads()
        download_csv()
        process_to_userat()
        process_to_userhd()
        process_to_usermd2017()
        process_to_userbin()
        process_to_usrbin()
        process_to_pistar()
        print("All operations completed.")
    else:
        print(f"Invalid option '{option}'. Use '-h' for help.")
        exit(1)
