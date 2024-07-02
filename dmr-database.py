#!/opt/homebrew/bin/python3.11
##!/usr/bin/python3
##Please set your python path above
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
ext_filename = 'user_ext.csv'
city_state_csv = 'citys_nl.csv'
countrys_filename = 'countrys.csv'
states_filename = 'states.csv'
line = "============================="

# Search for empty County in Dutch callsign and fill them
def fill_empty_state():
    print(f"{line}")
    print(f"Starting filling States from citys_nl.csv")
    # Check if the necessary files exist
    if not os.path.exists(csv_filename):
        print(f"Error: {csv_filename} not found.")
        return
    if not os.path.exists(city_state_csv):
        print(f"Error: {city_state_csv} not found.")
        return

    # Load city-state mapping from citys_nl.csv into a dictionary
    city_state_map = {}
    with open(city_state_csv, 'r', newline='', encoding='utf-8') as city_file:
        city_reader = csv.DictReader(city_file)
        
        # Debug: Print the headers to ensure they are correct
        headers = city_reader.fieldnames
        #print(f"Headers in {city_state_csv}: {headers}")
        
        if 'CITY' not in headers or 'STATE' not in headers:
            print(f"Error: Expected headers 'CITY' and 'STATE' not found in {city_state_csv}")
            return
        
        for row in city_reader:
            city_state_map[row['CITY'].strip().lower()] = row['STATE']

    # Read user.csv and update the STATE where it is empty
    updated_rows = []
    with open(csv_filename, 'r', newline='', encoding='utf-8') as user_file:
        user_reader = csv.DictReader(user_file)
        fieldnames = user_reader.fieldnames
        
        if 'CITY' not in fieldnames or 'STATE' not in fieldnames:
            print(f"Error: Expected headers 'CITY' and 'STATE' not found in {csv_filename}")
            return
        
        user_data = list(user_reader)
        total_rows = len(user_data)
        
        for current_row, row in enumerate(user_data, start=1):
            if row['STATE'] == '' and row['CALLSIGN'].startswith(('PA', 'PB', 'PC', 'PD', 'PE', 'PF', 'PG', 'PH', 'PI')):
                city = row['CITY'].strip().lower()  # Normalize city name to lowercase
                if city in city_state_map:
                    row['STATE'] = city_state_map[city]
        #            print(f"Updated STATE for CITY {row['CITY']} to {city_state_map[city]}")
            updated_rows.append(row)
            show_row_progress(current_row, total_rows, row['RADIO_ID'], row['CALLSIGN'])
    
    # Write the updated data back to user.csv
    with open(csv_filename, 'w', newline='', encoding='utf-8') as user_file:
        user_writer = csv.DictWriter(user_file, fieldnames=fieldnames)
        user_writer.writeheader()
        user_writer.writerows(updated_rows)
    
    print(f"\nCompleted updating {csv_filename}")

# Convert Long Country names to Short version
def load_country_mapping():
    country_mapping = {}
    with open(countrys_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            country_mapping[row[0]] = row[1]  # Country_long -> Country_short
    return country_mapping

# Convert Long State names to Short version
def load_state_mapping():
    state_mapping = {}
    with open(states_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            state_mapping[row['State_long']] = row['State_short']
    return state_mapping

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
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()

    if os.path.exists(csv_filename) and os.path.exists(ext_filename):
        print(f"Merging {ext_filename} into {csv_filename}...")
        
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
        if not os.path.exists(csv_filename):
            print(f"Failed to merge {ext_filename} into {csv_filename}: {csv_filename} not found.")
        if not os.path.exists(ext_filename):
            print(f"Failed to merge {ext_filename} into {csv_filename}: {ext_filename} not found.")

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
    temp_filename = 'usermd2017_temp.csv'
    line = "-" * 40

    print(f"{line}")
    print(f"Starting process {csv_filename} to {usermd2017_filename}...")
    if not os.path.exists(csv_filename):
        print(f"{csv_filename} not found. Downloading it first.")
        download_csv()
        merge_csv()
        fill_empty_state()
        print(f"{line}")

    # Load country and state mappings
    country_mapping = load_country_mapping()
    state_mapping = load_state_mapping()
    
    # Open user.csv for reading and a temporary file for writing
    with open(csv_filename, 'r', newline='', encoding='utf-8') as infile, \
         open(temp_filename, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)
        
        # Check if all required headers are present
        required_headers = ['RADIO_ID', 'CALLSIGN', 'FIRST_NAME', 'LAST_NAME', 'CITY', 'STATE', 'COUNTRY']
        if not all(header in reader.fieldnames for header in required_headers):
            print("Some required headers are missing in user.csv.")
            exit(1)
        
        # Write header to temporary file
        #writer.writerow(['Radio ID', 'Callsign', 'Name', 'City', 'State', 'Country'])
        
        total_rows = sum(1 for line in open(csv_filename, 'r', newline='', encoding='utf-8'))
        current_row = 0
        max_users = 100000
        
        for row in reader:
            current_row += 1
            if current_row > max_users:
                break
            
            # Extract fields from the row
            radio_id = row.get('RADIO_ID', '')  # Use .get() to avoid KeyError
            callsign = row.get('CALLSIGN', '')
            name = f"{row.get('FIRST_NAME', '')} {row.get('LAST_NAME', '')}"
            city = row.get('CITY', '')
            state = row.get('STATE', '')
            country = row.get('COUNTRY', '')
            
            # Convert long country name to short version if mapping exists
            if country in country_mapping:
                country = country_mapping[country]
            
            # Convert long state name to short version if mapping exists
            if state in state_mapping:
                state = state_mapping[state]
            
            # Write updated row to the temporary file
            writer.writerow([radio_id, callsign, name, city, state, country])
            
            # Show progress
            show_row_progress(current_row, total_rows, radio_id, callsign)
    
    print()  # Move to the next line after the progress completes
    
    # Calculate the number of characters in the temporary file
    with open(temp_filename, 'r', encoding='utf-8') as temp_file:
        content = temp_file.read()
        char_count = len(content)
    
    # Write the final output file with the character count header
    with open(usermd2017_filename, 'w', newline='', encoding='utf-8') as outfile:
        outfile.write(f"{char_count},,,,,\n")
        outfile.write(content)
    
    # Remove the temporary file
    os.remove(temp_filename)
    
    print(f"Generated {usermd2017_filename}")
    

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
    print("Usage: dmr-database.py [option]")
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
        merge_csv()
        fill_empty_state()
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
        fill_empty_state()
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
