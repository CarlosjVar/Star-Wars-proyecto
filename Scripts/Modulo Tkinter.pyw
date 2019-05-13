###################################################
#Elaborado por: Carlos Varela y Joseph Tenorio
#Fecha de creación: 08/05/2019
#Fecha de última de modificación: 13/05/2019
#Versión: 3.7.3
###################################################

#Importación de librerías
from MainModule import *
from tkinter.filedialog import askopenfilename
import os
import winsound


#Definiciión de variables globales
matrizFrases = []
DiccionarioPersonajes = {}
contP=[0]

#Definición de botones
def BotonDeSolicitar(matrizFrases,listbox,etiqueta1,contP):
    """
    Funcionamiento: Llama las funciones necesarias para pedir de frases
    Entradas: matrizFrases (list), listbox (listbox,TKinter), etiqueta1(label,TKinter), contP (list)
    Salidas: N/A
    """
    try:
        repet=int(numeroveces.get())
        if repet>0 and repet<=50:
            if repet<25:
                dividirFrases (matrizFrases,listbox,etiqueta1,contP,repet)
            else:
                dividirFrases (matrizFrases,listbox,etiqueta1,contP,25)
                dividirFrases (matrizFrases,listbox,etiqueta1,contP,(repet-25))
        else:
            msg=messagebox.showinfo("Error","La cantidad de solicitudes debe ser un número mayor o igual a 1 y menor o igual a 50")
            sonidoError()
    except ValueError:
        msg=messagebox.showinfo("Error","Debe insertar un número de veces que se solicitarán frases")
    return

def BotonDeCompartir(matrizFrases):
    """
    Funcionamiento: Llama los elementos necesarios para el envío de correo electrónico
    Entradas: matrizFrases (list)
    Salidas: N/A
    """
    ventana=Tk()
    ventana.geometry("1330x270")
    ventana.title("Compartir Frases")
    ventana.resizable(width=False, height=False)
    frame = Frame(ventana)
    frame.place(x=6, y=40)
    frasesCompartir=Listbox(frame,width=217,selectmode=MULTIPLE)
    frasesCompartir.pack(side="left", fill="y")
    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.config(command=frasesCompartir.yview)
    scrollbar.pack(side="right", fill="y")
    correo=Entry(ventana,width=50)
    correo.place(x=335,y=215)
    etiqueta5=Label(ventana,text="Seleccione las frases que desea compartir: ",font=("Comic Sans",11))
    etiqueta5.place(x=7,y=15)
    etiqueta6=Label(ventana,text="Dirección del correo electrónico del destinatario: ",font=("Comic Sans",11))
    etiqueta6.place(x=7,y=212)
    BotonDeRefrescar (matrizFrases,frasesCompartir)
    obtener=Button(ventana,text="Enviar frases seleccionadas",command= lambda:prepararCorreo(frasesCompartir,correo))
    obtener.place(x=665,y=212)
    refrescar=Button(ventana,text="Actualizar listado de frases por enviar",command= lambda:BotonDeRefrescar(matrizFrases,frasesCompartir))
    refrescar.place(x=1000,y=212)
    ventana.mainloop()
    return

def BotonDeRefrescar (matrizFrases,frasesCompartir):
    """
    Funcionamiento: Actualiza la listbox de frases por compartir
    Entradas: matrizFrases (list), frasesCompartir (listbox,TKinter)
    Salidas: N/A
    """
    frasesCompartir.delete(0,'end')
    for pj in matrizFrases:
        for frase in pj[1]:
            frasesCompartir.insert(END, pj[3] + ": " + frase + " ~ " + pj[0])
    return

def BotonDeManual():
    """
    Funcionamiento: Llama al manual del usuario
    Entradas: N/A
    Salidas: N/A
    """
    try:
        os.startfile("Manual_del_Usuario.pdf")
        return
    except:
        msg=messagebox.showinfo("Error","El manual del usuario no se ha podido abrir, favor verificar la existencia de esté junto a un programa lector de archivos PDF")
        return
   
def BotonDeCargarShare():
    """
    Funcionamiento: Permite la lectura de archivos "Share" enviados por correo electrónico
    Entradas: N/A
    Salidas: N/A
    """
    ventana = Tk()
    ventana.geometry("680x280+140+550")
    ventana.title("Frases Compartidas")
    ventana.resizable(width=False, height=False)
    ventana.lift
    frame2 = Frame(ventana)
    frame2.place(x=6, y=40)
    lbe = Listbox(frame2, width=100, selectmode=SINGLE)
    lbe.pack(side="left", fill="y")
    scrollbar = Scrollbar(frame2, orient="vertical")
    scrollbar.config(command=lbe.yview)
    scrollbar.pack(side="right", fill="y")
    etiqueta2=Label(ventana,text="Un usuario de ¨Frases de Star Wars¨ decidió compartir estas frases contigo",font=("Comic Sans",15))
    etiqueta2.place(x=5,y=10)
    filename = askopenfilename()
    try:
        lista=cargarShareXML(filename)
        for frase in lista:
            lbe.insert(END,frase)
    except:
        msgb=messagebox.showinfo("Error","No se pudo leer el archivo")
        ventana.destroy()
    ventana.mainloop()
    return

