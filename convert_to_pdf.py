
# Python3 program to convert image to pdf
# using img2pdf library
 
# importing necessary libraries
import img2pdf
from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import re
import sys

print('Starting convert_to_pdf.py ...', sys.argv)

if (len(sys.argv) < 3):
    print()    
    raise Exception('Need at least three arguments.\nExample: `python convert_to_pdf.py assets/path1 output/path2`')
else:
    # storing image path
    img_path = os.path.abspath(sys.argv[1])
    # getting file names
    onlyfiles = [f for f in listdir(img_path) if isfile(join(img_path, f))]
    # # storing pdf path
    pdf_path = os.path.abspath(sys.argv[2])

    pdf_name = r""
    limit = 10
    for index, file in enumerate(onlyfiles):
        if index <= limit:
            pdf_name = file.rstrip('.jpeg').rstrip('.jpg').rstrip('.png')
            prev_pdf_name =  onlyfiles[index-1].rstrip('.jpeg').rstrip('.jpg').rstrip('.png')
            print(index)
            # # opening image
            image = Image.open(f"{img_path}\\{file}")
            # Specify the directory name
            pdf_name_split = re.split('-+|__', pdf_name)
            prev_pdf_name_split = re.split('-+|__', prev_pdf_name)

            first_word_current =  f"{pdf_name_split[0]}-{pdf_name_split[1]}"
            first_word_prev =  f"{prev_pdf_name_split[0]}-{prev_pdf_name_split[1]}"
            directory_name = f"{pdf_name_split[0]}-{pdf_name_split[1]}"
            if first_word_current != first_word_prev or index < 1:
                print("New Directory!!")            
                print(first_word_current, first_word_prev)
                        # Create the directory
                try:
                    os.mkdir(f"{pdf_path}\\{directory_name}")
                    print(f"Directory '{directory_name}' created successfully.")
                except FileExistsError:
                    print(f"Directory '{directory_name}' already exists.")
                except PermissionError:
                    print(f"Permission denied: Unable to create '{directory_name}'.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            pdf_file_path = f"{pdf_path}\\{directory_name}\\{pdf_name}.pdf"
            # converting into chunks using img2pdf
            pdf_bytes = img2pdf.convert(image.filename, rotation=img2pdf.Rotation.ifvalid)
                # # opening or creating pdf file
            file = open(pdf_file_path, "wb")
                #  
                # # writing pdf files with chunks
            file.write(pdf_bytes)
                #  
                # # closing image file
            image.close()
                #  
                # # closing pdf file
            file.close()
            # # output
            print("Successfully made pdf file", directory_name + pdf_name)
    