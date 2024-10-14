#https://codelabs.developers.google.com/codelabs/cloud-vision-api-python#0
#   (Part 8-- Perform Text Detection)

from __future__ import print_function
from google.cloud import vision
import os, io
import matplotlib.pyplot as plt

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'teak-clarity-218502-59fd687fc810.JSON'

#image right here
path = input("Enter the path: ")

client = vision.ImageAnnotatorClient()

with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)


#performing text detection
response = client.text_detection(image=image)

appendToFile = ""

for text in response.text_annotations:
    #print('=' * 30) #comment this out
    #print(text.description) #comment this out

    if(text.description.isnumeric()):
        print(text.description) #comment this once it is confirmed that appending to file name works
        print(text.confidence)
        appendToFile += "_"+text.description

    vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
    print('bounds:', ",".join(vertices))

#TODO Once all text is processed, add this string to file name
print(appendToFile)