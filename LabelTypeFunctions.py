import shutil
import yaml
import smallPartDb

from PIL import ImageFont

STORAGE_NAME_SIZE = 20
pxmm = 8
PART_NAME_MAX_SIZE = 240
partList = []
part_name = []

with open("settings.yaml") as stream:
    try:
        settings = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise RuntimeError(exc)
partDb = smallPartDb.smallPartDb(settings['host'], settings['token'])

from main import drawer_x, drawer_y
from main import drawer_x_2, drawer_y_2

class LabelType():

    def is_a_file_name(self):
        # To DO
        return None
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
        if status == None:
            print("Storage Location not found")
            return
            # To do, detect typing errors/similar worlds
        else:
            if status.status_code == 200:
                i = 0
                part_name = []
                for c in partDb.partsbyStorage:
                    # print("id: " + str(c['id']) + ", name: " + c['name'])
                    i = i + 1
                    print(str(i) + "- " + c['name'])

            if i == nParts:
                print("Preview")
                for c in range(0, nParts , 1):
                    part = partDb.partsbyStorage[c]['name']
                    part_name.append("- " + part)
            else:
                print("This label requires  " + str(nParts) + " parts, specify the number pls:")

                for c in range(0, nParts, 1):
                    partNumber = int(input("Part_" + str(c + 1) + ": "))
                    if partNumber != 0:
                        part_name.append("- " + partDb.partsbyStorage[partNumber - 1]['name'])
                    else:
                        for d in range(c, nParts, 1):
                            part_name.append("")
                        break

            font = ImageFont.truetype("arial.ttf", size=30, encoding="unic")
            size = font.getlength(storage)
            fontSize = 30
            # print(size)

            coordenada_rx = pxmm * drawer_x

            if size + 113 > coordenada_rx:
                fontSize = (coordenada_rx-113) * 30 / size
            url_QR = "http://" + partDb.host + "/en/store_location/" + str(partDb.id) + "/parts"


            coordenada_ry = 10 + pxmm* drawer_y
            Diferencia_1 = 120 - 60
            Diferencia_2 = coordenada_ry-160
            print(str(Diferencia_2/pxmm))
            if Diferencia_2/pxmm < 5:
                Suma = Diferencia_1+Diferencia_2
                y_1 = Suma/2 + 60 - 5
            else:
                y_1 = 100

            y_2 = y_1 + 30
            y_3 = y_2 + 30

            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{Y_1}", str(y_1))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{Y_2}", str(y_2))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{Y_3}", str(y_3))



            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{RECTANGLE_X}", str(pxmm * drawer_x))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{RECTANGLE_Y}", str(pxmm * drawer_y))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PRINTER_DARKNESS}", "10")
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_NAME_SIZE}", str(fontSize))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_QRCODE}", url_QR)
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{STORAGE_NAME}", str(storage))


            maximum = 0
            oversize_flag = False
            for c in range(0, nParts, 1):
                # print(c)
                string = "{PART_" + str(c + 1) + "}"
                # print(string)
                self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", string, str(part_name[c]))

                font2 = ImageFont.truetype("arial.ttf", size=23, encoding="unic")
                size_storage = font2.getlength(part_name[c])
                max_length = 122 + size_storage
                if max_length > coordenada_rx:
                    oversize_flag = True
                    if size_storage > maximum:
                        maximum = size_storage

            if oversize_flag == True:
                fontSize_storage = (coordenada_rx - 122) * 20 / maximum
                print(fontSize_storage)
            else:
                fontSize_storage = 20
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{STORAGE_NAME_SIZE}", str(fontSize_storage))
        return self




    def Part_Label(self):


        part = input("Enter part name: ")
        print("You selected " + part + "")
        id = partDb.lookupPart(part)
        print(id)
        status = partDb.getParts()
        if status.status_code == 200:
            for p in partDb.parts:
                # print(str(p['id']) + ": " + p['name'])
                if str(p['id']) == str(id):
                    part_n = p['name']
                    part_description = p['description']
                    print(part_n)
                    print(part_description)

            junk, storage_location = partDb.getStorageByPart(id)
            if storage_location == "Gavetas":
                QR_Y = 110
                PART_NAME_Y = 50
                DESCRIPTION_Y = 80
                drawer_x_2 = 58  # 58
                drawer_y_2 = 15  # 15
            else:
                QR_Y = 120
                PART_NAME_Y = 60
                DESCRIPTION_Y = 90
                drawer_x_2 = 45  # 58
                drawer_y_2 = 20  # 15


            font = ImageFont.truetype("arial.ttf", size=30, encoding="unic")
            size = font.getlength(part_n)
            fontSize = 30
            # print(size)

            coordenada_rx = pxmm * drawer_x_2

            if size + 140 > coordenada_rx:
                fontSize = (coordenada_rx-140) * 30 / size
            url_QR = "http://" + partDb.host + "/en/part/" + str(id) + "#part_lots"

            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{QR_Y}", str(QR_Y))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_NAME_Y}", str(PART_NAME_Y))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{DESCRIPTION_Y}", str(DESCRIPTION_Y))


            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{RECTANGLE_X}", str(pxmm * drawer_x_2))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{RECTANGLE_Y}", str(pxmm * drawer_y_2))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PRINTER_DARKNESS}", "10")
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_NAME_SIZE}", str(fontSize))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_DESCRIPTION_SIZE}", str(20))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_DESCRIPTION_BOX}", str(coordenada_rx-140-10))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_QRCODE}", url_QR)
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_NAME}", str(part_n))
            self.search_and_replace("Templates/WorkingFile/WorkingFile.txt", "{PART_DESCRIPTION}", str(part_description))


        return self


    def search_label_metadata(self, file_name):
        """Search metadata on the desired template"""

        # First the template is copy into a file called WorkingFile
        # Now is easier to work with the file withou erasing/ modifying the template
        shutil.copy('Templates/' + file_name, 'Templates/WorkingFile/WorkingFile.txt')
        f = open("Templates/WorkingFile/WorkingFile.txt", "r")
        i = 0
        text = f.readlines()  # Read the text in lines
        f.close()
        while text[i][0] == "#":  # If metadata "#" is present on the line evaluated we can continue searching info
            i = i + 1
            if 'Label Type:' in text[i]:  # First label type is searched
                if 'Storage_location' in text[i]:  # If found, read which label type is
                    label = "Storage_location"
                    print("Label type storage selected")
                if 'Part' in text[i]:  # If found, read which label type is
                    label = "Part"
                    print("Label type part selected")
            if 'Storage Location BoxWidth:' in text[i]:  # Read data
                box = int(text[i][28:])
            if 'Number of parts:' in text[i]:
                nParts = int(text[i][18:])
            if 'Resolution (dpmm):' in text[i]:
                pxmm = int(text[i][21:])

        self.erase_metadata(i)
        return (label, box, nParts, pxmm)


    def erase_metadata(self, n_lines):
        """ Quit metadata from worrking file"""

        f = open("Templates/WorkingFile/WorkingFile.txt", "r")
        lines = f.readlines()
        f.close()

        with open("Templates/WorkingFile/WorkingFile.txt", 'w') as fp:
            # iterate each line

            for number, line in enumerate(lines):
                # delete line 5 and 8. or pass any Nth line you want to remove
                # note list index starts from 0
                if number >= n_lines:
                    fp.write(line)
        fp.close()



