from PIL import Image
import pillow_heif
import os
import sys

print('Starting convert_to_pdf.py ...', sys.argv)

if (len(sys.argv) < 3):
    print()    
    raise Exception('Need at least three arguments.\nExample: `python convert_to_png.py exceptions/path1 output/path2`')
else:
    # Register HEIF/HEIC support for Pillow
    pillow_heif.register_heif_opener()
    img_path =  os.path.abspath(sys.argv[1])
    destination_path =  os.path.abspath(sys.argv[2])

    def convert_heic_images_in_folder(folder_path, output_format="png"):
        output_format = output_format.lower()
        valid_formats = ["png", "pdf"]
        if output_format not in valid_formats:
            raise ValueError(f"Output format must be one of: {valid_formats}")

        converted = []

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".heic"):
                heic_path = os.path.join(folder_path, filename)
                base_name = os.path.splitext(filename)[0]
                output_filename = f"{base_name}.{output_format}"
                output_path = os.path.join(destination_path, output_filename)

                try:
                    image = Image.open(heic_path)
                    if output_format == "pdf":
                        image = image.convert("RGB")
                    image.save(output_path, format=output_format.upper())
                    print(f"✅ Converted: {filename} -> {output_filename}")
                    converted.append(output_filename)
                except Exception as e:
                    print(f"❌ Failed to convert {filename}: {e}")

        return converted

    convert_heic_images_in_folder(img_path)

