## DMR Database Tool

Introduction
------------
The DMR Database Tool is a command-line utility designed to manage and process Digital Mobile Radio (DMR) user databases. It facilitates downloading the latest user data, cleaning up files, and converting data into formats suitable for various DMR radio models and systems.


The DMR Database Tool supports converting data into formats suitable for the following DMR radio models or systems:

- Anytone Radio *supported*
- Ailunce HD1 *not yet*
- Tytera MD2017 *not yet*
- Tytera MD380/MD390 *not yet*
- Pi-Star SSH Helper *not yet*
- Pi-Star *supported*

These are the specific formats into which the tool can process the downloaded DMR user data (user.csv). Each option (-userat, -userhd, -usermd2017, -userbin, -usrbin, -pistar) corresponds to converting the data into a format compatible with the respective radio model or system listed above.

Features
--------
Core Features:
- Download: Fetch the latest DMR user data from a specified URL.
- Process: Convert downloaded data into different formats for specific DMR radio models.
- Clean Up: Remove downloaded files and metadata for a clutter-free workspace.

Optional Features:
- Single-Command Operation: Combine download, cleaning, and processing in one command (-a option).
- Detailed Help Menu: Access comprehensive command descriptions and usage (-h option).
- MD5 Checksum Verification: Ensure data integrity by comparing MD5 hashes before processing.

Installation
------------
Requirements:
- Python 3.x
- Required Python modules: requests, csv, os, sys, shutil, hashlib

Setup:
1. Install Python 3: Download and install Python 3 from python.org/downloads/.
2. Install Required Modules: Open a terminal or command prompt and install required modules: requests, csv, os, sys, shutil and hashlib
3. Download the Tool: Download the dmr-database.py script.

Usage
-----
Command Line Options:

- Download Latest Data (-d)
./dmr-database.py -d
Downloads the latest user data in CSV format from a specified URL.

- Clean Up Files (-c)
./dmr-database.py -c
Removes all downloaded files (user.csv, userat.csv, etc.) and metadata (count.txt).

- Process Data (-userat, -userhd, etc.)
./dmr-database.py -userat
./dmr-database.py -userhd
./dmr-database.py -usermd2017
./dmr-database.py -userbin
./dmr-database.py -usrbin
./dmr-database.py -pistar
Converts user.csv into specific formats for different DMR radio models/systems.

- Single-Command Operation (-a)
./dmr-database.py -a
Cleans up, downloads the latest data, and processes it into all supported formats.

- Help (-h)
./dmr-database.py -h
Displays a detailed help menu with command descriptions and examples.

Examples:

- Download and Process for Anytone Mobile Radio
./dmr-database.py -d -userat

- Clean Up All Files
./dmr-database.py -c

- Download, Clean, and Process for All Formats
./dmr-database.py -a

Notes
-----
- Ensure Python 3 and required modules are installed and accessible.
- Output files (userat.csv, userhd.csv, etc.) are generated based on processed data from user.csv.
- Use -h option for detailed command help and usage examples.
