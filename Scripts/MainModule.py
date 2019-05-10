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
import datetime
from requests.exceptions import HTTPError
import re
import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename


#Definición de funciones

def obtenerFrase ():
    while True:
        if revisarInternet()==True:
            break
        else:
            msg=messagebox.showinfo("Error","No hay conexión a internet")
            return False
    respuesta=requests.get("http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote")
    try:
        respuesta.raise_for_status()
        respuesta=respuesta.text
        respuesta=dict(eval(respuesta))   
        print(respuesta)
        return respuesta
    except HTTPError as http_err:
        msg1=messagebox.showinfo("Error","La API no ha respondido")
        return False

def montarEnDicccionario(DiccionarioPersonajes,contP,cita):
    personaje=cita[1]
    if personaje not in DiccionarioPersonajes.keys():
        contP+=1
        letraF=(personaje[len(personaje)-1]).upper()
        DiccionarioPersonajes[personaje]=[("#"+personaje[0]+str("%03d"%contP)+"-"+letraF),1]
    else:
        lista=DiccionarioPersonajes[personaje]
        ant=lista[1]
        lista[1]=ant+1
        DiccionarioPersonajes[personaje]=lista
    return [DiccionarioPersonajes,contP]

def montarEnMatriz (matrizFrases,cita,DiccionarioPersonajes,contP):
    if cita == False:
        return
    diccionario=montarEnDicccionario(DiccionarioPersonajes,contP,cita)
    for i in range(len(matrizFrases)):
        fila=matrizFrases[i]
        if cita[1]==fila[0]:
            if cita[0] not in fila[1]:
                (matrizFrases[i])[1].append(cita[0])
                (matrizFrases[i])[2].append(cita[2])
                return [matrizFrases,diccionario[0],diccionario[1]]
            else:
                return [matrizFrases,diccionario[0],diccionario[1]]
    nuevaFila=[cita[1],[cita[0]],[cita[2]],(diccionario[0])[cita[1]][0]]
    matrizFrases.append(nuevaFila)
    return [matrizFrases,diccionario[0],diccionario[1]]
    
def determinarCita ():
    diccionario = obtenerFrase()
    if diccionario == False:
        return False
    cita = diccionario["starWarsQuote"]
    if diccionario["id"]==15:
        cita=cita.split (". — ")
        cita.append(diccionario["id"])
        return cita
    cita = cita.split(" — ")
    if len (cita)==1:
        cita=cita[0].split (" ? ")
        if len (cita)==1:
            cita=cita[0].split (" - ")
            if len (cita)==1:
                cita=cita[0].split (" _ ")
    cita[1]=re.sub(r' \([^)]*\)','', cita[1])
    cita.append(diccionario["id"])
    return cita

def crearXML(matrizFrases,DiccionarioPersonajes,contP):
    root=ET.Element("Backup")
    matriz=ET.SubElement(root,"Matriz")
    for lista in matrizFrases:
        personaje=ET.SubElement(matriz,"Personaje",)
        name=ET.SubElement(personaje,"Name",infoP=lista[0],Code=lista[3])
        for frase in lista[1]:
            phrase = ET.SubElement(personaje, "Phrases",frases=frase)
        for id in lista[2]:
            ID= ET.SubElement(personaje,"ID",ID=str(id))
    Diccionario=ET.SubElement(root,"Diccionario")
    for key in DiccionarioPersonajes:
        personaje = ET.SubElement(Diccionario, "Personaje")
        for i in range(1):
            codigoP=ET.SubElement(personaje,"App_Code",Key=key,Code=DiccionarioPersonajes[key][i])
            llamadaAPI=ET.SubElement(personaje,"Llamadas",Llamadas=str(DiccionarioPersonajes[key][i+1]))
    variables=ET.SubElement(root,"Variables",contador=str(contP))
    xml=(prettify(root))
    with open('Backup.xml', "w") as file:
        file.write(xml)
    return

