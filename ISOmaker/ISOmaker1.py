import os
from pycdlib import PyCdlib
from tqdm import tqdm  # Add this import

def count_files(folder_path):
    count = 0
    for root, dirs, files in os.walk(folder_path):
        count += len(files)
    return count

def add_folder_to_iso(iso, folder_path, iso_path='/', root_dir=None, pbar=None):
    if iso_path != '/' and iso_path != root_dir:
        iso.add_directory(iso_path.upper())
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        iso_item_path = os.path.join(iso_path, item).replace('\\', '/')
        if os.path.isdir(item_path):
            add_folder_to_iso(iso, item_path, iso_item_path, root_dir, pbar)
        else:
            iso.add_file(item_path, iso_item_path.upper() + ';1')
            if pbar:
                pbar.update(1)

def folder_to_iso(source_folder, output_iso):
    iso = PyCdlib()
    iso.new(interchange_level=4)
    folder_name = os.path.basename(os.path.normpath(source_folder))
    iso_root = f'/{folder_name.upper()}'
    iso.add_directory(iso_root)
    total_files = count_files(source_folder)
    print(f"Total files to add: {total_files}")
    with tqdm(total=total_files, desc="Building ISO", unit="file") as pbar:
        add_folder_to_iso(iso, source_folder, iso_root, root_dir=iso_root, pbar=pbar)
    iso.write(output_iso)
    iso.close()
    print(f"ISO image '{output_iso}' created successfully.")

if __name__ == '__main__':
    folder_path = input("Input path to folder: ").strip()
    output_iso = input("Output .iso name: ").strip()
    if not output_iso.lower().endswith('.iso'):
        output_iso += '.iso'
    folder_to_iso(folder_path, output_iso)
