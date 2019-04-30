import xml.etree.ElementTree as ET
from xml.dom import minidom
tree=ET.parse('Backup.xml')
root=tree.getroot()
ET.dump(tree)



