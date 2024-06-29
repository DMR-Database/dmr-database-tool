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
APP_VERSION = "v0.2"
APP_MAKER = "PD2EMC aka Einstein"
APP_MAKERS = "ChatGPT and maybe you ?"

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
ext_filename = 'users_ext.csv'
line = "============================="

# Display header information about the application.
def header():
    print(f"===== {APP_NAME} =====")
    print(f"Version: {APP_VERSION}")
    print(f"Made by: {APP_MAKER}")
    print(f"Helped by: {APP_MAKERS}")

# Display a progress bar for file download.
def show_progress_bar(downloaded, total_size, bar_length=50):
    progress = downloaded / total_size
    block = int(bar_length * progress)
    bar = "#" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\r[{bar}] {progress * 100:.2f}%")
    sys.stdout.flush()

# Display progress of processing each row of data.
def show_row_progress(current_row, total_rows, id='', callsign='', bar_length=50):
    progress = current_row / total_rows
    callsign_truncated = callsign[:7] if callsign else ''
    if current_row < total_rows:
        sys.stdout.write(f"\rProcessing... {progress * 100:.2f}% ({current_row}/{total_rows} rows) - ID: {id} - Callsign: {callsign_truncated:<6}")
    else:
        sys.stdout.write(f"\rProcessing... 100.00% ({total_rows}/{total_rows} rows)")
    sys.stdout.flush()

# Calculate the MD5 hash of a file.
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

# Download the CSV file from a specified URL.
def download_csv():
    print(f"{line}")
    print(f"Download started from: {url}") 
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        block_size = 1024  # 1 KB

        # Download the file in chunks and show the progress bar
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

    # Calculate the MD5 hash of the new file
    new_md5 = calculate_md5(csv_filename)
    if new_md5 is None:
        exit(1)

    old_md5 = None
    if os.path.exists(md5_filename):
        with open(md5_filename, 'r') as file:
            old_md5 = file.read().strip()

    # Check if the file has changed by comparing MD5 hashes
    if old_md5 and old_md5 == new_md5:
        print('The file has not changed.')
        print(f'Old MD5: {old_md5}')
        print(f'New MD5: {new_md5}')
        entry_count = count_entries()
    else:
        with open(md5_filename, 'w') as file:
            file.write(new_md5)
        entry_count = count_entries()
        print("Download completed.")
        print(f'The count of entries is {entry_count}.')
        print(f'New MD5 hash: {new_md5}')
        if old_md5:
            print(f'Old MD5 hash: {old_md5}')

    # Write the count of entries to the count file
    with open(count_filename, 'w') as file:
        file.write(str(entry_count))
    print(f'The count of entries is {entry_count}.')
    
# Merge users_ext.csv into user.csv, overwriting data in user.csv.
def merge_csv():
    print(f"{line}")
    print(f"Merging {ext_filename} into {csv_filename}...")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        # Read user.csv into a dictionary keyed by RADIO_ID
        user_data = {}
        with open(csv_filename, 'r', newline='', encoding='utf-8') as user_file:
            user_reader = csv.DictReader(user_file)
            for row in user_reader:
                user_data[row['RADIO_ID']] = row

        # Read users_ext.csv and overwrite user.csv data with it
        merge_count = 0
        with open(ext_filename, 'r', newline='', encoding='utf-8') as ext_file:
            ext_reader = csv.DictReader(ext_file)
            for row in ext_reader:
                user_data[row['RADIO_ID']] = row
                merge_count += 1

        # Write the merged data back to user.csv
        with open(csv_filename, 'w', newline='', encoding='utf-8') as user_file:
            fieldnames = ext_reader.fieldnames  # Use the fieldnames from the extension file
            user_writer = csv.DictWriter(user_file, fieldnames=fieldnames)
            user_writer.writeheader()
            for row in user_data.values():
                user_writer.writerow(row)

        print(f"Merged {merge_count} lines from {ext_filename} into {csv_filename}.")

    else:
        print(f"Failed to merge {ext_filename} into {csv_filename}.")
        exit(1)

# Count the number of entries (rows) in the CSV file.
def count_entries():
    try:
        with open(csv_filename, 'r') as file:
            reader = csv.reader(file)
            entry_count = sum(1 for row in reader) - 1  # Subtracting 1 to exclude header row
    except Exception as e:
        print(f"Error counting entries: {e}")
        return 0
    return entry_count

