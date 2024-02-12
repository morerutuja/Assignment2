# Use the official Jupyter image as a parent image
# Start from the official Ubuntu image
FROM ubuntu:20.04

# Avoid prompts from apt during build
ARG DEBIAN_FRONTEND=noninteractive

# Install Python, pip, and other necessary system packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    wget \
    curl \
    gnupg2 \
    software-properties-common \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    chromium-browser \
    chromium-chromedriver \
    # Additional dependencies for Jupyter and headless Chrome execution
    xvfb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python3 as the default python version
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Jupyter Notebook using pip
RUN python3 -m pip install --no-cache-dir notebook jupyter

# Copy the requirements.txt files into the container
COPY ./Snowflake_Transfer1/requirements.txt /usr/src/app/Snowflake_Transfer1/requirements.txt
COPY ./Webscrape/requirements.txt /usr/src/app/Webscrape/requirements.txt

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/Snowflake_Transfer1/requirements.txt \
    && pip install --no-cache-dir -r /usr/src/app/Webscrape/requirements.txt

# Set the working directory
WORKDIR /usr/src/app

# Copy your application code
COPY ./Snowflake_Transfer1/snowflake_sqlalchemy.ipynb /usr/src/app/Snowflake_Transfer1/
COPY ./Webscrape/Webscrape.ipynb /usr/src/app/Webscrape/
COPY ./Webscrape/extracted.csv /usr/src/app/Webscrape/

# Expose the port Jupyter Notebook runs on
EXPOSE 8888

# Start Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]

