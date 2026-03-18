import os
from processor import process_all_pdfs
from config import I_ROOT_DIRECTORY

if __name__ == "__main__":
    
    ROOT_DIRECTORY = I_ROOT_DIRECTORY
    
    if not os.path.isdir(ROOT_DIRECTORY):
        print(f"ERROR: The specified PDF input path '{ROOT_DIRECTORY}' is invalid. Please modify the I_ROOT_DIRECTORY variable in config.py.")
    else:
        # Start the main processing function
        process_all_pdfs(ROOT_DIRECTORY)