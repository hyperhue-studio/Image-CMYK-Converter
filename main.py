import os
from PIL import Image, ImageCms, ImageFile
import tkinter as tk
from tkinter import filedialog, simpledialog
import platform

# Increase pixel limit to avoid "DecompressionBombWarning."
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

# Paths for color profiles
PROFILE_RGB = os.path.join(os.path.dirname(__file__), "sRGB_IEC61966-2-1_black_scaled.icc")
PROFILE_CMYK = os.path.join(os.path.dirname(__file__), "USWebCoatedSWOP.icc")

def convert_image_to_cmyk(img_path, output_path, dpi):
    with Image.open(img_path) as img:
        # Convert any input format to CMYK and save as JPG
        if img.mode != 'CMYK':
            img_cmyk = ImageCms.profileToProfile(img, PROFILE_RGB, PROFILE_CMYK, outputMode="CMYK")
        else:
            img_cmyk = img

        # Always save as JPG with the specified DPI
        output_path_jpg = os.path.splitext(output_path)[0] + ".jpg"
        img_cmyk.save(output_path_jpg, "JPEG", dpi=(dpi, dpi))
        print(f"Converted and saved as: {output_path_jpg}")

def process_files(file_paths, output_folder, dpi):
    os.makedirs(output_folder, exist_ok=True)

    for file_path in file_paths:
        try:
            filename = os.path.basename(file_path)
            output_file_path = os.path.join(output_folder, filename)

            convert_image_to_cmyk(file_path, output_file_path, dpi)

        except Exception as e:
            print(f"Error converting {filename}: {e}")

def select_files_and_convert():
    # Initialize the tkinter window
    root = tk.Tk()
    root.withdraw()

    # Prompt the user to enter the DPI
    dpi = simpledialog.askinteger("DPI", "Enter the DPI for CMYK images:", minvalue=1, maxvalue=3000)

    if dpi is None:
        print("DPI not provided. Closing the program.")
        return

    # Show the dialog window to select files
    file_paths = filedialog.askopenfilenames(
        title="Select image files",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.tiff;*.tif")]
    )

    if not file_paths:
        print("No files selected.")
        return

    # Generate the output folder
    output_folder = os.path.join(os.path.dirname(file_paths[0]), f"CMYK_converted_{int(dpi)}dpi")

    process_files(file_paths, output_folder, dpi)

    print("Conversion completed.")
    input("Press Enter to close the program...")

# MacOS-specific adjustments
if platform.system() == 'Darwin':
    import subprocess
    def open_file_dialog_mac():
        process = subprocess.Popen(
            ['osascript', '-e', 'tell app "System Events" to choose file of type {"public.image"} with multiple selections allowed'],
            stdout=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        file_paths = stdout.decode('utf-8').strip().split(', ')
        return file_paths

    filedialog.askopenfilenames = open_file_dialog_mac

# Run the program
select_files_and_convert()
