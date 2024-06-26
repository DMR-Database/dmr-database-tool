#!/usr/bin/python3
import requests
import csv
import os
import sys
import hashlib
import time
import shutil

# Application information
APP_NAME = "DMR Database Tool"
APP_VERSION = "v0.1"
APP_MAKER = "PD2EMC aka Einstein"
APP_MAKERS = "ChatGPT, and you ?"

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
line = "============================="

# Function to display header information
def header():
    print(f"===== {APP_NAME} =====")
    print(f"Version: {APP_VERSION}")
    print(f"Made by: {APP_MAKER}")
    print(f"Helped by: {APP_MAKERS}")

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
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except Exception as e:
        print(f"Error calculating MD5: {e}")
        return None
    return hash_md5.hexdigest()

# Function to download the CSV file and handle count checking
def download_csv():
    print(f"{line}")
    print(f"Download started from : {url}") 
    try:
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
    except requests.RequestException as e:
        print(f"Error downloading the CSV file: {e}")
        exit(1)

    new_md5 = calculate_md5(csv_filename)
    if new_md5 is None:
        exit(1)

    old_md5 = None
    if os.path.exists(md5_filename):
        with open(md5_filename, 'r') as file:
            old_md5 = file.read().strip()

    if old_md5 and old_md5 == new_md5:
        print('The file has not changed.')
        print(f'Old MD5: {old_md5}')
        print(f'New MD5: {new_md5}')
        entry_count = count_entries()
    else:
        with open(md5_filename, 'w') as file:
            file.write(new_md5)
        entry_count = count_entries()
        print(f"Download completed.")
        print(f'The count of entries is {entry_count}.')
        print(f'New MD5 hash: {new_md5}')
        if old_md5:
            print(f'Old MD5 hash: {old_md5}')

    with open(count_filename, 'w') as file:
        file.write(str(entry_count))
    print(f'The count of entries is {entry_count}.')

# Function to count entries in user.csv
def count_entries():
    try:
        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            entry_count = sum(1 for row in reader) - 1  # Subtracting 1 to exclude header row
    except Exception as e:
        print(f"Error counting entries: {e}")
        return 0
    return entry_count

# Function to process user.csv to userat.csv for Anytone Mobile Radio database
def process_to_userat():
    print(f"{line}")
    print(f"Starting process {csv_filename} to {userat_filename}...")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        # Step 1: Count total rows in user.csv
        total_rows = count_entries()
        current_row = 0

        with open(csv_filename, 'r') as infile, open(userat_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = ['No.', 'Radio ID', 'Callsign', 'Name', 'City', 'State', 'Country', 'Remarks', 'Call Type', 'Call Alert']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, row in enumerate(reader, start=1):
                current_row += 1
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

                # Step 2: Update progress bar
                progress = current_row / total_rows
                bar_length = 50
                block = int(bar_length * progress)
                bar = "#" * block + "-" * (bar_length - block)
                sys.stdout.write(f"\r[{bar}] {progress * 100:.2f}%")
                sys.stdout.flush()

        print()  # Move to the next line after the progress bar completes
        print(f"Processed {csv_filename} to {userat_filename}")

    else:
        print(f"Failed to process {csv_filename} to {userat_filename}.")
        exit(1)

# Function to process user.csv to DMRIds.dat for Pi-Star database
def process_to_pistar():
    print(f"{line}")
    print(f"Starting process {csv_filename} to {pistar_filename}...")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        # Step 1: Count total rows in user.csv
        total_rows = count_entries()
        current_row = 0

        with open(csv_filename, 'r') as infile, open(pistar_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            for row in reader:
                current_row += 1
                name = row['FIRST_NAME'].split()[0] if row['FIRST_NAME'].strip() else ''  # Use only the first name
                outfile.write(f"{row['RADIO_ID']}\t{row['CALLSIGN']}\t{name}\n")

                # Step 2: Update progress bar
                progress = current_row / total_rows
                bar_length = 50
                block = int(bar_length * progress)
                bar = "#" * block + "-" * (bar_length - block)
                sys.stdout.write(f"\r[{bar}] {progress * 100:.2f}%")
                sys.stdout.flush()

        print()  # Move to the next line after the progress bar completes
        print(f"Processed {csv_filename} to {pistar_filename}")

    else:
        print(f"Failed to process {csv_filename} to {pistar_filename}.")
        exit(1)

# Function to process user.csv to userhd.csv for Ailunce HD1 database
def process_to_userhd():
    print(f"{line}")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        try:
            shutil.copyfile(csv_filename, userhd_filename)
            print(f"Copied {csv_filename} to {userhd_filename}")
        except Exception as e:
            print(f"Error copying to {userhd_filename}: {e}")
    else:
        print(f"Failed to copy {csv_filename} to {userhd_filename}.")
        exit(1)

# Function to process user.csv to usermd2017.csv for Tytera MD2017 database
def process_to_usermd2017():
    print(f"{line}")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        try:
            shutil.copyfile(csv_filename, usermd2017_filename)
            print(f"Copied {csv_filename} to {usermd2017_filename}")
        except Exception as e:
            print(f"Error copying to {usermd2017_filename}: {e}")
    else:
        print(f"Failed to copy {csv_filename} to {usermd2017_filename}.")
        exit(1)

# Function to process user.csv to user.bin for Tytera MD380/390 database
def process_to_userbin():
    print(f"{line}")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        try:
            shutil.copyfile(csv_filename, userbin_filename)
            print(f"Copied {csv_filename} to {userbin_filename}")
        except Exception as e:
            print(f"Error copying to {userbin_filename}: {e}")
    else:
        print(f"Failed to copy {csv_filename} to {userbin_filename}.")
        exit(1)

# Function to process user.csv to usr.bin for Motorola database
def process_to_usrbin():
    print(f"{line}")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        try:
            shutil.copyfile(csv_filename, usrbin_filename)
            print(f"Copied {csv_filename} to {usrbin_filename}")
        except Exception as e:
            print(f"Error copying to {usrbin_filename}: {e}")
    else:
        print(f"Failed to copy {csv_filename} to {usrbin_filename}.")
        exit(1)


# Function to clean up downloaded and generated files
def clean_downloads():
    print(f"{line}")
    print(f"Cleanup all downloaded an converted files.")
    files_to_remove = [csv_filename, userat_filename, userhd_filename, usermd2017_filename, userbin_filename, usrbin_filename, pistar_filename, count_filename, md5_filename]
    for filename in files_to_remove:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"Removed {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")
#        else:
#            print(f"{filename} not found")

# Function to display help message
def display_help():
    print(f"{line}")
    print("Usage: dmr_tool.py [option]")
    print("Options:")
    print("  -d            Download the CSV file")
    print("  -userat       Process CSV to Anytone Mobile Radio database (userat.csv)")
    print("  -userhd       Process CSV to Ailunce HD1 database (userhd.csv)")
    print("  -usermd2017   Process CSV to Tytera MD2017 database (usermd2017.csv)")
    print("  -userbin      Process CSV to Tytera MD380/390 database (user.bin)")
    print("  -usrbin       Process CSV to Motorola database (usr.bin)")
    print("  -pistar       Process CSV to Pi-Star database (DMRIds.dat)")
    print("  -c            Clean all downloaded and generated files")
    print("  -a            Perform all operations (download, process to all formats, and clean)")

# Main function to handle user input
if __name__ == "__main__":
    header()
    start_time = time.time()

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
        print(f"{line}")
        print("All operations completed.")
    else:
        print(f"Invalid option '{option}'. Use '-h' for help.")
        exit(1)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{line}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

