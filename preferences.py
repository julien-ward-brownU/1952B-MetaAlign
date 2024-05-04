from helper_classes import *

class UserPreferences:

        # ANNOTATION: For each web
    def __init__(self, name, data: list[DataType], granularity: list[Granularity], 
                 edits: list[EditType], default: bool):
        self.name = name
        self.data = data
        self.granularity = granularity
        self.edits = edits
        self.is_default = default
        
    # set the users current preferences
    # TODO move code from main into here
    def set_preferences(self):
        pass
    
    # Displays the users current prefernces for this website.
    def get_preferences(self):
        print("Preferences for: " + self.name + "\n")
        for data in self.data:
            print("Data: " + data.name + "\nType of edit: " + self.edits[data.value].name + "\nGranularity: " + self.granularity[data.value].name + "\n \n")
        print("Are these default preferences? " + self.is_default)

    # Makes this set of preferences default
    def set_default(self):
        self.is_default = True

    # Code to move to other classes
    
    # Maybe have a pickle file that on start up gets loaded? 
    preferences: list[UserPreferences] = list()
    
    def get_preferences():
        for pref in preferences:
            if pref.name == location:
                return pref
        # else: no prefernces founf
        return set_new_preferences()




    