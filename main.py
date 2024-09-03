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


if __name__ == '__main__':
    with open("settings.yaml") as stream:
        try:
            settings = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise RuntimeError(exc)
    partDb = smallPartDb.smallPartDb(settings['host'], settings['token'])
    LabelTemplate = LabelTypeFunctions.LabelType()
    # show info
    print(partDb)
    dir = 'Templates'
    ext = '.txt'
    txt_files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(ext)]

    print("I founded the following templates:")

    for i in range(0, len(txt_files), 1):
        print("\t" + str(i+1) + "-\t" + txt_files[i])

    index = input("Select which template to use (1 - " + str(len(txt_files)) + "):")
    if index.isnumeric() == 1:
        file_name = txt_files[int(index) - 1]
        print("Perfect")
    else:
        print("Wrong data")

    shutil.copy('Templates/' + file_name, 'Templates/WorkingFile/WorkingFile.txt')
    f = open("Templates/WorkingFile/WorkingFile.txt", "r")
    i = 0
    text = f.readlines()
    f.close()
    while text[i][0] == "#":
        i = i + 1
        if 'Label Type:' not in text[i]:
            continue
        else:
            if 'Storage_location' in text[i]:
                if()
                print("Label type storage selected")
                LabelTemplate.StorageLabel()
                """
                storageLoaction = input("Enter storage location: ")
                print("You selected " + storageLoaction + "")
                print("There are the following parts")
                print(" ID      |        Part Name      ")
                """
                """
                status = partDb.getParts()
                if status.status_code == 200:
                    for p in partDb.parts:
                        print(str(p['id']) + ": " + p['name'])
                """
                """
                status = partDb.getPartsByStorage(storageLoaction)
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
                size = font.getlength(storageLoaction)
                fontSize = 30
                # print(size)

                if size > PART_NAME_MAX_SIZE:
                    fontSize = PART_NAME_MAX_SIZE*30/size
                url_QR= "http://" + partDb.host + "/en/store_location/" + str(partDb.id) + "/parts"

                search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PRINTER_DARKNESS}", "10")
                search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_NAME_SIZE}", str(fontSize))
                search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_QRCODE}", url_QR)
                search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{STORAGE_NAME}", str(storageLoaction))
                search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_1}", str(PART_1))
                search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_2}", str(PART_2))
                search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_3}", str(PART_3))

                """

    # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = 'http://api.labelary.com/v1/printers/8dpmm/labels/3.14961x1.5748/0/'

    f = open("Templates/WorkingFile/WorkingFile.txt", "rb")
    files = {'file': f.read()}
    # headers = {'Accept': 'application/pdf'}  # omit this line to get PNG images back
    response = requests.post(url, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open('Templates/WorkingFile/label.png', 'wb') as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
    else:
        print('Error: ' + response.text)


    """
    image = Image.open("label.png")
    image.show()
    """
    # reading png image file

    im = img.imread("Templates/WorkingFile/label.png")

    # show image
    plt.imshow(im)
    plt.show()


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
