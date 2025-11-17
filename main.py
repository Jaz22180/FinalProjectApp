from tkinter import filedialog
import numpy as np
import tkinter.messagebox
from customtkinter import *
from tkinter import * 
from tkinter import filedialog
import numpy as np
import tkinter.messagebox
import sys                                                          #NUEVO JAZ
sys.stdout.reconfigure(encoding='utf-8')                            #NUEVO JAZ

class App:
    
    # Constructor
    def __init__(self, master):
        
        # Atributos/Características de la clase
        # Listas de frames del GIF de inicio (splash screen)

        self.state_stop = False
        self.cont_headers = 0
        self.master = master
        self.master.title("Análisis bibliográficos de textos")
        self.master.state("zoomed")
        self.master.resizable(0, 0) 
        self.ancho = master.winfo_screenwidth()
        self.alto = master.winfo_screenheight()
        self.file_name_t = ""

        # Botones
        self.txts_btn = CTkButton(master, text = "Selecciona la ruta del archivo a examinar", command = self.elegirPathTXTs, width = self.ancho/3, height = self.alto/12)
        self.txts_btn.place(x = self.ancho/12, y = self.alto/12)

        # Etiquetas
        self.nombre_archivo_label = CTkLabel(master, text = "Nombre del archivo: ", anchor = 'w', width = self.ancho/3, height = self.alto/14)
        self.nombre_archivo_label.place(x = self.ancho/12, y = self.alto/12 * 2)
        self.referencias = CTkLabel(master, text = "Referencias: ", anchor = 'w', width = self.ancho/3, height = self.alto/19) #NUEVO JAZ
        self.referencias.place(x = self.ancho/12, y = self.alto/12 * 3)                                                        #NUEVO JAZ

        # Nombre de los desarroladores     
        self.dev_label = CTkLabel(master, text = "Developers: Jazmín, Alexis & Emiliano", anchor = 'w', width = self.ancho/6, height = self.alto/25)  
        self.dev_label.place(x = self.ancho / 8 * 6, y = self.alto / 35 * 28) 

    # Métodos
    def elegirPathTXTs(self):
        
        # Try and except para cachar los errores al cargar el achivo
        try:
            
            self.cont = 0
            # Abrir la ruta del archivo
            self.filename = filedialog.askopenfilename(initialdir='C:/', title = "Abrir archivo para procesar sus textos")
            # Inicializar los renglones del archivo
            self.filas = []
            
            if self.filename != "":
                # Obtener solo el nombre del archivo sin todo el path
                self.file_name_t = os.path.basename(self.filename)
                # Setear el texto de la etiqueta para que incluya el nombre del archivo
                self.nombre_archivo_label.configure(text = "Nombre del archivo: " + str(self.file_name_t), anchor = "w")
                self.nombre_header = "PROTOCOLO DE INVESTIGACIÓN"
                # "Barrer" el archivo línea por línea
                with open(self.filename, "r", encoding="utf-8-sig", errors="replace") as archivo:
                    for linea in archivo:
                        # linea.isspace(): la línea contiene puros espacios en blanco
                        if linea != "" and linea.isspace() == False and self.eliminarHeader(self.nombre_header, linea): 
                            # rstrip() elimina el salto de línea al final
                            self.filas.append(linea.rstrip())
                            # Imprimir en consola la fila "cont" 
                            self.cont += 1

                    # Imprimir archivo filtrado
                    for i in range (0, len(self.filas), 1):
                        print(self.filas[i]) 

                
                tkinter.messagebox.showinfo(title = "Aviso", message="Archivo Cargado")
            print(str(self.filename))
            self.ReferenciasAPA7()                                          #NUEVO JAZ

        except FileNotFoundError:
            tkinter.messagebox.showinfo(title = "Error", message="El archivo no existe en la ruta especificada")

        except Exception as e:
            print("ERROR REAL:", e)                                                                                      #NUEVO JAZ
            tkinter.messagebox.showinfo(title="Error", message="Un error ocurrió al momento de cargar el archivo")

    # Método para eliminar el header que tiene una imagen 
    def eliminarHeader(self, text_b, lin):
        if text_b in lin:
            # Eliminar el header completo porque aparecen 3 líneas:
            # el número de páf, espacio y nómbre del header
            if(self.cont_headers != 0):
                # Eliminar las filas que pertenecen al header
                self.filas.pop() # Espacios en blanco
                self.filas.pop() # Número de página
                self.cont -= 2
            self.cont_headers += 1

            return False
        else:
            return True

    #Método para comprobar si las referencias están en formato APA7           #NUEVO JAZ
    def ReferenciasAPA7(self):
        #ENCONTRANDO SECCIÓN DE REFERENCIA
        fin = None
        for i, fila in enumerate(self.filas):
            if "REFERENCIAS" in fila:
               fin = i
               break

        referencias_encontradas = self.filas[fin + 1:]
        referencias_separadas = []   # lista final de referencias ya separadas
        referencia_actual = []       # acumula una referencia

        for fila in referencias_encontradas:
            referencia_actual.append(fila)

        # Cuando aparece DOI se cierra una referencia
        if "DOI" in fila.upper():
            referencias_separadas.append(referencia_actual)
            referencia_actual = []        # reiniciar para la siguiente referencia

    
        if referencia_actual:
            referencias_separadas.append(referencia_actual)

    # Convertir a texto para mostrar
        texto = ""
        for ref in referencias_separadas:
            texto += "\n".join(ref) + "\n\n"

        self.referencias.configure(text=texto, anchor="w")



GUI = CTk( )
AppTXTs = App(GUI)
AppTXTs.master.mainloop()

