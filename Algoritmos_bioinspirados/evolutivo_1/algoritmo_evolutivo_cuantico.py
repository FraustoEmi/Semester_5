#ALGORITMO CUANTICO
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,10,100)
y = abs((x-5)/(2+np.sin(x)))

plt.plot(x,y,'r')
plt.grid()
#plt.show()

#funcion que inicializa las amplitudes de probabilidad
#al principio todas las amplitudes seran iguales 1/sqrt(2)

#ponemos todos los numeros en la misma probabilidad
def amplitudes(tam_pob,num_qbits):
    pob_amp = np.full((tam_pob,num_qbits),1/np.sqrt(2))
    return pob_amp

#FUNCION QUE PASA LAS AMPLITUDES A 0 Y 1 MEDIANTE NUM ALEATORIOS
def generar_soluciones(amplitudes):
    r,c = amplitudes.shape
    matriz_binaria = np.zeros((r,c),dtype= int)
    matriz_aleatoria = np.random.rand(r,c)
    for renglones in range(r):
        for columnas in range(c):
            if matriz_aleatoria[renglones,columnas] < amplitudes [renglones,columnas]:
                matriz_binaria[renglones,columnas] = 1
            else:
                matriz_binaria[renglones,columnas] = 0
    return matriz_binaria

a = amplitudes(10,5)
print(a)

bin = generar_soluciones(a)
print(bin)

def rotacion_gate(p,soluciones,mejor_solucion,theta=np.pi/50):
    '''
    p = matriz de porcentajes
    '''
    r,c = p.shape
    for renglones in range(r):
        for columnas in range(c):
            if soluciones[renglones,columnas] != mejor_solucion[columnas]:
                if mejor_solucion[columnas] == 1:
                    p[renglones,columnas] = p[renglones,columnas] + np.sin(theta)*(1-p[renglones,columnas])
                else:
                    p[renglones,columnas] = p[renglones,columnas] - np.sin(theta)*(1-p[renglones,columnas])
    next_p = np.clip(p,0.05,0.95)
    
    return next_p

def mutation_gate(p,pm):
    r,c = p.shape
    Ma_aux = np.random.rand(r,c)
    mascara = np.zeros((r,c), dtype=bool)
    for lines in range(r):
        for cols in range(c):
            if Ma_aux[lines,cols] < pm:
                mascara[lines,cols] = True
            else:
                mascara[lines,cols] = False
    next_p = np.where(mascara,1-p,p)
    return next_p

p = np.array([[0.5,0.7,0.2,0.9],
               [0.3, 0.4, 0.6, 0.8],
               [0.9, 0.1, 0.5,0.5]])
a_mut = mutation_gate(p,0.05)
print(a_mut)


#ALGORITMO GENETICO CUANTICO 
#*******************************PARAMETROS*********************************
tam_pob = 6
num_qbits = 10
generaciones = 10
pm = 0.05
Imin = -10
Imax = 10

#*******************************FUNCIONES***********************************


#*******************************EJECUCION***********************************

P = 'INICIAR LA MATRIZ DE PROBABILIDADES'
mejor_solucion = None
mejor_fitness = float('inf')

for k in range(generaciones):
    soluciones = 0
    aptitud = 0
    actual_mejor_fitness = 0
    actual_mejor_solucion = 0
    
    if actual_mejor_fitness < mejor_fitness:
        mejor_fitness = actual_mejor_fitness
        mejor_solucion = actual_mejor_solucion
        
    p = rotacion_gate()
    p = mutation_gate()