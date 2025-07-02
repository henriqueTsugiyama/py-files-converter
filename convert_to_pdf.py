
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
from random import randint

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
                pdf_name = file.rstrip('.jpeg').rstrip('.jpg').rstrip('.png')
                prev_pdf_name =  onlyfiles[index-1].rstrip('.jpeg').rstrip('.jpg').rstrip('.png')
                print(index)
                ## Construct the full path to the input image file and get size
                current_image_full_path = os.path.join(img_path, file)
                image_size_bytes = os.path.getsize(current_image_full_path)
                within_size_limit = size_acc < size_limit
                if within_size_limit:
                    size_acc += format_size(image_size_bytes)
                    print("Size so far:", size_acc)
                else:
                    size_acc = 0
                    print('Reached Size limit!', size_acc)

                # # opening image
                image = Image.open(f"{img_path}\\{file}")
                # Specify the directory name
                pdf_name_split = re.split('-+|__', pdf_name)
                prev_pdf_name_split = re.split('-+|__', prev_pdf_name)

                first_word_current =  f"{pdf_name_split[0]}-{pdf_name_split[1]}"
                first_word_prev =  f"{prev_pdf_name_split[0]}-{prev_pdf_name_split[1]}"
                directory_name = f"{pdf_name_split[0]}-{pdf_name_split[1]}"

                if first_word_current != first_word_prev or index < 1 or not within_size_limit:
                    print("New Directory!!")            
                    print(first_word_current, first_word_prev)
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

                pdf_file_path = os.path.join(file_path_to_save, f"{pdf_name}.pdf")
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
                print("Successfully made pdf file", file_path_to_save)
        