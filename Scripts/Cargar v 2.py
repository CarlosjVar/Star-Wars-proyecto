import xml.etree.ElementTree as ET
import codecs
# string_data = open('Backup.xml')
# with codecs.open('Backup.xml', 'r', encoding='latin-1') as xml:
#     tree = ET.parse(xml)
# root=tree.getroot()
# ET.dump(tree)
# for child in root.iter("Name"):
#     print(child.attrib.get("infoP"))
#     for child2 in root.iter("Phrases"):
#         keys=child.attrib.keys
#         frase=child2.attrib.get("frases")
#         frase=frase.replace("","’")
#         print(frase)
#
#
root=ET.Element("Raiz Principal")
ramita1=ET.SubElement(root,"Soy un ramita muy gei")
ramita2=ET.SubElement(root,"Soy una raminta no tan gei")
ramitaderamita1=ET.SubElement(ramita1,"Lo que dice ramita2 es mentira")
arbol=ET.ElementTree(root)
ET.dump(arbol)

