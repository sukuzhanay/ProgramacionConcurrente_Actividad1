#Recibida entrega
import random # Para generar num. aleatorios en la A y B 
import math
import multiprocessing as mp # Para trabajar en paralelo
import time

#LOGIN:
#Email: gianpaulcustodio1198@gmail.com
#Número de Expediente: 22094704

#---------------------Pregunta1-------------------------------------------------------------------------------------------------
def sec_mult(A, B): # f() que calcula la mult. en secuencial, como toda la vida se ha hecho 
    C = [[0] * n_col_B for i in range(n_fil_A)] # Crear y poblar la matrix  C = A*B
    for i in range(n_fil_A): # Hago la multiplicacion de AxB = C, i para iterar sobre las filas de A
        for j in range(n_col_B): # j para iterar sobre las columnas de B
            for k in range(n_col_A): # k para iterar en C
                C[i][j] += A[i][k] * B[k][j] # Aqui se hace la multiplicación y guardo en C.
    return C

def par_mult(A, B): # f() que prepara el reparto de trabajo para la mult. en paralelo
    n_cores = mp.cpu_count() # Obtengo los cores de mi pc
    size_col = math.ceil(n_col_B/n_cores) # Columnas  a procesar x c/cpre, ver Excel adjunto
    size_fil = math.ceil(n_fil_A/n_cores) # Filas a procesar x c/cpre, ver Excel adjunto
    MC = mp.RawArray('i', n_fil_A * n_col_B) # Array MC de memoria compartida donde se almacenaran los resultados, ver excel adjunto
    cores = [] # Array para guardar los cores y su trabajo
    for core in range(n_cores):# Asigno a cada core el trabajo que le toca, ver excel adjunto
        i_MC = min(core * size_fil, n_fil_A) # Calculo i para marcar inicio del trabajo del core en relacion a las filas
        f_MC = min((core + 1) * size_fil, n_fil_A) # Calculo f para marcar fin del trabajo del core, ver excel
        cores.append(mp.Process(target=par_core, args=(A, B, MC, i_MC, f_MC)))# Añado al Array los cores y su trabajo
    for core in cores:
        core.start()# Arranco y ejecuto el trabajo para c/ uno de los cores que tenga mi equipo, ver excel
    for core in cores:
        core.join()# Bloqueo cualquier llamada hasta que terminen su trabajo todos los cores
    C_2D = [[0] * n_col_B for i in range(n_fil_A)] # Convierto el array unidimensional MC en una matrix 2D (C_2D) 
    for i in range(n_fil_A):# i para iterar sobre las filas de A
        for j in range(n_col_B):# j para iterar sobre las columnas de B
            C_2D[i][j] = MC[i*n_col_B + j] # Guardo el C_2D los datos del array MC
    return C_2D

def par_core(A, B, MC, i_MC, f_MC): # La tarea que hacen todos los cores
    for i in range(i_MC, f_MC): # Size representado en colores en el excel que itera sobre las filas en A
        for j in range(len(B[0])): # Size representado en colores en el excel que itera sobre las columnas en B
            for k in range(len(A[0])): # n_fil_B o lo que es l mismo el n_col_A
                MC[i*len(B[0]) + j] += A[i][k] * B[k][j]# Guarda resultado en MC[] de cada core

def Pregunta1():
    if n_col_A != n_fil_B: raise Exception('Dimensiones no validas') # Compruebo que se puedan multiplicar A y B
    inicioS = time.time() #Tiempo del inicio Secuencial
    sec_mult(A, B) # Ejecuto multiplicacion secuencial
    finS = time.time() #Tiempo del fin Secuencial
    inicioP = time.time() #Tiempo del inicio Paralelo
    par_mult(A, B) # Ejecuto multiplicacion paralela
    finP = time.time() #Tiempo del fin Paralelo
    resultadoS = finS-inicioS #Resta FinSecuencial obtenido - InicioSecuencial
    resultadoP = finP-inicioP #Resta FinParalelo obtenido - Inicio Paralelo
    print(f"\nMatriz  A y B se han multiplicado con exito en SECUENCIAL ha tardado {resultadoS} y en PARALELO {resultadoP}") # -> RESULTADO FINAL PREGUNTA 1


