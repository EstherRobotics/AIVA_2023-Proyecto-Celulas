
import unittest
from tests import testCelulas
from imagenCelula import *

if __name__ == '__main__':
    #cel = ImagenCelula("./imagen.jpg", "./modelo.sav")

    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCelulas))
    unittest.TextTestRunner().run(suite)