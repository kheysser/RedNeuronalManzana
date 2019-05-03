import cv2
import numpy as np
from os import listdir


def orilla(Combinacion):
    Combinacion = Combinacion.copy()
    #encontramos la orilla eliminando cada uno de los puntos redundantes, esto encuentra los puntos maximos cv2.CHAIN_APPROX_SIMPLE
    #cv2.retr_tree sabe como va la jerarquia de contornos
    (Orillas, Ordenamiento)  = cv2.findContours(Combinacion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #encuentra los tamanos de la orillas
    tamano = [(cv2.contourArea(contorno), contorno) for contorno in Orillas]
    print("tamano")
    print(tamano)
    #asigna ese tamano
    tamanofinal = max(tamano, key=lambda x: x[0])[1]
    print("final")
    print(tamanofinal)
    #vuelve oscura la imagen
    manzana = np.zeros(Combinacion.shape, np.uint8)
    #cv2.imshow('titulo', manzana)
    #cv2.waitKey(0)
    #dibuja los contornos basicamente encuentra los que estaba antes
    hola = cv2.drawContours(manzana, [tamanofinal], -1, 255, -1)
    #cv2.imshow('titulo', hola)
    #cv2.waitKey(0)
    return tamanofinal, manzana

def RecorteRectangulo(imagen, contorno):

    imgElipse = imagen.copy()
    #Ajustamos la elipse
    elipse = cv2.fitEllipse(contorno)
    tamanorectangulo = 0.4
    sx = int((elipse[1][0]*tamanorectangulo)/2)
    sy = int((elipse[1][1]*tamanorectangulo)/2)
    x = int(elipse[0][0]) - sy
    y = int(elipse[0][1]) - sx
    cv2.ellipse(imgElipse, elipse, (0,255,0), 2)
    PRUEBA=cv2.rectangle(imgElipse, (x,y), ((x + sy*2), (y + sx*2)), (255,0,0),2)
    #cv2.imshow('titulo', PRUEBA)
    #cv2.waitKey(0)
    imgElipse = imgElipse[y:(y + sx*2), x:(x + sy*2)]

    return imgElipse


def ManzanaRecorte(imagen):
    imagenManzana = imagen.copy()
    imagenCopia = imagen.copy()
    #cv2.imshow('titulo', imagenManzana)
    #cv2.waitKey(0)
    #Convierte una imagen de un espacio de color a otro aca los bits se invierten los de colores
    imagenManzana = cv2.cvtColor(imagenManzana, cv2.COLOR_BGR2HSV)
    #cv2.imshow('titulo', imagenManzana)
    #cv2.waitKey(0)
    #Encuentra las dimensiones de la foto
    dimension = max(imagenManzana.shape)
    print(dimension)
    dimensionFinal = 700/dimension
    print(dimensionFinal)
    imagenManzana = cv2.resize(imagenManzana, None, fx=dimensionFinal, fy=dimensionFinal)
    #cv2.imshow('titulo', imagenManzana)
    #cv2.waitKey(0)
    imagenCopia = cv2.resize(imagenCopia, None, fx=dimensionFinal, fy=dimensionFinal)
    #cv2.imshow('titulo', imagenCopia)
    #cv2.waitKey(0)

    #Difuminacion de la imagen con blur tiene que ser impar
    Difuminacion = cv2.blur(imagenManzana, (7, 7))
    #cv2.imshow('titulo', Difuminacion)
    #cv2.waitKey(0)
    #se ve el rango de colores que necesitaremos encontrar en la foto
    ColorMinimo = np.array([0, 100, 80])
    ColorMaximo = np.array([10, 256, 256])
    Verde_Amarillo = cv2.inRange(Difuminacion, ColorMinimo, ColorMaximo)
    #cv2.imshow('titulo', Verde_Amarillo)
    #cv2.waitKey(0)
    #se ve el rango de colores que necesitaremos encontrar en la foto
    ColorMinimo2 = np.array([170, 100, 80])
    ColorMaximo2 = np.array([180, 256, 256])
    Rojo = cv2.inRange(Difuminacion, ColorMinimo2, ColorMaximo2)

    ColorMinimo4 = np.array([15, 100, 80])
    ColorMaximo4 = np.array([105, 255, 255])
    Amarillo = cv2.inRange(Difuminacion, ColorMinimo4, ColorMaximo4)

    Combinacion = Verde_Amarillo + Rojo + Amarillo
    #cv2.imshow('titulo', Combinacion)
    #cv2.waitKey(0)
    #forma y tamano
    Elipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    #limpiamos la imagen de las pequenas imperfecciones que tenga con la primera cerramos orificios dentro de nuestros objetos"""
    LimpiezaOrificiosCombinacion = cv2.morphologyEx(Combinacion, cv2.MORPH_CLOSE, Elipse)
    #cv2.imshow('titulo', LimpiezaOrificiosCombinacion)
    #cv2.waitKey(0)
    #con esta limpiamos todo lo que esta fuera de nuestros objetos"""
    LimpiezaFinalCombinacion = cv2.morphologyEx(LimpiezaOrificiosCombinacion, cv2.MORPH_OPEN, Elipse)
    #cv2.imshow('titulo', LimpiezaFinalCombinacion)
    #cv2.waitKey(0)

    contorno, mascaraFinal = orilla(LimpiezaFinalCombinacion)
    Recorte = RecorteRectangulo(imagenCopia, contorno)
    return Recorte


def Directorio(carpeta_Manzanas, carpeta_Recortes, imagenes):
    #toma el nombre de cada una de las imagenes
    for imagen in imagenes:
        #print imagen
        #obtiene la imagen que sera nuestra entrada
        Entrada = cv2.imread(carpeta_Manzanas + "/" + imagen)
        #la imagen se manda a recortar
        SalidaRecorte = ManzanaRecorte(Entrada)
        #se guarda la imagen en la carpeta de salida
        cv2.imwrite(carpeta_Recortes + "/" + imagen, SalidaRecorte)


#busca en los directorios manzana1 es donde esta la carpeta de las fotos originales
#manzanaRecortada es donde se almacena las imagenes recortadas
#./manzana1 es la lista de imagenes que tendremos en la carpeta manzana1
Directorio("manzanaInmadura", "manzanarecortadainmadura", listdir("./manzanaInmadura"))
Directorio("manzanaMadura", "manzanarecortadamadura", listdir("./manzanaMadura"))
Directorio("manzanaPodrida", "manzanarecortadapodrida", listdir("./manzanaPodrida"))
