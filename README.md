DMR Database Tool

About the DMR Database Tool
------------
The DMR Database Tool is a versatile script designed to manage and update DMR user data for various radio models. Originally developed as a shell script (.sh), it has been transitioned (*work in progress*) to Python (.py) to leverage Python's robust data processing capabilities, readability and cross-platform compatibility.

Why the Change?
------------
- Enhanced Functionality: Python provides more powerful libraries and tools for data processing and automation, allowing us to expand the script's features.
- Improved Readability: Python's clear syntax makes the script easier to read, maintain, and extend, encouraging community contributions.
- Cross-Platform Compatibility: Python ensures the script can run on different operating systems without modification.

Why Release It Now?
------------
After five years of private development and refinement, we are transitioning to python from shell scripts and releasing the DMR Database Tool (beta) to the public to:

- Share Our Work: Contribute a mature and stable tool to the DMR community.
- Encourage Collaboration: Invite feedback and enhancements from a broader audience.
- Support the Community: Help radio operators easily keep their devices updated with the latest user data.

Beta Status
------------
While transitioning from .sh to .py, the tool is currently in beta. This means it is functional but still undergoing testing and improvements. We appreciate your patience and welcome any feedback to make it better.

We believe this release will foster innovation and collaboration, benefiting the entire DMR community.

Introduction
------------
The DMR Database Tool is a command-line utility designed to manage and process Digital Mobile Radio (DMR) user databases. It facilitates downloading the latest user data, cleaning up files and converting data into formats suitable for various DMR radio models and systems.


The DMR Database Tool supports converting data into formats suitable for the following DMR radio models or systems:

- Anytone Radio **supported*
- Ailunce HD1 **wip** 1% done
- Tytera MD2017 **wip** 1% done
- Tytera MD380/MD390 **wip** 1% done
- Pi-Star SSH Helper **wip** 1% done
- Pi-Star **supported*

These are the specific formats into which the tool can process the downloaded DMR user data (user.csv). Each option (-userat, -userhd, -usermd2017, -userbin, -usrbin, -pistar) corresponds to converting the data into a format compatible with the respective radio model or system listed above.

Features
--------
Core Features:
- Download: Fetch the latest DMR user data from a specified URL.
- Process: Convert downloaded data into different formats for specific DMR radio models.
- Clean Up: Remove downloaded files and metadata for a clutter-free workspace.

Optional Features:
- Single-Command Operation: Combine cleaning, download and processing in one command (-a option).
- Detailed Help Menu: Access comprehensive command descriptions and usage (-h option).
- MD5 Checksum Verification: Ensure data integrity by comparing MD5 hashes before processing.

Installation
------------
Requirements:
- Python 3.x
- Required Python modules: requests, csv, os, sys, shutil and hashlib

Setup:
1. Install Python 3: Download and install Python 3 from python.org/downloads/.
2. Install Required Modules: Open a terminal or command prompt and install required modules: requests, csv, os, sys, shutil and hashlib
3. Download the Tool: Download the dmr-database.py script.

Usage
-----
Command Line Options:

- Download Latest Data (-d)
Downloads the latest user data in CSV format from a specified URL.

- Clean Up Files (-c)
Removes all downloaded files (user.csv, userat.csv, etc.) and metadata (count.txt).

- Process Data (-userat, -userhd, etc.)
Converts user.csv into specific formats for different DMR radio models/systems.

- Single-Command Operation (-a)
Cleans up, downloads the latest data and processes it into all supported formats.

- Help (-h)
Displays a detailed help menu with command descriptions and examples.

Examples:

- Download and Process for Anytone Mobile Radio
./dmr-database.py -d -userat

- Clean Up All Files
./dmr-database.py -c

- Clean, Download and Process for All Formats
./dmr-database.py -a

Notes
-----
- Ensure Python 3 and required modules are installed and accessible.
- Output files (userat.csv, userhd.csv, etc.) are generated based on processed data from user.csv.
- Use -h option for detailed command help and usage examples.
