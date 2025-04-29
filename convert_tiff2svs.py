import os
import shutil

# Define source and destination directories
src_dir = "path/to/quadrants_svs"        
dst_dir = "path/to/quadrants_tiff2svs"    

# Create the destination directory if it doesn't exist
os.makedirs(dst_dir, exist_ok=True)

# Iterate over all files in the source directory
for filename in os.listdir(src_dir):
    if filename.lower().endswith(".tiff"):
        src_path = os.path.join(src_dir, filename)
        new_filename = os.path.splitext(filename)[0] + ".svs"
        dst_path = os.path.join(dst_dir, new_filename)
        shutil.copy2(src_path, dst_path)

print("Conversion completed.")
