# Quick Start Guide - File Converter GUI

## For Users Who Just Want to Use the Application

### Step 1: Install Python (One-Time Setup)
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. **Important**: During installation, check "Add Python to PATH"

### Step 2: Install Dependencies (One-Time Setup)
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to this folder
3. Run: `pip install -r requirements.txt`

### Step 3: Run the Application
**Easy Way:**
- **Windows**: Double-click `run_gui.bat`
- **Mac/Linux**: Double-click `run_gui.sh`

**Manual Way:**
- Open Command Prompt/Terminal in this folder
- Run: `python file_converter_gui.py`

### Step 4: Use the Application
1. Click "Browse..." next to **Input Folder** and select your files
2. Click "Browse..." next to **Output Folder** and select where to save results
3. Click one of the operation buttons:
   - **Convert Images to PDF**: For .png, .jpg, .jpeg files
   - **Convert HEIC to PNG**: For Apple HEIC images
   - **Zip Files**: To compress folders into .zip files
4. Watch the progress window for status updates

## Creating a Standalone Executable (Optional)

If you want to share this with others who don't have Python installed:

1. Install PyInstaller: `pip install pyinstaller`
2. Create executable:
   - **Windows**: `pyinstaller --onefile --windowed --name="FileConverter" file_converter_gui.py`
   - **Mac**: `pyinstaller --onefile --windowed --name="FileConverter" file_converter_gui.py`
   - **Linux**: `pyinstaller --onefile --name="FileConverter" file_converter_gui.py`
3. Find the executable in the `dist` folder
4. Share just that file - no Python installation needed!

## Need Help?

See the full README.md for detailed instructions and troubleshooting.
