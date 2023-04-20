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
import os
import pandas as pd


# Clase para ejecutar la aplicación CellCountApp
##############################################################
class CellCountApp:
    def __init__(self):
        # Variables auxiliares
        self.path_image = ""
        self.img_pred = None
        self.totalCells = 0

        # Creación de la window principal
        self.window = tk.Tk()
        self.window.title("CellCountApp")
        self.window.geometry("1200x600")

        # Creación de la entrada para el nivel de confianza con él que se desea la detección
        self.confidenceLabel = tk.Label(self.window, text="Nivel de confianza mínimo deseado:")
        self.confidenceLabel.pack()

        # Creación de widget para que el usuario pueda elegir el nivel de confianza (comprendido entre 0 y 1)
        self.confidenceScale = tk.Scale(self.window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL)
        self.confidenceScale.set(0.35) # Valor por defecto de 0.35 para el nivel de confianza al abrir la interfaz
        self.confidenceScale.pack()
        self.confThresh = self.confidenceScale.get()

        # Se agrega un botón para cargar la imagen
        self.loadButton = tk.Button(self.window, text="Cargar imagen", command=self.selectAndProcessImage, width=20, height=2)
        self.loadButton.pack(pady=5) #Separación con respecto al widget anterior

        # Se agrega un botón para guardar los resultados
        self.saveButton = tk.Button(self.window, text="Guardar imagen", command=self.saveResults, width=20,
                                      height=2)
        self.saveButton.pack(pady=5)
        self.saveButton.config(state='disabled')  # Deshabilita el botón

        # Se agrega un botón para cerrar la imagen
        self.closeButton = tk.Button(self.window, text="Cerrar imagen", command=self.closeProcessedImage, width=20, height=2)
        self.closeButton.pack(pady=5)
        self.closeButton.config(state='disabled') # Deshabilita el botón hasta que se cargue una imagen

        # Se agrega una etiqueta para mostrar el conteo de células
        # Le añadimos el tipo de letra, tamaño, y diferentes ajustes para que se ajuste a la interfaz
        self.count = tk.Label(self.window, font=('Times New Roman', 16, 'bold'),anchor="center",fg='white', bg='#4b86b4')
        self.count.pack(pady=20, fill=tk.X)

        # Creación de un contenedor para mostrar dentro la imagen cargada por el usuario
        self.ImageOriginalContainer = tk.LabelFrame(self.window, text="Imagen elegida por el usuario", width=200, height=200)
        self.ImageOriginalContainer.place(x=250, y=300) #Ajustamos donde debe estar ese contenedor en la interfaz

        # Creación de un contenedor para mostrar dentro la imagen tras la detección
        self.ImagePredContainer = tk.LabelFrame(self.window, text="Imagen tras detección", width=200, height=200)
        self.ImagePredContainer.place(x=800, y=300)

        # Agrega un panel para mostrar la imagen original y que se muestre dentro del Contenedor creado
        self.panelImageOrig = tk.Label(self.ImageOriginalContainer)
        self.panelImageOrig.place(x=250, y=300)

        # Agrega un panel para mostrar la imagen predicha y que se muestre dentro del contenedor creado
        self.panelImagePred = tk.Label(self.ImagePredContainer)
        self.panelImagePred.place(x=800, y=300)

        # Inicia el bucle principal de la aplicación
        self.window.mainloop()



    def selectAndProcessImage(self):
        """Abre el directorio del usuario para que seleccione la imagen a procesar
        y muestra las detecciones de las células"""

        self.path_image = filedialog.askopenfilename() #Se extrae el path de la imagen seleccionada por el usuario

        if (self.path_image!=""):
            
            # Oculta la imagen anterior y la etiqueta de conteo
            self.count.pack_forget()
            self.panelImageOrig.pack_forget()
            self.panelImagePred.pack_forget()

            # Carga la nueva imagen y la muestra
            image_pil = Image.open(self.path_image)
            image_pil = image_pil.resize((250, 250)) #Hacemos resize porque sino la interfaz corta ambas imágenes
            image_np = tf.keras.preprocessing.image.img_to_array(image_pil)

            imagen_mostrada = ImageTk.PhotoImage(image_pil)

            self.panelImageOrig.config(image=imagen_mostrada)
            self.panelImageOrig.image = imagen_mostrada

            # Muestra la nueva imagen original
            self.panelImageOrig.pack(side=tk.LEFT)


            #Se extrae el nivel de confianza elegido por el usuario
            self.confThresh = self.confidenceScale.get()

            # Detección de células en la imagen con la clase ImageCell
            self.detectCells = ImageCell(self.path_image,'yolov5s_cells.onnx')
            self.detectCells.loadImage()
            self.detectCells.prepareImage()
            self.detectCells.loadModel()

            out =  self.detectCells.detectCells(conf_thresh=self.confThresh)
            
            #Conteo de células detectadas
            self.totalCells = self.detectCells.countCells()

            #Imagen tras detección
            self.img_pred = self.detectCells.drawBoundingBox()

            # Mostrar total de células detectadas en la interfaz
            self.count.config(text="Número de células detectadas: " + str(self.totalCells))
            self.count.pack(pady=20, fill=tk.X)

            # Mostrar imagen con bounding boxes en la interfaz
            self.img_pred = cv2.cvtColor(self.img_pred, cv2.COLOR_BGR2RGB)
            self.img_pred = cv2.resize(self.img_pred, (250,250))
            self.img_pred = Image.fromarray(self.img_pred)
            img_pred_tk = ImageTk.PhotoImage(self.img_pred)

            self.panelImagePred.config(image=img_pred_tk)
            self.panelImagePred.image = img_pred_tk

            # Mostrar la nueva imagen procesada
            self.panelImagePred.pack(side=tk.RIGHT)

            # Deshabilitar botón de cargar imagen y de configuración del threshold
            self.loadButton.config(state='disabled')
            self.confidenceScale.config(state='disabled')

            # Habilitar botones para guardar y cerrar la imagen
            self.closeButton.config(state='normal')
            self.saveButton.config(state='normal')


    def saveResults(self):
        """Guarda la imagen procesada y un fichero de texto con la cantidad de células detectadas"""
        # Crear diretorio para guardar la imagen
        path = os.getcwd()
        dir_save = path+'\images_detected\\'
        if(not os.path.exists(dir_save)):
            os.mkdir(dir_save)

        # Añadir la confianza utilizada y el número de células detectadas al nombre de la imagen y guardar
        name_image = self.path_image.split('/')[-1].split('.')[0]
        path_save = dir_save + name_image + '_thresh' + str(self.confThresh) + '_cells' + str(self.totalCells) + '.jpg'
        self.img_pred.save(path_save)

        # Añadir detección al fichero de detecciones CSV
        path_csv = path + '\\results.csv'
        if(not os.path.exists(path_csv)):
            # Crear el documento de detecciones si no existe
            df = pd.DataFrame(columns=["Image_path", "Confidence", "Total_cells"])
        else:
            # Abrir documento de detecciones
            df = pd.read_csv(path_csv)

        # Añadir datos de la detección actual al csv
        datos = {"Image_path": path_save, "Confidence": self.confThresh, "Total_cells": self.totalCells}
        df = df.append(datos, ignore_index=True)
        df.to_csv(path_csv, index=False)

        # Deshabilitar botón de guardado
        self.saveButton.config(state='disabled')

        print("Imagen con predicciones guardada")
        print("Fichero results.csv actualizado")


    def closeProcessedImage(self):
        """Cierra las imágenes mostradas actualmente en la interfaz y habilita el botón para cargar otra imagen"""
        # Oculta la imagen procesada y la etiqueta de conteo
        self.count.pack_forget()
        self.panelImagePred.pack_forget()
        self.panelImageOrig.pack_forget()

        # Deshabilita el botón para guardar y cerrar la imagen
        self.closeButton.config(state='disabled')
        self.saveButton.config(state='disabled')

        # Habilitar botón de cargar imagen y configuración del threshold
        self.loadButton.config(state='normal')
        self.confidenceScale.config(state='normal')


#Ejecución de la aplicación
CellCountApp()