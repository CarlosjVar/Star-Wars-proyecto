from tkinter import *
from tkinter import messagebox
import xml.etree.ElementTree as ET
import requests
from xml.dom import minidom
import itertools
def procesoBoton(matrizFrases,listbox,etiqueta1):
    montarEnMatriz()
    etiqueta1.config(text=definirMayor(DiccionarioPersonajes))
    listbox.delete(0,END)
    for pj in matrizFrases:
        for frase in pj[1]:
            listbox.insert(END, frase+ " - " + pj[0])
def solicitar():
    msg=messagebox.showinfo("Soy el marco de la ventana", "Soy el contenido de la ventana")
    
top=Tk()
top.geometry("850x400")
listbox = Listbox(top,width=100)
listbox.place(x=34,y=107)
etiqueta1= Label(top,text=definirMayor(DiccionarioPersonajes),font=("Comic Sans",24))
etiqueta1.grid(row=0,column=1)
numeroveces=Entry(top)
numeroveces.place(x=691,y=125)
solicitar= Button(top,text="Soy un botón",command= lambda: procesoBoton(matrizFrases,listbox,etiqueta1))
solicitar.place(x=725,y=162)
top.mainloop()
