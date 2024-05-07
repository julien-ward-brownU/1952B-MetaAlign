# subprocess API: https://docs.python.org/3/library/subprocess.html#subprocess.run
import subprocess
import os
import pandas as pd
from preferences import *
from helper_classes import *
import datetime

'''
ExifTool class manipulates meta data of an image by accessing the orginal ExifTool through the command line (https://exiftool.org/).

:param (str) img: Directory of current input image to modify. (OS format)
:param (str) exif_tool: Directory of exiftool program from https://exiftool.org/. (OS format)
:param (str) data_dr: Directory containing folders of input images, output images and metadata files (txt, csv).  (OS format)
:param (str) output_dr: Directory containing output images.  (OS format)
:param (str) preferences: User preferences to decided how to manipulate the metadata.  (OS format)
'''
class ExifTool:
    def __init__(self, img, exif_tool, data_dr, output_dr):
        self.img = img
        self.exif = exif_tool
        self.data = data_dr
        self.output = output_dr


    def delete(self, data: DataType):

        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        # Command to call exiftool to delete all the metadata in exif_tags and output the new image in the outputs folder
        command = [self.exif]
        tags, text = exif_tags(data)
        command += tags
        command += [self.output, self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Metadata sucessfully removed.")
        else:
            print("Error removing metadata: ", result)
    

    '''
    Turn specific data type in metadata into a string, by calling caption_string, then add this string of metadata to to the metadata field "Caption".

    :param (list) datatype: List of a specific dataType that will be accessed and manipulated. (List from helper_classes.py)
    '''
    # Deletes all metadata and adds preference to caption/comment (idk which one to pick)
    def caption(self, datatype: DataType):
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)
        # TODO: need to change the input to this to whatever the user preference is
        meta_string = self.caption_string(datatype)

        command = [self.exif,"-caption="+ meta_string, "-o",  self.output,  self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Meta data sucessfully deleted and added to caption.")
        else:
            print("Error deleting and adding meta data to caption:", result)

        # deletes the metadata after adding to caption (could be designed so theres an option for this)
        self.delete(DataType)



    # def obscure(self, data: DataType, rand_type: EditType, gran: Granularity): 

    #     match data:
    #         case DataType.TIME:
    #         case DataType.LOCATION:
    #         case DataType.CAMERA_TYPE:
    #         case DataType.CAMERA_SETTINGS:
        
    #     pass
    
    '''
    Prints all available metadata of input file into terminal.
    '''
    def print_metadata(self):
        # Command to call exiftool access the image and print out the metadata
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

        # Command to call exiftool to write the metadata to a .txt file
        command = [self.exif, '-w', '%dtemp.txt',  self.img]
        # Run the command in the terminal
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Input image meta_data text file was created successfully.")
        else:
            print("Error creating input image meta_data text file:", print(result))
    
    '''
    Accesses output file metadata to export and temporarly store data in a text file within the output_images 
    folder to manually test if changes have been made. 
    '''
    # For development testing, exact same as above function but for checking output values.
    def output_metadata_txt(self):

        metadata_txt = os.path.join(self.data, "output_images", "temp.txt")
        output_jpg = os.path.join(self.data, "output_images", "output.jpg")
        
        
        if not os.path.exists(output_jpg):
            print("Can't call this function without creating an output file.")
            return 0
        
        if os.path.exists(metadata_txt):
            self.remove_metadata(metadata_txt)

        # Command to call exiftool to write the metadata to a .txt file
        command = [self.exif, '-w', '%dtemp.txt',  self.output]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Output image meta_data text file was created successfully.")
        else:
            print("Error creating output image meta_data text file:", print(result))

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

    :return (dictionary) data: A dictionary of all the metadata of the image.
    '''
    def temp_metadata_dic(self):
        
        # Read in the metadata text file line by line
        with open(self.data + r"\input_images\temp.txt", 'r') as file:
            lines = file.readlines()
        # Parse key-value pairs
        data = {}
        
        # Loop through the lines, parse them and add them to a dictionary
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

        # Convert dictionary to DataFrame and save as CSV
        data = self.temp_metadata_dic()
        df = pd.DataFrame([data])
        df.to_csv(self.data + r'\meta_data\temp.csv')
        print("Metadata successfully converted from TXT to CSV.")

    '''
    Turn specific data type in metadata into a string to be added to captions.

    :param (list) data_type: List of a specific dataType that will be accessed and manipulated. (List from helper_classes.py)
    :return (str) meta_string: A string of a subset of metadata based on the data_type (user preference).
    '''
    def caption_string(self, data_type):
        tags, data = exif_tags(data_type) # get dictionary metadata
        meta_string = ''

        # Loop through the data type list, access the data from the dictionary and add
        if data_type != DataType.CAMERA_SETTINGS:
            for item in data_type:
                if item in data.keys():
                    meta_string += " " + item + ": " + data[item] + "\n"
                else:
                    meta_string += " " + item + ": "
        else: # this is because the settings list is just what is not settings
                if item not in data.keys():
                    meta_string += " " + item + ": " + data[item] + "\n"
                else:
                    meta_string += " " + item + ": "

        return meta_string
    
    '''
    Turn specific data type in metadata into a string, by calling caption_string, then add this string of metadata to the metadata field "Caption".

    :param (list) data_type: List of a specific dataType that will be accessed and manipulated. (List from helper_classes.py)
    '''
    def metadata_caption(self, data_type):
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        # TODO: need to change the input to this to whatever the user preference is
        meta_string = self.caption_string(data_type)

        # Command to call exiftool to write specific metadata to the metadata field "Caption" and output the new image in the outputs folder
        command = [self.exif, "-caption="+ meta_string, "-o",  self.output, self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("Meta data sucessfully added to caption.")
        else:
            print("Error adding meta data to caption:", result)



    '''
    Delete all metadata (that is possible to delete) in the image.
    '''
    def delete_all_metadata(self):

        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        # Command to call exiftool to delete all the metadata and output the new image in the outputs folder
        command = [self.exif, "-all=", "-o", self.output, self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("All meta data sucessfully deleted.")
        else:
            print("Error deleting all meta data: ", result)

    '''
    Edit and change the values and granularity of GPS metadata.

    :param (str) latitude: Format: ("XX deg XX' X.XX\" C") X: Any real number, C: "N", "S"
    :param (str) lat_ref: Format: "North", "South"
    :param (str) longitude: Format: ("XX deg XX' X.XX\" C") X: Any real number, C: "N", "S"
    :param (str) long_ref: Format: "East", "West"
    :param (str) altitude: Format: ("XX m") X: Any real number
    :param (str) alt_ref: Format: "Above Sea Level", "Below Sea Level"
    '''
    def edit_gps(self, latitude, lat_ref, longitude, long_ref, altitude, alt_ref):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        # Command to call exiftool to edit GPS metadata and output the new image in the outputs folder
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
    
    '''
    Delete all GEO metadata (that is possible to delete) in the image.
    '''
    def delete_geo_tag(self):

        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        # Command to call exiftool to delete all GPS metadata and output the new image in the outputs folder
        command = [self.exif, "-gps:all=", "-o", self.output, self.img]
        result = subprocess.run(command)

        if result.returncode == 0:
            print("GEO Meta data sucessfully removed.")
        else:
            print("Error removing geo metadata: ", result)

    '''
    Edit and change the values of the time metadata.

    :param (str) new_time: Format: "YYYY:MM:DD HH:MM:SS"
    Example: "2024:05:10 12:00:00"
    '''
    def edit_time(self, new_time):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        # Command to call exiftool to edit all time metadata and output the new image in the outputs folder
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

        
    '''
    Delete all GEO metadata (that is possible to delete) in the image.
    '''
    def delete_time(self):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        # Command to call exiftool to delete all time metadata and output the new image in the outputs folder
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
            print("Time metadata deleted successfully.")
        else:
            print("Error deleting time metadata:", result)

    '''
    Edit and change the values of the time metadata.

    :param (str) make: Format: "Make"
    :param (str) model: Format: "Model"
    :param (str) serial_num: Format: "Serial Number"
    Example: "NIKON", "COOLPIX P6000", "12311"
    '''
    def edit_device_tags(self, make, model, serial_num):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)
        
        # Command to call exiftool to edit camera metadata and output the new image in the outputs folder
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
    
    '''
    Delete all Camera metadata (that is possible to delete) in the image.
    '''
    def delete_device_tags(self):
        
        # This prevents an error of the file already existing
        if os.path.exists(self.output):
            self.remove_metadata(self.output)

        # Command to call exiftool to delete camera metadata and output the new image in the outputs folder
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


    
    



