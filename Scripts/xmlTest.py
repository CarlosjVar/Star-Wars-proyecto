
import xml.etree.ElementTree as ET
from xml.dom import minidom
#def func
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
#pp
matriz=[["Yoda","fsdf"],["Alejo","sdfsdf"],["Gay","fdfdf"],["Pitovare","Dios"]]
top = ET.Element("Personajes")

child = ET.SubElement(top,"Yoda")
child.text="Yoda es gay"

child2 = ET.SubElement(top, "Chewbaca")
child2.text="CHEWBACA ES DIOS"

child3 = ET.SubElement(top, "Luke_Skywalker")
child3.text="Luke me la pela"

child4= ET.SubElement(top,"Storm_Tropper")
child4.text="No le importo a nadie"
ET.dump(top)
tree=ET.ElementTree(top)
tree.write("123.xml")
myattrib="Se uno con el uno"
pitovare=prettify(top)
with open('personajes.xml',"w") as file:
    file.write(pitovare)


