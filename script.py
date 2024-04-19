# subprocess API: https://docs.python.org/3/library/subprocess.html#subprocess.run
import subprocess

'''
Method takes in two file locations and returns the metadata into the command line
:param exif_tool_dr: is the exiftool.exe file
:param img: simple flower jpg image 
'''
def print_metadata(img, exif_tool):
    
    # The command is list of the exiftool.exe and the image location
    command = [exif_tool, img]

    # A subprocess is created and the command is called using echo 
    # https://www.geeksforgeeks.org/how-to-run-bash-script-in-python/
    subprocess.run(command)

def main():
    img_dr = r"C:\Users\jules\Documents\Brown Work\Spring 2024\CS 1952B\Final Project\MetaAlign\1952B-MetaAlign\ExifTool\Images\flower.jpg"
    exif_tool_dr= r"C:\Users\jules\Documents\Brown Work\Spring 2024\CS 1952B\Final Project\MetaAlign\1952B-MetaAlign\ExifTool\exiftool.exe"
    print_metadata(img_dr, exif_tool_dr)

if __name__ == "__main__":
    main()