# File Converter Using Python Modules

This project provides Python scripts to convert image files into PDF, handle `.heic` images, and zip files.

## Setup the Environment

```bash
python3 -m venv img_to_pdf
```
## Activate the environment Windows
```bash
Scripts\activate
```
Or
```bash
img_to_pdf\Scripts\activate
```

## Install modules
```bash
pip install -r requirements.txt
```

## Place your input files in /assets
**NOTE: the scripts work for __.png__, __.jpeg__, __.jpg__ files only**

## In case you might want to handle specific exceptions, place them in /exceptions

## To convert images to pdf
```bash
python convert_to_pdf.py
```

## To convert .heic to png
```bash
python convert_to_png.py
```

## To zip files to a output
```bash
python zip_files.py assets/path1 output/path2
```