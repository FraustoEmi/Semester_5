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

def seleccion_torneo(poblacion,k,Imin,Imax):
    '''
    k: indica el tamaño del torneo
    '''
    r,c = poblacion.shape
    aptitud = evaluar(poblacion,Imin,Imax).reshape(r,1)
    M = np.concatenate([poblacion,aptitud],axis=1)
    
    #seleccionamos k individuos al azar para el torneo 
    indices_torneo = np.random.choice(r,size=k,replace=False)
    torneo = M[indices_torneo,:]
    
    #Ordenamos por aptitud descendiente 
    indices = np.argsort(torneo[:,-1])[::-1]
    torneo_ordenado = torneo[indices]
    
    #Mantenemos al mejor individuo
    mejor_individuo = torneo_ordenado[0,0:c]
    
    return mejor_individuo

#Funcion que crea una nueva poblacion por torneo
def next_generation(poblacion,k,Imin,Imax):
    r,c = poblacion.shape
    n_gen = np.zeros((r,c))
    
    #Se repite el torneo para llenar la matriz de poblacion nueva
    for i in range(r):
        n_gen[i,:] = seleccion_torneo(poblacion,k,Imin,Imax)
    
    return n_gen

#Seleccion por ruleta
def seleccion_por_ruleta(poblacion, Imin, Imax):
    [r,c]=poblacion.shape
    aptitud=evaluar(poblacion, Imin, Imax)
    min_fitness = np.min(aptitud)
    if (min_fitness<0):
        aptitud = aptitud - min_fitness + 1e-6
    #Evitemos dividir por 0
    if np.sum(aptitud) == 0:
        probs= np.ones(r)/r
    else:
        probs= aptitud/np.sum(aptitud)
    #Generamos un numero aleatorio para simular la rotacion de la ruleta
    acumuladas=np.cumsum(probs)

    #Generamos un numero alkeatorio para simular la rotacion de la ruleta
    num=np.random.rand()
    ganador=None
    #Se busca el individuo donde cae num
    for i in range(r):
        if num<acumuladas[i]:
            ganador=poblacion[i,:]
            break
    return ganador

#Ciclo for que crea una nueva poblacion mediante el torneo
def nueva_poblacion_ruleta(poblacion, Imin, Imax):
    [r,c]=poblacion.shape
    nueva_poblacion=np.zeros((r,c))

    # Repite el torneo para llevar la matriz de poblacion nueva
    for i in range(r):
        nueva_poblacion[i,:]=seleccion_por_ruleta(poblacion, Imin, Imax)
    return nueva_poblacion

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
x = np.linspace(0,2,generaciones)
y=f(x)
y_mejores = []
for i in mejor_decimal_per_gen:
    y_mejores.append(f(i))
plt.plot(x,y)
plt.scatter(x,y_mejores,color='red')
plt.grid(True)
plt.show()

#**********************************************************Representacion real****************************************************************
print('ALGORITMO GENETICO (Representacion real)\n')

#Parametros
n=100
l=1
generaciones = 50
ps = 0.6 
pc = 0.5
pm = 0.05
Imin = -2
Imin = 2

def poblar_real(n,l,Imin,Imax):
    poblacion = np.random.uniform(Imin,Imax,size=(n,l))
    return poblacion

def evaluar_real(poblacion):
    fitness = -(0.1+((1-poblacion)**2)-0.1*np.cos(6*np.pi*(1-poblacion))) + 2
    return fitness

def cruzar_real(poblacion,pc,Imin,Imax):
    r,c = poblacion.shape
    n=int(r*pc)
    M = np.zeros((r,1))
    
    for i in range(n):
        r1 = np.random.randint(0,r,size=(1,2))
        padre1 = poblacion[r1[0,0],0]
        padre2 = poblacion[r1[0,1],0]
        alpha = np.random.rand()
        Hijo1 = alpha*padre1 + (1-alpha)*padre2
        Hijo2 = alpha*padre2 + (1-alpha)*padre1
        
        #mantenemos los individuos dentro del espacio de busqueda
        Hijo1 = np.clip(Hijo1,Imin,Imax)
        Hijo2 = np.clip(Hijo2,Imin,Imax)
        
        #Se guardan los hijos
        M[2*i,0]=Hijo1
        M[2*i,0]=Hijo2
        
    for i in range(r):
        if M[i,0] == 0:
            M[i,0] = np.random.uniform(Imin,Imax)
            
    return M

def mutar_real(poblacion,Imin,Imax,beta=0.05):
    r,c = poblacion.shape
    sigma = beta*(Imax-Imin)
    n = int(np.ceil(pm*r))
    
    for i in range(n):
        r1 = np.random.randint(0,r)
        N = np.random.normal(0,sigma)
        poblacion[r1,0] = poblacion[r1,0] + N
        poblacion[r1,0] = np.clip(poblacion[r1,0],Imin,Imax)
        
    return poblacion

def hacer_ranking_real(poblacion,ps,Imin,Imax):
    '''
    ps = porcentaje de poblacion para seleccionar
    '''
    r,c = poblacion.shape
    next_gen = np.zeros([r,c])
    n = int(ps*r)
    aptitud = evaluar_real(poblacion).reshape(r,1)
    poblacion_ampliada = np.concatenate([poblacion,aptitud],axis=1)
    indices = np.argsort(poblacion_ampliada[:,-1])[::-1]
    poblacion_ordenada = poblacion_ampliada[indices]
    poblacion_ordenada_seleccionada = poblacion_ordenada[0:n]
    poblacion_seleccionada = poblacion_ordenada_seleccionada[:,0:c]
    for i in range(r):
        if (i<n):
            next_gen[i] = poblacion_seleccionada[i]
        else:
            next_gen[i] = np.random.uniform(Imin,Imax)
    
    return next_gen

p = poblar_real(n,l,Imin,Imax)

for k in range(generaciones):
    C = cruzar_real(p,pc,Imin,Imax)
    M = mutar_real(p,pm,Imin,Imax)
    nueva_gene = hacer_ranking_real(M,ps,Imin,Imax)

x_mejor = nueva_gene[0]
print(f'El mejor individuo es: {nueva_gene[0]}')
print(f'Con un valor decimal de {x_mejor}\n')
