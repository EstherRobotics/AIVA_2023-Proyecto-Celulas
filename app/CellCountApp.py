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

        # Crear entrada para el conf_thresh
        self.confThreshLabel = tk.Label(self.window, text="Nivel de confianza mínimo deseado:")
        self.confThreshLabel.pack()

        # Crear widget Scale para el conf_thresh
        self.confThreshScale = tk.Scale(self.window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.confThreshScale.set(0.5) # Valor por defecto
        self.confThreshScale.pack()

        # Se agrega un botón para cargar la imagen
        self.loadButton = tk.Button(self.window, text="Cargar imagen", command=self.selectAndProcessImage, width=20, height=2)
        self.loadButton.pack(pady=5)

        # Se agrega un botón para cerrar la imagen
        self.closeButton = tk.Button(self.window, text="Cerrar imagen", command=self.closeProcessedImage, width=20, height=2)
        self.closeButton.pack(pady=10)
        self.closeButton.config(state='disabled') # Deshabilita el botón hasta que se cargue una imagen

        # Agrega una etiqueta para mostrar el conteo de células
        # Se agrega una etiqueta para mostrar el conteo de células
        #self.count = tk.Label(self.window)
        self.count = tk.Label(self.window, font=('Times New Roman', 16, 'bold'),anchor="center",fg='white', bg='#4b86b4')
        self.count.pack(pady=20, fill=tk.X)

        # Contenedor para la imagen original
        self.panelImageOrigContainer = tk.LabelFrame(self.window, text="Imagen Original", width=200, height=200)
        self.panelImageOrigContainer.place(x=250, y=300)

        # Contenedor para la imagen predicha
        self.panelImagePredContainer = tk.LabelFrame(self.window, text="Imagen tras detección", width=200, height=200)
        self.panelImagePredContainer.place(x=800, y=300)

        # Agrega un panel para mostrar la imagen original
        self.panelImageOrig = tk.Label(self.panelImageOrigContainer)
        self.panelImageOrig.place(x=250, y=300)

        # Agrega un panel para mostrar la imagen predicha
        self.panelImagePred = tk.Label(self.panelImagePredContainer)
        self.panelImagePred.place(x=800, y=300)



        # Inicia el bucle principal de la aplicación
        self.window.mainloop()

    def selectAndProcessImage(self):
        """Abre el directorio del usuario para que seleccione la imagen a procesar
        y muestra las detecciones de las células"""

        path_image = filedialog.askopenfilename()
        if path_image:
            # Oculta la imagen anterior y la etiqueta de conteo
            self.count.pack_forget()
            self.panelImageOrig.pack_forget()
            self.panelImagePred.pack_forget()

            #PONER EL PACKFORGET ELIMINA LAS IMÁGENES
            #self.panelImageOrigContainer.pack_forget()
            #self.panelImagePredContainer.pack_forget()


            # Carga la nueva imagen y la muestra
            image_pil = Image.open(path_image)
            image_pil = image_pil.resize((250, 250)) #Hacemos resize porque sino la interfaz corta ambas imágenes
            image_np = tf.keras.preprocessing.image.img_to_array(image_pil)

            imagen_mostrada = ImageTk.PhotoImage(image_pil)

            self.panelImageOrig.config(image=imagen_mostrada)
            self.panelImageOrig.image = imagen_mostrada

            # Muestra la nueva imagen original
            self.panelImageOrig.pack(side=tk.LEFT)

            # Detección de células en la imagen con la clase ImageCell
            self.detectCells = ImageCell(path_image,'yolov5s_cells1.onnx')
            self.detectCells.loadImage()
            self.detectCells.prepareImage()
            self.detectCells.loadModel()

            conf_thresh = self.confThreshScale.get()

            out =  self.detectCells.detectCells(conf_thresh=conf_thresh)

            #conf_thresh = float(self.confThreshEntry.get())
            #conf_thresh = float(self.conf_thresh_entry.get())


            totalCells = self.detectCells.countCells()
            img_pred = self.detectCells.drawBoundingBox()

            # Mostrar total de células detectadas 

            self.count.config(text="Número de células detectadas: " + str(totalCells))
            self.count.pack(pady=20, fill=tk.X)
            # Mostrar imagen con bounding boxes
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


        # Vuelve a mostrar la imagen original
        #self.panelImageOrig.pack(side=tk.LEFT, padx=10)

        # Deshabilita el botón para cerrar la imagen procesada
        self.closeButton.config(state='disabled')

CellCountApp()