def cargarBackup(matrizFrases,DiccionarioPersonajes):
    with codecs.open('Backup.xml', 'r', encoding='latin-1') as xml:
        tree = ET.parse(xml)
    root = tree.getroot()
    for personaje in root.iter("Personaje"):
        for name in personaje.iter("Name"):
            lista=[]
            listaFrases = []
            listaID=[]
            lista.append(name.attrib.get("infoP"))
            for frase in personaje.iter("Phrases"):
                frase = frase.attrib.get("frases")
                frase = frase.replace("", "’")
                listaFrases.append(frase)
            lista.append(listaFrases)
            for id in personaje.iter("ID"):
                ids= id.attrib.get("ID")
                listaID.append(int(ids))
            lista.append(listaID)
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
def cargarContador():
    with codecs.open('Backup.xml', 'r', encoding='latin-1') as xml:
        tree = ET.parse(xml)
    root = tree.getroot()
    for contador in root.iter("Variables"):
        contP1=int(contador.attrib.get("contador"))
    return contP1


def prettify(elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
def shareBackup(lista):
    fecha = str(datetime.datetime.now())
    fecha = fecha[0:19].replace(":", "-").replace(" ", "-")
    root=ET.Element("Share")
    for frase in lista:
        ET.SubElement(root,"Frase",Phrase=frase)
    archivo="share-"+fecha+".xml"
    xml = (prettify(root))
    with open(archivo, "w") as file:
        file.write(xml)
    file.close()
    return archivo

def cargarShareXML(archivo):
    listaFra=[]
    with codecs.open(archivo, 'r', encoding='latin-1') as xml:
        tree = ET.parse(xml)
    root = tree.getroot()
    ET.dump(tree)
    for frase in root.iter("Frase"):
        frase = frase.attrib.get("Phrase")
        frase = frase.replace("", "’")
        listaFra.append(frase)
    print(listaFra)
    return listaFra
        

def definirMayor (DiccionarioPersonajes):
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

def enviarCorreo (matrizFrases,destinatario):
    while True:
        if revisarInternet()==True:
            break
        else:
            msg=messagebox.showinfo("Error","No hay conexión a internet")
            return
    nombre = shareBackup(matrizFrases)
    context = ssl.create_default_context()
    while True:
        if destinatario==None or destinatario=="":
            msg=messagebox.showinfo("Error","Favor ingresar un correo de destino")
            return
        elif re.match(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?",destinatario):
            break
        else:
            msg=messagebox.showinfo("Error","El correo ingresado no tiene el formato de una dirección válida")
            return
    msg = MIMEMultipart()
    msg['From'] = "lagalleradepython@gmail.com"
    msg['To'] = destinatario
    msg['Subject'] = "Citas de StarWars"
    mensaje = "Alguien desea compartir las siguientes citas de StarWars contigo"
    msg.attach(MIMEText(mensaje, 'plain'))
    filename = nombre
    attachment = open(nombre, "rb")
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
            msg=messagebox.showinfo("Error","El correo ingresado contiene carácteres no válidos")
            os.remove(nombre) 
            return 
    msg=messagebox.showinfo("Envío de frases","Correo enviado")
    attachment.close()
    os.remove(nombre)
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

def nuevaFrase (matrizFrases,DiccionarioPersonajes,contP):
    cita=determinarCita()
    if cita!=False:
        Provisional=montarEnMatriz (matrizFrases,cita,DiccionarioPersonajes,contP)
        contP=Provisional[2]
        DiccionarioPersonajes=Provisional[1]
        matrizFrases=Provisional[0]
        return contP
    else:
        return contP
#PP
# print  ("1 - Sacar frase")
# print  ("2 - Sacar mayor")
# print  ("3 - Sacar diccionario")
# print  ("4 - Sacar matriz")
# print  ("5 - Guardar bakcup")
# print  ("6 - Cargar bakcup")
# print  ("7 - Enviar bakcup")
# print  ("Otra cosa - Salir")
# while True:
#     opcion = int(input ("Que quiere hacer?: "))
#     if opcion==1:
#         contP=nuevaFrase (matrizFrases,DiccionarioPersonajes,contP)
#     elif opcion==2:
#         print(definirMayor(DiccionarioPersonajes))
#     elif opcion==3:
#         print (DiccionarioPersonajes)
#     elif opcion==4:
#         print (matrizFrases)
#     elif opcion==5:
#         crearXML (matrizFrases,DiccionarioPersonajes)
#     elif opcion==6:
#         cargarBackup (matrizFrases,DiccionarioPersonajes)
#         contP=cargarContador(contP)
#     elif opcion==7:
#         enviarCorreo (matrizFrases)
#     else:
#         break





