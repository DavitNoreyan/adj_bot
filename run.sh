#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3."
    exit 1
fi

if [ ! -d "env" ]
then
    echo "Virtual environment not found. Please run the create_env.sh script."
    exit 1
fi

source env/bin/activate

if ! command -v python &> /dev/null
then
    echo "Python is not installed in the virtual environment. Please install it."
    exit 1
fi

python ui_part.py

deactivate

echo "UI part has been executed successfully."
