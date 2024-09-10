"""
Python script for printing labels from [partDb](https://github.com/Part-DB/Part-DB-server)
Author: Pablo Fernández Silva
Created: 1st September, 2024
"""

import yaml
import json
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
import time

label_x = 80
labe_y = 40

drawer_x = 50  # 50
drawer_y = 25  # 25

drawer_x_2 = 45  # 58
drawer_y_2 = 20  # 15

tcp_printer = []
lines = []

"""This function is in charge of reading the CMD input and detecting if the user is using any special keyword
such as SETTINGS or HELP
"""


def CMD_Read(text):
    data = input(text)
    global valid_input

    match data:
        case "Settings" | "settings":
            print("Settings selected")
            print("What do you want to do:")
            print("\t1- Change PartDB adress: ")
            print("\t2- Change PartDB token:")
            print("\t3- TPC Printer configuration:")
            selection = input("Write number option to select:")
            match selection:
                case "1"|"adress"|"Adress":
                    adress = input("Type the new PartDB adress:")
                    with open("settings.yaml", "r+") as f:
                        lines = f.readlines()
                        for i in range(0,len(lines),1):
                            if 'host' in lines[i]:
                                lines[i] = " host: " + "\"" + adress + "\" \n"
                        f.truncate(0)  # truncates the file
                        f.seek(0)  # moves the pointer to the start of the file
                        f.writelines(lines)  # write the new data to the file
                        f.close()
                case "2"|"token"|"Token":
                    token = input("Type the new PartDB token:")
                    with open("settings.yaml", "r+") as f:
                        lines = f.readlines()
                        for i in range(0, len(lines), 1):
                            if 'token' in lines[i]:
                                lines[i] = "token: " + "\"" + token + "\" ,\n"
                        f.truncate(0)  # truncates the file
                        f.seek(0)  # moves the pointer to the start of the file
                        f.writelines(lines)  # write the new data to the file
                        f.close()
                case "3"|"TCP Printer"|"tcp printer":
                    # Not yet implemented
                    tcp_printer.append(input("Type TCP printer IP:"))
                    tcp_printer.append(input("Type TCP printer port:"))
                    print(tcp_printer)

                case _:
                    return data

        case "Help" | "help":
            print("Help")
        case "Exit"|"exit":
            print("Bye, thank for using this application :)")
            time.sleep(1)
            valid_input = True
            return "Exit"
        case _:
            print("That's not a valid day of the week.")
            return data
    return "settings"


if __name__ == '__main__':
    with open("settings.yaml") as stream:
        try:
            settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise RuntimeError(exc)

    valid_input = False
    while not valid_input:
        partDb = smallPartDb.smallPartDb(settings['host'], settings['token'])
        # show info
        print("\n\n")
        print(partDb)
        if str(partDb) == "Error":
            token = input("Type correct the token: ")
            with open("settings.yaml", "r+") as f:
                lines = f.readlines()
                for i in range(0, len(lines), 1):
                    if 'token' in lines[i]:
                        lines[i] = "  token: " + "\"" + token + "\" ,\n"
                f.truncate(0)  # truncates the file
                f.seek(0)  # moves the pointer to the start of the file
                f.writelines(lines)  # write the new data to the file
                f.close()
                settings['token'] = token
                continue
        LabelTemplate = LabelTypeFunctions.LabelType()

        print("Type SETTINGS to change current API configuration")
        """Search for label templates on the directory "Templates """

        dir = 'Templates'  # The path
        ext = '.txt'  # File extension of the desired files

        # Store all file with "txt" extension on the lsit "txt_files"
        txt_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(ext)]

        print("\n")
        print("I founded the following templates:")

        for i in range(0, len(txt_files), 1):
            print("\t" + str(i + 1) + "-\t" + txt_files[i])  # It's used to display all files with an Index

        # Now we can use the index to select the desired template
        index = CMD_Read("Select which template to use (1 - " + str(len(txt_files)) + "):")
        # index = input("Select which template to use (1 - " + str(len(txt_files)) + "):")
        if index.isnumeric() == 1:  #T esting if is a numeric value or a file name
            file_name = txt_files[int(index) - 1]  # Assign filename
            print("Perfect")
        else:
            print("Wrong data")
            LabelTemplate.is_a_file_name()
            continue
            # Ideally here must be evaluated if the user had typed the tempalte name instead of the number.
            # Right now is not implemented


        """Read metadata template fields and erase them from working file"""

        metadata = LabelTemplate.search_label_metadata(file_name)

        # Evaluate the label type
        match metadata[0]:
            case "Storage_location":
                LabelTemplate.StorageLabel(metadata[2], metadata[1])
            case "Part":
                LabelTemplate.Part_Label()
            case _:
                None


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

        a = input("Print?")
        if a == "1":
            print("Pritning")
            mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = "192.168.1.68"
            port = 9100
            try:
                print("Hi")
                mysocket.connect((host, port))  # connecting to host
                print("TRE")
                f = open("Templates/WorkingFile/WorkingFile.txt", "rb")
                a = f.read()
                f.close()
                mysocket.send(a)  # using bytes
                mysocket.close()  # closing connection
            except:
                print("Error with the connection")

