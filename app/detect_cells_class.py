import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import onnxruntime
import torch
from utils.general import non_max_suppression
from PIL import Image, ImageTk
import tensorflow as tf

class Detect_Cells:
    def __init__(self):
        #Cargamos el modelo preentrenado YOLO
        self.Model = onnxruntime.InferenceSession('yolov5s_cells.onnx')
    
    def process_image(self, img_path):
        img = cv2.imread(img_path)

        # Preprocesamiento de la imagen
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640, 640))
        image = np.transpose(image, [2, 0, 1])
        image = np.expand_dims(image, axis=0).astype(np.float32) / 255.0

        # Ejecuta la inferencia en el modelo ONNX
        input_name = self.Model.get_inputs()[0].name
        output_name = self.Model.get_outputs()[0].name
        result = self.Model.run([output_name], {input_name: image})

        output = torch.from_numpy(np.array(result[0]))
        out = non_max_suppression(output, conf_thres=0.7, iou_thres=0.5)

        for i, (x0, y0, x1, y1, score, cls_id) in enumerate(out[0]):

            y0 = 480*y0 / 640
            y1 = 480*y1 / 640

            box = np.array([x0, y0, x1, y1])
            box = box.round().astype(np.int32).tolist()

            cls_id = int(cls_id)
            score = round(float(score), 3)

            name = 'cell ' + str(score)

            cv2.putText(img, name, (box[0], box[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.75, [225, 255, 255], thickness=2)
            cv2.rectangle(img, box[:2], box[2:], (0, 255, 0), 2)
        
        return img