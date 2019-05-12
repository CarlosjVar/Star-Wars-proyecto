#Importación de librerías
from MainModule import*
from tkinter.filedialog import askopenfilename
import webbrowser
import os



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
                temp=nuevaFrase(matrizFrases, DiccionarioPersonajes, contP[0])
                if type(temp)==list:
                    contP[0]=temp[0]
                    break
                contP[0]=temp
                etiqueta1.config(text=definirMayor(DiccionarioPersonajes))
                listbox.delete(0,END)
                for pj in matrizFrases:
                    for frase in pj[1]:
                        listbox.insert(END, pj[3]+": "+frase+ " ~ " + pj[0])
        else:
            msg=messagebox.showinfo("Error","La cantidad de solicitudes debe ser un número mayor o igual a 1")
    except ValueError:
        msg=messagebox.showinfo("Error","Debe insertar un número de veces que se solicitarán frases")
        
def preguntarBackup(contP):
    MsgBox =messagebox.askquestion('Guardar Backup', '¿Desea hacer un archivo de respaldo de las frases actuales?')
    if MsgBox == 'yes':
        crearXML(matrizFrases, DiccionarioPersonajes,contP[0])
        top.destroy()
    else:
        top.destroy()


def BotonDeCompartir(matrizFrases):
    ventana=Tk()
    ventana.geometry("1317x270")
    ventana.title("Compartir Frases")
    frasesCompartir=Listbox(ventana,width=217,selectmode=MULTIPLE)
    frasesCompartir.place(x=6,y=40)
    correo=Entry(ventana,width=50)
    correo.place(x=335,y=215)
    etiqueta5=Label(ventana,text="Seleccione las frases que desea compartir: ",font=("Comic Sans",11))
    etiqueta5.place(x=7,y=15)
    etiqueta6=Label(ventana,text="Dirección del correo electrónico del destinatario: ",font=("Comic Sans",11))
    etiqueta6.place(x=7,y=212)
    BotonDeRefrescar (matrizFrases,frasesCompartir)
    obtener=Button(ventana,text="Enviar frases seleccionadas",command= lambda:prepararCorreo(frasesCompartir,correo,ventana))
    obtener.place(x=665,y=212)
    refrescar=Button(ventana,text="Actualizar listado de frases por enviar",command= lambda:BotonDeRefrescar(matrizFrases,frasesCompartir))
    refrescar.place(x=1000,y=212)
    ventana.mainloop()

def BotonDeRefrescar (matrizFrases,frasesCompartir):
    frasesCompartir.delete(0,'end')
    for pj in matrizFrases:
        for frase in pj[1]:
            frasesCompartir.insert(END, pj[3] + ": " + frase + " ~ " + pj[0])
    return
    

def prepararCorreo(frases,correo,ventana):
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

def abrirManual():
    os.startfile("Manual_del_Usuario.pdf")
   
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
top=Tk()
top.geometry("1317x325")
top.title("Frases de Star Wars")
top.config(bg="gray95")
try:
    cargarBackup(matrizFrases,DiccionarioPersonajes)
    contP.pop(0)
    contP.append(cargarContador())
    Tk().withdraw()
    back=messagebox.showinfo("Archivo de respaldo","Se encontró un backup previo, se han agregado al listado las frases contenidas en este")
except:
    noback=messagebox.showinfo("Archivo de respaldo","No se ha encontrado un archivo de respaldo")
top.protocol("WM_DELETE_WINDOW",lambda: preguntarBackup(contP))
listbox = Listbox(top,width=217, selectmode=BROWSE)
listbox.place(x=6,y=40)
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
cargarShareB=Button(top,text="Cargar frases compartidas",command=cargarShare)
cargarShareB.place(x=1100,y=249)
acercaDe=Button(top, text="Acerca De",command=abrirManual)
acercaDe.place(x=611,y=290)
top.mainloop()
