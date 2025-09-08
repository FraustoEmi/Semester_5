import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ruta = 'economia\Analisis de rendimiento.csv'
data_frame = pd.read_csv(ruta, sep=',')

#RENDIMIENTO SIMPLE
precios = [100,105,110,108,112]

serie_precio = pd.Series(precios)

rendimientos_simple = ((serie_precio / serie_precio.shift(1)) -1).dropna()

print(f'Rendimientos simples: \n{rendimientos_simple}')

#RENDIMIENTO LOGARITMICO
rendimiento_logaritmico = (np.log(serie_precio/ serie_precio.shift(1))).dropna()


print(f'Rendimientos logaritmico: \n{rendimiento_logaritmico}')

#GRAFICAR LOS RENDIMIENTOS
plt.figure(figsize=(8,5))
plt.bar(range(1,len(rendimientos_simple) + 1),rendimientos_simple, color='skyblue')

plt.title('Rendimiento simple diario')
plt.xlabel('Dia')
plt.ylabel('Rendimiento')
plt.axhline(0, color='gray', linestyle='--')
plt.grid()
plt.show()