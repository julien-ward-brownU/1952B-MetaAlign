# subprocess API: https://docs.python.org/3/library/subprocess.html#subprocess.run
import subprocess
import os
import pandas as pd
'''
Method takes in two file locations and returns the metadata into the command line
:param exif_tool_dr: is the exiftool.exe file
:param img: simple flower jpg image 
'''

'''
ExifTool class manipulates meta data of an image by accessing the orginal ExifTool through the command line (https://exiftool.org/).

:param (str) img: Directory of current input image to modify. (OS format)
:param (str) exif_tool: Directory of exiftool program from https://exiftool.org/. (OS format)
:param (str) data_dr: Directory containing folders of input images, output images and metadata files (txt, csv).  (OS format)
:param (str) output_dr: Directory containing output images.  (OS format)
:param (str) preferences: User preferences to decided how to manipulate the metadata.  (OS format)
'''
class ExifTool:
    def __init__(self, img, exif_tool, data_dr, output_dr, preferences):
        self.img = img
        self.exif = exif_tool
        self.data = data_dr
        self.output = output_dr
        self.preferences = preferences
    
    '''
    Prints all available metadata of input file into terminal.
    '''
    def print_metadata(self):
        # Terminal Command: exiftool.exe input_image.jpg
        command = [self.exif, self.img]
        # A subprocess is created and the command is called using echo 
        # https://www.geeksforgeeks.org/how-to-run-bash-script-in-python/
        subprocess.run(command)

    '''
    Accesses input file metadata to export and temporarly store data in a text file within the input_images folder. 
    '''
    def temp_metadata_txt(self):

        metadata_txt = os.path.join(self.data, "input_images", "temp.txt")
        # Does a txt file already exist? If so, remove it as it produces errors if there is one that already exists with the same name.
        if os.path.exists(metadata_txt):
            self.remove_metadata(metadata_txt)

        # Terminal Command: exiftool.exe -w "temp.txt" input_image.jpg
        command = [self.exif, '-w', '%dtemp.txt',  self.img]
        # Run the command in the terminal
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Meta_data text file was created successfully.")
        else:
            print("Error creating meta_data text file:", print(result))
    
    '''
    Accesses output file metadata to export and temporarly store data in a text file within the output_images 
    folder to manually test if changes have been made. 
    '''
    # For development testing, exact same as above function but for checking output values.
    def output_metadata_txt(self):

        metadata_txt = os.path.join(self.data, "output_images", "temp.txt")
        if os.path.exists(metadata_txt):
            self.remove_metadata(metadata_txt)

        command = [self.exif, '-w', '%dtemp.txt',  self.output]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Meta_data text file was created successfully.")
        else:
            print("Error creating meta_data text file:", print(result))


    
    '''
    Delete file in path. Used to remove temporary metadata that are in text and csv files to preserve user privacy.

    :param (str) file_path: File to be deleted. (OS format)
    '''
    def remove_metadata(self, file_path):
        print("Deleting file!")
        os.remove(file_path) # ATTENTION!!!: Becareful what path you provide to this function! It will DELETE the file!!!

    '''
    Accesses the temporary metadata text file and creates a dictionary of the data. Keys are data headers and values represent the data.
    Example: {"Modify Date" : "2024:05:10 12:00:00"}
    '''
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
    
    '''
    Accesses the temporary metadata dictonary and produce a temporary csv file. A column and two rows represent a data header and a data point.
    '''
    # creates a csv file using pandas dataframe to convert a dictionary to a csv.
    def temp_metadata_csv(self):

        # Convert to DataFrame and save as CSV
        data = self.temp_metadata_dic()
        df = pd.DataFrame([data])
        df.to_csv(self.data + r'\meta_data\temp.csv')
        print("Metadata successfully converted from TXT to CSV.")

    '''
    Turn specific data type in metadata into a string to be added to captions.
    :param (list) data: List of a specific dataType that wants to be accessed and manipulated. (List from helper_classes.py)
    '''
    #TODO should take in what you want to save into caption
    def caption_string(self, data):
        data = self.temp_metadata_dic() # get dictionary metadata
        meta_string = ''
        # you can change this to whatever is in the helper function
        for item in data:
            meta_string += item + ": " + data[item] + "\n"
        return meta_string
    
    # This just takes metadata preferences and add its to comment/caption
    def metadata_caption(self, datatype):
        if os.path.exists(self.output):
            self.remove_metadata(self.output)
        # TODO: need to change the input to this to whatever the user preference is
        meta_string = self.caption_string(datatype)

        command = [self.exif, "-comment="+ meta_string, "-o",  self.output, self.img]
        
        result = subprocess.run(command)
        if result.returncode == 0:
            print("Meta data sucessfully added to caption.")
        else:
            print("Error adding meta data to caption:", result)

    # Deletes all metadata and adds preference to caption/comment (idk which one to pick)
    def delete_metadata_add_caption(self, datatype):
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)
        # TODO: need to change the input to this to whatever the user preference is
        meta_string = self.caption_string(datatype)

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

    # Input Format: "00 deg 00' 0.00\" N", "00 deg 00' 0.00\" E", "00 deg 00' 0.00\" N, 00 deg 00' 0.00\" E"
    def edit_gps(self, latitude, lat_ref, longitude, long_ref, altitude, alt_ref):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        command = [self.exif,
            f"-GPSLatitude={latitude}", # Set latitude metadata to the new latitude 
            f"-GPSLatitudeRef={lat_ref}",
            f"-GPSLongitude={longitude}",  # Set longitude metadata to the new longitude
            f"-GPSLongitudeRef={long_ref}",
            f"-GPSAltitude={altitude}",  # Set altitude metadata to the new altitude
            f"-GPSAltitudeRef={alt_ref}",
            "-o", self.output, self.img]
        result = subprocess.run(command)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            print("Geo metadata edited successfully.")
        else:
            print("Error editing Geo metadata:", result)

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


    # new_time: "2024:05:10 12:00:00"
    def edit_time(self, new_time):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        command = [
            self.exif,
            f"-AllDates={new_time}",  # Set all date/time metadata to the new time
            f"-GPSTimeStamp={new_time}",  # Set GPS TimeStamp to the new time
            f"-GPSDateStamp={new_time}",  # Set GPS DateStamp to the new time
            "-o", self.output,  # Output file path
            self.img  # Input file path
        ]
 
        result = subprocess.run(command)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            print("Time metadata edited successfully.")
        else:
            print("Error editing time metadata:", result)

        # new_time: "2024:05:10 12:00:00"
    def delete_time(self):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        command = [
            self.exif,
            f"-AllDates=",  # Set all date/time metadata to the new time
            f"-GPSTimeStamp=",  # Set GPS TimeStamp to the new time
            f"-GPSDateStamp=",  # Set GPS DateStamp to the new time
            "-o", self.output,  # Output file path
            self.img  # Input file path
        ]
 
        result = subprocess.run(command)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            print("Time metadata edited successfully.")
        else:
            print("Error editing time metadata:", result)

    # Input Format: "make", "model", "sn"
    def edit_device_tags(self, make, model, serial_num):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        command = [
            self.exif,
            f"-Make={make}",  # Set make of the camera
            f"-model={model}",  # Set the model of the camera
            f"-SerialNumber={serial_num}",  # Set serial number of the camera
            "-o", self.output,  # Output file path
            self.img  # Input file path
        ]
 
        result = subprocess.run(command)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            print("Camera metadata edited successfully.")
        else:
            print("Error editing camera metadata:", result)
    
    def delete_device_tags(self):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        command = [
            self.exif,
            f"-Make=",  # Delete make of the camera
            f"-model=",  # Delete the model of the camera
            f"-SerialNumber=",  # Delete serial number of the camera
            "-o", self.output,  # Output file path
            self.img  # Input file path
        ]
 
        result = subprocess.run(command)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            print("Camera metadata deleted successfully.")
        else:
            print("Error deleting camera metadata:", result)


    
    



