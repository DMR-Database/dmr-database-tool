# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
ADD https://raw.githubusercontent.com/DMR-Database/dmr-database-tool/main/dmr-database.py /usr/src/app 
ADD https://raw.githubusercontent.com/DMR-Database/dmr-database-tool/main/citys_nl.csv /usr/src/app
ADD https://raw.githubusercontent.com/DMR-Database/dmr-database-tool/main/user_ext.csv /usr/src/app
COPY run_script.py /usr/src/app

RUN pip install requests

# Command to run the script
CMD ["python", "./run_script.py"]