#Funciones auxiliares de los botones y la interfaz
def dividirFrases (matrizFrases,listbox,etiqueta1,contP,repet):
    """
    Funcionamiento: Inserta las frases en la listbox indicada y muestra el personaje con más respuestas
    Entradas: matrizFrases (list), listbox (listbox,TKinter), etiqueta1(label,TKinter), contP (list), repet (int)
    Salidas: N/A
    """
    for i in range(repet):
        while True:
            temp=nuevaFrase(matrizFrases, DiccionarioPersonajes, contP[0])
            if type(temp)!=tuple:
                break
            else:
                contP[0]=temp[0]
        if type(temp)==list:
            contP[0]=temp[0]
            break
        contP[0]=temp
        etiqueta1.config(text=definirMayor(DiccionarioPersonajes))
        listbox.delete(0,END)
        for pj in matrizFrases:
            for frase in pj[1]:
                listbox.insert(END, pj[3]+": "+frase+ " ~ " + pj[0])
    return

def preguntarBackup(contP):
    """
    Funcionamiento: Pregunta al usuario si desea guardar un respaldo y llama a la respectiva función si es el caso
    Entradas: contP (list)
    Salidas: N/A
    """
    MsgBox =messagebox.askquestion('Guardar Backup', '¿Desea hacer un archivo de respaldo de las frases actuales?')
    if MsgBox == 'yes':
        crearXML(matrizFrases, DiccionarioPersonajes,contP[0])
        top.destroy()
    else:
        top.destroy()
    return

def prepararCorreo(frases,correo):
    """
    Funcionamiento: Prepara la lista de frases a ser enviadas por correo electrónico y llama a la función respectiva
    Entradas: frases (list), correo (Entry,TKinter)
    Salidas: N/A
    """
    destinatario=correo.get()
    lista = []
    listaFr = frases.curselection()
    for item in listaFr:
        var = frases.get(item)
        lista.append(var)
    if lista==[]:
        msg=messagebox.showinfo("Error","Debe seleccionar al menos una frase para compartir")
        return
    if enviarCorreo(lista,destinatario)==True:
        return

#Programa Principal (interfaz gráfica)
root=Tk()
root.geometry("100x100")
try:
    cargarBackup(matrizFrases,DiccionarioPersonajes)
    contP.pop(0)
    contP.append(cargarContador())
    Tk().withdraw()
    back=messagebox.showinfo("Archivo de respaldo","Se encontró un backup previo, se han agregado al listado las frases contenidas en este")

except:
    noback=messagebox.showinfo("Archivo de respaldo","No se ha encontrado un archivo de respaldo")
root.destroy()
top=Tk()
top.geometry("1330x325")
top.title("Frases de Star Wars")
top.config(bg="gray95")
top.protocol("WM_DELETE_WINDOW",lambda: preguntarBackup(contP))
top.resizable(width=False,height=False)
top.iconbitmap("icono.ico")
frame=Frame(top)
frame.place(x=6,y=40)
listbox = Listbox(frame ,width=217, selectmode=BROWSE)
listbox.pack(side="left", fill="y")
scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="right", fill="y")
for pj in matrizFrases:
    for frase in pj[1]:
        listbox.insert(END, pj[3]+": "+frase+ " ~ " + pj[0])
etiqueta3 = Label(top,text="Listado actual de frases: ",font=("Cominc Sans",11))
etiqueta3.place(x=7,y=15)
etiqueta1= Label(top,text=definirMayor(DiccionarioPersonajes),font=("Comic Sans",11))
etiqueta1.place(x=7,y=210)
etiqueta4= Label(top,text="Indique la cantidad de frases a solicitar: ",font=("Comic Sans",11))
etiqueta4.place(x=7,y=250)
numeroveces=Entry(top)
numeroveces.place(x=275,y=253)
solicitar= Button(top,text="Solicitar frases",command= lambda: BotonDeSolicitar(matrizFrases,listbox,etiqueta1,contP))
solicitar.place(x=415,y=249)
share= Button(top,text="Enviar frases por correo electrónico",command= lambda : BotonDeCompartir(matrizFrases))
share.place(x=700,y=249)
cargarShareB=Button(top,text="Cargar frases compartidas",command=BotonDeCargarShare)
cargarShareB.place(x=1100,y=249)
acercaDe=Button(top, text="Acerca de...",command=BotonDeManual)
acercaDe.place(x=611,y=290)
top.mainloop()
