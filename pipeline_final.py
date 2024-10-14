from __future__ import print_function
from google.cloud import vision
import os, io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'teak-clarity-218502-59fd687fc810.JSON'

#image right here
path = input("Enter the path of the folder: ")

client = vision.ImageAnnotatorClient()
digits = "0123456789"
freq = {}


for imagePath in os.listdir(path):

    with io.open(os.path.join(path, imagePath), 'rb') as image_file:
        content = image_file.read()

    print(os.path.join(path, imagePath))

    image = vision.Image(content=content)


    #performing text detection
    response = client.text_detection(image=image)

    appendToFile = ""
    numsFound = False

    for text in response.text_annotations:
        #print('=' * 30) #comment this out
        #print(text.description) #comment this out

        if(text.description.isnumeric()):
            isNumber = True

            for c in text.description:
                if c not in digits:
                    isNumber = False
                    break

            if isNumber and not text.description.startswith("0"):
                #print(text.description) #comment this once it is confirmed that appending to file name works
                #print(text.confidence) #does not work for text_detection, only document_text_detection
                numsFound = True
                if text.description not in freq:
                    freq[text.description] = 1
                else:
                    freq[text.description] += 1
                appendToFile += "_"+text.description

        """
        vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
        print('bounds:', ",".join(vertices))
        """

    #print(appendToFile)

    if not numsFound:
        appendToFile = "_LOST"

    pre, ext = os.path.splitext(os.path.join(path, imagePath))
    os.rename(os.path.join(path, imagePath), pre+appendToFile+ext)


for key in freq.keys():
    if freq[key] > 50: #Change this number later?
        print("Possible error: Consider checking number " + key + " manually")