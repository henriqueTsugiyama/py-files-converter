#File converter using Python modules


##Setup the environment

```python3 -m venv img_to_pdf

##Activate the environment Windows
```Scripts\activate
Or
```img_to_pdf\Scripts\activate

##Install modules
```pip install -r requirements.txt

##Place your input files in /assets
###*NOTE: the scripts work for .png, .jpeg, .jpg files only

##In case you might want to handle specific exceptions, place them in /exceptions

##To convert images to pdf
```python convert_to_pdf.py

##To convert .heic to png
```python convert_to_png.py

##To zip files to a output
```python zip_files.py assets/path1 output/path2