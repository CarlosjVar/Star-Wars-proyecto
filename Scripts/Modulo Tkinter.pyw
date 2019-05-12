#Importación de librerías
from MainModule import*
from tkinter.filedialog import askopenfilename


#Varibles Globales
matrizFrases = []
DiccionarioPersonajes = {}
contP=[0]

#Definición de botones
def BotonDeSolicitar(matrizFrases,listbox,etiqueta1,contP):
    try:
        repet=int(numeroveces.get())
        if repet>0:
            for i in range(repet):
                contP[0]=nuevaFrase(matrizFrases, DiccionarioPersonajes, contP[0])
                etiqueta1.config(text=definirMayor(DiccionarioPersonajes))
                listbox.delete(0,END)
                for pj in matrizFrases:
                    for frase in pj[1]:
                        listbox.insert(END, pj[3]+": "+frase+ " - " + pj[0])
        else:
            msg=messagebox.showinfo("Error","La cantidad de solicitudes debe ser un número mayor o igual a 1")
    except ValueError:
        msg=messagebox.showinfo("Error","Debe insertar un número de veces para poder buscar frases")
        
def preguntarBackup(contP):
    MsgBox =messagebox.askquestion('Guardar Backup', '¿Desea respaldar la información almacenada hasta el momento?')
    if MsgBox == 'yes':
        crearXML(matrizFrases, DiccionarioPersonajes,contP[0])
        top.destroy()
    else:
        top.destroy()

def BotonDeCompartir(matrizFrases):
    ventana=Tk()
    ventana.geometry("1144x325")
    ventana.title("Compartir Frases")
    frasesCompartir=Listbox(ventana,width=188,selectmode=MULTIPLE)
    frasesCompartir.place(x=6,y=40)
    correo=Entry(ventana,width=50)
    correo.place(x=335,y=215)
    etiqueta5=Label(ventana,text="Seleccione las frases que desea compartir: ",font=("Comic Sans",11))
    etiqueta5.place(x=7,y=15)
    etiqueta6=Label(ventana,text="Dirección del correo electrónico del destinatario: ",font=("Comic Sans",11))
    etiqueta6.place(x=7,y=212)
    for pj in matrizFrases:
        for frase in pj[1]:
            frasesCompartir.insert(END, pj[3] + ": " + frase + " - " + pj[0])
    obtener=Button(ventana,text="Enviar frases seleccionadas",command= lambda:prepararCorreo(frasesCompartir,correo))
    obtener.place(x=665,y=212)

def prepararCorreo(frases,correo):
    destinatario=correo.get()
    lista = []
    listaFr = frases.curselection()
    for item in listaFr:
        var = lb.get(item)
        lista.append(var)
    print (lista)
    print (destinatario)
    enviarCorreo(lista,destinatario)
    return

def cargarShare():
    ventana = Tk()
    ventana.geometry("800x350")
    ventana.title("Frases Compartidas")
    etiqueta2=Label(ventana,text="Un usuario decidió compartir estas frases contigo",font=("Comic Sans",15))
    etiqueta2.place(x=34,y=70)
    lbe = Listbox(ventana, width=100, selectmode=SINGLE)
    lbe.place(x=34, y=107)
    filename = askopenfilename()
    try:
        lista=cargarShareXML(filename)
        for frase in lista:
            lbe.insert(END,frase)
    except:
        msgb=messagebox.showinfo("Error","No se pudo leer el archivo")
        ventana.destroy()
    ventana.mainloop()

#Programa Principal
try:
    cargarBackup(matrizFrases,DiccionarioPersonajes)
    contP.pop(0)
    contP.append(cargarContador())
    Tk().withdraw()
    back=messagebox.showinfo("Archivo de respaldo","Se encontró un backup previo, se han agregado al listado las frases contenidas en este")
except:
    noback=messagebox.showinfo("Archivo de respaldo","No se ha encontrado un archivo de respaldo")
top=Tk()
top.geometry("1144x325")
top.title("Frases de Star Wars")
top.config(bg="gray95")
top.protocol("WM_DELETE_WINDOW",lambda: preguntarBackup(contP))
listbox = Listbox(top,width=188, selectmode=BROWSE)
listbox.place(x=6,y=40)
for pj in matrizFrases:
    for frase in pj[1]:
        listbox.insert(END, pj[3]+": "+frase+ " - " + pj[0])
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
share.place(x=590,y=249)
cargarShareB=Button(top,text="Cargar frases compartidas",command=cargarShare)
cargarShareB.place(x=890,y=249)
top.mainloop()
