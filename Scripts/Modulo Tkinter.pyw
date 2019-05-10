#Importación de librerías
from MainModule import*
from tkinter.filedialog import askopenfilename


#Varibles Globales
matrizFrases = []
DiccionarioPersonajes = {}
contP=[0]
def procesoBoton(matrizFrases,listbox,etiqueta1,contP):
    try:
        repet=int(numeroveces.get())
        for i in range(repet):
            contP[0]=nuevaFrase(matrizFrases, DiccionarioPersonajes, contP[0])
            etiqueta1.config(text=definirMayor(DiccionarioPersonajes))
            listbox.delete(0,END)
            for pj in matrizFrases:
                for frase in pj[1]:
                    listbox.insert(END, pj[3]+":"+frase+ " - " + pj[0])
    except ValueError:
        msg=messagebox.showinfo("Error","Debe insertar un número de veces para poder buscar frases")
def preguntarBackup():
    global contP
    MsgBox =messagebox.askquestion('Guardar Backup', 'Desea respaldar la información almacenada hasta el momento?')
    if MsgBox == 'yes':
        crearXML(matrizFrases, DiccionarioPersonajes,contP[0])
        top.destroy()
    else:
        top.destroy()
def shareF(matrizFrases):
    ventana=Tk()
    ventana.geometry("800x350")
    ventana.title("Compartir Frases")
    lb=Listbox(ventana,width=100,selectmode=MULTIPLE)
    lb.place(x=34,y=107)
    correo=Entry(ventana,width=50)
    correo.place(x=36,y=279)
    comentario=Label(ventana,text="Selecciones las frases que desea compartir",font=("Comic Sans",15))
    comentario.place(x=36,y=80)
    for pj in matrizFrases:
        for frase in pj[1]:
            lb.insert(END, pj[3] + ":" + frase + " - " + pj[0])
    obtener=Button(ventana,text="Sacar Frases",command= lambda :EnviarCorreo(lb))
    obtener.place(x=700,y=150)
def sacarLista(lb):
    lista = []
    listaFr = lb.curselection()
    for item in listaFr:
        var = lb.get(item)
        lista.append(var)
    return lista
def EnviarCorreo(lb):
    lista=sacarLista(lb)
    enviarCorreo(lista)

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


try:
    cargarBackup(matrizFrases,DiccionarioPersonajes)
    contP.pop(0)
    contP.append(cargarContador())
    Tk().withdraw()
    back=messagebox.showinfo("Info Backup","Se encontró un backup, las frases apareceran en pantalla la primer vez que presione el botón de buscar frases")

except:
    noback=messagebox.showinfo("Info Backup","No se encontró un backup")
top=Tk()
top.geometry("850x400")
top.title("Star Wars Frases")
top.config(bg="gray95")
top.protocol("WM_DELETE_WINDOW", preguntarBackup)
labelinfo=Label(text="Frases Star Wars",font=("Comic Sans",15))
labelinfo.place(x=33,y=80)
listbox = Listbox(top,width=100)
listbox.place(x=34,y=107)
etiqueta1= Label(top,text=definirMayor(DiccionarioPersonajes),font=("Comic Sans",15))
etiqueta1.place(x=33,y=270)
numeroveces=Entry(top)
numeroveces.place(x=691,y=125)
solicitar= Button(top,text="Pedir frases",command= lambda: procesoBoton(matrizFrases,listbox,etiqueta1,contP))
solicitar.place(x=695,y=162)
share= Button(top,text="Compartir frases",command= lambda : shareF(matrizFrases))
share.place(x=695,y=190)
cargarShareB=Button(top,text="Cargar frases compartidas",command=cargarShare)
cargarShareB.place(x=695,y=217)
top.mainloop()
