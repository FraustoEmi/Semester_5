import numpy as np


def leer_tsp_explicito(ruta):
    matriz = []
    leyendo_coord = False
    cont = 0
    
    with open(ruta,'r') as tsp_txt:
        matriz = np.zeros((52,3))
        for num , linea in enumerate(tsp_txt):
            linea = linea.strip()
            if linea.startswith('NAME:') or linea.startswith('TYPE:') or linea.startswith('COMMENT:'):
                continue
            elif linea.startswith('DIMENSION:') or linea.startswith('EDGE_WEIGHT_TYPE:'):
                continue
            elif linea.startswith('NODE_COORD_SECTION'):
                leyendo_coord = True
                continue
            elif linea.startswith('EOF'):
                break
            if leyendo_coord == True:
                palabra = linea.split()
                nombre = str(palabra[0])
                x      = (palabra[1])
                y      = (palabra[2])
                matriz[cont,0] = nombre
                matriz[cont,1] = x
                matriz[cont,2] = y
                cont+=1
    return matriz

def matriz_distancias(matriz):
    matriz_dist = np.zeros((52,52))
    
    for actual in range(52):
        for todas in range(52):
            ciudad_actual = [matriz[actual,1],matriz[actual,2]]
            ciudad_sig = [matriz[todas,1],matriz[todas,2]]
            
            distancia = np.sqrt( (ciudad_sig[0] - ciudad_actual[1])**2 + (ciudad_sig[0] - ciudad_actual[1])**2)
            
            matriz_dist[actual,todas] = distancia
    
    return matriz_dist
            
ruta = 'paralelo_1\practicas_clase\TSP\Berlin52.tsp'
ciudades = leer_tsp_explicito(ruta)

m_dist = matriz_distancias(ciudades)
print(m_dist.shape)


