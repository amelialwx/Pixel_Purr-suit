#!/bin/bash

VENV_DIR="venv"

setPythonCommand() {
    if command -v python3 &>/dev/null; then
        PYTHON_CMD=python3
        echo "Python 3 found: Using python3"
    elif command -v python &>/dev/null && python --version 2>&1 | grep -q "Python 3"; then
        PYTHON_CMD=python
        echo "Python found: Using python"
    else
        echo "Error: Python is not installed."
        exit 1
    fi
}

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    setPythonCommand
    $PYTHON_CMD -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
    setPythonCommand
fi

echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting the application..."
$PYTHON_CMD code/runner.py

if [ $? -ne 0 ]; then
    echo "Failed to start runner.py. Please check the file path and permissions."
fi

deactivate
