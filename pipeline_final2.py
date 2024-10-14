#Not using this one

from __future__ import print_function
from google.cloud import vision
import os, io

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'teak-clarity-218502-59fd687fc810.JSON'

#image right here
path = input("Enter the path: ")

client = vision.ImageAnnotatorClient()

with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)


#performing text detection
response = client.document_text_detection(image=image)

appendToFile = ""

for page in response.full_text_annotation.pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            for word in paragraph.words:
                word_text = ''.join([
                    symbol.text for symbol in word.symbols
                ])
                if(word_text.isnumeric()):
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))
                    appendToFile += "_"+word_text

    """
    vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
    print('bounds:', ",".join(vertices))
    """

#TODO Once all text is processed, add this string to file name
print(appendToFile)