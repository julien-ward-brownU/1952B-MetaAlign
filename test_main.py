from preferences import UserPreferences 
from edit import ExifTool
import os
import argparse
from helper_classes import timeTags, locationTags, deviceTags


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

    # directory to remove txt file (probably should be caled at end of file)
    meta_txt_dr = os.getcwd() + r"\data\input_images\temp.txt"
    # directory to remove csv file
    meta_csv_dr = os.getcwd() + r"\data\meta_data\temp.csv"

    # Access user preferences
    #user_pref = UserPreferences()
    user_pref = "sad"

    edit = ExifTool(img_file, exif_tool, data_dr, output_file, user_pref)

    #edit.print_metadata() # Print metadata of image to terminal
    edit.temp_metadata_txt() # Translate metadata to txt !!NEEDED FOR BASICALLY ALL FUNCTIONS!!
    #edit.temp_metadata_csv() # Translate metadata to cvs (Not needed tbh)
    
    # data_type = deviceTags # CHANGE to any data type from helper class
    # edit.metadata_caption(data_type) # Add datetype fields to caption
    #edit.delete_metadata_add_caption(data_type) # Delete all metadata and add datetype fields to caption

    #edit.delete_all_metadata() # Delete all metadata
    #edit.delete_geo_tag() # Deletes all geo tags
    #edit.delete_device_tags() #deletes all device tags
    #edit.delete_time() #deletes all time tags

    # time_preference = "2024:05:10 12:00:00" #preference should come from userpreference class
    # edit.edit_time(time_preference) #edit all time based on preferences
    # latitude, latref, longitude, longref, altitude, altref = "00 deg 00' 0.00\"", "South", "00 deg 00' 0.00\"", "West", "10000000", "Unknown" 
    # edit.edit_gps(latitude, latref, longitude, longref, altitude, altref) # edit gps based on userpreference class
    # make, model, sn = "CAMERA_NAME", "COOL", "11111"
    # edit.edit_device_tags(make, model, sn) # edit gps based on userpreference class

    edit.output_metadata_txt() # just for testing to check output (this will not work if an output file instet pre)
    # edit. remove_metadata(meta_txt_dr) # Use at end to remove all temp.txt files in input_images 
if __name__ == "__main__":
    main()




    # # Access saved preferences
    # default = user_pref.get_saved_preferences()

    # if default != None:
    #     data, edits, gran  = default
    # else:
    #     data, edits, gran = user_pref.get_preset_preferences()

    # # TODO: change this to actuall work and make it so that we can take the individual preferences and call the appropriate functions
    # parser = argparse.ArgumentParser(description='Process user preferences.')
    # parser.add_argument('filename')           # positional argument
    # parser.add_argument('-data_type', type=str, default= data, help='Data type preference (ALL, TIME, LOCATION, CAMERA_TYPE, CAMERA_SETTINGS)')
    # parser.add_argument('-edit_type', type=str, default= edits, help='Edit type preference (KEEP, RANDOM_LEADING, RANDOM_CENTER, DEFAULT, CAPTION, SCRUB)')
    # parser.add_argument('-gran-type', type=str, default= gran, help='Granularity type preference' )

    # # SIMULATES AUTO DETECT IMAGE UPLOAD (doesn't do anything)
    # input_img = image_detection(img_dr)


    # # TODO: need to add these arguments to the user preferences 
    # args = parser.parse_args()
    # preferences = (input("Would you like to use these as your default preferences? Y OR N: ")).upper()

    # while preferences.upper() not in ['Y', 'N']:
    #     print("Invalid input. Please enter Y or N.")
    #     preferences = input("Would you like to use these as your default preferences? Y or N: ")

    # # TODO: actually add preferences
    # if preferences == "Y":
    # # You would set the preferences 
    #     user_pref.set_saved_preferences()
    # elif preferences == "N":
    #     user_pref.set_preferences()
