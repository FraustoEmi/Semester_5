import numpy as np
import threading
import time

def poblar(n,long): 
    '''n =      numero de individuos o tamaño de la poblacion''' 
    '''long =   la longitud de los cromosomas'''
    return np.random.randint(0,2,size=(n,long))

def ayudantes(id_ayudante,reporte,lock,poblacion,inrange,endrange,n,pc,pm):
    r,c = poblacion.shape
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
        
    #***********************MUTAR*************************
    print(f'El ayudante {id_ayudante} acabo de cruzar su mitad {M.shape}')
    print(f'El ayudante {id_ayudante} empezara a mutar su mitad')
    r , c = M.shape
    n = int(pm*c)
    for i in range(n):
        r1 = np.random.randint(0,r) #numero aleatorio para seleccionar al individuo
        r2 = np.random.randint(0,c) #numero aleatorio para seleccionar el gen a mutar
        if (M[r1,r2] == 0):
            M[r1,r2] = 1
        else:
            M[r1,r2] = 0
            
        
    
    with lock:
        print(f'El ayudante {id_ayudante} acabo sus tareas de cruza y mutacion')
        reporte[id_ayudante] = M
    
            
    
    
    

def god(reporte,lock,total_ayudantes,progreso_anterior):
    '''
    god es el hilo principal que estara suervisando el progreso de los hilos
    '''
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

    
#*****************************************************************
#hiperparametros
n=100
l=8
pc = n/2
pm = 0.05
total_ayudantes = 2
inrange = [0,(n/2)+1]
endrange = [n/2 , n]


#variables necesarias
mejor_decimal_per_gen = []
lock = threading.Lock()
reporte={}
progreso_anterior = -1
p=poblar(n,l)

hilo_creador = threading.Thread(
    target=god,
    args=(reporte,lock,total_ayudantes,progreso_anterior),
    name='Dios'
)
nombres= ['Adan','Eva']
hilo_ayudantes = []
for i in range(total_ayudantes):
    hilo = threading.Thread(
        target=ayudantes,
        args=(nombres[i],reporte,lock,p,inrange[i],endrange[i],n,pc,pm),
        name=f'Ayudante - {nombres[i]}'
    )
    hilo_ayudantes.append(hilo)



#*****************************************************************

print('='*60)
print('SIMULACION DE ALGORITMO EVOLUTIVO EN PARALELO')
print('='*60)

print('\n Comienza la evolucion...')
time.sleep(1)

hilo_creador.start()

for i, hilo in enumerate(hilo_ayudantes):
    hilo.start()

for hilo in hilo_ayudantes:
    hilo.join()
    
next_gen = np.vstack((reporte['Adan'],reporte['Eva']))  

hilo_creador.join()

print(next_gen.shape)



