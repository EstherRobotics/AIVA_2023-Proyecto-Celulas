
# Clase para el procesamiento y detección de células en la imagen
##############################################################
class ImagenCelula:

    def __init__(self, path, modelo):
        self.path = path
        self.modelo = modelo
        self.boundingBox = []
        self.totalCelulas = 0
        self.imagen = []
        self.imagenBoundingBox = []

    def cargarImagen(self):
        """Abre la imagen de la ruta proporcionada por el usuario"""
        return -1

    def detectarCelulas(self):
        """Ejecuta el modelo entrenado sobre la imagen y devuelve un
        array de los bounding boxes donde se detectan células"""
        return -1

    def dibujarBoundingBox(self):
        """Dibuja los bounding boxes obtenidos del procesamiento de la imagen
        con el modelo para poder visualizar las células detectadas."""
        return -1

    def contarCelulas(self):
        """Cuenta el total de células detectadas según el número de bounding boxes obtenidos."""
        return -1


