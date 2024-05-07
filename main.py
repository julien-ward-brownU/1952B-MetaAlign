from preferences import UserPreferences 
from edit import ExifTool
import os
import argparse
from helper_classes import *


def main():

    # Ideally, this is a database, but for now I have just made some examples for demonstration
    preferences: list[UserPreferences] = list()
    pref_one = UserPreferences("instagram", [DataType.TIME, DataType.LOCATION, DataType.CAMERA_TYPE],
                               [EditType.KEEP, EditType.CAPTION, EditType.DELETE],
                                [Granularity.MEDIUM, Granularity.HIGH, Granularity.NOT_APPLICABLE], False)
    pref_two = UserPreferences("facebook", [DataType.TIME, DataType.LOCATION, DataType.CAMERA_TYPE],
                               [EditType.KEEP, EditType.CAPTION, EditType.RANDOM_WINDOW],
                                [Granularity.NOT_APPLICABLE, Granularity.NOT_APPLICABLE, Granularity.LOW], False)
    pref_all = UserPreferences("default", [DataType.ALL], [EditType.DELETE], [Granularity.NOT_APPLICABLE], True)
    preferences = [pref_one, pref_two, pref_all]

    # Detect where an image is being uploaded and get the prefereces for that site (or make a new one)
    location, image_name = image_detection()
    pref = get_preferences(location, preferences)
    
    # Image file
    img_file = os.path.join(os.getcwd(), "data", "input_images", image_name)
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

    edit = ExifTool(img_file, exif_tool, data_dr, output_file)
    #edit.print_metadata() # Print metadata of image to terminal
    edit.temp_metadata_txt() # Translate metadata to txt !!NEEDED FOR BASICALLY ALL FUNCTIONS!!
    #edit.temp_metadata_csv() # Translate metadata to cvs (Not needed tbh)
   
    adjust_metadata(edit, pref)

    image_upload(output_file, location)
     # ANNOTATION: This call is especially important because it removes any temporary metadata that has been stored to be used for manipulation. This deletes those files.
     # should always be at the end
    #edit.remove_metadata(meta_txt_dr)
    # edit.remove_metadata(meta_csv_dr)


'''
This is the brains of this program. Based on the user's preferences, each category of metadata is
adjusted. 

'''
def adjust_metadata(edit, pref):

    data = pref.data
    edits = pref.edits
    gran = pref.granularity
    # If someone has selected ALL, go through all categories
    if DataType.ALL in pref.data:
        data = [DataType.list()]
        data = data[1:] # remove ALL
        edits = [edits[0] * 4] # make all prefs the same for all
        gran = [gran[0] * 4]
    
    # For each type of data, go through and perform the appropriate edit action
    for i in range(len(data)):
        match (edits[i]):
            case EditType.KEEP: 
                continue
            case EditType.DELETE:
                edit.delete(data[i])
            case EditType.CAPTION:
                edit.caption(data[i])
            # Obscuring Data
            case EditType.RANDOM_PERIOD, EditType.RANDOM_WINDOW, EditType.DEFAULT:
                edit.obscure(data[i], edits[i], gran[i])
            case _:
                print("Error in match and case")
                

# Helper Methods for setup

# Find the preferences that match the site, otherwise make a new one. Returns a UserPreferences
def get_preferences(website, preferences):
    for pref in preferences:
        if pref.name == website:
            return pref
        # else: no prefernces founf
    return set_new_prefernces(website)

# see create_new_preferences in the preferences class for what this would look like, would be the 
# input from some UI that we did not get functional. 
def set_new_prefernces(website): 
    return

# TODO: Pseudocode - Image Upload Detection 
def image_detection():
    """
    Detects when image is uploaded onto website and stores image temp into placeholder value (input).
    input = detected_image
    return name of the website, file name of the image. 
    """
    # TORUN: change these!!! 
    website = "instagram"
    image_name = "test_image.jpg"
    return website, image_name

# TODO: Pseudocode - Image Deletion after use 
def image_upload(image, website):
    """
    Detects when image is uploaded onto website and stores image temp into placeholder value (input).
    print("Deleting Image data file: ", input)
    os.remove(image)
    """
    pass


if __name__ == "__main__":
    main()