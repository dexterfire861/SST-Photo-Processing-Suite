# Import necessary libraries

import io
import os
import re
from google.cloud import vision
from zipfile import ZipFile
from PIL import Image, ImageDraw
import argparse
import time
import math

#Begin timer

start_time = time.time()

#Default values for arguments

standardize = True
unusualNumber = 50
lowerbound = 0
upperbound = 100000

# Take an optional argument to not standardize the numbers if desired (i.e. 28 -> 28)

parser = argparse.ArgumentParser(description="Check for standardization requirement")

parser.add_argument("--unstandardize", default=False, action="store_true", help="Flag to not standardize numbers")
parser.add_argument("--unusualFrequency", default=50, help="Display warnings for bib numbers with more than this number of occurances in pictures",type=int)
parser.add_argument("--lb", default=0, help="Lowest bib number in the race (lower bound)",type=int)
parser.add_argument("--ub", default=100000, help="Highest bib number in the race (upper bound)",type=int)

args = parser.parse_args()

for item in os.listdir(): # loop through items in dir
    if item.endswith('.zip'): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = ZipFile(file_name) # create zipfile object
        zip_ref.extractall() # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file

if(args.unstandardize):
    standardize = False
unusualNumber = args.unusualFrequency
lowerbound = args.lb
upperbound = args.ub

# API token for use within the program

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'teak-clarity-218502-59fd687fc810.JSON'

client = vision.ImageAnnotatorClient()



def get_crop_hint(path):
    """Detect crop hints on a single image and return the first result."""

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    crop_hints_params = vision.CropHintsParams(aspect_ratios=[1])
    image_context = vision.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    # Get bounds for the first crop hint using an aspect ratio of 1.
    vertices = hints[0].bounding_poly.vertices

    return vertices

def crop_to_hint(image_file):
    """Crop the image using the hints in the vector list."""

    vects = get_crop_hint(image_file)

    im = Image.open(image_file)
    im2 = im.crop([vects[0].x, vects[0].y,
                  vects[2].x - 1, vects[2].y - 1])
    im2.save('output-crop.jpg', 'JPEG')
    #print('Saved new image to output-crop.jpg')

"""
def draw_hint(image_file):
    #Draw a border around the image using the hints in the vector list.
    vects = get_crop_hint(image_file)
    print(vects)

    im = Image.open(image_file)
    draw = ImageDraw.Draw(im)
    draw.polygon([
        vects[0].x, vects[0].y,
        vects[1].x, vects[1].y,
        vects[2].x, vects[2].y,
        vects[3].x, vects[3].y], None, 'red')
"""

#Get path of folder with images to detect numbers

path = input("Enter the path of the folder: ")

client = vision.ImageAnnotatorClient()
digits = "0123456789"
numDigits = int(math.log10(upperbound))+1

freq = {}
previous = ""

#Iterate through images in the directory for text detection

for imagePath in os.listdir(path):

    print(os.path.join(path, imagePath))
    crop_to_hint(os.path.join(path, imagePath))

    with io.open('output-crop.jpg', 'rb') as image_file:
        content = image_file.read()


    image = vision.Image(content=content)


    # Perform text detection

    response = client.text_detection(image=image)

    appendToFile = ""
    numsFound = False
    outOfRange = False


    # Checking that the text detection returns only numbers

    for text in response.text_annotations:

        if(text.description.isnumeric()):
            isNumber = True

            for c in text.description:
                if c not in digits:
                    isNumber = False
                    break

            if isNumber and not text.description.startswith("0"):
                """
                vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
                print('bounds:', ",".join(vertices))
                """
                numsFound = True

                if text.description not in freq:
                    freq[text.description] = 1
                else:
                    freq[text.description] += 1

                if int(text.description) < lowerbound or int(text.description) > upperbound:
                    outOfRange = True

                    #Check previous image for numbers containing these digits (if it is not a 1 digit number)
                    if(int(math.log10(int(text.description))) + 1 > 1 and int(math.log10(int(text.description))) + 1 < numDigits):
                        matches = re.finditer(text.description, previous)

                        matches_positions = [match.start() for match in matches]
                        for pos in matches_positions:
                            lower = pos
                            while previous[lower] != "_":
                                lower-= 1
                            upper = pos+1
                            while previous[upper] != "_" and upper < len(previous):
                                upper+= 1
                            appendToFile+= "_" + previous[lower:upper]


                else:
                    if standardize:
                        appendToFile += "_" + text.description.zfill(numDigits)
                    else:
                        appendToFile += "_" + text.description

    # print(appendToFile)

    # If no number is found, the picture is put in the LOST pile

    if not numsFound or outOfRange:
        appendToFile += "_LOST"

    # Changing the name of the file to add the number(s) found from the text detection

    pre, ext = os.path.splitext(os.path.join(path, imagePath))
    os.rename(os.path.join(path, imagePath), pre+appendToFile+ext)

    previous = appendToFile


# Deleting the cropped image as it is not useful

os.remove('output-crop.jpg')


# Using the frequencies put in the dictionary, check to see if there are more than 50 recognitions of the number,
# and if there is, send a possible error message for manual checking

for key in freq.keys():
    if freq[key] > unusualNumber:
        print("Possible error: Consider checking number " + key + " manually due to high number of occurrences")


#Return total time elapsed

elapsed = time.time()-start_time
print("\nTime elapsed: " + str(int(elapsed/60)) + " minutes and " + str(round(elapsed%60, 2)) + " seconds.")

