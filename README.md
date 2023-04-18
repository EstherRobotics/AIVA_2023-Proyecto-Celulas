# AIVA_2023-Proyecto-Celulas

## Índice

1. [Introducción](#introducción)

2. [Estructura del proyecto](#estructura-del-proyecto)

3. [Descripción detallada](#descripción-detallada)

4. [Tutorial de ejecución](#tutorial-de-ejecución)

5. [Instalación de la aplicación con Docker](#instalación-de-la-aplicación-con-docker)

6. [Interfaz gráfica CellCountApp](#interfaz-gráfica-cellcountapp)


## Introducción

Este proyecto se basa en el desarrollo de la aplicación **CellCountApp** para la detección y conteo de células en imágenes de microscopía. En este respositorio están todos los documentos asociados al proyecto sobre los requerimientos funcionales y el sistema. Asimismo, se puede encontrar tanto el Mock-Up, como el dataset utilizado y los códigos asociados para el entrenamiento de la red neuronal de detección. En el directorio de **App** se encuentra la versión final de la aplicación que también puede ejecutarse con el contenedor *cellprojectdocker* como se explicará en las siguientes secciones. 

## Estructura del proyecto
La estructura del respositorio se divide en varias carpetas, donde se han destacado sus directorios principales: 

* Code
  * trainingCell
* Dataset
  * Annotations
  * JPEGImages 
* Dataset preprocessing 
  * annotations_YOLO
  * xml_preprocessing
* Diagrams 
* Docker
  * Dockerfile 
* Docs
  * DSR_Células
  * Documento_sistema_funcional_células
  * Documento_diseño_células 
  * Presupuesto
* Mock-up
* Tests
  * tests
  * run_tests
* App
  * CellCountApp
  * imageCell  

En el directorio de **Code** se encuentra *trainingCell*, que incluye los archivos necesarios utilizados en el entrenamiento de la red neuronal para la detección de células. En la carpeta de **Dataset**, están contenidas las imágenes de células y las anotaciones de sus posiciones proporcionadas inicialmente. El procesamiento de este **Dataset**, fue realizado en **Dataset_preprocessing**, donde se extrayeron las anotaciones de las imágenes en el formato requerido por YOLO. Por otra parte, en **Diagrams**, se pueden ver los diagramas de clases, secuencia, actividades y despliegue. Dentro de **Docker**, está el *Dockerfile* junto con los archivos necesarios para poder crear la imagen *cellprojectdocker*. En la sección de **Docs** se guarda el documento DSR, el de presupuesto y el nuevo documento de diseño. Dentro del **Mock-up**, está un esquema general de programación de la aplicación con los test unitarios desarrollados inicialmente. Los nuevos tests unitarios están dentro de **Tests**, en el archivo *tests.py*, y pueden ejecutarse con run_tests.py para comprobar su funcionamiento. Finalmente, en el directorio **App**, se puede ver el código de la aplicación contenido en *CellCountApp.py*, que utiliza funciones de *imageCell.py* para el procesamiento. 


## Descripción detallada

**CellCountApp** está diseñada principalmente para poder detectar y contar el número de células de imágenes de microscopía. Esta detección se hace mediante el uso de la red neuronal YOLOv5 y obtiene las posiciones de las células mediante la mediante la definición de zonas rectangulares. Se puede ver un ejemplo del tipo de imágenes que se utilizan a continuación: 

<p align="center">
<img src="https://user-images.githubusercontent.com/46898686/225309474-a1989b4f-5393-4303-9fd0-03c5c3c1fd35.png" width="40%" height="40%">
</p>

Si se procesa la información contenida en **Dataset/Annotations** sobre la imagen correspondiente, se pueden dibujar los *bounding boxes* asociados a cada célula: 

<p align="center">
<img src="https://user-images.githubusercontent.com/46898686/225309987-9d719387-2e36-418b-bc1b-7fe2e3083437.png" width="40%" height="40%">
</p>


Se puede observar que hay varios tipos de células y que además estas pueden encontrarse a lo largo de toda la imagen en orientaciones distintas. Se debe tener en cuenta que pueden ocurrir superposiciones entre las células por lo que este será un tema clave a la hora de realizar la detección. 

Para el desarrollo del proyecto se entrenará la red neuronal YOLOv5 con distintos parámetros, eligiendo aquella que ofrezca mejores resultados de detección. En la entrega actual, se ha entrenado una versión básica de esta red y el modelo completo se encuentra guardado en el archivo *yolov5s_cells.onnx*. Siguiendo el tutorial descrito abajo, se puede ejecutar la aplicación y ver el procesamiento de forma visual, así como el número total de células detectadas. 

Como ya se ha visto en la estructura del proyecto, se han desarrollado los Diagramas UML de clases, secuencias y actividad, que muestran un esquema sobre el funcionamiento de las clases programadas. Estos diagramas, así como los tests unitarios realizados, han sido descritos con más detalle en el documento de diseño. Por otra parte, se encuentra el documento del sistema funcional, que ofrece una descripción más detallada de la versión final de la aplicación, su instalación y el diagrama de despliegue y secuencias. 


## Tutorial de ejecución
En esta parte se explican los pasos necesarios para poder poner en marcha cada uno de los códigos desarrollados para el entrenamiento y la detección de células en las imágenes. Algunos de ellos ya han sido ejecutados, como la parte de reestructuración del dataset o el entrenamiento, por lo que no es necesario volver a procesarlos. Si se desea únicamente probar la aplicación o los tests se puede ir directamente a la sección *Ejecución de la aplicación* y *Ejecución de los tests unitarios*. 

Para poder utilizar cualquiera de los códigos, se debe hacer una instalación previa de un entorno virtual, por ejemplo de Anaconda, utilizando la lista de dependencias *requirements.txt* con el comando: 

<code>conda install --yes --file requirements.txt</code>


### Reestructuración del dataset 
Para poder entrenar la red neuronal, primero se necesita configurar las carpetas y anotaciones de las imágenes de la manera esperada por YOLO. Esto ya ha sido realizado con el código contenido en **Dataset preprocessing**. Este código obtiene los XML que definen los *bounding boxes* de cada imagen reescalada y normalizada para poder utilizarlos en el entrenamiento de YOLOv5 y los guarda en la carpeta *annotations_YOLO*. 

A continuación, se han copiado los archivos de esta carpeta a *Code/trainingCell/data*, así como las imágenes correspondientes a los TXT. Ejecutando las funciones de *trainCell.py*: *loadDataset()*, *splitDataset()* y *saveSplittedDataset()*, se reordenan las imágenes y anotaciones dentro de la carpeta *Code/trainingCell/dataset/*, en carpetas de entrenamiento y validación. En el repositorio actual, este desarrollo ya ha sido realizado, por lo que no sería necesario volver a ejecutar este procedimiento. 


### Entrenamiento de YOLOv5
Si se desease volver a entrenar el modelo de YOLOv5 con las imágenes y anotaciones de las células se debe instalar el repositorio de YOLOv5. Dentro del directorio de */Code/trainingCell*, se ejecuta el siguiente comando: 

<code>git clone https://github.com/ultralytics/yolov5</code>

Ya con el dataset organizado dentro de la carpeta *trainingCell* según el paso anterior, se copia el archivo *dataset.yaml* dentro de la carpeta *trainingCell/yolov5/data* y se comprueba que las rutas contenidas en él sean las adecuadas según nuestro ordenador. Se deberán actualizar si es necesario con las rutas donde se encuentra el *trainingCell/dataset*. 

Finalmente, ya se puede ejecutar la función *trainModel()* de *trainCell.py* que ejecuta el entrenamiento de YOLOv5 con las imágenes y anotaciones de las células. Se pueden modificar el tamaño de los *batches* y las épocas en esta función. Al final de la ejecución, se obtendrá el peso de la red entrenada dentro de la carpeta de *yolov5/runs/train/expX/weights*. Para guardar este peso como una red, se selecciona el archivo *best.pt* de la carpeta anterior y dentro del directorio *trainingCells*, se ejecuta la función *saveModel()* con las rutas correspondientes actualizadas (*path_save* y *path_weight*) para guardar la red neuronal completa.  


### Ejecución de la aplicación en el sistema local 
La ejecución de **CellCountApp** es realmente sencilla. Dentro del entorno virtual, se deberá ejecutar el código *CellCountApp.py* contenido en **App** que abrirá una ventana de **Tkinker** donde aparecen los botones *Cargar imagen* y *Cerrar imagen* como en la siguiente imagen:


<p align="center">
<img src="https://user-images.githubusercontent.com/93343403/228200416-95f98ff9-4917-4374-82d0-20fcbd0d2b13.png" width="40%" height="40%">
</p>


Al pulsar en *Cargar imagen*, se puede elegir cualquier imagen por ejemplo de la carpeta de validación contenida en *Code/trainingCell/dataset/images/val* y se mostrarán tanto la imagen sin procesar como la imagen con los *bounding boxes* predichos por la red neuronal *yolov5s_cells1.onnx*. Después, se puede pulsar en el botón de cerrar para cargar una nueva imagen. 

<p align="center">
<img src="https://user-images.githubusercontent.com/93343403/228200340-0c8efc8c-9271-427e-a6b6-9ca114077f1a.png" width="40%" height="40%">
</p>

### Ejecución de los tests unitarios
Para poder probar el funcionamiento de los tests, dentro de la carpeta **Tests** se debe ejecutar el código *run_tests.py*. En la línea de comandos se mostrará información sobre si los tests se han pasado con éxito o ha habido algún fallo en la ejecución. 


## Instalación de la aplicación con Docker 


## Interfaz gráfica 






