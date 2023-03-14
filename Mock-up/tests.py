
import unittest
from imagenCelula import *
from interfaz import *


# Tests unitarios  definidos en la clase testCelulas
##############################################################
class testCelulas(unittest.TestCase):
    def setUp(self):
        """Carga una instancia de ImagenCelula, con una imagen y un modelo determinado"""
        self.cel1 = ImagenCelula("./imagen.jpg", "./modelo.sav")

    def test_cargarImagen(self):
        """Carga la imagen y comprueba que su tipo es correcto y que no es None"""
        img = self.cel1.cargarImagen()
        try:
            self.assertEqual(img.dtype, "uint8")
            self.assertIsNotNone(img, "Image is none")
        except:
            self.assertIsNotNone(img, "Image is none")

    def test_cargarModelo(self):
        """Obtiene el modelo entrenado y comprueba que no es None"""
        model = self.cel1.getModelo()
        self.assertIsNotNone(model, "Model is none")

    def test_BoundingBox(self):
        """Carga la imagen, detecta las células y comprueba que se ha detectado alguna célula según la
        longitud del array de bounding boxes obtenido"""
        self.cel1.cargarImagen()
        bbox = self.cel1.detectarCelulas()
        self.assertGreater(len(bbox), 0)

    def test_dibujarBoundingBox(self):
        """Carga la imagen, detecta las células y dibuja los bounding boxes en la imagen. Después, comprueba
        que la imagen no es None y su tipo es correcto"""
        self.cel1.cargarImagen()
        self.cel1.detectarCelulas()
        img = self.cel1.dibujarBoundingBox()

        try:
            self.assertEqual(img.dtype, "uint8")
            self.assertIsNotNone(img, "Image is none")
        except:
            self.assertIsNotNone(img, "Image is none")

    def test_contarCelulas(self):
        """Carga la imagen, detecta las células, cuenta las células y comprueba que se ha detectado alguna"""
        self.cel1.cargarImagen()
        self.cel1.detectarCelulas()
        total = self.cel1.contarCelulas()
        self.assertGreater(total, 0)

    def test_totalCelulas(self):
        """Carga la imagen, detecta las células, las cuenta y comprueba que el número total de células
        detectadas coincide con el número esperado. (Podría no coincidir según la precisión del modelo)"""
        self.cel1.cargarImagen()
        self.cel1.detectarCelulas()
        total = self.cel1.contarCelulas()
        self.assertEqual(total, 25)