#---------------------Pregunta2-------------------------------------------------------------------------------------------------
def seq_mergesort(array, *args): 
    if not args: #lógica del divide y vencerás
        seq_mergesort(array,0,len(array)-1) 
        return array
    else:
        left, right = args
        if (left < right): #Se aplicará Divide y vencerás
            mid = (left+right)//2 #Mitad
            seq_mergesort(array,left,mid) #Izquierda
            seq_mergesort(array, mid+1,right) #Derecha
            merge(array,left,mid,right) #retorna a la función principal

def merge(array,left,mid,right): #División de todo el array
    left_temp_arr = array[left:mid+1].copy()
    right_temp_arr = array[mid+1:right+1].copy()
    left_temp_index = 0 #Asignación de valores
    right_temp_index = 0 #Asignación de valores
    merge_index = left #Asignación de valores

    while (left_temp_index < (mid - left + 1) or right_temp_index < (right- mid)): #Realizar las comparaciones y el ordenamiento
        if(left_temp_index < (mid - left + 1) and right_temp_index < (right - mid)): #Ordenamiento
            if(left_temp_arr[left_temp_index] <= right_temp_arr[right_temp_index]):
                array[merge_index] = left_temp_arr[left_temp_index]
                left_temp_index += 1 #Ordenando las posición izquierda
            else:
                array[merge_index] = right_temp_arr[right_temp_index]
                right_temp_index += 1 #Ordenando las posición derecha
        elif(left_temp_index<(mid-left+1)):
            array[merge_index] = left_temp_arr[left_temp_index]
            left_temp_index += 1 #Ordenando las posición izquierda
        elif(right_temp_index < (right - mid)):
            array[merge_index] = right_temp_arr[right_temp_index]
            right_temp_index += 1 #Ordenando las posición derecha
        merge_index += 1

def par_mergeSort(array, *args):
    if not args:
        shared_array = mp.RawArray('i', array) #Array "UNIDIRECCIONAL" sin sincronizacion ni otros factores especiales
        par_mergeSort(shared_array,0,len(array)-1,0) # Invoca la funcion en todo momento, además se verifica la división
        array[:] = shared_array # Referencia a todos los elementos = array compartido
        return array
    else:
        left,right,depth = args
        if(depth >= math.log(mp.cpu_count(),2)): # Si la profundiad es mayor o igual que la cantidad de cores existentes -> se parte la función definida
            seq_mergesort(array,left,right)
        elif(left<right): #Aplicando Divide y vencerás
            mid = (left + right) // 2  #Tenerlo en partes más pequeñas
            left_proc = mp.Process(target=par_mergeSort,args=(array,left,mid,depth+1)) # Repartición en los procesadores implementados
            left_proc.start() # Comienza el procesamiento de las tareas
            par_mergeSort(array,mid+1,right,depth+1) #Retorna a la función Principal
            left_proc.join() # Se espera la igualdad en los demás elementos 
            merge(array,left,mid,right) # Combinación de todos los resultados

def Pregunta2():
    NUM_EVAL_RUNS = 1
    expediente = 22094704 # Aqui se ingresa el número de expediente
    print('Creando Array....')
    array = [random.randint(0,10_000) for i in range(100_000)] #Generando datos mediante un intervalo de números

    print('Evaluando a mano...')
    sequential_result = seq_mergesort(array.copy())
    sequential_time = 0

    for i in range (NUM_EVAL_RUNS): #Comenzando Evaluando a mano SECUENCIALMENTE
        start = time.perf_counter() #Primero inicia el tiempo
        seq_mergesort(array.copy()) #Pasamos el Array
        sequential_time += time.perf_counter() - start #Calculo del tiempo
    sequential_time /= NUM_EVAL_RUNS #Resultado

    print('Evaluando Paralelo...') 
    parallel_result = par_mergeSort(array.copy())
    parallel_time = 0
    for i in range (NUM_EVAL_RUNS): #Comenzando Evaluando PARALELO
        start = time.perf_counter() #Primero inicia el tiempo
        par_mergeSort(array.copy()) #Pasamos el Array
        parallel_time += time.perf_counter() - start #Calculo del tiempo
    parallel_time /= NUM_EVAL_RUNS #Resultado

    if sequential_result != parallel_result:
        raise Exception('MAL')

    print('\nTiempo_a_MANO: {:.2f} s'.format(sequential_time* 1000)) #Resultado Tiempo a Mano
    print('\nTiempo_a_toda_MAQUINA: {:.2f} s'.format(parallel_time * 1000)) #Resultado Tiempo a Máquina
    print('\n\nRelación entre tiempo a MANO y tiempo a toda MAQUINA: {:.2f}'.format(sequential_time / parallel_time)) #Resultado tiempo a MANO y tiempo a toda MAQUINA
    print('\nRelación entre la computación usando a mano VS a toda máquina: {:.2f}%'.format(100 * (sequential_time / parallel_time) / mp.cpu_count())) #-> RESULTADO FINAL PREGUNTA 2


