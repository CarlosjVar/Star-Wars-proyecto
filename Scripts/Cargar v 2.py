import xml.etree.ElementTree as ET
import codecs
string_data = open('Backup.xml')
with codecs.open('Backup.xml', 'r', encoding='latin-1') as xml:
    tree = ET.parse(xml)
root=tree.getroot()
ET.dump(tree)
for child in root.iter("Name"):
    print(child.attrib.get("infoP"))
    for child2 in root.iter("Phrases"):
        keys=child.attrib.keys
        frase=child2.attrib.get("frases")
        frase=frase.replace("","’")
        print(frase)


