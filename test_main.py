from preferences import UserPreferences 
from edit import ExifTool
import os
import argparse

# CREATED THIS TO JUST TEST EXIFTOOL FUNCTIONS
def main():
    # Take in user preferences (for our simple case we will use the terminal inputs of the user: main.py preferences img_in_file)
    # print image metadata to terminal using ExifTool class function print_metadata
    # give user preferences to preferences class parse metadata for prefereces
    # scrub original image
    # add parsed preferences to caption
    
    img_dr = os.getcwd() + r"\data\input_images\DSCN0010 test.jpg"
    exif_tool_dr= os.getcwd() + r"\ExifTool\exiftool.exe"
    data_dr = os.getcwd() + r"\data"
    # directory to remove txt file
    meta_txt_dr = os.getcwd() + r"\data\input_images\temp.txt"
    # directory to remove csv file
    meta_csv_dr = os.getcwd() + r"\data\meta_data\temp.csv"

    edit = ExifTool(img_dr, exif_tool_dr, data_dr)

    # TODO: these calls should probably be moved into preferences based on what preferences they selected.
    #edit.print_metadata()
    edit.temp_metadata_txt()
    edit.temp_metadata_csv()
    edit.metadata_caption()

    # Should delete all data except user preferences, should always be at the end
    edit.remove_metadata(meta_txt_dr)
    #edit.remove_metadata(meta_csv_dr)

if __name__ == "__main__":
    main()