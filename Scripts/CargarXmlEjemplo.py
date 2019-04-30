import xml.etree.ElementTree as ET
from xml.dom import minidom
tree=ET.parse('123.xml')
root=tree.getroot()
ET.dump(tree)



