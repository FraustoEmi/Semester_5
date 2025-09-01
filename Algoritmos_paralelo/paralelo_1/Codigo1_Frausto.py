import threading
import time
import random
import multiprocessing
import os
import concurrent.futures
import Codigo01a as CA
import Codigo01b as CB
import Codigo01c as CC
import numpy as np
import matplotlib.pyplot as plt


def main():
    salonA = CA.main_threading()
    salonB = CB.main_multiprocessing()
    salonC = CC.main_concurrent_futures()
    return salonA, salonB, salonC
    
if __name__ == '__main__':
    salonA, salonB, salonC = main()
    A = []
    B = []
    C = []
    
    for i in salonA:
        A.append(i['tiempo'])
    for i in salonB:
        B.append(i['tiempo'])
    for i in salonC:
        C.append(i['tiempo'])
        
    tiempo_a = np.array(A)
    tiempo_b = np.array(B)
    tiempo_c = np.array(C)
    x = np.linspace(1,40,40)
    
    plt.title('Comparacion de tiempos')
    plt.plot(x,tiempo_a,color='red',label='Threading')
    plt.plot(x,tiempo_b,color='blue', label='Multiprocessing')
    plt.plot(x,tiempo_c,color='green', label='Concurrent')
    plt.grid(True)
    plt.xlabel('Alumno')
    plt.ylabel('Tiempo')
    plt.legend()
    
    plt.show()
    