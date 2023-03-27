import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import onnxruntime
import torch
from utils.general import non_max_suppression
from PIL import Image, ImageTk
import tensorflow as tf
from imageCell import *


# Clase para ejecutar la aplicación CellCountApp
##############################################################
class CellCountApp:
    def __init__(self):
        # Creación de la window principal
        self.window = tk.Tk()
        self.window.title("CellCountApp")
        self.window.geometry("900x600")

        # Se agrega un botón para cargar la imagen
        self.loadButton = tk.Button(self.window, text="Cargar imagen", command=self.selectAndProcessImage)
        self.loadButton.pack()

        # Se agrega un botón para cerrar la imagen
        self.closeButton = tk.Button(self.window, text="Cerrar imagen", command=self.closeProcessedImage)
        self.closeButton.pack()
        self.closeButton.config(state='disabled') # Deshabilita el botón hasta que se cargue una imagen

        # Se agrega una etiqueta para mostrar el conteo de células
        self.count = tk.Label(self.window)

        # Agrega un panel para mostrar la imagen
        self.panelImage = tk.Label(self.window)

        # Agrega un panel para mostrar la imagen predicha
        self.panelImagePred = tk.Label(self.window)

        # Inicia el bucle principal de la aplicación
        self.window.mainloop()

    def selectAndProcessImage(self):
        """Abre el directorio del usuario para que seleccione la imagen a procesar
        y muestra las detecciones de las células"""

        path_image = filedialog.askopenfilename()
        if path_image:
            # Oculta la imagen anterior y la etiqueta de conteo
            self.count.pack_forget()
            self.panelImage.pack_forget()
            self.panelImagePred.pack_forget()

            # Carga la nueva imagen y la muestra
            image_pil = Image.open(path_image)
            image_pil = image_pil.resize((224, 224)) #Hacemos resize porque sino la interfaz corta ambas imágenes
            image_np = tf.keras.preprocessing.image.img_to_array(image_pil)

            imagen_mostrada = ImageTk.PhotoImage(image_pil)
            
            self.panelImage.config(image=imagen_mostrada)
            self.panelImage.image = imagen_mostrada

            # Muestra la nueva imagen y la etiqueta de conteo
            self.count.pack()
            self.panelImage.pack()

            # Detección de células en la imagen con la clase ImageCell
            self.detectCells = ImageCell(path_image,'yolov5s_cells.onnx')
            self.detectCells.loadImage()
            self.detectCells.prepareImage()
            self.detectCells.loadModel()
            out = self.detectCells.detectCells()
            print(type(out))

            totalCells = self.detectCells.countCells()
            img_pred = self.detectCells.drawBoundingBox()

            # Mostrar total de células detectadas 
            self.count.config(text="El número de células detectadas: " + str(totalCells))

            # Mostrar imagen con bounding boxes
            img_pred = cv2.cvtColor(img_pred, cv2.COLOR_BGR2RGB)
            img_pred = cv2.resize(img_pred, (224,224))
            img_pred = Image.fromarray(img_pred)
            img_pred_tk = ImageTk.PhotoImage(img_pred)

            self.panelImagePred.config(image=img_pred_tk)
            self.panelImagePred.image = img_pred_tk
            self.panelImagePred.pack()

            # Botón para cerrar la imagen
            self.closeButton.config(state='normal')

    def closeProcessedImage(self):
        """Cierra las imágenes mostradas actualmente en la interfaz y habilita el botón para cargar otra imagen"""
        # Oculta la imagen y la etiqueta de conteo
        self.count.pack_forget()
        self.panelImage.pack_forget()
        self.panelImagePred.pack_forget()
        
        # Habilita el botón para cargar otra imagen
        self.loadButton.config(state='normal')

        # Deshabilita el botón para cerrar la imagen
        self.closeButton.config(state='disabled')

CellCountApp()