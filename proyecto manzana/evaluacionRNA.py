"""
Aplicacion para extraer un recorte de la imagen donde se encuentra
una manzana.

"""

from __future__ import division
import cv2
import numpy as np
from PIL import Image
from os import listdir
import os
import neurolab as nl
import scipy as sp


def mostar(imagen):
    imagen = cv2.resize(imagen, (600, 400))
    cv2.imshow('manzana', imagen)
    cv2.waitKey(0)

def encontrar_contorno(imagen):
    imagen = imagen.copy()
    (contornos, jerarquia) = cv2.findContours(imagen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = \
        [(cv2.contourArea(contorno), contorno) for contorno in contornos]
    mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

    mascara = np.zeros(imagen.shape, np.uint8)
    cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
    return mayor_contorno, mascara

def contorno_rectangulo(imagen, contorno):
    imagenConElipse = imagen.copy()
    elipse = cv2.fitEllipse(contorno)
    factor_redn = 0.5
    sx = int((elipse[1][0]*factor_redn)/2)
    sy = int((elipse[1][1]*factor_redn)/2)
    x = int(elipse[0][0]) - sy
    y = int(elipse[0][1]) - sx
    #cv2.elipse(imagenConElipse, elipse, green, 2, cv2.LINE_AA)
    #cv2.rectangle(imagenConElipse, (x,y), ((x + sy*2), (y + sx*2)), (255,0,0),2)
    imagenConElipse = imagenConElipse[y:(y + sx*2), x:(x + sy*2)]
    return imagenConElipse

def encontrar_manzana(imagen):
    imagen2 = imagen.copy()
    imagen3 = imagen.copy()
    imagen2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2HSV)
    max_dimension = max(imagen2.shape)
    scale = 700/max_dimension
    imagen2 = cv2.resize(imagen2, None, fx=scale, fy=scale)
    imagen3 = cv2.resize(imagen3, None, fx=scale, fy=scale)
    imagen_azul = cv2.GaussianBlur(imagen2, (7, 7), 0)
    min_rojo = np.array([0, 100, 80])
    max_rojo = np.array([10, 256, 256])

    mascara1 = cv2.inRange(imagen_azul, min_rojo, max_rojo)
    min_rojo2 = np.array([170, 100, 80])
    max_rojo2 = np.array([180, 256, 256])

    mascara2 = cv2.inRange(imagen_azul, min_rojo2, max_rojo2)
    mascara = mascara1 + mascara2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mascara_cerrada = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    mascara_limpia = cv2.morphologyEx(mascara_cerrada, cv2.MORPH_OPEN, kernel)

    contorno_manzana_grande, mascara_manzana = encontrar_contorno(mascara_limpia)

    rectangulo_manzana = contorno_rectangulo(imagen3, contorno_manzana_grande)
    return rectangulo_manzana

"""

===============================================================================================================

"""

def sacar_pixels(imagen):
    #se abre la imagen
    im = Image.open(imagen)
    im = im.resize((40, 10), Image.ANTIALIAS)
    #lectura de pixels
    pixels = im.load()
    filas, columnas = im.size
    decimales = 4
    cadena = ""
    for columna in range (columnas):
        for fila in range(filas):
            #se separan los valores RGB y se escriben en el archivo
            rojo = str(normalizar(pixels[fila,columna][0]))
            verde = str(normalizar(pixels[fila,columna][1]))
            azul = str(normalizar(pixels[fila,columna][2]))
            cadena = cadena + rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "

    return cadena


def normalizar(valor):
    salida = (valor*1.)/255.
    return salida

"""
=======================================================================================
"""

imagen = cv2.imread("prueba.jpg")
imagen = encontrar_manzana(imagen)
cv2.imwrite("manzana-recortada.jpg",imagen)

cadena =  sacar_pixels("manzana-recortada.jpg")

if(os.path.exists("datos-manzana.csv")== True):
    os.remove("datos-manzana.csv")

archivo_entrenamiento = open("datos-manzana.csv", "a")

archivo_entrenamiento.write(cadena)
archivo_entrenamiento.close()

datos = np.matrix(sp.genfromtxt("datos-manzana.csv", delimiter=" "))

#print datos.shape

rna = nl.load("RNA.txt")

salida = rna.sim(datos)

maduro = salida[0][0] * 100
verde = salida[0][1] * 100
podrido = salida[0][2] * 100

resultado = ""
print maduro
print verde
print podrido

if (podrido > 80.):
    if (maduro > 40.):
        resultado = "La manzana esta a punto de podrirse"
    else:
        resultado = "La manzana esta podrida"
elif (maduro > 80.):
    if (podrido > 40.):
        resultado = "La manzana esta pasandose de su madurez"
    elif (verde > 40.):
        resultado = "La manzana esta a punto de llegar a su madurez"
    else:
        resultado = "La manzana esta en su mejor punto"
elif (verde > 80.):
    if (maduro > 40.):
        resultado = "La manzana esta madurando"
    else:
        resultado = "La manzana esta verde"

print resultado
