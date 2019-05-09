from tkinter import *
from tkinter import messagebox
import tkinter
from MainModule import*

#Varibles Globales
matrizFrases = []
DiccionarioPersonajes = {}
contP=0
def procesoBoton(matrizFrases,listbox,etiqueta1,contP):
    try:
        repet=int(numeroveces.get())
        for i in range(repet):
            contP = nuevaFrase(matrizFrases, DiccionarioPersonajes, contP)
            etiqueta1.config(text=definirMayor(DiccionarioPersonajes))
            listbox.delete(0,END)
            for pj in matrizFrases:
                for frase in pj[1]:
                    listbox.insert(END, pj[3]+":"+frase+ " - " + pj[0])
    except ValueError:
        msg=messagebox.showinfo("Error","Debe insertar un número de veces para poder buscar frases")
def solicitar():
    msg=messagebox.showinfo("Soy el marco de la ventana", "Soy el contenido de la ventana")
def shareF(matrizFrases):
    ventana=Tk()
    ventana.geometry("800x350")
    lb=Listbox(ventana,width=100,selectmode=MULTIPLE)
    lb.place(x=34,y=107)
    for pj in matrizFrases:
        for frase in pj[1]:
            lb.insert(END, pj[3] + ":" + frase + " - " + pj[0])
    obtener=Button(ventana,text="Sacar Frases",command= lambda :sacarLista(lb))
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
    enviarCorreo(lb)


    
top=Tk()
top.geometry("850x400")
listbox = Listbox(top,width=100)
listbox.place(x=34,y=107)
etiqueta1= Label(top,text=definirMayor(DiccionarioPersonajes),font=("Comic Sans",15))
etiqueta1.grid(row=0,column=1)
numeroveces=Entry(top)
numeroveces.place(x=691,y=125)
solicitar= Button(top,text="Pedir frases",command= lambda: procesoBoton(matrizFrases,listbox,etiqueta1,contP))
solicitar.place(x=725,y=162)
share= Button(top,text="Compartir frases",command= lambda : shareF(matrizFrases))
share.place(x=725,y=190)
top.mainloop()
