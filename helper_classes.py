from enum import Enum

# Shared classes to be used by preferences and edit

# Grouping tags! 
timeTags = ["Date/Time Original", "Create Date", "GPS Date/Time", "GPS Date Stamp", "Modify Date"]
locationTags = ["GPS Position", "GPS Latitude", "GPS Longitude", "GPS Altitude Ref",
                "GPS Longitude Ref", "GPS Altitude Ref", "GPS Satellites", "GPS Img Direction Ref" 
                "GPS Map Datum"]
deviceTags = ["Make", "Camera Model Name", "Serial Number"]

class DataType(Enum):
    ALL = 0
    TIME = 1
    LOCATION = 2
    CAMERA_TYPE = 3
    CAMERA_SETTINGS = 4

# ANNOTATION: Types of edits allowed 
class EditType(Enum):
    KEEP = 0
    RANDOM_WINDOW = 1
    RANDOM_PERIOD = 2
    DEFAULT = 3
    CAPTION = 4
    DELETE = 5

class Granularity(Enum):
    NOT_APPLICABLE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


# TODO: Pseudocode - Image Upload Detection 
def image_detection(image):
    """
    Detects when image is uploaded onto website and stores image temp into placeholder value (input).
    input = detected_image
    return name of the website, file name of the image. 
    """
    # TORUN: change these!!! 
    website = "instagram"
    image_name = "test2.jpg"
    return website, image_name

# TODO: Pseudocode - Image Deletion after use 
def image_upload(image, website):
    """
    Detects when image is uploaded onto website and stores image temp into placeholder value (input).
    print("Deleting Image data file: ", input)
    os.remove(image)
    """
    pass
    