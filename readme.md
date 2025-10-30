# File Converter Using Python Modules

This project provides both a **user-friendly GUI desktop application** and Python command-line scripts to convert image files into PDF, handle `.heic` images, and zip files.

## 🖥️ GUI Desktop Application (Recommended for Non-Technical Users)

The GUI application provides an easy-to-use interface for file conversion without needing to use the command line.

### Quick Start - Running the GUI

1. **Install Python** (if not already installed)
   - Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"

2. **Download or Clone this project**
   ```bash
   git clone https://github.com/henriqueTsugiyama/py-files-converter.git
   cd py-files-converter
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the GUI application**
   
   **Easy way (double-click):**
   - **Windows**: Double-click `run_gui.bat`
   - **macOS/Linux**: Double-click `run_gui.sh` (or run `./run_gui.sh` in terminal)
   
   **Manual way:**
   ```bash
   python file_converter_gui.py
   ```
   Or on some systems:
   ```bash
   python3 file_converter_gui.py
   ```

### Using the GUI Application

1. **Select Input Folder**: Click "Browse..." next to Input Folder and select the folder containing your files
2. **Select Output Folder**: Click "Browse..." next to Output Folder and select where you want the results saved
3. **Choose Operation**: Click one of the three buttons:
   - **Convert Images to PDF**: Converts .png, .jpeg, .jpg images to PDF files
   - **Convert HEIC to PNG**: Converts Apple HEIC format images to PNG
   - **Zip Files**: Compresses files from subdirectories into ZIP archives
4. **Monitor Progress**: Watch the progress window for status updates and results

### Creating a Standalone Executable (Optional)

To create an executable file that can run without installing Python:

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Create the executable**
   
   **For Windows:**
   ```bash
   pyinstaller --onefile --windowed --name="FileConverter" file_converter_gui.py
   ```
   
   **For macOS:**
   ```bash
   pyinstaller --onefile --windowed --name="FileConverter" file_converter_gui.py
   ```
   
   **For Linux:**
   ```bash
   pyinstaller --onefile --name="FileConverter" file_converter_gui.py
   ```

3. **Find your executable**
   - The executable will be in the `dist` folder
   - **Windows**: `dist/FileConverter.exe`
   - **macOS**: `dist/FileConverter.app` (double-click to run)
   - **Linux**: `dist/FileConverter` (may need to set executable permission: `chmod +x dist/FileConverter`)

4. **Distribute the executable**
   - You can share just the executable file with others
   - They don't need to install Python or any dependencies
   - Note: The executable is platform-specific (Windows .exe only runs on Windows, etc.)

## 📟 Command-Line Scripts (For Advanced Users)

The original command-line scripts are still available for automation and scripting purposes.

### Setup the Environment

```bash
python3 -m venv img_to_pdf
```

### Activate the environment

**Windows:**
```bash
Scripts\activate
```
Or
```bash
img_to_pdf\Scripts\activate
```

**macOS/Linux:**
```bash
source img_to_pdf/bin/activate
```

### Install modules
```bash
pip install -r requirements.txt
```

### Place your input files in /assets
**NOTE: the scripts work for __.png__, __.jpeg__, __.jpg__ files only**

In case you might want to handle specific exceptions, place them in **/exceptions**

### To convert images to pdf
```bash
python convert_to_pdf.py assets/path1 output/path2
```

### To convert .heic to png
```bash
python convert_to_png.py assets/path1 output/path2
```

### To zip files
```bash
python zip_files.py assets/path1 output/path2
```

## 🔧 Troubleshooting

### GUI doesn't open
- Make sure you have Python 3.8 or higher installed
- On Linux, you may need to install tkinter: `sudo apt-get install python3-tk`
- Try running from the command line to see any error messages

### "Module not found" errors
- Make sure you ran `pip install -r requirements.txt`
- Try using `pip3` instead of `pip` if on macOS/Linux

### Executable doesn't work
- Executables are platform-specific - Windows .exe won't run on Mac/Linux
- Some antivirus software may flag PyInstaller executables as suspicious (false positive)
- Try running the Python script directly if the executable has issues
