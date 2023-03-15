


# Clase para el procesamiento y detección de células en la imagen
##############################################################
class ImageCell:

    def __init__(self, path, path_model):
        self.path = path
        self.path_model = path_model
        self.boundingBox = []
        self.totalCells = 0
        self.image = []
        self.imageBoundingBox = []

    def loadImage(self):
        """Abre la imagen de la ruta proporcionada por el usuario"""
        return []
    def getModel(self):
        """Carga el modelo para el procesamiento y lo devuelve"""
        return None
    def detectCells(self):
        """Ejecuta el modelo entrenado sobre la imagen y devuelve un
        array de los bounding boxes donde se detectan células"""
        return []

    def drawBoundingBox(self):
        """Dibuja los bounding boxes obtenidos del procesamiento de la imagen
        con el modelo para poder visualizar las células detectadas."""
        return None

    def countCells(self):
        """Cuenta el total de células detectadas según el número de bounding boxes obtenidos."""
        return 25


