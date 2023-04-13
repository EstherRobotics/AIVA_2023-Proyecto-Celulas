
import torch
import onnxruntime
import cv2
import numpy as np
from utils.general import non_max_suppression


# Clase para cargar el modelo entrenado y detectar, contar y mostrar células
##############################################################
class ImageCell:
    def __init__(self, path_image: str, path_model: str):
        self.path_image = path_image
        self.path_model = path_model
        self.boundingBox = []
        self.totalCells = 0
        self.image = []
        self.imageBoundingBox = []
        self.session = []
        self.out = []

    def loadImage(self):
        """Abre la imagen de la ruta proporcionada por el usuario y guarda una copia"""
        self.image = cv2.imread(self.path_image)
        self.imageBoundingBox = self.image.copy()
        print("Imagen cargada")
        return self.image

    def prepareImage(self):
        """Procesa la imagen proporcionada para poder realizar la inferencia"""
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.resize(self.image, (640, 640))
        self.image = np.transpose(self.image, [2, 0, 1])
        self.image = np.expand_dims(self.image, axis=0).astype(np.float32) / 255.0
        print("Imagen procesada para poder realizar la inferencia")
        return self.image

    def loadModel(self):
        """Carga el modelo ONNX para el procesamiento y lo ejecuta con onnxruntime"""
        self.session = onnxruntime.InferenceSession(self.path_model)
        print("Sesión de inferencia a realizar por el modelo ", self.path_model, " cargado")
        return self.session

    def detectCells(self, conf_thresh : float):
        """Ejecuta el modelo entrenado sobre la imagen y devuelve un
        array de los bounding boxes donde se detectan células, la clase
        a la que pertenecen y el score. Se le añade como argumento el intervalo 
        de confianza que será elegido por el usuario en la interfaz"""

        print("Detectando células de la imagen ", self.path_image, " con el modelo ", self.path_model)

        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name
        result = self.session.run([output_name], {input_name: self.image})

        output = torch.from_numpy(np.array(result[0]))
        self.out = non_max_suppression(output, conf_thresh , iou_thres=0.5)
        print("Detección terminada")

        return self.out

    def countCells(self):
        """Cuenta el total de células detectadas según el número de bounding boxes obtenidos."""
        self.totalCells = len(self.out[0])
        print("Total de células detectadas: ", self.totalCells)
        return self.totalCells

    def drawBoundingBox(self):
        """Dibuja los bounding boxes obtenidos del procesamiento de la imagen
        con el modelo para poder visualizar las células detectadas."""

        print("Dibujando bounding boxes sobre la imagen")
        for i, (x0, y0, x1, y1, score, cls_id) in enumerate(self.out[0]):
            # Reescalar bounding boxes
            y0 = 480 * y0 / 640
            y1 = 480 * y1 / 640
            box = np.array([x0, y0, x1, y1])
            box = box.round().astype(np.int32).tolist()

            # Obtener clase y score
            cls_id = int(cls_id)
            score = round(float(score), 3)
            # print(cls_id)
            # print(score)

            # Dibujar bounding boxes
            name = 'cell ' + str(score)
            cv2.putText(self.imageBoundingBox, name, (box[0], box[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.75, [225, 255, 255],
                        thickness=2)
            cv2.rectangle(self.imageBoundingBox, box[:2], box[2:], (0, 255, 0), 2)

        print("Bounding boxes dibujados sobre la imagen")
        return self.imageBoundingBox


# Ejemplo de prueba
'''# Directorios para cargar imagen y modelo yolo
path_image = 'a.jpg'
path_model = 'yolov5s_cells.onnx'

# Crear instancia de ImageCell
imgCell = ImageCell(path_image, path_model)
imgCell.loadImage()
imgCell.prepareImage()
imgCell.loadModel()
imgCell.detectCells()
imgCell.countCells()
img_detection = imgCell.drawBoundingBox()

# Muestra la imagen con las células detectadas
cv2.imshow('Células detectadas', img_detection)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''





