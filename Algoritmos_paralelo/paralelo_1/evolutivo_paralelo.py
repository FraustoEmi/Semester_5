import numpy as np
import threading
import time

def poblar(n,long): 
    '''n =      numero de individuos o tamaño de la poblacion''' 
    '''long =   la longitud de los cromosomas'''
    return np.random.randint(0,2,size=(n,long))




def ayudantes(id_ayudante,reporte,lock,poblacion,inrange,endrange,n,pc):
    r,c = poblacion.shape
    with lock:
        print(f'{id_ayudante} comenzo su tarea y si mitad de [{inrange},{endrange}]')
    M = np.zeros((int(n/2),c)) #Matriz de 50 pares por cada ayudante
    for par in range(int(pc/2)):
        r1 = np.random.randint(inrange,endrange,size=(1,2)) #par de padres en esa mitad
        r2 = np.random.randint(0,c)

        #seleccionar padres a cruzar
        Padre_1 = poblacion[r1[0,0],:]
        Padre_2 = poblacion[r1[0,1],:]
                
        #Crear descendientes 
        hijo_1 = np.concatenate((Padre_1[0:r2],Padre_2[r2:]))
        hijo_2 = np.concatenate((Padre_2[0:r2],Padre_1[r2:]))
                
        #Se almacenan los decendientes en la matriz auxiliar M
        M[2*par,:] = hijo_1
        M[2*par+1,:] = hijo_2
        
        
    
    with lock:
        print(f'El ayudante {id_ayudante} acabo de cruzar su mitad')
        reporte[id_ayudante] = M
        print(M.shape)
    
            
    
    
    

def god(reporte,lock,total_ayudantes):
    '''
    god es el hilo principal que estara suervisando el progreso de los hilos
    '''
    progreso_anterior = -1
    while True:
        with lock:
            progreso_actual = len(reporte)
        
        if progreso_actual != progreso_anterior:
            if progreso_actual < total_ayudantes:
                print(f'God says: {reporte}')
                print(progreso_actual,progreso_anterior)
            progreso_anterior = progreso_actual
        
        if progreso_actual >= total_ayudantes:
            break
        
        time.sleep(0.3)
                
def añadir(id_ayudante,reporte,sig_gen):
    for i in nombres:
        sig_gen += reporte[i]

#*****************************************************************
#hiperparametros
n=100
l=8
pc = n/2
total_ayudantes = 2
inrange = [0,(n/2)+1]
endrange = [n/2 , n]

#variables necesarias
mejor_decimal_per_gen = []
lock = threading.Lock()
reporte={}


hilo_creador = threading.Thread(
    target=god,
    args=(reporte,lock,total_ayudantes),
    name='Dios'
)




#*****************************************************************

print('='*60)
print('SIMULACION DE ALGORITMO EVOLUTIVO EN PARALELO')
print('='*60)

p=poblar(n,l)

print('\n Comienza la evolucion...')
time.sleep(1)

nombres= ['Adan','Eva']
hilo_ayudantes = []
for i in range(total_ayudantes):
    hilo = threading.Thread(
        target=ayudantes,
        args=(nombres[i],reporte,lock,p,inrange[i],endrange[i],n,pc),
        name=f'Ayudante - {nombres[i]}'
    )
    hilo_ayudantes.append(hilo)



hilo_creador.start()

for i, hilo in enumerate(hilo_ayudantes):
    hilo.start()
    
print('\nEsperando...')

for hilo in hilo_ayudantes:
    hilo.join()
    
p_cruzada = np.zeros(p.shape)
p_cruzada = añadir(nombres,reporte,p_cruzada)    

hilo_creador.join()

print((reporte['Adan']).shape)
print(p_cruzada.shape)




