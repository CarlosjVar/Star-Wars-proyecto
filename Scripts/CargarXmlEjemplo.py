import xml.etree.ElementTree as ET
from xml.dom import minidom
tree=ET.parse('Backup.xml')
root=tree.getroot()
#ET.dump(tree)
for child in root.iter("Name"):
    print(child.attrib.get("infoP"))
    for child2 in root.iter("Phrases"):
        keys=child.attrib.keys
        print(child2.attrib.get("frases"))



