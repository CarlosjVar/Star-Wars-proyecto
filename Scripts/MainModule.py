#Importacón de librerías
import xml.etree.ElementTree as ET
import requests
from xml.dom import minidom
import codecs
#Variables Globales
matrizFrases = []
DiccionarioPersonajes = {}
contP=0

#Definición de funciones

def obtenerFrase ():
    respuesta=(requests.get("http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote")).text
    respuesta=dict(eval(respuesta))
    print(respuesta)
    return respuesta

def montarEnDicccionario(cita):
    global contP
    global DiccionarioPersonajes
    personaje=cita[1]
    if personaje not in DiccionarioPersonajes.keys():
        global contP
        contP+=1
        letraF=(personaje[len(personaje)-1]).upper()
        DiccionarioPersonajes[personaje]=[("#"+personaje[0]+str("%03d"%contP)+"-"+letraF),1]
    else:
        lista=DiccionarioPersonajes[personaje]
        ant=lista[1]
        lista[1]=ant+1
        DiccionarioPersonajes[personaje]=lista
    return DiccionarioPersonajes

def montarEnMatriz ():
    global matrizFrases
    cita=determinarCita()
    diccionario=montarEnDicccionario(cita)
    for i in range(len(matrizFrases)):
        fila=matrizFrases[i]
        if cita[1]==fila[0]:
            if cita[0] not in fila[1]:
                (matrizFrases[i])[1].append(cita[0])
                (matrizFrases[i])[2].append(cita[2])
                return
            else:
                return
    nuevaFila=[cita[1],[cita[0]],[cita[2]],diccionario[cita[1]][0]]
    matrizFrases.append(nuevaFila)
    return
    
def determinarCita ():
    diccionario = obtenerFrase()
    cita = diccionario["starWarsQuote"]
    cita = cita.split(" — ")
    if len (cita)==1:
        cita=cita[0].split (" ? ")
        if len (cita)==1:
            cita=cita[0].split (" - ")
    cita.append(diccionario["id"])
    return cita

def crearXML():
    global matrizFrases
    global DiccionarioPersonajes
    global contP
    root=ET.Element("Backup")
    matriz=ET.SubElement(root,"Matriz")
    for lista in matrizFrases:
        personaje=ET.SubElement(matriz,"Personaje",)
        name=ET.SubElement(personaje,"Name",infoP=lista[0],ID=lista[2],Code=lista[3])
        for frase in lista[1]:
            phrase = ET.SubElement(personaje, "Phrases",frases=frase)
    Diccionario=ET.SubElement(root,"Diccionario")
    for key in DiccionarioPersonajes:
        personaje = ET.SubElement(Diccionario, "Personaje")
        for i in range(1):
            codigoP=ET.SubElement(personaje,"App_Code",Key=key,Code=DiccionarioPersonajes[key][i])
            llamadaAPI=ET.SubElement(personaje,"Cantidad_de_llamadas_a_la_API",Llamadas=str(DiccionarioPersonajes[key][i+1]))
    variables=ET.SubElement(root,"Variables",contador=str(contP))
    tree=ET.ElementTree(root)
    xml=(prettify(root))
    with open('Backup.xml', "w") as file:
        file.write(xml)
    return

def cargarBackup():
    global matrizFrases
    global DiccionarioPersonajes
    with codecs.open('Backup.xml', 'r', encoding='latin-1') as xml:
        tree = ET.parse(xml)
    root = tree.getroot()
    for personaje in root.iter("Personaje"):
        for name in personaje.iter("Name"):
            lista=[]
            listaFrases = []
            lista.append(name.attrib.get("infoP"))
            for frase in personaje.iter("Phrases"):
                frase = frase.attrib.get("frases")
                frase = frase.replace("", "’")
                listaFrases.append(frase)
            lista.append(listaFrases)
            lista.append(name.attrib.get("ID"))
            lista.append(name.attrib.get("Code"))
            matrizFrases.append(lista)
    for personaje in root.iter("Diccionario"):
        for info in personaje.iter("App_Code"):
            for contador in personaje.iter("Cantidad_de_llamadas_a_la_API"):
                DiccionarioPersonajes[info.attrib.get("Key")]=[info.attrib.get("Code"),int(contador.attrib.get("Llamadas"))]
    print(matrizFrases)
    print(DiccionarioPersonajes)
    return

def prettify(elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

def definirMayor ():
    global DiccionarioPersonajes
    mayor=0
    resul=""
    for key in DiccionarioPersonajes:
        if DiccionarioPersonajes[key][1]>mayor:
            mayor=DiccionarioPersonajes[key][1]
            resul=key
        elif DiccionarioPersonajes[key][1]==mayor:
            resul=resul+", "+key
    return "El o los personajes con más resultados: "+resul
            
#PP
while True:
    opcion = int(input ("Que quiere hacer?: "))
    if opcion==1:
       montarEnMatriz()
    else:
        #print (matrizFrases)
        print (DiccionarioPersonajes)
        break
print(definirMayor())
#crearXML()
#cargarBackup()
#print(matrizFrases[0][1])