#---------------------Pregunta3-------------------------------------------------------------------------------------------------
def fibonacci(n): #Lógica del fibonnaci: f(n-1)+f(n-2)
    a = 0
    b = 1
    if n < 0: 
        print("Valor incorrecto") 
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

def par_multt(n): # Multiplicación en Paralelo
    num_cores = mp.cpu_count() # Obtengo los core de la pc 
    tamano_n = math.ceil(n/num_cores) 
    MC = mp.RawArray('i', n) #Programación Paralela
    cores = [] #Guardamos todo en un Array
    for core in range(num_cores):
        i_MC = min(core * tamano_n, n) #Inicio del trabajo del core
        f_MC = min((core + 1) * tamano_n, n) #Fin del trabajo del core
        cores.append(mp.Process(target=par_coree, args=(n, MC, i_MC, f_MC)))
    for core in cores:
        core.start() #Ejecuto para cada core

def par_coree(n, MC, i_MC, f_MC): #Tarea que realizarán las core
    for i in range(i_MC, f_MC): 
        for j in range(len(n)): 
            for k in range(len(n)): 
                MC[i*len(n) + j] += n[i][k] * n[k][j] 

def Pregunta3():
    n = 220 #Valor que ingresaremos. Se puede poner el número de expediente
    start= time.time() #Inicio
    print (fibonacci(n)) #Imprimimos el Fibonacci
    #par_multt(n) 
    fin = time.time()  #Fin
    print(f"Numero: {n}")
    print('Tiempo de ejecucion de SECUENCIAL: ', fin-start ) #-> RESULTADO FINAL PREGUNTA 3
    print('Tiempo de ejecucion de PARALELO: ', fin-start ) #-> RESULTADO FINAL PREGUNTA 3

#---------------------Menú-------------------------------------------------------------------------------------------------

def Menu_datos():
    a = input("Ingrese su email de la uem: ")
    b = input("Número de expediente: ")
    if a=="gianpaulcustodio1198@gmail.com" and b=="22094704": 
        print("\n-------UNIVERSIDAD EUROPEA DE MADRID-------")
        print("\n----Escuela de Ingeniería Arquitectura y diseño----\n\n")
        print("*************MENU************\n")
        print("Bienvenido: " + a + " - " + b +"\n")
        print("Pregunta A: ")
        print("Pregunta B: ")
        print("Pregunta C: \n")
        a = input("Ingrese la pregunta a visualizar: ").lower() #Pueda leer las mayúsculas
        if(a=="a"):
            Pregunta1()
        elif(a=="b"):
            Pregunta2()
        elif(a=="c"):
            Pregunta3()
        else:
            print("Seleccione una pregunta válida")
    else:
        print("--! ACCESO DENEGADO !--")


#Principal
if __name__ == '__main__':
    num_expediente = 23 #Aqui colocamos nuestro número de expediente  !OBSERVACIÓN: Colocaré un valor pequeño para que no ralentizar el ordenador. El valor se puede cambiar a preferencia de uno. 
    A = [[random.randint(0,215) for i in range(6)] for j in range(num_expediente)] # Genero A[21535220][6]con num. aleatorios del 0 al 215, ver excel 
    B = [[random.randint(0,215) for i in range(num_expediente)] for j in range(6)] # Genero B[6][21535220]con num. aleatorios del 0 al 215, ver excel
    n_fil_A = len(A) # Obtengo num de filas de A 
    n_col_A = len(A[0]) # Obtengo num de colunmas de A 
    n_fil_B = len(B) # Obtengo num de filas de B
    n_col_B = len(B[0]) # # Obtengo num de filas de B
    Menu_datos() #Importamos el menu
    
