#!/usr/bin/python3
##Please set your python path above
import requests
import sys
import os
import argparse
import json
import csv

# Function to display a progress bar
def show_progress_bar(downloaded, total_size, bar_length=50):
    progress = downloaded / total_size
    block = int(bar_length * progress)
    bar = "#" * block + "-" * (bar_length - block)
    sys.stdout.write(f"\r[{bar}] {progress * 100:.2f}%")
    sys.stdout.flush()

# Function to download the JSON file
def download_json(url, output_file):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        chunk_size = 1024  # 1 Kilobyte

        with open(output_file, 'wb') as file:
            for data in response.iter_content(chunk_size):
                file.write(data)
                downloaded += len(data)
                show_progress_bar(downloaded, total_size)
        print(f'\nJSON file downloaded and saved successfully as {output_file}.')
    else:
        print('Failed to download the JSON file.')

# Function to remove the downloaded JSON file
def clean_json(output_file):
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f'{output_file} has been removed.')
    else:
        print(f'{output_file} does not exist.')

# Function to process the JSON file and save it to a CSV file
def process_to_csv(json_file, csv_file):
    if not os.path.exists(json_file):
        print(f'{json_file} does not exist. Downloading it now...')
        url = 'https://metatopos.dijkewijk.nl/metatopos-places.json'
        download_json(url, json_file)
    
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if 'places' not in data:
        print(f'No "places" key found in {json_file}.')
        return

    places = data['places']
    total_places = len(places)
    processed = 0

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CITY', 'STATE'])

        for place in places:
            city = place.get('place', '')
            state = place.get('province', '')
            writer.writerow([city, state])
            processed += 1
            show_progress_bar(processed, total_places)
    print(f'\nData processed and saved to {csv_file}.')

# Main function
def main():
    parser = argparse.ArgumentParser(description="Download and manage JSON file.")
    parser.add_argument('-d', '--download', action='store_true', help='Download the JSON file.')
    parser.add_argument('-c', '--clean', action='store_true', help='Remove the downloaded JSON file.')
    parser.add_argument('-p', '--process_to_csv', action='store_true', help='Process the JSON file and save to CSV.')
    args = parser.parse_args()

    url = 'https://metatopos.dijkewijk.nl/metatopos-places.json'
    json_file = 'citys_nl.json'
    csv_file = 'citys_nl.csv'

    if args.download:
        download_json(url, json_file)
    if args.clean:
        clean_json(json_file)
    if args.process_to_csv:
        process_to_csv(json_file, csv_file)
    if not args.download and not args.clean and not args.process_to_csv:
        print('Please specify an action: -d to download, -c to clean, -p to process to CSV.')

if __name__ == '__main__':
    main()





