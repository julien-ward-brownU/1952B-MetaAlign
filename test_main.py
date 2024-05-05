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
    
    # Image file
    img_file = os.path.join(os.getcwd(), "data", "input_images", "test2.jpg")
    # to check if output file has 
    #img_file = os.path.join(os.getcwd(), "data", "output_images", "output.jpg")
    # ExifTool file
    exif_tool = os.path.join(os.getcwd(), "exiftool.exe")
    # Data directory; Includes: input images, temp meta data and output images
    data_dr = os.path.join(os.getcwd(), "data")

    # output file for image created
    output_file  = os.path.join(data_dr, "output_images", "output.jpg") 
    # Temporary meta data files (CSV, TXT) (can't get temp.txt to be in this folder ;c)
    #temp_dr  = os.path.join(data_dr, "meta_data")

    # directory to remove txt file
    meta_txt_dr = os.getcwd() + r"\data\input_images\temp.txt"
    # directory to remove csv file
    meta_csv_dr = os.getcwd() + r"\data\meta_data\temp.csv"

    edit = ExifTool(img_file, exif_tool, data_dr, output_file)

    # TODO: these calls should probably be moved 
    #edit.print_metadata()
    #edit.temp_metadata_csv()
    edit.temp_metadata_txt()
    #edit.metadata_caption()
    #edit.delete_metadata_add_caption()
    #edit.delete_all_metadata()
    #edit.delete_geo_tag()
    #edit.remove_metadata(meta_txt_dr)
    #edit.temp_metadata_txt()

    # Should delete all data except user preferences, should always be at the end
    #edit.remove_metadata(meta_csv_dr)

if __name__ == "__main__":
    main()