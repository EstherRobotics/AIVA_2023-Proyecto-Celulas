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
        self.window.geometry("1200x600")

        # Creación de la entrada para el nivel de confianza con él que se desea la detección
        self.confidenceLabel = tk.Label(self.window, text="Nivel de confianza mínimo deseado:")
        self.confidenceLabel.pack()

        # Creación de widget para que el usuario pueda elegir el nivel de confianza (comprendido entre 0 y 1)
        self.confidenceScale = tk.Scale(self.window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.confidenceScale.set(0.5) # Valor por defecto de 0.5 para el nivel de confianza al abrir la interfaz
        self.confidenceScale.pack()

        # Se agrega un botón para cargar la imagen
        self.loadButton = tk.Button(self.window, text="Cargar imagen", command=self.selectAndProcessImage, width=20, height=2)
        self.loadButton.pack(pady=5) #Separación con respecto al widget anterior

        # Se agrega un botón para cerrar la imagen
        self.closeButton = tk.Button(self.window, text="Cerrar imagen", command=self.closeProcessedImage, width=20, height=2)
        self.closeButton.pack(pady=10)
        self.closeButton.config(state='disabled') # Deshabilita el botón hasta que se cargue una imagen

        # Se agrega una etiqueta para mostrar el conteo de células
        # Le añadimos el tipo de letra, tamaño, y diferentes ajustes para que se ajuste a la interfaz
        self.count = tk.Label(self.window, font=('Times New Roman', 16, 'bold'),anchor="center",fg='white', bg='#4b86b4')
        self.count.pack(pady=20, fill=tk.X)

        # Creación de un contenedor para mostrar dentro la imagen cargada por el usuario
        self.ImageOriginalContainter = tk.LabelFrame(self.window, text="Imagen elegida por el usuario", width=200, height=200)
        self.ImageOriginalContainter.place(x=250, y=300) #Ajustamos donde debe estar ese contenedor en la interfaz

        # Creación de un contenedor para mostrar dentro la imagen tras la detección
        self.ImagePredContainter = tk.LabelFrame(self.window, text="Imagen tras detección", width=200, height=200)
        self.ImagePredContainter.place(x=800, y=300)

        # Agrega un panel para mostrar la imagen original y que se muestre dentro del Contenedor creado
        self.panelImageOrig = tk.Label(self.ImageOriginalContainter)
        self.panelImageOrig.place(x=250, y=300)

        # Agrega un panel para mostrar la imagen predicha y que se muestre dentro del contenedor creado
        self.panelImagePred = tk.Label(self.ImagePredContainter)
        self.panelImagePred.place(x=800, y=300)

        # Inicia el bucle principal de la aplicación
        self.window.mainloop()

    def selectAndProcessImage(self):
        """Abre el directorio del usuario para que seleccione la imagen a procesar
        y muestra las detecciones de las células"""

        path_image = filedialog.askopenfilename() #Se extrae el path de la imagen seleccionada por el usuario

        if path_image:
            
            # Oculta la imagen anterior y la etiqueta de conteo
            self.count.pack_forget()
            self.panelImageOrig.pack_forget()
            self.panelImagePred.pack_forget()

            # Carga la nueva imagen y la muestra
            image_pil = Image.open(path_image)
            image_pil = image_pil.resize((250, 250)) #Hacemos resize porque sino la interfaz corta ambas imágenes
            image_np = tf.keras.preprocessing.image.img_to_array(image_pil)

            imagen_mostrada = ImageTk.PhotoImage(image_pil)

            self.panelImageOrig.config(image=imagen_mostrada)
            self.panelImageOrig.image = imagen_mostrada

            # Muestra la nueva imagen original
            self.panelImageOrig.pack(side=tk.LEFT)


            #Se extrae el nivel de confianza elegido por el usuario
            conf_thresh = self.confidenceScale.get()

            # Detección de células en la imagen con la clase ImageCell
            self.detectCells = ImageCell(path_image,'yolov5s_cells.onnx')
            self.detectCells.loadImage()
            self.detectCells.prepareImage()
            self.detectCells.loadModel()

            out =  self.detectCells.detectCells(conf_thresh=conf_thresh)
            
            #Conteo de células detectadas
            totalCells = self.detectCells.countCells()

            #Imagen tras detección
            img_pred = self.detectCells.drawBoundingBox()

            # Mostrar total de células detectadas en la interfaz
            self.count.config(text="Número de células detectadas: " + str(totalCells))
            self.count.pack(pady=20, fill=tk.X)

            # Mostrar imagen con bounding boxes en la interfaz
            img_pred = cv2.cvtColor(img_pred, cv2.COLOR_BGR2RGB)
            img_pred = cv2.resize(img_pred, (250,250))
            img_pred = Image.fromarray(img_pred)
            img_pred_tk = ImageTk.PhotoImage(img_pred)

            self.panelImagePred.config(image=img_pred_tk)
            self.panelImagePred.image = img_pred_tk

            # Mostrar la nueva imagen procesada
            self.panelImagePred.pack(side=tk.RIGHT)

            # Botón para cerrar la imagen
            self.closeButton.config(state='normal')

    def closeProcessedImage(self):
        """Cierra las imágenes mostradas actualmente en la interfaz y habilita el botón para cargar otra imagen"""
        # Oculta la imagen procesada y la etiqueta de conteo
        self.count.pack_forget()
        self.panelImagePred.pack_forget()
        self.panelImageOrig.pack_forget()

        # Deshabilita el botón para cerrar la imagen procesada
        self.closeButton.config(state='disabled')

#Ejecución de la aplicación
CellCountApp()