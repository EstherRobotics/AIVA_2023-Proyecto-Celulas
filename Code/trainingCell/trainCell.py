
import torch
import glob
import os
import shutil
from sklearn.model_selection import train_test_split
import subprocess



# Clase para el entrenamiento de YOLO para detectar células en la imagen
##############################################################
class trainCell:

    def __init__(self, path_dataset: str):
        self.path_dataset = path_dataset
        self.path_model = ""
        self.imgs = []
        self.labels = []
        self.X_train = []
        self.X_val = []
        self.y_train = []
        self.y_val = []

    def loadDataset(self):
        """Carga las imágenes y las etiquetas del directorio /data y las ordena"""
        print("Cargando dataset de ", path_dataset)

        self.imgs = [f for f in glob.glob(os.path.join(self.path_dataset, '*.jpg'))]
        self.labels = [f for f in glob.glob(os.path.join(self.path_dataset, '*.txt'))]
        self.imgs.sort()
        self.labels.sort()
        print("Dataset cargado")

    def splitDataset(self):
        """Divide el dataset cargado en el formato de entrenamiento y validación esperado por YOLO y lo guarda
        en las carpetas correspondientes"""

        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(self.imgs, self.labels, test_size=0.20, random_state=42)

        print("El dataset se ha dividido en entrenamiento y validación")

    def saveSplittedDataset(self, trainImgPath: str, trainLabelPath: str, valImgPath: str, valLabelPath: str):
        """Guarda las imágenes y anotaciones divididas en entrenamiento y validación en las carpetas correspondientes
        según el formato esperado por YOLO"""

        print("Guardando las imágenes de train y validación en las carpetas correspondientes")

        # Guardar imágenes de train en el directorio correspondiente
        for i in range(len(self.X_train)):
            # Obtener nombre de los archivos
            img_name = self.X_train[i].split("\\")[-1]
            label_name = self.y_train[i].split("\\")[-1]

            # Copiar imagen y txt al directorio dataset correspondiente
            shutil.copy(self.X_train[i], os.path.join(trainImgPath, img_name))
            shutil.copy(self.y_train[i], os.path.join(trainLabelPath, label_name))

        # Guardar imágenes de validación en el directorio correspondiente
        for i in range(len(self.X_val)):
            # Obtener nombre de los archivos
            img_name = self.X_val[i].split("\\")[-1]
            label_name = self.y_val[i].split("\\")[-1]

            # Copiar imagen y txt al directorio dataset correspondiente
            shutil.copy(self.X_val[i], os.path.join(valImgPath, img_name))
            shutil.copy(self.y_val[i], os.path.join(valLabelPath, label_name))

        print("Imágenes y anotaciones guardadas")

    def trainModel(self, batch: int, epochs: int):
        """Entrena la red neuronal YOLO con el dataset configurado mediante la línea de comandos"""
        print("Entrenando red YOLO")
        #cmd = '!python yolov5/train.py --img 640 --batch 4 --epochs 5 --data dataset.yaml --weights yolov5s.pt --cache'

        cmd = "python yolov5/train.py --img 640 --batch " + str(batch) +" --epochs "+ str(epochs) +" --data dataset.yaml --weights yolov5s.pt --cache"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        print("Entrenamiento terminado")

    def saveModel(self, path_weight: str, path_save: str):
        """Carga el modelo de YOLO y los pesos entrenados y guarda el modelo completo"""

        model = torch.hub.load('ultralytics/yolov5', 'custom', path=path_weight, force_reload=True)

        # Definir tensor de entrada a la red neuronal
        input_size = (3, 640, 640)
        dummy_input = torch.randn(1, *input_size)

        # Exportar modelo en formato ONNX
        torch.onnx.export(model, dummy_input, path_save, opset_version=12)

        print("Los pesos ", path_weight, " han sido guardados dentro del modelo ", path_save)




# Directorios para guardar correctamente imágenes de entrenamiento y validación para poder entrenar la red
trainImgPath = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\trainingCell\\dataset\\images\\train\\'
trainLabelPath = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\trainingCell\\dataset\\labels\\train\\'

valImgPath = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\trainingCell\\dataset\\images\\val\\'
valLabelPath = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\trainingCell\\dataset\\labels\\val\\'

# Directorio donde se han guardado los pesos
#path_weight = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\trainingCell\\yolov5\\runs\\train\\exp5\\weights\\best.pt'
path_weight = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\trainingCell\\best.pt'

# Nombre para guardar el modelo completo entrenado
path_save = "yolov5s_cells.onnx"

# Directorio donde se encuentran las imágenes y las anotaciones mezcladas
path_dataset = 'C:\\Users\\Usuario\\Desktop\\AIVA_2023-Proyecto-Celulas\\Code\\trainingCell\\data\\'

# Crear instancia de trainCell
trainCell1 = trainCell(path_dataset)
'''trainCell1.loadDataset()
trainCell1.splitDataset()
trainCell1.saveSplittedDataset(trainImgPath, trainLabelPath, valImgPath, valLabelPath)
trainCell1.trainModel(batch=4,epochs=50)'''
trainCell1.saveModel(path_weight, path_save)




