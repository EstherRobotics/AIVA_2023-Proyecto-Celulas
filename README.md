# AIVA_2023-Proyecto-Celulas

## Índice

*[Introducción](#introducción)

*[Estructura del proyecto](#estructura-del-proyecto)

*[Descripción detallada](#descripción-detallada)

*[Tutorial de ejecución](#tutorial-ejecución)

*[Conclusión](#conclusión)

## Introducción

Este proyecto se basa en el desarrollo de la aplicación **CellCountApp** para la detección y conteo de células en imágenes de microscopía. En este respositorio se encuentran todos los documentos asociados al proyecto sobre los requerimientos funcionales y de diseño del sistema. Asimismo, se puede encontrar tanto el Mock-Up, como el Dataset utilizado y los códigos asociados para el enternamiento de la red neuronal de detección. En el directorio de App se puede ver una primera versión de la interfaz de la aplicación sencilla, capaz de obtener la localización y conteo de algunas células al cargar una imagen mediante *bounding boxes*. 


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



## Tutorial de ejecución
En esta parte se explican los pasos necesarios para poder poner en marcha cada uno de los códigos desarrollados para el entrenamiento y la detección de células en las imágenes. Si se desea únicamente probar la aplicación puede ir directamente a la sección *Ejecución de la aplicación*. 

### Restructuración del dataset 
Para poder entrenar la red neuronal, primero se necesita configurar las carpetas y anotaciones de las imágenes de la manera esperada por YOLO. Esto ya ha sido realizado con el código contenido en **Dataset preprocessing**. Este código obtiene los XML que definen los *bounding boxes* de cada imagen reescalada y normalizada para poder utilizarlos en el entrenamiento de YOLOv5. Estos se guardan en la carpeta *annotations_YOLO*. 

A continuación, se han copiado los archivos de esta carpeta a Code/trainingCell/Data, así como las imágenes correspondientes a los txt. Ejecutando las funciones de *trainCell.py*: *loadDataset()*, *splitDataset()* y *saveSplittedDataset()*, se reordenan las imágenes y anotaciones dentro de la carpeta *Code/trainingCell/dataset/*, en carpetas de entrenamiento y validación. 


### Entrenamiento de YOLOv5
Si se desease volver a entrenar el modelo de YOLOv5 con las imágenes y anotaciones de las células se debe instalar el repositorio de YOLOv5. Dentro del directorio de /Code/trainingCell, se ejecuta el siguiente comando: 

<code>git clone https://github.com/ultralytics/yolov5</code>

Después, se debe crear un entorno virtual utilizando el archivo *requirements.txt* proporcionado. Ya con el dataset organizado dentro de la carpeta trainingCell según el paso anterior, se copia el archivo *dataset.yaml* dentro de la carpeta *trainingCell/yolov5/data* y se comprueba que las rutas contenidas en el sean las adecuadas según nuestro ordenador. 

Finalmente, ya se puede ejecutar la función *trainModel()* de *trainCell.py* que ejecuta el entrenamiento de YOLOv5 con las imágenes y anotaciones de las células. Se pueden modificar el tamaño de los *batches* y las épocas en esta función. Al final de la ejecución, se obtendrá el peso de la red entrenada dentro de la carpeta de *yolov5/runs/train/expX/weights*. Para guardar este peso como una red, se selecciona el archivo *best.pt* de la carpeta anterior y dentro del directorio *trainingCells*, se ejecuta la función *saveModel()* con las rutas correspondientes para guardar la red neuronal completa.  


### Ejecución de la aplicación
La ejecución de **CellCountApp** es realmente sencilla. Para ello, se debe crear un entorno virtual donde se añadan las dependencias adjuntadas dentro del archivo *requirements.txt*. A continuación, solo se deberá ejecutar el código *CellCountApp.py* que deberá abrir una ventana de **Tkinker** donde aparezcan los botones *Cargar imagen* y *Cerrar imagen*:


<p align="center">
<img src="https://user-images.githubusercontent.com/93343403/228200416-95f98ff9-4917-4374-82d0-20fcbd0d2b13.png" width="40%" height="40%">
</p>


Al pulsar cargar imagen, se puede elegir cualquier imagen por ejemplo de la carpeta de validación contenida en *Code/trainingCell/dataset/images/val* y se mostrarán tanto la imagen sin procesar como la imagen con los *bounding boxes* predichos por la red neuronal *yolov5s_cells1.onnx*. Después se puede pulsar en el botón de cerrar para cargar una nueva imagen. 

<p align="center">

<img src="https://user-images.githubusercontent.com/93343403/228200340-0c8efc8c-9271-427e-a6b6-9ca114077f1a.png" width="40%" height="40%">
</p>


# Conclusión 

Cabe decir que este repositorio se encuentra bajo desarrollo por lo que actualmente, solo posee los documentos para el comienzo del proyecto, el conjunto de datos que se utilizará para el entrenamiento del modelo y el mock-up del sistema. 

