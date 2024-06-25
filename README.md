# DMR Database Tool

## Description

The DMR Database Tool is a versatile Python script developed to streamline the management and processing of Digital Mobile Radio (DMR) user databases. Built with efficiency and usability in mind, this tool offers functionalities such as downloading the latest user data from a specified URL, transforming it into various formats compatible with different DMR radios and systems, and ensuring easy cleanup of downloaded files when necessary. Whether you're a radio enthusiast, system administrator, or developer working with DMR technology, this tool simplifies the process of accessing and utilizing user data, enhancing your workflow with its straightforward command-line interface and robust functionality.

## Features

The DMR Database Tool is designed to provide comprehensive functionality for managing Digital Mobile Radio (DMR) user databases efficiently. Key features include:

Download Capability: Fetches the latest user data in CSV format from a specified URL, ensuring you always have access to up-to-date information.

Versatile Processing Options: Converts the downloaded CSV file into formats suitable for various DMR radio models and systems:

- -userat: Formats data for Anytone Mobile Radio databases.
- -userhd: Prepares data for Ailunce HD1 databases.
- -usermd2017: Converts data for Tytera MD2017 databases.
- -userbin: Generates data files for Tytera MD380/390 radios.
- -usrbin: Formats data for Pi-Star SSH Helper databases.
- -pistar: Converts data for Pi-Star systems.

Comprehensive Cleaning Options: Allows for the removal of all downloaded files and associated metadata (count.txt), ensuring a clean workspace when needed (-c option).

Convenient Help Functionality: Provides a clear and concise help menu (-h option) detailing all available commands and their usage.

## **Additional Options**:
In addition to its core functionalities, the DMR Database Tool offers optional features that enhance its utility and flexibility:

- Download Functionality: The -d option allows users to download the latest DMR user data in CSV format from a specified URL. This ensures that users can easily update their databases with the most current information available.
- Automatic Cleanup: With the -c option, users can automatically clean up all downloaded files (user.csv, userat.csv, etc.) and the metadata file (count.txt). This feature ensures a clutter-free workspace and simplifies maintenance tasks.
- Single-Command Operations: The -a option combines cleaning, downloading the latest user data, and processing it into all specified formats in one single command. This streamlined workflow saves time and effort for users needing to update and distribute DMR user databases across multiple platforms.

Detailed Help Menu: The -h option provides access to a detailed help menu, guiding users through all available commands, their descriptions, and usage examples. This feature ensures that users can quickly familiarize themselves with the tool's capabilities and leverage its full potential effectively.

## Required Python Modules

The DMR Database Tool leverages several Python modules to provide its functionality:

- requests: Essential for making HTTP requests to download the latest DMR user data from a specified URL.
- csv: Provides robust support for reading and writing CSV files, enabling the tool to process user data in a structured format.
- os: Facilitates interaction with the operating system, allowing the tool to manage files and directories, check file existence, and perform cleanup operations.
- sys: Enables access to system-specific parameters and functions, used in the tool for displaying progress bars and handling command-line arguments.
- shutil: Offers high-level file operations, including file copying, which the tool utilizes to duplicate downloaded user data into different formats.
- hashlib: Provides secure hash and digest algorithms, used in the tool to compute MD5 checksums of downloaded files for integrity verification.

## Usage

The DMR Database Tool provides a command-line interface (CLI) with various options to manage and process Digital Mobile Radio (DMR) user databases. Below are the available options and their usage:

- Clean Option (-c):
- - Cleans up all downloaded files (user.csv, userat.csv, etc.) and the metadata file (count.txt).
- - Usage: ./dmr-database.py -c

- Download Option (-d):
- - Downloads the latest user data in CSV format from a specified URL.
- - Usage: ./dmr-database.py -d

- Make all Option (-a):
- - Combines cleaning, downloading the latest user data, and processing it into all formats in one command.
- - Usage: ./dmr-database.py -a

- Help Option (-h):
- - Displays a detailed help menu with descriptions of all available commands and their usage.
- - Usage: ./dmr-database.py -h

## Process Options:
Converts the downloaded user.csv file into various formats suitable for different DMR radio models and systems:
- -userat: For Anytone Mobile Radio databases.
- -userhd: For Ailunce HD1 databases.
- -usermd2017: For Tytera MD2017 databases.
- -userbin: For Tytera MD380/390 radios.
- -usrbin: For Pi-Star SSH Helper databases.
- -pistar: For Pi-Star systems.

Usage: ./dmr-database.py -userat, ./dmr-database.py -userhd, etc.

## Notes:

Ensure Python 3 and the required modules (requests, csv, os, sys, shutil, hashlib) are installed and accessible.
The tool generates output files (userat.csv, userhd.csv, etc.) based on the processed data from user.csv.
This usage guide provides a comprehensive overview of how to utilize the DMR Database Tool's functionalities effectively, catering to radio enthusiasts, system administrators, and developers working with DMR technology.

## Author
PD2EMC aka Einstein with help of ChatGPT
