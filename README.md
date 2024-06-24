DMR Database Tool (public release)

This script is designed to download a CSV file from a specified URL, process the data,
and convert it into various formats suitable for different radio databases. It can also
clean up the downloaded files and display the current count of entries in the CSV file.

Features:
- Download the CSV file with a custom progress bar.
- Count entries in the downloaded CSV file and compare with the previous count.
- Process the CSV file into different formats for various radio databases.
- Clean up all downloaded files and count.txt.
- Perform all operations sequentially with a single command.

Options:
- -a : Clean all files, download the CSV file, and process it to all destination formats.
- -d : Download the CSV file.
- -c : Clean all downloaded files and count.txt.
- -h : Display this help message.
- -userat : Process user.csv to userat.csv for Anytone Mobile Radio database.
- -userhd : Process user.csv to userhd.csv for Ailunce HD1 database.
- -usermd2017 : Process user.csv to usermd2017.csv for Tytera MD2017 database.
- -userbin : Process user.csv to user.bin for Tytera MD380/390 database.
- -usrbin : Process user.csv to usr.bin for Pi-Star SSH Helper database.
- -pistar : Process user.csv to DMRIds.dat for Pi-Star database.

Required Python Modules:
- requests: For downloading the CSV file.
- csv: For reading and counting entries in the CSV file.
- os: For file operations like checking if files exist.
- sys: For command-line argument handling and displaying the progress bar.
- shutil: For copying files.

Application Information:
- Name: DMR Database Tool
- Version: v0.1
- Author: PD2EMC aka Einstein with help of ChatGPT
