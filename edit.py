# subprocess API: https://docs.python.org/3/library/subprocess.html#subprocess.run
import subprocess
import os
import pandas as pd
from helper_classes import timeTags, locationTags, deviceTags
'''
Method takes in two file locations and returns the metadata into the command line
:param exif_tool_dr: is the exiftool.exe file
:param img: simple flower jpg image 
'''

class ExifTool:
    def __init__(self, img, exif_tool, data_dr, output_dr):
        self.img = img
        self.exif = exif_tool
        self.data = data_dr
        self.output = output_dr
        
    def print_metadata(self):
        # The command is list of the exiftool.exe and the image location
        command = [self.exif, self.img]
        # A subprocess is created and the command is called using echo 
        # https://www.geeksforgeeks.org/how-to-run-bash-script-in-python/
        subprocess.run(command)

    # get metadata and exports it into txt file
    def temp_metadata_txt(self):
        metadata_txt = os.path.join(self.data, "input_images", "temp.txt")
        # Does a temp already exist? If so remove it!
        if os.path.exists(metadata_txt):
            self.remove_metadata(metadata_txt)

        command = [self.exif, '-w', '%dtemp.txt',  self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Meta_data text file was created successfully.")
        else:
            print("Error creating meta_data text file:", print(result))


    # CAREFUL WHAT FILE YOU PUT HERE IN PATH! will delete file!!!!!!!!!!!!!!!
    def remove_metadata(self, file_path):
        print("Deleting file!")
        os.remove(file_path)

    # Takes text file, and stores information in a dictionary to be used for preferences.
    def temp_metadata_dic(self):
        
        with open(self.data + r"\input_images\temp.txt", 'r') as file:
            lines = file.readlines()
        # Parse key-value pairs
        data = {}
        for line in lines:
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))
                data[key] = value
        return data
    
    # creates a csv file using pandas dataframe to convert a dictionary to a csv.
    def temp_metadata_csv(self):

        # Convert to DataFrame and save as CSV
        data = self.temp_metadata_dic()
        df = pd.DataFrame([data])
        df.to_csv(self.data + r'\meta_data\temp.csv')
        print("Metadata successfully converted from TXT to CSV.")


    #TODO should take in what you want to save into caption
    def caption_string(self, data):
        data = self.temp_metadata_dic() # get dictionary metadata
        meta_string = ''
        # you can change this to whatever is in the helper function
        for item in data:
            meta_string += item + ": " + data[item] + "\n"
        return meta_string
    
    # This just takes metadata preferences and add its to comment/caption
    def metadata_caption(self):
        if os.path.exists(self.output):
            self.remove_metadata(self.output)
        # TODO: need to change the input to this to whatever the user preference is
        meta_string = self.caption_string(deviceTags)

        command = [self.exif, "-comment="+ meta_string, "-o",  self.output, self.img]
        
        result = subprocess.run(command)
        if result.returncode == 0:
            print("Meta data sucessfully added to caption.")
        else:
            print("Error adding meta data to caption:", result)

    # Deletes all metadata and adds preference to caption/comment (idk which one to pick)
    def delete_metadata_add_caption(self):
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)
        # TODO: need to change the input to this to whatever the user preference is
        meta_string = self.caption_string(deviceTags)

        command = [self.exif, "-all=","-comment="+ meta_string, "-o",  self.output,  self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Meta data sucessfully deleted and added to caption.")
        else:
            print("Error deleting and adding meta data to caption:", result)

    # Deletes all metadata
    def delete_all_metadata(self):

        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        command = [self.exif, "-all=", "-o", self.output, self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("All meta data sucessfully deleted.")
        else:
            print("Error deleting all meta data: ", result)
    
    # Delete geo tags within file
    def delete_geo_tag(self):

        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        command = [self.exif, "-gps:all=", "-o", self.output, self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("GEO Meta data sucessfully removed.")
        else:
            print("Error removing geo metadata: ", result)
    



