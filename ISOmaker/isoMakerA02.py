import os
from pycdlib import PyCdlib
from tqdm import tqdm

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

def folder_to_iso(source_folder, output_iso, volume_label=None):
    iso = PyCdlib()
    
    if volume_label:
        iso.new(vol_ident=volume_label.upper()[:32], interchange_level=4)
    else:
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
    
    success_message = f"ISO image created successfully at '{os.path.abspath(output_iso)}'"
    if volume_label:
        success_message += f" with label '{volume_label[:32]}'"
    print(success_message + ".")

def ensure_iso_extension(filename):
    if not filename.lower().endswith('.iso'):
        return filename + '.iso'
    return filename

if __name__ == '__main__':
    folder_path = input("Input path to folder: ").strip()
    default_name = os.path.basename(os.path.normpath(folder_path)) + '.iso'
    
    output_choice = input(f"Output ISO name [default: {default_name}]: ").strip()
    iso_name = ensure_iso_extension(output_choice) if output_choice else default_name
    
    save_location = input("Save directory [default: current]: ").strip()
    output_path = os.path.join(save_location, iso_name) if save_location else iso_name
    
    volume_label = input("Enter volume/device label (optional, 32 chars max): ").strip()
    volume_label = volume_label if volume_label else None
    
    folder_to_iso(folder_path, output_path, volume_label)
