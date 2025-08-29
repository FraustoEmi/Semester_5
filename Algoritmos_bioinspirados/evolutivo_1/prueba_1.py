import numpy as np 
import matplotlib.pyplot as plt 

#La funcion
def f(x):
    return -(0.1+((1-x)**2)-0.1*np.cos(6*np.pi*(1-x))) + 2

#Creacion de individuos o poblacion
def poblar(n,long): 
    '''n =      numero de individuos o tamaño de la poblacion''' 
    '''long =   la longitud de los cromosomas'''
    return np.random.randint(0,2,size=(n,long))

'''p = poblar(10,8)
print(p)'''

#Funcion para decodificar los individuos de binario a decimal
def decodificar(poblacion,Imin,Imax):
    '''Poblacion = es la cantidad de individuos'''
    '''Imin      = intervalo minimo'''
    '''Imax      = intervalo maximo'''
    r,c = poblacion.shape
    decimal = np.zeros(r)               # arreglo vacio para llenarlo con los valores enteros
    decimal_reescalado = np.zeros(r)    # arreglo vacio para llenarlo con los valores decimales
    
    for row in range(r):
        for column in range(c):
            #Se transforma de binario a decimal entero
            decimal[row] = decimal[row] + poblacion[row,column]*2**(c-column-1)
            #se reescala el valor decimal entero en el espacio de busqueda
            decimal_reescalado[row] = (Imax-Imin)*decimal[row]/(2**c-1)+Imin
    
    return decimal,decimal_reescalado

'''p_decodificado_entero , p_decodificado_decimal = decodificar(p,0,2)
print(p_decodificado_entero)
print(p_decodificado_decimal)'''

#Funcion para evualar los individuos y asi obtener las abtitudes (Fitness)
def evaluar(poblacion,Imin,Imax):
    r,c = poblacion.shape
    individuo_entero, individuo_decimal = decodificar(poblacion,Imin,Imax)
    fitness = -(0.1+((1-individuo_decimal)**2)-0.1*np.cos(6*np.pi*(1-individuo_decimal))) + 2
    return fitness

'''print(evaluar(p,0,2))'''

#Funcion que realiza la cruza de individuos
def cruza(poblacion,pc):
    '''pc =     pares de cromosomas a cruzar'''
    r,c = poblacion.shape
    M = np.zeros((int(2*pc),c))    #Matriz auxiliar para guardar decendientes
    for par in range(int(pc)):
        r1 = np.random.randint(0,r,size=(1,2))  #par de padres 
        r2 = np.random.randint(0,c)
        
        #seleccionar los padres a cruzar 
        Padre_1 = poblacion[r1[0,0],:]      #del par r1 agarra el primer numero
        Padre_2 = poblacion[r1[0,1],:]      #del par r1 agarra el segundo numero
        
        #Crear decendientes
        hijo_1 = np.concatenate((Padre_1[0:r2],Padre_2[r2:]))
        hijo_2 = np.concatenate((Padre_2[0:r2],Padre_1[r2:]))
        
        #Se almacenan los decendientes en la matriz auxiliar M
        M[2*par,:]      = hijo_1
        M[2*par+1,:]    = hijo_2
        
    return M
    
'''cruzas = cruza(p,5)
print(cruzas)'''

def mutacion(poblacion, pm):
    '''
    pm = porcentaje de la poblacion a mutar
    '''
    r , c = poblacion.shape
    n = int(pm*c)
    for i in range(n):
        r1 = np.random.randint(0,r) #numero aleatorio para seleccionar al individuo
        r2 = np.random.randint(0,c) #numero aleatorio para seleccionar el gen a mutar
        if (poblacion[r1,r2] == 0):
            poblacion[r1,r2] = 1
        else:
            poblacion[r1,r2] = 0
    return poblacion

#FUNCION QUE REALIZA EL PROCESO DE SELECCION POR RANKING
def hacer_ranking(poblacion,ps,Imin,Imax):
    '''
    ps = porcentaje de poblacion para seleccionar
    '''
    r,c = poblacion.shape
    next_gen = np.zeros([r,c])
    n = int(ps*r)
    aptitud = evaluar(poblacion,Imin,Imax).reshape(r,1)
    poblacion_ampliada = np.concatenate([poblacion,aptitud],axis=1)
    indices = np.argsort(poblacion_ampliada[:,-1])[::-1]
    poblacion_ordenada = poblacion_ampliada[indices]
    poblacion_ordenada_seleccionada = poblacion_ordenada[0:n]
    poblacion_seleccionada = poblacion_ordenada_seleccionada[:,0:c]
    for i in range(r):
        for j in range(c):
            if (i<n):
                next_gen[i,j] = poblacion_seleccionada[i,j]
            else:
                next_gen[i,j] = np.random.randint(0,2)
    
    return next_gen

#************************************************Implementar el algoritmo genetico completo**************************************************** 
print('\nALGORITMO GENETICO (REPRESENTACION BINARIA)')

#***********************Parametros de arranque********************************
n=100
l=8
generaciones = 100
ps = 0.6    #porcentaje de seleccion
pc = n/2    #porcentaje de cruza
pm = 0.05   #porcentaje de mutacion
Imin = 0
Imax = 2

#********************************ALGORITMO GENETICO****************************
P = poblar(n,l) #Se crea poblacion aleatoria
mejor_decimal_per_gen = []
for i in range(generaciones):
    mejor_aptitud , evaluada_decimal = decodificar(P,Imin,Imax)
    mejor_decimal_per_gen.append(evaluada_decimal[0])
    C = cruza(P,pc) #Cruzar la poblacion y guardarla en una matriz
    M = mutacion(C,pm) #Mutar y guardarla en una matriz
    next_gen = hacer_ranking(M,ps,Imin,Imax)
    P = next_gen
    

#**********************************RESULTADOS***********************************
P_mejor_decimal,decimal = decodificar(P,Imin,Imax)
x_mejor = decimal[0]
print(f'El mejor individuo es: {P_mejor_decimal[0]} con los genes de {P[0,:]}')
print(f'Con un valor decimal de {x_mejor}\n')

#Graficar la funcion
x = np.linspace(0,2,100)
y=f(x)
y_mejores = []
for i in mejor_decimal_per_gen:
    y_mejores.append(f(i))
plt.plot(x,y)
plt.scatter(x,y_mejores,color='red')
plt.grid(True)
plt.show()