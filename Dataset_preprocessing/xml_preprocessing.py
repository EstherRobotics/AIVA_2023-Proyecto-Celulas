import glob
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


#Esta función recibe el path de la carpeta que contiene todos los xml a analizar
def extract_xml (path):
    anotaciones=[]
    for filepath in glob.iglob(path+'/**/*.*', recursive=True):
        if not filepath.endswith((".xml",".XML")):
            continue
        anotaciones.append(filepath)

    dataset=[]
    for file in range(len(anotaciones)):
        with open(anotaciones[file], 'r') as f:
            data = f.read()

        Bs_data = BeautifulSoup(data, "xml")
        objeto=Bs_data.find_all('object')

        for j in range(len(objeto)):

            xmin=objeto[j].find("xmin").text
            xmax=objeto[j].find("xmax").text
            ymin=objeto[j].find("ymin").text
            ymax=objeto[j].find("ymax").text
            
            #Guardamos en el formato adecuado para YOLO
            center_x=((int(xmin)+int(xmax))/2)/640
            center_y=((int(ymin)+int(ymax))/2)/480
            width=(int(xmax)-int(xmin))/640
            height=(int(ymax)-int(ymin))/480

            columnas=[anotaciones[file].split("\\")[2].split('.')[0]+'.jpg',center_x,center_y,width,height]
            dataset.append(columnas)

    #Creamos dataframe con el nombre correspondiente, xmin, xmax, ymin, ymax. Habrá tantas filas por xml como bounding box tenga el mismo
    data = pd.DataFrame(dataset, columns=["Nombre", "xmin", "xmax", "ymin", "ymax"])

    return data

#Esta función recibe el path de la carpeta que contiene todas las imágenes a analizar
def extract_filename_images(path):
    imagenes=[]
    for filepath in glob.iglob(path+'/**/*.*', recursive=True):
        if not filepath.endswith((".jpeg",".JPEG",'jpg',".JPG")):
            continue
        imagenes.append(filepath)
    return imagenes


#Recibe el dataset con formato de nombre, xmin, xmax, ymin, ymax y una lista con el nombre de todas las imágenes que se tienen
def create_txt(dataset, filename_images):
#CREAR TXT
    contador=0
    for img in range(len(filename_images)):
        yolo_list=[]
        try:
            #El .split dependerá de la ruta. Habría que poner el número donde se encuentre el nombre BloodIMage..
            while filename_images[img].split('\\')[2]==dataset["Nombre"][contador]:
                clase=str(0)
                xmin=str(dataset["xmin"][contador])
                xmax=str(dataset["xmax"][contador])
                ymin=str(dataset["ymin"][contador])
                ymax=str(dataset["ymax"][contador])

                yolo_list.append([clase, xmin, xmax, ymin, ymax])
                contador+=1
            #Creamos .txt por xml. El .txt tendrá tantas filas como células tenga, y cada fila contendrá la clase, xmin, xmax, ymin, ymax
            #La clase será 0 por defecto, ya que no vamos a diferenciar entre diferentes tipos de células
            np.savetxt(str(filename_images[img].split('\\')[2])[:-4]+'.txt', yolo_list, fmt='%s') 
        except:
            print("No hay más anotaciones")

#data=extract_xml('Archive')
#filenames=extract_filename_images('Archive')
#txt=create_txt(data, filenames)
