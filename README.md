# AIVA_2023-Proyecto-Celulas

## Índice

*[Introducción](#introducción)

*[Estructura del proyecto](#estructura-del-proyecto)

*[Descripción detallada](#descripción-detallada)

*[Conclusión](#conclusión)

## Introducción

Este proyecto se basa en el desarrollo de la aplicación CellCountApp para la detección y conteo de células en imágenes de microscopía. En este respositorio se encuentran todos los documentos asociados al proyecto, tanto de los requerimientos del sistema como de la primera parte de su implementación. El objetivo final es desarrollar una interfaz capaz de obtener la localización de cada célula en la imagen mediante *bounding boxes*. 


## Estructura del proyecto
La estructura actual se divide en tres carpetas aunque posteriormente será ampliado al desarrollar el código de la aplicación: 

* Dataset
  * Annotations
  * JPEGImages 
* Docs
  * DSR_Células
  * Presupuesto
* Mock-up

En Dataset se encuentran las imágenes de células y las anotaciones de las posiciones de las células. En la sección de Docs, se encuentra el documento DSR y el presupuesto y finalmente en el Mock-up, se halla un esquema general de programación de la aplicación con los test unitarios. 


## Descripción detallada

CellCountApp estará diseñada principalmente para el conteo de células al enviar una imagen de microscopio y poder obtener su posición mediante la definición de zonas rectangulares. Un ejemplo de las imágenes a tratar se muestra en la siguiente imagen: 

<p align="center">
<img src="https://user-images.githubusercontent.com/46898686/225309474-a1989b4f-5393-4303-9fd0-03c5c3c1fd35.png" width="50%" height="50%">
</p>

Al procesar las anotaciones de Dataset/Annotations para la imagen correspondiente, se pueden dibujar los bounding boxes asociados a cada célula como se muestra a continuación: 

<p align="center">
<img src="https://user-images.githubusercontent.com/46898686/225309987-9d719387-2e36-418b-bc1b-7fe2e3083437.png">
</p>


Se puede observar que hay varios tipos de células y que además estas pueden encontrarse a lo largo de toda la imagen en orientaciones distintas. Además, pueden ocurrir superposiciones entre ellas. 


Para el desarrollo del proyecto se programarán distintos modelos de YOLO que serán evaluados con métricas IoU. Estos modelos, procesarán la imagen, obteniendo la localización de las células esperada. 

La interfaz final de CellCountApp, estará programada en Tkinker. El usuario podrá cargar la imagen a procesar y se mostrará la información del procesamiento de forma visual, otorgando también el número total de células detectadas. 



# Conclusión 
Cabe decir que este repositorio se encuentra bajo desarrollo por lo que actualmente, solo posee los documentos para el comienzo del proyecto, el conjunto de datos que se utilizará para el entrenamiento del modelo y el mock-up del sistema. 

