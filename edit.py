# subprocess API: https://docs.python.org/3/library/subprocess.html#subprocess.run
import subprocess
import os
'''
Method takes in two file locations and returns the metadata into the command line
:param exif_tool_dr: is the exiftool.exe file
:param img: simple flower jpg image 
'''

class ExifTool:
    def __init__(self, img, exif_tool, temp_dr) -> None:
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
        
        command = [self.exif, '-w', '%dtemp.txt', self.img]

        print(subprocess.run(command))

    # takes temp.txt file and turns it into a dictionary
    def get_metadata(self, txtfile):
        metadata = {}
        with open(txtfile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                entry = line.split(":")
                metadata[entry[0]] = entry[1]
        return metadata

    #TODO: broken meant to turn metadata to csv vile
    def temp_metadata_csv(self):
    
        command = [self.exif, '-csv', '.DSCN0010.jpg', '>', '.temp.csv']

        os.system(self.exif + ' -csv ' + self.img + ' > temp.csv')
        #print(subprocess.run(command, capture_output=True))

def main():
    img_dr = r"C:\Users\jules\Documents\Brown Work\Spring 2024\CS 1952B\Final Project\MetaAlign\1952B-MetaAlign\ExifTool\Images\DSCN0010.jpg"
    exif_tool_dr= r"C:\Users\jules\Documents\Brown Work\Spring 2024\CS 1952B\Final Project\MetaAlign\1952B-MetaAlign\ExifTool\exiftool.exe"
    temp_dr = r"C:\Users\jules\Documents\Brown Work\Spring 2024\CS 1952B\Final Project\MetaAlign\1952B-MetaAlign\ExifTool\Images"
    
    edit = ExifTool(img_dr, exif_tool_dr, temp_dr)
    #edit.print_metadata()
    edit.temp_metadata_txt()
    #edit.temp_metadata_csv()
    print(edit.get_metadata(r'C:\Users\jules\Documents\Brown Work\Spring 2024\CS 1952B\Final Project\MetaAlign\1952B-MetaAlign\ExifTool\Images\temp.txt'))

if __name__ == "__main__":
    main()

