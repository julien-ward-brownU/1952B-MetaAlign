from helper_classes import *

class UserPreferences:

    # ANNOTATION: For each web
    def __init__(self, name, data: list[DataType], edits: list[EditType], 
                 granularity: list[Granularity], default: bool):
        self.name = name
        self.data = data
        self.granularity = granularity
        self.edits = edits
        self.is_default = default
    
    # Displays the users current prefernces for this website.
    def get_preferences(self):
        print("Preferences for: " + self.name + "\n")
        for data in self.data:
            print("Data: " + data.name + "\nType of edit: " + self.edits[data.value].name + "\nGranularity: " + self.granularity[data.value].name + "\n \n")
        print("Are these default preferences? " + self.is_default)

    # Makes this set of preferences default
    def set_default(self):
        self.is_default = True

    # set the users current preferences
    # TODO move code from main into here
    def set_preferences(self):
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
        pass
    





    