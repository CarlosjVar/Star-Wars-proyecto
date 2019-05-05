#Definición de Funciones
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from validate_email import validate_email
from email.mime.base import MIMEBase 
from email import encoders
import http.client as httplib

#PP
def enviarCorreo ():
    while True:
        if revisarInternet()==True:
            break
        else:
            x = input ("No hay una conexión a internet disponible, revise su conexión y presione enter para continuar")        
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
            server.login("lagalleradepython@gmail.com", "Joseph20*")
            server.sendmail("lagalleradepython@gmail.com",destinatario,text)
    print ("Mensaje Enviado")
    return

def revisarInternet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False

#PP
enviarCorreo()
