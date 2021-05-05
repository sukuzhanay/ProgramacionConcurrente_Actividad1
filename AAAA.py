def Menu_datos():
    a = input("Ingrese su email de la uem: ")
    b = input("Número de expediente: ")
    Principal(a,b)

def Principal(a,b):
    print("\n----UNIVERSIDAD EUROPEA DE MADRID----")
    print("\n----Escuela de Ingeniería Arquitectura y diseño----\n\n")
    print("*************MENU************\n")
    print("Bienvenido " + a + " - " + b)
    print("Pregunta 1: AAAA")
    print("Pregunta 2: BBBB")
    print("Pregunta 3: CCCC\n")
    a = int(input("Ingrese la pregunta a visualizar: "))
    if(a==1):
        print('\n\nMatriz  A y B se han multiplicado con exito en SECUENCIAL ha tardado ', finS-inicioS, ' y en PARALELO ', finP-inicioP)
    elif(a==2):
        print("Pregunta2")
    elif(a==3):
        print("Pregunta3")
    else:
        print("Seleccione una pregunta válida")

Menu_datos()