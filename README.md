# SST-Photo-Processing-Suite Project Documentation

**Objective:**
The purpose of the project is to develop a system that achieves the following:
* **Phase 1**: Records numerical values from a given photo, essentially capturing each runner's RFID bib number.
* **Phase 2**: Uses said recorded number to rename each individual picture (renaming feature should include the bib number recorded from phase one).
* **Phase 3**: Uploads the new zip file of renamed photos back to SmugMug through the API.

**Dependencies:**
* *Flask 2.0.1*: Python API used to build web-applications. Codependent on Jinja template engine and the Werkzeug WSGI toolkit. 
* *Jinja2 3.0.1*: Web template engine 
* *MarkupSafe 2.0.1*: Makes text safe for HTML and XML. 
* *Pillow 8.3.1*: Python Imaging Library with image processing capabilities
* *Werkzeug 2.0.1*: Comprehensive web server gateway interface web application library  
* *beautifulsoup4 4.9.3*: Pulls data out of HTML 
* *cachetools*: Memorizes collections and decorators
* *certifi*: Collection of root certificates for validating the trustworthiness of SSL certificates
* *chardet*: Character encoding detector
* *click*: Creates beautiful command line interfaces in a composable way with as little code as necessary
* *google*: Encapsulates the google cloud dependencies
* *google-api-core*: Supports Google API clients
* *google-auth*: Provides ability to authenticate the Google APIs being used
* *google-cloud-vision*: Enables developer to understand the content of an image by encapsulating powerful ML models in an easy to use way
* *googleapis-common-protos*: Generates common protos
* *grpcio*: Package for gRPC Python tools
* *idna*: Internationalised Domain Names in Applications protocol
* *itsdangerous*: Used when you send some data to an untrusted environment and back. 
* *packaging*: Provides utilities that include version handling, specifiers, markers, requirements, tags, and utilities. 
* *pip*: Perhaps the **most** important module in this entire list because it is the installer program for Python. 
* *proto-plus*: Provides protocol buffer message classes and objects that largely behave like native types.
* *protobuf*: Protocol buffers
* *pyasn1*: Modules expressed in form of pyasn1 classes
* *pyasn1-modules*: Extension to above dependency
* *pyparsing*: Provides a library of classes that client code uses to construct the grammar directly in Python code. 
* *pytz*: Brings the Olson tz database in Python
* *requests*: Elegant and simple HTTP library for python
* *rsa*: Supports encryption and decryption, signing and verifying signatures.
* *setuptools*: Designed to facilitate packaging Python projects
* *six*: Provides utility functions for smoothing over the differences between the Python versions. 
* *soupsieve*: Extension to Beautifulsoup4
* *urllib3*: Used with Requests and Pip
* *vision*: Used with Google Cloud API

*Note*: If you need to manually install these depencies, go to terminal and run ```python3 -m pip install ______```. Please ensure that you have the right dependency version, as some of them are not updated to the newest version in the market. As a reminder, we are using Python 3.9 for the purposes of this project. The correct depency versions are attached to this email. 

**How to Run the Code:**
The important files in this project are in the App folder (you must run the code in this directory), pipeline_app.py, and pipeline_cropAndFinal.py. The App directory, along with pipeline_app.py, hold the components of the Flask web application which is where the user will input a zip file of the pictures. To turn to the App directory, write ```cd App``` in the terminal. Then, run ```python3 pipeline_app.py```. This will run the Flask web application. To access it, you must click the link that shows up on terminal (it will say ```Running on http://127.0.0.1:8080/```). Once the web application pops up on Google Chrome (or some other application), in which the user can now input a zip file of pictures. Once the zip file has been uploaded, run ```python3 pipeline_cropAndFinal.py```. At this point, the OCR system will start running and automatically change the labels of each picture. If no number is detected, the label will read as "LOST"; otherwise, the detected numbers will be appended to the file name.     

**Notes**
* If at any point you want to end the Flask application from running on the terminal, enter in CTRL + C. 

**Reference Links**

https://codelabs.developers.google.com/codelabs/cloud-vision-api-python#0
   (Part 8-- Perform Text Detection)

We are using pipeline_cropAndFinal.py as the testing draft. 

https://cloud.google.com/vision/docs/handwriting#vision_fulltext_detection_gcs-python

**Miscellaneous**
To run: Either clone this repository or simply download pipeline_cropAndFinal.py

For information and arguments help for the code, run ```python3 pipeline_cropAndFinal.py --help```

**Things in the Backburner**
* Less run time
* Higher accuracy for triathlon
* Determining bib number from multiple similar images
* Customizing the front end Flask website for the photographers to make it more user-friendly