# Process CSV to Anytone Mobile Radio database (userat.csv).
def process_to_userat():
    print(f"{line}")
    print(f"Starting process {csv_filename} to {userat_filename}...")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        total_rows = count_entries()
        current_row = 0

        # Open input and output files
        with open(csv_filename, 'r') as infile, open(userat_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            fieldnames = ['No.', 'Radio ID', 'Callsign', 'Name', 'City', 'State', 'Country', 'Remarks', 'Call Type', 'Call Alert']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, lineterminator='\n')  # Ensure consistent line endings
            writer.writeheader()

            # Process each row and write to the output file
            for i, row in enumerate(reader, start=1):
                current_row += 1
                name = row['FIRST_NAME'].split()[0] if row['FIRST_NAME'].strip() else ''
                writer.writerow({
                    'No.': i,
                    'Radio ID': row['RADIO_ID'],
                    'Callsign': row['CALLSIGN'],  # Keep full callsign
                    'Name': name,
                    'City': row['CITY'],
                    'State': row['STATE'],
                    'Country': row['COUNTRY'],
                    'Remarks': '',
                    'Call Type': 'Private Call',
                    'Call Alert': 'None'
                })

                # Show row processing progress with ID and truncated callsign for output
                show_row_progress(current_row, total_rows, row['RADIO_ID'], row['CALLSIGN'])

        print()  # Move to the next line after the progress completes
        print(f"Processed {csv_filename} to {userat_filename}")

    else:
        print(f"Failed to process {csv_filename} to {userat_filename}.")
        exit(1)

# Process CSV to Pi-Star database (DMRIds.dat).
def process_to_pistar():
    print(f"{line}")
    print(f"Starting process {csv_filename} to {pistar_filename}...")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename):
        total_rows = count_entries()
        current_row = 0

        # Open input and output files
        with open(csv_filename, 'r') as infile, open(pistar_filename, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            for row in reader:
                current_row += 1
                outfile.write(f"{row['RADIO_ID']}\t{row['CALLSIGN']}\n")  # Keep full callsign

                # Show row processing progress with ID and truncated callsign for output
                show_row_progress(current_row, total_rows, row['RADIO_ID'], row['CALLSIGN'])

        print()  # Move to the next line after the progress completes
        print(f"Processed {csv_filename} to {pistar_filename}")

    else:
        print(f"Failed to process {csv_filename} to {pistar_filename}.")
        exit(1)

# Process CSV to Ailunce HD1 database (userhd.csv).
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

# Process CSV to Tytera MD2017 database (usermd2017.csv).
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

# Process CSV to Tytera MD380/390 database (user.bin).
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

# Process CSV to Motorola database (usr.bin).
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

# Cleanup all downloaded and converted files.
def clean_downloads():
    print(f"{line}")
    print(f"Cleanup all downloaded and converted files.")
    files_to_remove = [csv_filename, userat_filename, userhd_filename, usermd2017_filename, userbin_filename, usrbin_filename, pistar_filename, count_filename, md5_filename]
    for filename in files_to_remove:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"Removed: {filename}")
            except Exception as e:
                print(f"Error removing {filename}: {e}")

# Display usage instructions and available options.
def display_help():
    print(f"{line}")
    print("Usage: dmr_tool.py [option]")
    print("Options:")
    print("  -c            Clean all downloaded and generated files")
    print("  -a            Perform all operations (clean, download and process to all formats)")
    print("  -d            Download the CSV file only")
    print("  -m            Download and merge the CSV file with users_ext.csv")
    print("  -userat       Process CSV to Anytone Mobile Radio database (userat.csv)")
    print("  -userhd       Process CSV to Ailunce HD1 database (userhd.csv)")
    print("  -usermd2017   Process CSV to Tytera MD2017 database (usermd2017.csv)")
    print("  -userbin      Process CSV to Tytera MD380/390 database (user.bin)")
    print("  -usrbin       Process CSV to Motorola database (usr.bin)")
    print("  -pistar       Process CSV to Pi-Star database (DMRIds.dat)")

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
    elif option == "-m":
        merge_csv()
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
        merge_csv()
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
