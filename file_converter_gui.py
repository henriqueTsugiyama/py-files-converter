"""
File Converter GUI Application

A user-friendly desktop application for converting images to PDF,
converting HEIC to PNG, and zipping files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import threading
import zipfile
from PIL import Image
import pillow_heif
import img2pdf
import re
from random import randint


class FileConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Converter - Easy File Processing")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Register HEIF/HEIC support for Pillow
        pillow_heif.register_heif_opener()
        
        # Variables for paths
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="File Converter", 
            font=("Arial", 20, "bold"),
            pady=10
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            self.root,
            text="Convert images to PDF, HEIC to PNG, or zip your files",
            font=("Arial", 10),
            fg="gray"
        )
        subtitle_label.pack()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input Path Section
        input_frame = ttk.LabelFrame(main_frame, text="Input Folder", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Browse...", command=self.browse_input).pack(side=tk.LEFT)
        
        # Output Path Section
        output_frame = ttk.LabelFrame(main_frame, text="Output Folder", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Entry(output_frame, textvariable=self.output_path, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output).pack(side=tk.LEFT)
        
        # Operations Section
        operations_frame = ttk.LabelFrame(main_frame, text="Select Operation", padding="10")
        operations_frame.pack(fill=tk.X, pady=5)
        
        # Create buttons for each operation
        btn_frame = ttk.Frame(operations_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(
            btn_frame, 
            text="Convert Images to PDF", 
            command=self.convert_to_pdf,
            width=25
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            btn_frame,
            text="Convert HEIC to PNG",
            command=self.convert_to_png,
            width=25
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        ttk.Button(
            btn_frame,
            text="Zip Files",
            command=self.zip_files,
            width=25
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.progress_text = scrolledtext.ScrolledText(
            progress_frame,
            height=15,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.progress_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
    def browse_input(self):
        """Open dialog to select input folder"""
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_path.set(folder)
            self.log(f"Input folder selected: {folder}")
    
    def browse_output(self):
        """Open dialog to select output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_path.set(folder)
            self.log(f"Output folder selected: {folder}")
    
    def log(self, message):
        """Add message to progress text area"""
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def set_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def validate_paths(self):
        """Validate that input and output paths are selected"""
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input folder")
            return False
        if not self.output_path.get():
            messagebox.showerror("Error", "Please select an output folder")
            return False
        if not os.path.exists(self.input_path.get()):
            messagebox.showerror("Error", "Input folder does not exist")
            return False
        if not os.path.exists(self.output_path.get()):
            messagebox.showerror("Error", "Output folder does not exist")
            return False
        return True
    
    def convert_to_pdf(self):
        """Convert images to PDF"""
        if not self.validate_paths():
            return
        
        self.set_status("Converting images to PDF...")
        self.log("=" * 50)
        self.log("Starting image to PDF conversion...")
        
        # Run in separate thread to prevent UI freezing
        thread = threading.Thread(target=self._convert_to_pdf_worker)
        thread.daemon = True
        thread.start()
    
    def _convert_to_pdf_worker(self):
        """Worker thread for PDF conversion"""
        try:
            img_path = self.input_path.get()
            pdf_path = self.output_path.get()
            
            # Get list of image files
            onlyfiles = [f for f in os.listdir(img_path) if os.path.isfile(os.path.join(img_path, f))]
            
            if not onlyfiles:
                self.log(f"No files found in {img_path}")
                self.set_status("No files found")
                return
            
            # Helper function to set file name
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
                return round(size, 2)
            
            limit = 10000000
            size_limit = 10.00
            size_acc = 0
            file_path_to_save = None
            
            for index, file in enumerate(onlyfiles):
                if index <= limit:
                    not_pdf = file.find(".pdf") == -1
                    pdf_name = file.rstrip('.jpeg').rstrip('.jpg').rstrip('.png')
                    prev_pdf_name = onlyfiles[index-1].rstrip('.jpeg').rstrip('.jpg').rstrip('.png') if index > 0 else ""
                    
                    # Construct the full path to the input image file and get size
                    current_file_full_path = os.path.join(img_path, file)
                    bytes_size = os.path.getsize(current_file_full_path)
                    within_size_limit = size_acc < size_limit
                    
                    if within_size_limit:
                        size_acc += format_size(bytes_size)
                        self.log(f"Size so far: {size_acc} MB")
                    else:
                        size_acc = 0
                        self.log('Reached size limit! Resetting...')
                    
                    # Split name and get store name
                    pdf_name_split = re.split('-+|__', pdf_name)
                    prev_pdf_name_split = re.split('-+|__', prev_pdf_name) if prev_pdf_name else []
                    
                    current_store_name = set_file_name(pdf_name_split)
                    previous_store_name = set_file_name(prev_pdf_name_split) if prev_pdf_name_split else ""
                    directory_name = current_store_name
                    
                    if current_store_name != previous_store_name or index < 1 or not within_size_limit:
                        self.log(f"Creating new directory for: {directory_name}")
                        
                        try:
                            if not within_size_limit:
                                size_acc = 0
                                file_path_to_save = os.path.join(pdf_path, f"{directory_name}-{randint(100,500)}")
                            else:
                                file_path_to_save = os.path.join(pdf_path, directory_name)
                            
                            os.makedirs(file_path_to_save, exist_ok=True)
                            self.log(f"Directory '{directory_name}' created successfully.")
                        except Exception as e:
                            self.log(f"Error creating directory: {e}")
                    
                    if not_pdf:
                        # Opening image
                        image = Image.open(current_file_full_path)
                        pdf_output_file_path = os.path.join(file_path_to_save, f"{pdf_name}.pdf")
                        # Converting using img2pdf
                        pdf_bytes = img2pdf.convert(image.filename, rotation=img2pdf.Rotation.ifvalid)
                        image.close()
                    else:
                        # Copying PDF file
                        pdf_output_file_path = os.path.join(file_path_to_save, pdf_name)
                        with open(current_file_full_path, "rb") as file_reader:
                            pdf_bytes = file_reader.read()
                    
                    # Writing PDF file
                    with open(pdf_output_file_path, "wb") as file_writer:
                        file_writer.write(pdf_bytes)
                    
                    self.log(f"✅ Successfully converted: {file}")
            
            self.log("=" * 50)
            self.log("✅ PDF conversion completed successfully!")
            self.set_status("PDF conversion completed")
            messagebox.showinfo("Success", "Images converted to PDF successfully!")
            
        except Exception as e:
            error_msg = f"Error during PDF conversion: {str(e)}"
            self.log(f"❌ {error_msg}")
            self.set_status("Error occurred")
            messagebox.showerror("Error", error_msg)
    
    def convert_to_png(self):
        """Convert HEIC images to PNG"""
        if not self.validate_paths():
            return
        
        self.set_status("Converting HEIC to PNG...")
        self.log("=" * 50)
        self.log("Starting HEIC to PNG conversion...")
        
        # Run in separate thread
        thread = threading.Thread(target=self._convert_to_png_worker)
        thread.daemon = True
        thread.start()
    
    def _convert_to_png_worker(self):
        """Worker thread for PNG conversion"""
        try:
            folder_path = self.input_path.get()
            destination_path = self.output_path.get()
            output_format = "png"
            
            converted = []
            
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(".heic") or filename.lower().endswith(".pdf"):
                    heic_path = os.path.join(folder_path, filename)
                    base_name = os.path.splitext(filename)[0]
                    output_filename = f"{base_name}.{output_format}"
                    output_path = os.path.join(destination_path, output_filename)
                    
                    try:
                        image = Image.open(heic_path)
                        if output_format == "pdf":
                            image = image.convert("RGB")
                        image.save(output_path, format=output_format.upper())
                        self.log(f"✅ Converted: {filename} -> {output_filename}")
                        converted.append(output_filename)
                    except Exception as e:
                        self.log(f"❌ Failed to convert {filename}: {e}")
            
            self.log("=" * 50)
            if converted:
                self.log(f"✅ Conversion completed! {len(converted)} file(s) converted.")
                self.set_status("HEIC to PNG conversion completed")
                messagebox.showinfo("Success", f"{len(converted)} file(s) converted to PNG successfully!")
            else:
                self.log("No HEIC or PDF files found to convert.")
                self.set_status("No files to convert")
                messagebox.showinfo("Info", "No HEIC or PDF files found to convert.")
                
        except Exception as e:
            error_msg = f"Error during PNG conversion: {str(e)}"
            self.log(f"❌ {error_msg}")
            self.set_status("Error occurred")
            messagebox.showerror("Error", error_msg)
    
    def zip_files(self):
        """Zip files from folders"""
        if not self.validate_paths():
            return
        
        self.set_status("Zipping files...")
        self.log("=" * 50)
        self.log("Starting file compression...")
        
        # Run in separate thread
        thread = threading.Thread(target=self._zip_files_worker)
        thread.daemon = True
        thread.start()
    
    def _zip_files_worker(self):
        """Worker thread for zipping files"""
        try:
            folder_path = self.input_path.get()
            out_path = self.output_path.get()
            
            zip_created = False
            
            for root, dirs, files in os.walk(folder_path):
                if root == folder_path:
                    continue
                
                # Get directory name for zip file
                dir_name = root.split(os.sep)
                zip_filename = dir_name[-1] + '.zip'
                zip_path = os.path.join(out_path, zip_filename)
                
                self.log(f"Creating zip: {zip_filename}")
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file in files:
                        if file == zip_filename:
                            continue
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, file)
                        self.log(f"  Added: {file}")
                
                self.log(f"✅ Zipped all files in '{root}' to '{zip_path}'")
                self.log("")
                zip_created = True
            
            self.log("=" * 50)
            if zip_created:
                self.log("✅ Zipping completed successfully!")
                self.set_status("Zipping completed")
                messagebox.showinfo("Success", "Files zipped successfully!")
            else:
                self.log("No subdirectories found to zip.")
                self.set_status("No subdirectories found")
                messagebox.showinfo("Info", "No subdirectories found to zip. Please ensure your input folder contains subdirectories.")
                
        except Exception as e:
            error_msg = f"Error during zipping: {str(e)}"
            self.log(f"❌ {error_msg}")
            self.set_status("Error occurred")
            messagebox.showerror("Error", error_msg)


def main():
    """Main entry point for the GUI application"""
    root = tk.Tk()
    app = FileConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
