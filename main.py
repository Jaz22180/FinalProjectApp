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
import re                                                           # --> Emiliano

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
        #self.resultado_APA = []
        self.etiquetas_referencias = []   # lista para guardarlas

        # Botones
        self.txts_btn = CTkButton(master, text = "Selecciona la ruta del archivo a examinar", command = self.elegirPathTXTs, width = self.ancho/3, height = self.alto/12)
        self.txts_btn.place(x = self.ancho/12, y = self.alto/12)
        self.referencias_btn = CTkButton(master, text = "Referencias", command = self.crear_etiquetas_referencias, width = self.ancho/3, height = self.alto/12)

        # Etiquetas
        self.nombre_archivo_label = CTkLabel(master, text = "Nombre del archivo: ", anchor = 'w', width = self.ancho/3, height = self.alto/14)
        self.nombre_archivo_label.place(x = self.ancho/12, y = self.alto/12 * 2)                                                     

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
                    #for i in range (0, len(self.filas), 1):
                    #    print(self.filas[i]) 

                tkinter.messagebox.showinfo(title = "Aviso", message="Archivo Cargado")
            print(str(self.filename))
            self.ReferenciasAPA7()                                          #SE ACTIVAN REFERENCIAS Y BOTÓN DESPUES DE CARGAR ARCHIVO
            self.referencias_btn.place(x = self.ancho/2, y = self.alto/12)

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

    # Método para comprobar si las referencias están en formato APA7         
    def ReferenciasAPA7(self):
        #VARIABLES QUE SE VAN A UTILIZAR
        referencias_separadas = []   # lista final de referencias ya separadas
        referencia_actual = []       # acumula una referencia
        referencia_n = []
        patron = r"\([^)]+\)"                   # Buscando patrones de año entre parentesis --> Emiliano
        fechaAPA = ""                           # Auxiliar para detectar la fecha de la cita --> Emiliano
        i = 0                                   # Para conocer en que fila empieza la referencia --> Emiliano
        CountRef = 0                            # Contador de referencias encontradas--> Emiliano
        referencias = []                        # EN referencias SE ALMACENA CADA REFERENCIA POR SEPARADO
        autores_lista = []   
        resultado_APA = []


        #ENCONTRANDO SECCIÓN REFERENCIAS
        fin = None
        for i, fila in enumerate(self.filas):
            if "REFERENCIAS" in fila:
                fin = i
                break
        referencias_encontradas = self.filas[fin + 1:] #Cuenta la cantidad de filas desde que se encontro REFERENCIAS hasta el fin AQUÍ ESTAN TODAS LAS REFRENCIAS
        


        #VALIDANDO APA7
             # SEPARANDO CADA REFERENCIA
        for linea in referencias_encontradas:
            referencia_n.append(linea)
            if "doi" in linea.lower():
                referencias.append(referencia_n)
                referencia_n = []
        self.referencias = referencias
             #VALIDANDO SI ES APA
        referencias_unidas = [" ".join(ref) for ref in referencias]                     #uniendo los valores de la lista referencias para poder usar la función search
        patron = r"^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+,\s+[A-Z](?:\.[A-Z])*.\s*\(\d{4}\)\."        #Este patrón valida que 
        #patron = r"""^([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+,\s+[A-Z](?:\.[A-Z])*\.(?:,\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+,\s+[A-Z](?:\.[A-Z])*\. )*)\(\d{4}\)\.\s+.+?\.\s[A-Z][A-Za-zÁÉÍÓÚÑáéíóúñ\s]+,\s*\d+(?:\(\d+\))?,\s*\d+[-–]\d+\.\s*(https?://doi\.org/\S+|https?://\S+)$"""
        for ref in referencias_unidas:
                if re.search(patron, ref):
                    resultado_APA.append(f"Es APA7: {ref}")
                else:
                    resultado_APA.append(f"NO es APA7: {ref}")
        self.resultado_APA = resultado_APA

#PATRÓN "^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+,\s+[A-Z](?:\.[A-Z])*.\s*\(\d{4}\)\."
# ^                         Inicio del texto
#[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+    Primer apellido comienza en mayuscula y despues letras minusculas
#,                          Coma después del apellido
#\s+                        Espación despues de la coma
#[A-Z](?:\.[A-Z])*          Iniciales del autor
#.\s*                       Puntos y espacios
#\(\d{4}\)\.                Año APA7
#\s+
#.+?\.\s                         # Título del artículo
#[A-Z][A-Za-zÁÉÍÓÚÑáéíóúñ\s]+,   # Nombre de la revista
#\s*
#\d+                             # Volumen
#(?:\(\d+\))?                    # Número opcional
#,\s*
#\d+[-–]\d+\.                    # Páginas
#\s*
#(https?://doi\.org/\S+          # DOI
#|https?://\S+)                  # O URL
#$
#"""


        #AQUI SE BUSCAN AUTORES
        for ref in referencias_unidas:
            autor = re.match(r"^(.*?)\s*\(", ref)
            if autor:
                autores_lista.append(autor.group(1))
        #print(autores_lista[1])

        #AQUÍ SE BUSCAN LAS COINCIDENCIAS ENTRE FECHAS
        for fila in referencias_encontradas:
            #Busco que haya una coincidencia en la fila
            coincidencia = re.search(r"\([^)]+\)", fila)
            if coincidencia:
                #Si existe una coincidencia la almaceno temporalmente el fechaAPA
                fechaAPA = coincidencia.group(0)
                if(len(fechaAPA) == 6):
                    CountRef += 1
                    #print(i, CountRef, fila)
                    referencia_actual.append(fila)
            i += 1
        # Temporalmente almaceno las referencias en este array
        #print(referencia_actual)

    # Metodo visualizar refrencias                                                    
    def crear_etiquetas_referencias(self):
        self.etiquetas_referencias = []

        #for i, ref in enumerate(self.referencias):
        for i, ref in enumerate(self.resultado_APA):
            etiqueta = CTkLabel(self.master, text=f"Referencia {i+1}: {ref}", anchor="w", width=self.ancho/2, wraplength=self.ancho * 0.9,justify = "left",font = ("Arial", 12))
            etiqueta.place(x=100, y=200 + i*40)     
            self.etiquetas_referencias.append(etiqueta)
        


GUI = CTk( )
AppTXTs = App(GUI)
AppTXTs.master.mainloop()



# TODO:
        # Que haría yo?...
        # Ahora que ya tenemos un array con las referencias en APA (Autores y Año), crearia otro array creando las referencias,
        # una vez creadas buscaria los elementos de ese array en mi texto y solo contaria la cantidad de veces que se aparecen...
        # es correcto Magia Magia... lo comentamos. Saludos cordiales.



