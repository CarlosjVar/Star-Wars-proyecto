#Importacón de librerías
import xml.etree.ElementTree as ET
import requests
from xml.dom import minidom
import codecs
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email import validate_email
from email.mime.base import MIMEBase 
from email import encoders
import http.client as httplib

#Variables Globales
matrizFrases = []
DiccionarioPersonajes = {}
contP=0

#Definición de funciones

def obtenerFrase ():
    while True:
        if revisarInternet()==True:
            break
        else:
            x = input ("No hay una conexión a internet disponible, revise su conexión y digite 1 para devolverse"\
                        +"o cualquier otra tecla para reintentar: ")        
            if x == "1":
                return False
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
    if cita == False:
        return
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
    if diccionario == False:
        return False
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
            llamadaAPI=ET.SubElement(personaje,"Llamadas",Llamadas=str(DiccionarioPersonajes[key][i+1]))
            print(DiccionarioPersonajes[key][i+1])
    variables=ET.SubElement(root,"Variables",contador=str(contP))
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
    for diccionario in root.iter("Diccionario"):
        for personaje in diccionario:
            for info in personaje.findall("App_Code"):
                name=info.attrib.get("Key")
                code=info.attrib.get("Code")
            for contador in personaje.findall("Llamadas"):
                peticiones = int(contador.attrib.get("Llamadas"))
            DiccionarioPersonajes[name]= [code,peticiones]
    return

def prettify(elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
def shareBackup(lista):
    root=ET.Element("Share")
    for frase in lista:
        ET.SubElement(root,Frase,Phrase=frase)
    xml = (prettify(root))
    with open('Backup.xml', "w") as file:
        file.write(xml)

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
    if mayor==0:
        return "No se han solicitado frases aún"
    else:
        return "El o los personajes con más resultados: "+resul

def enviarCorreo ():
    while True:
        if revisarInternet()==True:
            break
        else:
            x = input ("No hay una conexión a internet disponible, revise su conexión, digite 1 para devolverse o cualquier otra tecla para reintentar: ")        
            if x == "1":
                return
    context = ssl.create_default_context()
    while True:
        destinatario=input("Digite el correo electrónico del destinatario: ")
        if validate_email(destinatario):
            break
        else:
            print ("El correo brindado no tiene el formato de una dirección válida, favor reingresarlo")
    msg = MIMEMultipart()
    msg['From'] = "lagalleradepython@gmail.com"
    msg['To'] = destinatario
    msg['Subject'] = "Citas de StarWars"
    mensaje = "Alguien desea compartir las siguientes citas de StarWars contigo"
    msg.attach(MIMEText(mensaje, 'plain'))
    filename = "Backup.xml"
    attachment = open("Backup.xml", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    text = msg.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login("lagalleradepython@gmail.com", "Joseph20*")
            server.sendmail("lagalleradepython@gmail.com",destinatario,text)
        except UnicodeEncodeError:
            print("Dado que la dirección de destino contiene el caracter 'ñ', el mensaje no se ha enviado")
            return
    print ("Mensaje Enviado")
    return


def revisarInternet():
    conn = httplib.HTTPConnection("www.google.com", timeout=4)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False
            
#PP
print  ("1 - Sacar frase")
print  ("2 - Sacar mayor")
print  ("3 - Sacar diccionario")
print  ("4 - Sacar matriz")
print  ("5 - Guardar bakcup")
print  ("6 - Cargar bakcup")
print  ("7 - Enviar bakcup")
print  ("Otra cosa - Salir")
while True:
    opcion = int(input ("Que quiere hacer?: "))
    if opcion==1:
       montarEnMatriz()
    elif opcion==2:
        print(definirMayor())
    elif opcion==3:
        print (DiccionarioPersonajes)
    elif opcion==4:
        print (matrizFrases)
    elif opcion==5:
        crearXML ()
    elif opcion==6:
        cargarBackup ()
    elif opcion==7:
        enviarCorreo ()
    else:
        break 





