# DMR Database Tool

## Description

DMR Database Tool is a Python script designed to facilitate downloading and processing DMR (Digital Mobile Radio) user databases. It provides functionality to download a CSV file containing user information, process it into various formats suitable for different DMR radios and systems, and manage the downloaded files efficiently.

## Features

- **Download Feature**: Downloads a CSV file containing DMR user information from a specified URL.
- **Processing Options**:
  - `-userat`: Processes user.csv to userat.csv for Anytone database.
  - `-userhd`: Processes user.csv to userhd.csv for Ailunce HD1 database.
  - `-usermd2017`: Processes user.csv to usermd2017.csv for Tytera MD2017 database.
  - `-userbin`: Processes user.csv to user.bin for Tytera MD380/390 database.
  - `-usrbin`: Processes user.csv to usr.bin for Pi-Star SSH Helper database.
  - `-pistar`: Processes user.csv to DMRIds.dat for Pi-Star database.
- **Additional Options**:
  - `-d`: Downloads the CSV file.
  - `-c`: Cleans all downloaded files and count.txt.
  - `-a`: Cleans all, downloads, and processes to all destinations.
  - `-h`: Displays help information.

## Required Python Modules

The script requires the following Python modules, which can typically be installed using pip:

- `requests`
- `csv`
- `os`
- `sys`
- `shutil`
- `hashlib`

## Usage

Ensure you have Python 3 installed. Navigate to the directory containing the script and execute it using Python:

```bash
python dmr-database.py [option]
Replace [option] with one of the available options (-d, -c, -a, -h, -userat, -userhd, -usermd2017, -userbin, -usrbin, -pistar).

Examples
Download the CSV file:
python dmr-database.py -d

Process to Anytone Mobile Radio database:
python dmr-database.py -userat

Clean all and process to all destinations:
python dmr-database.py -a

Display help:
python dmr-database.py -h
````
Author
Author: PD2EMC aka Einstein with help of ChatGPT
