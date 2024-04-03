#!/home/genuis/venv/bin/python3

import argparse
import logging
import os
import shutil

def setup_logger():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    return logging.getLogger()

logger = setup_logger()

def get_absolute_path(folder_path):
    """Get the absolute path for a given folder path."""
    return os.path.abspath(os.path.expanduser(folder_path))

def print_with_style(message):
    """Print messages with style using ASCII art and colors."""
    try:
        from pyfiglet import figlet_format
        from termcolor import colored
        logger.info(colored(figlet_format(message, font='slant'), 'cyan'))
    except ImportError:
        logger.info(message)

class FolderManager:
    """Manages folders and files within a specified directory."""

    def __init__(self, folder_path):
        self.folder_path = get_absolute_path(folder_path)

    def create_folder(self, folder_name):
        """Create a folder with the given name."""
        folder_path = os.path.join(self.folder_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print_with_style(f"Created folder: {folder_path}")

    def move_file(self, file_path, destination_folder):
        """Move a file to the specified destination folder."""
        try:
            shutil.move(file_path, destination_folder)
            print_with_style(f"Moved {file_path} to {destination_folder}")
        except Exception as e:
            logger.error(f"Error moving file: {e}")

    def organize_files_by_type(self):
        """Organize files in the directory by their file type."""
        if not os.path.exists(self.folder_path):
            print_with_style("Folder does not exist.")
            return

        file_mapping = {}
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext:
                    if ext not in file_mapping:
                        file_mapping[ext] = []
                    file_mapping[ext].append(os.path.join(root, file))

        for ext, files in file_mapping.items():
            destination_folder = os.path.join(self.folder_path, ext[1:])
            if not os.path.exists(destination_folder):
                self.create_folder(ext[1:])

            for file in files:
                self.move_file(file, destination_folder)

        print_with_style("Files organized by type successfully.")

def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by their type.")
    parser.add_argument("folder_path", type=str, help="Path to the folder to organize")
    args = parser.parse_args()

    folder_manager = FolderManager(args.folder_path)
    folder_manager.organize_files_by_type()

if __name__ == "__main__":
    main()

