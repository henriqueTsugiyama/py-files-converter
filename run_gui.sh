#!/bin/bash
# macOS/Linux launcher script for File Converter GUI
# Make executable with: chmod +x run_gui.sh
# Then run with: ./run_gui.sh

echo "Starting File Converter GUI..."
python3 file_converter_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Could not start the application."
    echo "Please make sure Python 3 is installed and requirements are installed."
    echo "Run: pip3 install -r requirements.txt"
    echo ""
    echo "On Linux, you may also need: sudo apt-get install python3-tk"
    read -p "Press enter to continue..."
fi
