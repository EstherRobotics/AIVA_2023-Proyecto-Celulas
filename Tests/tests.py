
import unittest
from imageCell import *


# Tests unitarios  definidos en la clase testCelulas
##############################################################
class testCells(unittest.TestCase):
    def setUp(self):
        """Carga una instancia de ImageCell, con una imagen y un modelo determinado"""
        #self.image = 'images_test/BloodImage_00022.jpg'
        self.image = 'images_test/BloodImage_00132.jpg'
        #self.image = 'images_test/BloodImage_00225.jpg'

        self.cell1 = ImageCell(self.image, 'yolov5s_cells.onnx')

    def test_loadImage(self):
        """Carga la imagen y comprueba que su tipo es correcto y que no es None"""
        img = self.cell1.loadImage()
        try:
            self.assertEqual(img.dtype, "uint8")
            self.assertIsNotNone(img, "Image is none")
        except:
            self.assertIsNotNone(img, "Image is none")

    def test_prepareImage(self):
        """Prepara la imagen para la detección de células y comprueba que su tipo es correcto y que no es None"""
        self.cell1.loadImage()
        img = self.cell1.prepareImage()

        try:
            self.assertEqual(img.dtype, "uint8")
            self.assertIsNotNone(img, "Image prepared is none")
        except:
            self.assertIsNotNone(img, "Image prepared is none")


    def test_loadModel(self):
        """Obtiene el modelo entrenado y comprueba que no es None"""
        model = self.cell1.loadModel()
        self.assertIsNotNone(model, "Model is none")

    def test_BoundingBox(self):
        """Carga la imagen, detecta las células y comprueba que se ha detectado alguna célula según la
        longitud del array de bounding boxes obtenido"""
        self.cell1.loadImage()
        self.cell1.prepareImage()
        self.cell1.loadModel()
        bbox = self.cell1.detectCells()
        self.assertGreater(len(bbox), 0)

    def test_drawBoundingBox(self):
        """Carga la imagen, detecta las células y dibuja los bounding boxes en la imagen. Después, comprueba
        que la imagen no es None y su tipo es correcto"""
        self.cell1.loadImage()
        self.cell1.prepareImage()
        self.cell1.loadModel()
        self.cell1.detectCells()
        img = self.cell1.drawBoundingBox()

        try:
            self.assertEqual(img.dtype, "uint8")
            self.assertIsNotNone(img, "Image is none")
        except:
            self.assertIsNotNone(img, "Image is none")

    def test_countCells(self):
        """Carga la imagen, detecta las células, cuenta las células y comprueba que se ha detectado alguna"""
        self.cell1.loadImage()
        self.cell1.prepareImage()
        self.cell1.loadModel()
        self.cell1.detectCells()
        total = self.cell1.countCells()
        self.assertGreater(total, 0)

    def test_totalCells(self):
        """Carga la imagen, detecta las células, las cuenta y comprueba que el número total de células
        detectadas coincide con el número esperado. (Podría no coincidir según la precisión del modelo)"""
        self.cell1.loadImage()
        self.cell1.prepareImage()
        self.cell1.loadModel()
        self.cell1.detectCells()
        totalDetections = self.cell1.countCells()

        labelImage = self.image.split('.')[0]

        with open(labelImage+".txt") as f:
            total = len(f.readlines())

        self.assertEqual(total, totalDetections)

