import yaml

import smallPartDb

from PIL import ImageFont


PART_NAME_MAX_SIZE = 240
partList = []
part_name = []

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

    def StorageLabel(self, nParts, box):
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
                # print("id: " + str(c['id']) + ", name: " + c['name'])
                i = i + 1
                print(str(i) + "- " + c['name'])


        if i == nParts:
            print("Preview")
            for c in range(0, nParts , 1):
                part = partDb.partsbyStorage[c]['name']
                part_name.append(part)
        else:
            print("This label requires  " + str(nParts) + " parts, specify the number pls:")
            for c in range(0, nParts, 1):
                partNumber = int(input("Part_" + str(c + 1) + ": "))
                part_name.append(partDb.partsbyStorage[partNumber]['name'])



        font = ImageFont.truetype("arial.ttf", size=30, encoding="unic")
        size = font.getlength(storage)
        fontSize = 30
        # print(size)

        if size > box:
            fontSize = PART_NAME_MAX_SIZE * 30 / size
        url_QR = "http://" + partDb.host + "/en/store_location/" + str(partDb.id) + "/parts"

        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PRINTER_DARKNESS}", "10")
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_NAME_SIZE}", str(fontSize))
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_QRCODE}", url_QR)
        self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{STORAGE_NAME}", str(storage))

        for c in range(0, nParts, 1):
            # print(c)
            string = "{PART_" + str(c + 1) + "}"
            # print(string)
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt",string , str(part_name[c]))


        return self





