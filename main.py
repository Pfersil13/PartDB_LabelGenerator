"""
Python script for printing labels from [partDb](https://github.com/Part-DB/Part-DB-server)
Author: Pablo Fernández Silva
Created: 1st September, 2024
"""

import yaml
import json
import os
import socket
import requests
import smallPartDb
import shutil
from PIL import ImageFont
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as img
import os
import LabelTypeFunctions

if __name__ == '__main__':
    with open("settings.yaml") as stream:
        try:
            settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise RuntimeError(exc)
    partDb = smallPartDb.smallPartDb(settings['host'], settings['token'])
    LabelTemplate = LabelTypeFunctions.LabelType()
    # show i2nfo
    print(partDb)

    """Search for label templates on the directory "Templates """

    dir = 'Templates'  # The path
    ext = '.txt'  # File extension of the desired files

    # Store all file with "txt" extension on the lsit "txt_files"
    txt_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(ext)]

    print("I founded the following templates:")

    for i in range(0, len(txt_files), 1):
        print("\t" + str(i + 1) + "-\t" + txt_files[i])  # It's used to display all files with an Index

    # Now we can use the index to select the desired template
    index = input("Select which template to use (1 - " + str(len(txt_files)) + "):")
    if index.isnumeric() == 1:  # T esting if is a numeric value or a file name
        file_name = txt_files[int(index) - 1]  # Assign filename
        print("Perfect")
    else:
        print("Wrong data")
        LabelTemplate.is_a_file_name()
        # Ideally here must be evaluated if the user had typed the tempalte name instead of the number.
        # Right now is not implemented

    """Search metadata on the desired template"""

    # First the template is copy into a file called WorkingFile
    # Now is easier to work with the file withou erasing/ modifying the template
    shutil.copy('Templates/' + file_name, 'Templates/WorkingFile/WorkingFile.txt')
    f = open("Templates/WorkingFile/WorkingFile.txt", "r")
    i = 0
    text = f.readlines()   # Read the text in lines
    f.close()
    while text[i][0] == "#":    # If metadata "#" is present on the line evaluated we can continue searching info
        i = i + 1
        if 'Label Type:' in text[i]:        # First label type is searched
            if 'Storage_location' in text[i]:   # If found, read which label type is
                label = "Storage_location"
                print("Label type storage selected")
        if 'Storage Location BoxWidth:' in text[i]: # Read data
            box = int(text[i][28:])
        if 'Number of parts:' in text[i]:
            nParts = int(text[i][18:])

    if label == "Storage_location": # Evaluate the label type, this should be a switch case statement
        LabelTemplate.StorageLabel(nParts, box)

    """Plot label using labelary API"""

    # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = 'http://api.labelary.com/v1/printers/8dpmm/labels/3.14961x1.5748/0/'

    f = open("Templates/WorkingFile/WorkingFile.txt", "rb")
    files = {'file': f.read()}
    response = requests.post(url, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open('Templates/WorkingFile/label.png', 'wb') as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
    else:
        print('Error: ' + response.text)

    """ Could be used to open picture on desktop image viewer"""
    """
    image = Image.open("label.png")
    image.show()
    """

    """ Plot the label using matplotlib"""

    # reading png image file

    im = img.imread("Templates/WorkingFile/label.png")

    # show image
    plt.imshow(im)
    plt.show()

    """ Print the label on TCP printer"""  # Commented because I do not want to waste all my labels testing :)


"""
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.1.68"
    port = 9100
    try:
        mysocket.connect((host, port))  # connecting to host
        f = open("WorkingFile.txt", "rb")
        a = f.read()
        mysocket.send(a)  # using bytes
        mysocket.close()  # closing connection
    except:
        print("Error with the connection")
"""
