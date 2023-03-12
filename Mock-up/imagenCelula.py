
# Clase para el procesamiento y detección de células en la imagen
##############################################################
class ImagenCelula:

    def __init__(self, path, path_modelo):
        self.path = path
        self.path_modelo = path_modelo
        self.boundingBox = []
        self.totalCelulas = 0
        self.imagen = []
        self.imagenBoundingBox = []

    def cargarImagen(self):
        """Abre la imagen de la ruta proporcionada por el usuario"""
        return []
    def getModelo(self):
        """Carga el modelo para el procesamiento y lo devuelve"""
        return None
    def detectarCelulas(self):
        """Ejecuta el modelo entrenado sobre la imagen y devuelve un
        array de los bounding boxes donde se detectan células"""
        return []

    def dibujarBoundingBox(self):
        """Dibuja los bounding boxes obtenidos del procesamiento de la imagen
        con el modelo para poder visualizar las células detectadas."""
        return None

    def contarCelulas(self):
        """Cuenta el total de células detectadas según el número de bounding boxes obtenidos."""
        return 25


