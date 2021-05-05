import random # Para generar num. aleatorios en la A y B 

import math

import multiprocessing as mp # Para trabajar en paralelo

import time




def fibonacci(n): 
    a = 0
    b = 1
    if n < 0: 
        print("Incorrect input") 
    elif n == 0: 
        return a 
    elif n == 1: 
        return b 
    else: 
        for i in range(2,n+1): 
            c = a + b 
            a = b 
            b = c
            if (i == n):
                print(b) 
        return b


def par_mult(n): # f() que prepara el reparto de trabajo para la mult. en paralelo

    n_cores = mp.cpu_count() # Obtengo los cores de mi pc  

    size_n = math.ceil(n/n_cores) # Filas a procesar x c/cpre, ver Excel adjunto

    MC = mp.RawArray('i', n) # Array MC de memoria compartida donde se almacenaran los resultados, ver excel adjunto

    cores = [] # Array para guardar los cores y su trabajo

    for core in range(n_cores):# Asigno a cada core el trabajo que le toca, ver excel adjunto

        i_MC = min(core * size_n, n) # Calculo i para marcar inicio del trabajo del core en relacion a las filas

        f_MC = min((core + 1) * size_n, n) # Calculo f para marcar fin del trabajo del core, ver excel

        cores.append(mp.Process(target=par_core, args=(n, MC, i_MC, f_MC)))# Añado al Array los cores y su trabajo

    for core in cores:

        core.start()# Arranco y ejecuto el trabajo para c/ uno de los cores que tenga mi equipo, ver excel





def par_core(n, MC, i_MC, f_MC): # La tarea que hacen todos los cores

    for i in range(i_MC, f_MC): # Size representado en colores en el excel que itera sobre las filas en A

        for j in range(len(n)): # Size representado en colores en el excel que itera sobre las columnas en B

            for k in range(len(n)): # n_fil_B o lo que es l mismo el n_col_A

                MC[i*len(n) + j] += n[i][k] * n[k][j]# Guarda resultado en MC[] de cada core


if __name__ == '__main__':
    n = 8
    start= time.time()
    print (fibonacci(n))
    fin = time.time()
    #print("Numero: 21845965")
    print('Tiempo de ejecucion de fibonacci =', fin-start )
    print('Tiempo de ejecucion de fibonacci', fin-start )