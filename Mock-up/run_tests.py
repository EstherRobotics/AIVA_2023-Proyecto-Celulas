
import unittest
from tests import testCelulas
from imagenCelula import *


# Función para poder ejecutar todos los tests unitarios de la clase testCelulas
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCelulas))
    unittest.TextTestRunner().run(suite)