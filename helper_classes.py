from enum import Enum

# Shared classes to be used by preferences and edit

timeTags = ["Date/Time Original", "Create Date", "GPS Date/Time", "GPS Date Stamp", "File Modification Date/Time",
"File Access Date/Time", "File Creation Date/Time", "Modify Date"]

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
    RANDOM_LEADING = 1
    RANDOM_CENTER = 2
    DEFAULT = 3
    CAPTION = 4
    SCRUB = 5

class Granularity(Enum):
    HOUR = 0
    DAY = 1
    MONTH = 2
    YEAR = 3
    DECADE = 4


