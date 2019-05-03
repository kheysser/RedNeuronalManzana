# RedNeuronalManzana
Proyecto que realiza el análisis de madurez de una manzana mediante una foto 
Tiene diferentes carpetas, las cuales son:

ManzanaMadura, manzanaPodrida, manzanainmadura son las carpetas que tienen las imágenes con las cuales entrenará la red neuronal.

Encontrar_manzanas.py es el archivo que utiliza los diferentes filtros y recorta las imágenes que se seleccionan para entrenar la neurona.

Valores_entrada.py es el archivo que convierte las imagenes recortadas en entradas para el uso de la RNA.

RedNeuronal.py en este archivo se entrena la red, pudiendose modificar las épocas que se quieren entrenar así también la meta del error menor que se solicita.

Manzanarecortadamadura, Manzanarecortadainmadura, Manzanarecortadapodrida tiene las imágenes recortadas que servirán para la entrada de la red neuronal.

RNA.txt: red neuronal ya entrenada.

En la consola se escribe "python evaluaciónRNA.py" para ejecutar el programa y seleccionar la imagen de la manzana que se quiere examinar.
