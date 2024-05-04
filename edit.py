# subprocess API: https://docs.python.org/3/library/subprocess.html#subprocess.run
import subprocess
import os
import pandas as pd
from helper_classes import timeTags
'''
Method takes in two file locations and returns the metadata into the command line
:param exif_tool_dr: is the exiftool.exe file
:param img: simple flower jpg image 
'''

class ExifTool:
    def __init__(self, img, exif_tool, temp_dr):
        self.img = img
        self.exif = exif_tool
        self.data = temp_dr

    def print_metadata(self):
        # The command is list of the exiftool.exe and the image location
        command = [self.exif, self.img]

        # A subprocess is created and the command is called using echo 
        # https://www.geeksforgeeks.org/how-to-run-bash-script-in-python/
        subprocess.run(command)

    #get metadata and exports it into txt file
    def temp_metadata_txt(self):
        # exiftool -w output.txt image_name.jpg
        command = [self.exif, '-w', '%dtemp.txt', self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Meta_data text file was created successfully.")
        else:
            print("Error creating meta_data text file:", print(result))


    # CAREFUL WHAT FILE YOU PUT HERE IN PATH! will delete file!!!!!!!!!!!!!!!
    def remove_metadata(self, file_path):
        print("Deleting Meta data file: ", file_path)
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
        # df = pd.DataFrame(data.items(), columns=['Attribute', 'Value'])
        # df.to_csv(self.data + r'\temp.csv', index=None)
        data = self.temp_metadata_dic(self.data)
        df = pd.DataFrame([data])
        
        df.to_csv(self.data + r'\meta_data\temp.csv')
        print("Metadata successfully converted from TXT to CSV.")


    # TODO: Takes preference and produces into caption (next should be to delete all of the in metadata)
    def metadata_caption(self):
        output = self.data + r'\output_images\output.jpg' # TODO: output into different folder zzzzz why no work

        data = self.temp_metadata_dic() # get dictionary metadata
        meta_string = ''
        # you can change this to whatever is in the helper function
        for item in timeTags:
            meta_string += item + ": " + data[item] + "\n"
        
        # TODO: command works, and caption in txt is edited but shoudn't we be able to see caption change in file?
        # also makes a new file...
        command = [self.exif, '-caption='+ meta_string, self.img]
        # This following line is meant to delete all metadata and include a comment (only test on TEST Image), 
        # the problem here is that it seems to obscure some data and doesn't effect date and time data?
        #command = [self.exif, '-all= ', '-comment='+ meta_string, self.img]
        
        result = subprocess.run(command)
        print(result)
        if result.returncode == 0:
            print("Meta data sucessfully added to caption.")
        else:
            print("Error adding meta data to caption")
    
    


