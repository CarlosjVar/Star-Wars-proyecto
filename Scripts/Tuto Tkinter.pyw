from tkinter import*
from tkinter import messagebox
def funcion():
    ventana=Tk()
    ventana.mainloop()
ventana=Tk()
ventana.title("Estar Guars")
ventana.geometry("650x300")
# marco=Frame(ventana)
# marco.config(bg="PaleGreen3")
# ventana.config(relief="raised")
# ventana.config(bd=15)
#botones
#etiquetas
etiqueta=Label(ventana,text="Soy una etiqueta")
etiqueta.grid(row=0,column=1)
#etiqueta.place(x="300",y="150")
#cuadros de texto
cuadro=Entry(ventana)
cuadro.grid(row=0,column=2)
#posiciones 3 formas
#.grid .place .pack
#botones
boton=Button(ventana,text="No soy un botón",command=funcion)
boton.grid(row=1,column=1)
ventana.mainloop()
