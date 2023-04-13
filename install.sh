#!/bin/bash

# Check if Git is installed
if command -v git >/dev/null 2>&1 ; then
  echo "Git is already installed"
else
  # Install Git
  sudo apt-get update
  sudo apt-get install git
fi

# Set variables
username="botbot2024"
password="97xl997&"

# Clone repository using HTTPS protocol
git clone https://$username:$password@github.com/DavitNoreyan/adj_bot.git
cd adj_bot

if ! command -v python3.10 &> /dev/null
then
    echo "Python 3.10 is not installed. Please install Python 3.10."
    exit 1
fi

if ! command -v pip &> /dev/null
then
    # Install pip
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

echo "Python 3.10 is installed on your system."
if ! python3 -m venv &> /dev/null
then
    echo "venv is not installed. Installing venv..."
    sudo apt-get update
    sudo apt-get install -y python3-venv
    echo "venv has been installed."
fi

echo "venv is installed on your system."

python3.10 -m venv env

source env/bin/activate

if ! command -v pip &> /dev/null
then
    echo "pip is not installed. Please install pip."
    exit 1
fi

pip install -r requirements.txt

sudo chmod +x run.sh

sudo chmod +x update.sh

echo "Packages installed successfully."