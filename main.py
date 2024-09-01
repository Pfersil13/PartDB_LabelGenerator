import yaml
import json
import os
import socket

import smallPartDb
import shutil
from PIL import ImageFont

PART_NAME_MAX_SIZE = 240
def eng_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'k' in x:
        if x.endswith('k'):
            return float(x.replace('k', '')) * 1000
        if len(x) > 1:
            return float(x.replace('k', '.')) * 1000
        return 1000.0
    if 'M' in x:
        if x.endswith('M'):
            return float(x.replace('M', '')) * 1000000
        if len(x) > 1:
            return float(x.replace('M', '.')) * 1000000
        return 1000000.0
    return float(x)

def search_and_replace(file_path, search_word, replace_word):
   with open(file_path, 'r') as file:
      file_contents = file.read()

      updated_contents = file_contents.replace(search_word, replace_word)

   with open(file_path, 'w') as file:
      file.write(updated_contents)

if __name__ == '__main__':
    with open("settings.yaml") as stream:
        try:
            settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise RuntimeError(exc)
    partDb = smallPartDb.smallPartDb(settings['host'], settings['token'])

    # show info
    print(partDb)
    print("List all parts")

    storageLoaction = "LDOs"
    status = partDb.getParts()
    if status.status_code == 200:
        for p in partDb.parts:
            print(str(p['id']) + ": " + p['name'])

    status = partDb.getPartsByStorage(storageLoaction)
    if status.status_code == 200:
        for c in partDb.partsbyStorage:
            print("id: " + str(c['id']) + ", name: " + c['name'])

    PART_1 = partDb.partsbyStorage[0]['name']
    PART_2 = partDb.partsbyStorage[1]['name']
    PART_3 = partDb.partsbyStorage[2]['name']


    shutil.copy('Plantillax3.txt', 'WorkingFile.txt')
    font = ImageFont.truetype("arial.ttf", size=30, encoding="unic")
    size = font.getlength(storageLoaction)
    fontSize = 30
    print(size)

    if size > PART_NAME_MAX_SIZE:
        fontSize = PART_NAME_MAX_SIZE*30/size

    search_and_replace("WorkingFile.txt", "{PRINTER_DARKNESS}", "10")
    search_and_replace("WorkingFile.txt", "{PART_NAME_SIZE}", str(fontSize))
    search_and_replace("WorkingFile.txt", "{PART_QRCODE}", str(partDb.id))
    search_and_replace("WorkingFile.txt","{STORAGE_NAME}",str(storageLoaction))
    search_and_replace("WorkingFile.txt","{PART_1}",str(PART_1))
    search_and_replace("WorkingFile.txt", "{PART_2}", str(PART_2))
    search_and_replace("WorkingFile.txt", "{PART_3}", str(PART_3))





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
    print("get all footprints")
    status = partDb.getFootprints()
    if status.status_code == 200:
        for c in partDb.footprints:
            print("id: " + str(c['id']) + ", name: " + c['name'])

    print("get all categories")
    status = partDb.getCategories()
    if status.status_code == 200:
        for c in partDb.categories:
            print("id: " + str(c['id']) + ", name: " + c['name'] + ", full_path: " + c['full_path'])

    print("get all manufacturers")
    status = partDb.getManufacturers()
    if status.status_code == 200:
        for m in partDb.manufacturers:
            print("id: " + str(m['id']) + ", name: " + m['name'])

    print("get all attachments")
    status = partDb.getAttachments()
    if status.status_code == 200:
        for m in partDb.attachments:
            print("id: " + str(m['id']) + ", name: " + m['name'])

    print("get all footprints")
    status = partDb.getFootprints()
    if status.status_code == 200:
        for f in partDb.footprints:
            print("id: " + str(f['id']) + ", name: " + f['name'])

    print("get all storageLocations")
    status = partDb.getStore_Location()
    if status.status_code == 200:
        for f in partDb.storage_location:
            print("id: " + str(f['id']) + ", name: " + f['name'])
"""

