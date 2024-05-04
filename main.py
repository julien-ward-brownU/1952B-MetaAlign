from preferences import UserPreferences 
from edit import ExifTool
import os
import argparse
from helper_classes import image_detection, image_deletion


def main():
    # Take in user preferences (for our simple case we will use the terminal inputs of the user: main.py preferences img_in_file)
    # print image metadata to terminal using ExifTool class function print_metadata
    # give user preferences to preferences class parse metadata for prefereces
    # scrub original image
    # add parsed preferences to caption
    
    img_dr = os.getcwd() + r"\data\input_images\DSCN0010 test.jpg"
    exif_tool_dr= os.getcwd() + r"/ExifTool/exiftool.exe"
    data_dr = os.getcwd() + r"\data"
    # directory to remove txt file
    meta_txt_dr = os.getcwd() + r"\data\input_images\temp.txt"
    # directory to remove csv file
    meta_csv_dr = os.getcwd() + r"\data\meta_data\temp.csv"

    # Access user preferences
    user_pref = UserPreferences()
    # Access saved preferences
    default = user_pref.get_saved_preferences()

    if default != None:
        data, edits, gran  = default
    else:
        data, edits, gran = user_pref.get_preset_preferences()

    # TODO: change this to actuall work and make it so that we can take the individual preferences and call the appropriate functions
    parser = argparse.ArgumentParser(description='Process user preferences.')
    parser.add_argument('filename')           # positional argument
    parser.add_argument('-data_type', type=str, default= data, help='Data type preference (ALL, TIME, LOCATION, CAMERA_TYPE, CAMERA_SETTINGS)')
    parser.add_argument('-edit_type', type=str, default= edits, help='Edit type preference (KEEP, RANDOM_LEADING, RANDOM_CENTER, DEFAULT, CAPTION, SCRUB)')
    parser.add_argument('-gran-type', type=str, default= gran, help='Granularity type preference' )

    # SIMULATES AUTO DETECT IMAGE UPLOAD (doesn't do anything)
    input_img = image_detection(img_dr)

    # initialize exif class tool
    edit = ExifTool(input_img, exif_tool_dr, data_dr)

    # TODO: need to add these arguments to the user preferences 
    args = parser.parse_args()
    preferences = (input("Would you like to use these as your default preferences? Y OR N: ")).upper()

    while preferences.upper() not in ['Y', 'N']:
        print("Invalid input. Please enter Y or N.")
        preferences = input("Would you like to use these as your default preferences? Y or N: ")

    # TODO: actually add preferences
    if preferences == "Y":
    # You would set the preferences 
        user_pref.set_saved_preferences()
    elif preferences == "N":
        user_pref.set_preferences()

    # TODO: these calls should probably be moved into preferences based on what preferences they selected.
    #edit.print_metadata()
    edit.temp_metadata_txt()
    edit.temp_metadata_csv()
    edit.metadata_caption()

    # Should delete all data except user preferences, should always be at the end
    edit.remove_metadata(meta_txt_dr)
    #edit.remove_metadata(meta_csv_dr)
    image_deletion()

if __name__ == "__main__":
    main()