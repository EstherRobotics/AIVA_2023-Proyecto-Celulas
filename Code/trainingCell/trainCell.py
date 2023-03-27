
import torch
import glob
import os
import shutil
from sklearn.model_selection import train_test_split
import subprocess




# Clase para el entrenamiento de YOLO para detectar células en la imagen
##############################################################
class trainCell:

    def __init__(self, path_dataset):
        self.path_dataset = path_dataset
        self.path_model = ""
        self.X_train = []
        self.X_val = []
        self.y_train = []
        self.y_val = []

    def loadDataset(self):
        imgs = []
        xmls = []

        imgs = [f for f in glob.glob(os.path.join(self.path_dataset, '*.jpg'))]
        labels = [f for f in glob.glob(os.path.join(self.path_dataset, '*.txt'))]

        imgs.sort()
        labels.sort()

        self.imgs = imgs
        self.labels = labels


    def splitDataset(self):
        """Divide el dataset cargado en el formato de entrenamiento y validación esperado por YOLO y lo guarda
        en las carpetas correspondientes"""

        X_train, X_val, y_train, y_val = train_test_split(self.imgs, self.labels, test_size=0.20, random_state=42)

        self.X_train = X_train
        self.X_val = X_val
        self.y_train = y_train
        self.y_val = y_val

    def saveSplittedDataset(self, trainImgPath, trainLabelPath, valImgPath, valLabelPath):

        # Guardar imágenes de train en el directorio correspondiente
        for i in range(len(self.X_train)):
            # Obtener nombre de los archivos
            img_name = self.X_train[i].split("\\")[-1]
            label_name = self.y_train[i].split("\\")[-1]

            # Copiar imagen y txt al directorio de dataset correspondiente
            shutil.copy(self.X_train[i], os.path.join(trainImgPath, img_name))
            shutil.copy(self.y_train[i], os.path.join(trainLabelPath, label_name))

        # Guardar imágenes de validación en el directorio correspondiente
        for i in range(len(self.X_val)):
            # Obtener nombre de los archivos
            img_name = self.X_val[i].split("\\")[-1]
            label_name = self.y_val[i].split("\\")[-1]

            # Copiar imagen y txt al directorio de dataset correspondiente
            shutil.copy(self.X_val[i], os.path.join(valImgPath, img_name))
            shutil.copy(self.y_val[i], os.path.join(valLabelPath, label_name))


    def trainModel(self, batch=4, epochs=1):
        """Entrena la red neuronal YOLO con el dataset configurado mediante la línea de comandos"""

        cmd = "python train.py --img 640 --batch " + str(batch) +" --epochs "+ str(epochs) +" --data dataset.yaml --weights yolov5s.pt --cache"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)


    def saveModel(self,  path_weight):
        """Carga el modelo de YOLO y los pesos entrenados y guarda el modelo completo"""

        # Cargar modelo YOLOv5 y los pesos entrenador
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=path_weight, force_reload=True)

        # Definir tamaño de entrada de la imagen
        input_size = (3, 640, 640)

        # Crear tensor de entrada
        dummy_input = torch.randn(1, *input_size)

        # Exportar modelo en formato ONNX
        torch.onnx.export(model, dummy_input, "yolov5s_cells.onnx", opset_version=12)





path_dataset = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\data\\'

# Directorios para guardar correctamente imágenes de entrenamiento y validación para poder entrenar la red
trainImgPath = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\dataset\\images\\train\\'
trainLabelPath = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\dataset\\labels\\train\\'

valImgPath = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\\\images\\val\\'
valLabelPath = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\dataset\\labels\\val\\'

# Directorio donde se han guardado los pesos
path_weight = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\yolov5\\runs\\train\\exp5\\weights\\best.pt'



