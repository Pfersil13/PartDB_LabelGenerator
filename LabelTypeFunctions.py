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
PART_NAME_MAX_SIZE = 240

with open("settings.yaml") as stream:
    try:
        settings = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise RuntimeError(exc)
partDb = smallPartDb.smallPartDb(settings['host'], settings['token'])

class LabelType():


    def search_and_replace(self, file_path, search_word, replace_word):
        with open(file_path, 'r') as file:
            file_contents = file.read()

            updated_contents = file_contents.replace(search_word, replace_word)

        with open(file_path, 'w') as file:
            file.write(updated_contents)

    def StorageLabel(self):
        storage = input("Enter storage location: ")
        print("You selected " + storage + "")
        print("There are the following parts")
        print(" ID      |        Part Name      ")

        """
        status = partDb.getParts()
        if status.status_code == 200:
            for p in partDb.parts:
                print(str(p['id']) + ": " + p['name'])
        """

        status = partDb.getPartsByStorage(storage)
        if status.status_code == 200:
            i = 0
            for c in partDb.partsbyStorage:
                print("id: " + str(c['id']) + ", name: " + c['name'])
                i = i + 1

        if i == 3:
            print("Preview")
        else:
            print("This label requires only 3 parts, specify the IDs pls:")
            # input("Part_1: ")
            # input("Part_2: ")
            # input("Part_3: ")
        PART_1 = partDb.partsbyStorage[0]['name']
        PART_2 = partDb.partsbyStorage[1]['name']
        PART_3 = partDb.partsbyStorage[2]['name']

        font = ImageFont.truetype("arial.ttf", size=30, encoding="unic")
        size = font.getlength(storage)
        fontSize = 30
        # print(size)

        if size > PART_NAME_MAX_SIZE:
            fontSize = PART_NAME_MAX_SIZE * 30 / size
        url_QR = "http://" + partDb.host + "/en/store_location/" + str(partDb.id) + "/parts"

        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PRINTER_DARKNESS}", "10")
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_NAME_SIZE}", str(fontSize))
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_QRCODE}", url_QR)
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{STORAGE_NAME}", str(storage))
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_1}", str(PART_1))
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_2}", str(PART_2))
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_3}", str(PART_3))

        return fontSize





