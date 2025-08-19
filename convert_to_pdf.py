
# Python3 program to convert image to pdf
# using img2pdf library
# importing necessary libraries
import img2pdf
from PIL import Image, PdfParser
import os
from os import listdir
from os.path import isfile, join
import re
import sys
from random import randint

def set_file_name(file_name):
    f_name = ''
    limit = 2

    if len(file_name) > 10:
        limit = 4


    for i, w in enumerate(file_name):
        if i > limit:
            break
        if i == 0:
            f_name = w
        else:
            f_name += f"-{w}"
    
    return f_name

def format_size(size_bytes):
    size = size_bytes / (1024 * 1024)
    print(f"{size:.2f} MB")

    return round(size, 2)

print('Starting convert_to_pdf.py ...', sys.argv)

if (len(sys.argv) < 3):
    print()    
    raise Exception('Need at least three arguments.\nExample: `python convert_to_pdf.py assets/path1 output/path2`')
else:
    # storing image path
    img_path = os.path.abspath(sys.argv[1])
    # getting file names
    # # storing pdf path
    pdf_path = os.path.abspath(sys.argv[2])
    pdf_name = r""

    limit = 10000000
    size_limit = 10.00
    size_acc = 0
    onlyfiles = [f for f in listdir(img_path) if isfile(join(img_path, f))]

    if not onlyfiles:
        print(f"No files found in {img_path}")
    else: 
        for index, file in enumerate(onlyfiles):
            if index <= limit:
                not_pdf = file.find(".pdf") == -1
                pdf_name = file.rstrip('.jpeg').rstrip('.jpg').rstrip('.png')
                prev_pdf_name = onlyfiles[index-1].rstrip('.jpeg').rstrip('.jpg').rstrip('.png')

                ## Construct the full path to the input image file and get size
                current_file_full_path = os.path.join(img_path, file)
                bytes_size = os.path.getsize(current_file_full_path)
                within_size_limit = size_acc < size_limit

                if within_size_limit:
                    size_acc += format_size(bytes_size)
                    print("Size so far:", size_acc)
                else:
                    size_acc = 0
                    print('Reached Size limit!', size_acc)

                # Specify the directory name
                pdf_name_split = re.split('-+|__', pdf_name)
                prev_pdf_name_split = re.split('-+|__', prev_pdf_name)
     
                # Need to differentiate store name  
                current_store_name = set_file_name(pdf_name_split)
                previous_store_name = set_file_name(prev_pdf_name_split)
                # Naming directories
                directory_name = current_store_name

                if current_store_name != previous_store_name or index < 1 or not within_size_limit:
                    print("New Directory!!")            
                    print(pdf_name, prev_pdf_name)
                    # Create the directory
                    try:
                        if not within_size_limit:
                            # reset folder size count
                            size_acc = 0
                            
                            file_path_to_save = os.path.join(pdf_path, f"{directory_name}-{randint(100,500)}")
                        else:
                            file_path_to_save = os.path.join(pdf_path, directory_name)

                        os.mkdir(file_path_to_save)
                        print(f"Directory '{directory_name}' created successfully.")
                    except FileExistsError:
                        print(f"Directory '{directory_name}' already exists.")
                    except PermissionError:
                        print(f"Permission denied: Unable to create '{directory_name}'.")
                    except Exception as e:
                        print(f"An error occurred: {e}")


                if not_pdf:
                    # # opening image
                    image = Image.open(f"{img_path}\\{file}")
                    pdf_output_file_path = os.path.join(file_path_to_save, f"{pdf_name}.pdf")
                    # converting into chunks using img2pdf
                    pdf_bytes = img2pdf.convert(image.filename, rotation=img2pdf.Rotation.ifvalid)
                    ## closing image file
                    image.close()
                else:
                    # # opening or creating pdf file
                    pdf_output_file_path = os.path.join(file_path_to_save, pdf_name)
                    file_reader = open(current_file_full_path, "rb")
                    pdf_bytes = file_reader.read()
                    file_reader.close()


                # # writing pdf files with chunks
                file_writer = open(pdf_output_file_path, "wb")
                file_writer.write(pdf_bytes)

                ## closing pdf file
                file_writer.close()
                # # output
                print("Successfully made pdf file", file_path_to_save)

        