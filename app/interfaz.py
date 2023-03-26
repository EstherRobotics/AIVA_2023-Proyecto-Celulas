import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import onnxruntime
import torch
from utils.general import non_max_suppression
from PIL import Image, ImageTk
import tensorflow as tf
from detect_cells_class import *

class CellCountApp:
    def __init__(self):

        #Llamada a la clase Detect_Cells
        self.detect_cells = Detect_Cells()

        # Creación de la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("CellCountApp")


        # Se agrega un botón para cargar la imagen
        self.boton_cargar = tk.Button(self.ventana, text="Cargar imagen", command=self.load_image)
        self.boton_cargar.pack()
        
        # Se agrega un botón para cerrar la imagen
        self.boton_cerrar = tk.Button(self.ventana, text="Cerrar imagen", command=self.close_image)
        self.boton_cerrar.pack()
        self.boton_cerrar.config(state='disabled') # Deshabilita el botón hasta que se cargue una imagen

        # Se agrega una etiqueta para mostrar el conteo de células
        self.count = tk.Label(self.ventana)

        # Agrega un panel para mostrar la imagen
        self.panel_imagen = tk.Label(self.ventana)

        # Agrega un panel para mostrar la imagen predicha
        self.panel_imagen_predicha = tk.Label(self.ventana)

        # Inicia el bucle principal de la aplicación
        self.ventana.mainloop()

    def load_image(self):
        ruta_imagen = filedialog.askopenfilename()
        if ruta_imagen:
            # Oculta la imagen anterior y la etiqueta de conteo
            self.count.pack_forget()
            self.panel_imagen.pack_forget()
            self.panel_imagen_predicha.pack_forget()

            # Carga la nueva imagen y la muestra
            imagen_pil = Image.open(ruta_imagen)
            imagen_pil = imagen_pil.resize((224, 224)) #Hacemos resize porque sino la interfaz corta ambas imágenes
            imagen_np = tf.keras.preprocessing.image.img_to_array(imagen_pil)

            #self.count.config(text="El número de células detectadas: ")

            imagen_mostrada = ImageTk.PhotoImage(imagen_pil)

            
            self.panel_imagen.config(image=imagen_mostrada)
            self.panel_imagen.image = imagen_mostrada

            # Muestra la nueva imagen y la etiqueta de conteo
            self.count.pack()
            self.panel_imagen.pack()

            # Muestra la imagen predicha
        
            imagen_predicha = self.detect_cells.process_image(ruta_imagen)
            imagen_predicha = cv2.cvtColor(imagen_predicha, cv2.COLOR_BGR2RGB)
            imagen_predicha = cv2.resize(imagen_predicha, (224,224))
            imagen_predicha = Image.fromarray(imagen_predicha)
            imagen_predicha_tk = ImageTk.PhotoImage(imagen_predicha)
            

            self.panel_imagen_predicha.config(image=imagen_predicha_tk)
            self.panel_imagen_predicha.image = imagen_predicha_tk
            self.panel_imagen_predicha.pack()

            # Botón para cerrar la imagen
            self.boton_cerrar.config(state='normal')


    def close_image(self):
        # Oculta la imagen y la etiqueta de conteo
        self.count.pack_forget()
        self.panel_imagen.pack_forget()
        self.panel_imagen_predicha.pack_forget()
        
        # Habilita el botón para cargar otra imagen

        self.boton_cargar.config(state='normal')

        # Deshabilita el botón para cerrar la imagen
        self.boton_cerrar.config(state='disabled')

CellCountApp()