# AIVA_2023-Proyecto-Celulas

## Índice

*[Introducción](#introducción)

*[Estructura del proyecto](#estructura-del-proyecto)

*[Tutorial de ejecución](#tutorial-ejecución)

*[Descripción detallada](#descripción-detallada)

*[Conclusión](#conclusión)

## Introducción

Este proyecto se basa en el desarrollo de la aplicación **CellCountApp** para la detección y conteo de células en imágenes de microscopía. En este respositorio se encuentran todos los documentos asociados al proyecto, tanto de los requerimientos del sistema como de la primera parte de su implementación. El objetivo final es desarrollar una interfaz capaz de obtener la localización de cada célula en la imagen mediante *bounding boxes*. 


## Estructura del proyecto
La estructura actual se divide varias carpetas, donde se destacan sus directorios principales: 

* Code
  * trainingCell
* Dataset
  * Annotations
  * JPEGImages 
* Dataset preprocessing 
  * annotations_YOLO
  * xml_preprocessing
* Docs
  * DSR_Células
  * Documento_diseño_células 
  * Presupuesto
* Mock-up
* Tests
  * tests
  * run_tests
* App
  * CellCountApp
  * imageCell
  

En el directorio de **Code** se encuentra *trainingCell*, que incluye los archivos necesarios utilizados en el entrenamiento de la red neuronal para la detección de células. En la carpeta de **Dataset**, están contenidas las imágenes de células y las anotaciones de sus posiciones proporcionadas inicialmente. El procesamiento de este **Dataset**, fue realizado en **Dataset_preprocessing**, donde se extrayeron las anotaciones de las imágenes en el formato requerido por YOLO. En la sección de **Docs**, podemos ver el documento DSR, el de presupuesto y el nuevo documento de diseño. Dentro del **Mock-up**, está un esquema general de programación de la aplicación con los test unitarios desarrollados inicialmente. Los nuevos tests unitarios están dentro de **Tests**, en el archivo *tests.py*, y pueden ejecutarse con run_tests.py para comprobar su funcionamiento. Finalmente, en el directorio **App**, se puede ver el código de la aplicación contenido en *CellCountApp.py*, que utiliza funciones de *imageCell.py* para el procesamiento. 

## Tutorial de ejecución
En esta parte se explican los pasos necesarios para poder poner en marcha cada uno de los códigos desarrollados para el entrenamiento y la detección de células en las imágenes. 

### Restructuración del dataset 
Para poder entrenar la red neuronal, primero se necesita configurar las carpetas y anotaciones de las imágenes de la manera esperada por YOLO. 

### Instalación del repositorio de YOLOv5
Este paso solo es necesario si se desea entrenar un modelo de YOLOv5. Dentro del directorio de /Code/trainingCell, se debe clonar el repositorio de YOLO con el comando: 


### Entrenamiento de YOLOv5



### Ejecución de la aplicación





## Descripción detallada

**CellCountApp** estará diseñada principalmente para el conteo de células al enviar una imagen de microscopio y poder obtener su posición mediante la definición de zonas rectangulares. Se puede ver un ejemplo del tipo de imágenes a tratar a continuación: 

<p align="center">
<img src="https://user-images.githubusercontent.com/46898686/225309474-a1989b4f-5393-4303-9fd0-03c5c3c1fd35.png" width="40%" height="40%">
</p>

Al procesar la información contenida en **Dataset/Annotations** sobre la imagen correspondiente, se pueden dibujar los bounding boxes asociados a cada célula: 

<p align="center">
<img src="https://user-images.githubusercontent.com/46898686/225309987-9d719387-2e36-418b-bc1b-7fe2e3083437.png" width="40%" height="40%">
</p>


Se puede observar que hay varios tipos de células y que además estas pueden encontrarse a lo largo de toda la imagen en orientaciones distintas. Se debe tener en cuenta que pueden ocurrir superposiciones entre las células por lo que este será un tema clave a la hora de realizar la detección. 

Para el desarrollo del proyecto se programarán distintos modelos de **YOLO** que serán evaluados con métricas IoU. Estos modelos, procesarán la imagen, obteniendo la localización de las células esperada. En el caso de la interfaz final de **CellCountApp**, esta será programada con **Tkinker**. El usuario podrá cargar la imagen a procesar y se mostrará la información del procesamiento de forma visual, otorgando también el número total de células detectadas. 


# Conclusión 

Cabe decir que este repositorio se encuentra bajo desarrollo por lo que actualmente, solo posee los documentos para el comienzo del proyecto, el conjunto de datos que se utilizará para el entrenamiento del modelo y el mock-up del sistema. 

