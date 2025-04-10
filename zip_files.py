import zipfile
import os
import sys

print('Starting ZipToFile ...', sys.argv)
if (len(sys.argv) < 3):
    print()    
    raise Exception('Need at least three arguments.\nExample: `python zip_files.py path1 path2`')
else:
    def zip_folder(folder_path, out_path):
        zip_path = ''
        for root, dirs, files in os.walk(folder_path):
            if root == folder_path:
                continue
            # where the files will be zipped to
            dir_name = root.split("\\")
            zip_filename = dir_name[-1] + '.zip'
            zip_path = os.path.join(out_path, zip_filename)
            print('DIR NAME =>',zip_filename)
            print('ZIP PATH =>', zip_path)
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    if file == zip_filename:
                        continue
                    file_path = os.path.join(root, file)
                    # arcname = os.path.relpath(file_path, folder_path)
                    # print(f'ARCHIVE NAME =>{arcname}')
                    zipf.write(file_path, file)


            print(f"Zipped all files in ✅ '{folder_path}' to ✅'{zip_path}'")
            print('')
        return zip_path
    # assets/samsclub-march-pdfs
    # assets/zip-samsclub-march
    path_to_read = sys.argv[1]
    path_to_output = sys.argv[2]

    read_path = os.path.abspath(path_to_read)
    output_path =  os.path.abspath(path_to_output)
    print('Argument 1 =>', path_to_read)
    print('Argument 2 =>', path_to_output)
    print('Reading arguments to paths ...')

    zips = zip_folder(read_path, output_path)

    print('Path 1 =>', read_path)
    print('Path 2 =>', output_path)
