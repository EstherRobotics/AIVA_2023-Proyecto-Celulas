# AIVA_2023-Proyecto-Celulas

## Índice

*[Introducción](#introducción)

*[Estructura del proyecto](#estructura-del-proyecto)

*[Descripción](#descripción)

*[Conclusión](#conclusión)

## Introducción

El objetivo de este proyecto es crear una aplicación que sea capaz de detectar y contar células al introducir una imagen de microscopía. En adelante, se denominará a dicha aplicación con el nombre de CellCountApp. CellCountApp estará diseñada principalmente para el conteo de células al enviar una imagen de microscopio, pero además será capaz de localizar cada una de las células con bounding box. Cabe añadir que podrá utilizarse con cualquier clase de célula, lo que implica que deberá reconocer distintos tipos de las mismas, así como una posible superposición entre ellas.

## Estructura del proyecto


## Descripción


En cuanto a la estructura del proyecto, la finalidad es desarrollar una aplicación (tipo interfaz gráfica) en Python con una arquitectura de cliente/servidor, de tal manera que el usuario pueda comunicarse con la aplicación creada. Es decir, que el cliente mande una imagen al servidor, este la procese, realice la detección de células y devuelva dicha imagen al cliente junto con el número de células encontradas.
Para abordar este problema se pretende utilizar técnicas robustas de deep learning como son las redes neuronales. En concreto, la idea es usar la arquitectura YOLO, a partir del método de transfer learning. 

Para un mayor entendimiento de este proyecto la aplicación recibirá una imagen de microscopía en color como la siguiente: 
<p align="center">
<img src="https://user-images.githubusercontent.com/46898686/225309474-a1989b4f-5393-4303-9fd0-03c5c3c1fd35.png">
</p>
Tras realizar la detección de células, la aplicación CellCountApp devolverá la imagen procesada con la posición de cada una de las células a partir de la utilización de bounding boxes como se muestra en la siguiente imagen:
![image](https://user-images.githubusercontent.com/46898686/225309987-9d719387-2e36-418b-bc1b-7fe2e3083437.png)

Además, como se ha dicho anteriormente, se proporcionará el número total de células encontradas a partir del conteo de los bounding boxes.



