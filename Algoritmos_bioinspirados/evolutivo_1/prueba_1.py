import numpy as np 
import matplotlib.pyplot as plt 

#La funcion
def f(x):
    return -(0.1+((1-x)**2)-0.1*np.cos(6*np.pi*(1-x))) + 2

#Graficar la funcion
x = np.linspace(0,2,100)
y=f(x)
plt.plot(x,y)
plt.grid(True)
#plt.show()

#Creacion de individuos o poblacion
def poblar(n,long): 
    '''n =      numero de individuos o tamaño de la poblacion''' 
    '''long =   la longitud de los cromosomas'''
    return np.random.randint(0,2,size=(n,long))

p = poblar(10,8)
print(p)

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

p_decodificado_entero , p_decodificado_decimal = decodificar(p,0,2)
print(p_decodificado_entero)
print(p_decodificado_decimal)

#Funcion para evualar los individuos y asi obtener las abtitudes (Fitness)
def evaluar(poblacion,Imin,Imax):
    r,c = poblacion.shape
    individuo_entero, individuo_decimal = decodificar(poblacion,Imin,Imax)
    fitness = -(0.1+((1-individuo_decimal)**2)-0.1*np.cos(6*np.pi*(1-individuo_decimal))) + 2
    return fitness

print(evaluar(p,0,2))

#Funcion que realiza la cruza de individuos
def cruza(poblacion,pc):
    '''pc =     pares de cromosomas a cruzar'''
    r,c = poblacion.shape
    M = np.zeros((2*pc,c))    #Matriz auxiliar para guardar decendientes
    for par in range(pc):
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
    
cruzas = cruza(p,5)
print(cruzas)