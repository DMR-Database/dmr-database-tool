# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy needed files from github into the container at /usr/src/app
ADD https://raw.githubusercontent.com/DMR-Database/dmr-database-tool/main/dmr-database.py /usr/src/app 
ADD https://raw.githubusercontent.com/DMR-Database/dmr-database-tool/main/citys_nl.csv /usr/src/app
ADD https://raw.githubusercontent.com/DMR-Database/dmr-database-tool/main/user_ext.csv /usr/src/app
ADD https://raw.githubusercontent.com/DMR-Database/dmr-database-tool/main/Docker/run_script.py /usr/src/app

# Update pip and install needed librarys
RUN pip install --upgrade pip
RUN pip install requests

# Command to run the script
CMD ["python", "./run_script.py"]

