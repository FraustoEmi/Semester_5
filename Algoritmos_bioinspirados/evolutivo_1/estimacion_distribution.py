import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('data.csv')
#print(data)
x=data['x']
y=data['y']
plt.plot(x,y,'ro')
plt.grid()
#plt.show()

def p(a,x):
    return a[0] + a[1]*x + a[2]*x**2 + a[3]*x**3 + a[4]*x**4 + a[5]*x**5

def evaluador(a,x,y):
    individuo = p(a,x)
    error = np.mean((individuo-y)**2)
    fitness = 1 /(1+error)
    return fitness ,  error , individuo
    

def poblacion(n,a,lmin,lmax):
    return np.random.uniform(lmin,lmax,size=(n,a))

n = 21
a = 6

conjunto = poblacion(n,a,-10,10)
print(conjunto)

fitness = []

for i in range(21):
    fit , error , individuo = evaluador(conjunto[i],x[i],y[i])
    print('Evaluando',i,'fitness',fit,'error',error)
    fitness.append(fit)
    