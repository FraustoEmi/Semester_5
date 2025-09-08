import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#EMILIO FRAUSTO ORTIZ
#***************************************************************************
#Ejercicio 1
print('*'*60)
print('Ejercicio 1')
capital_ini = 10000
interes_anual = 0.08
num_anos = 5

monto_final = capital_ini*(1+interes_anual)**num_anos
print(f'El monto final es de: {monto_final}\n')
#***************************************************************************
#Ejercicio 2
print('*'*60)
print('Ejercicio 2')
precios = [100,102,101,104,107,106,110]
precios = pd.Series(precios)

rendimientos = []
for i in precios:
    rendimientos.append(precios.pct_change())
#rendimiento = (precios.shift(1) - precios / precios).pct_change()

print(f'Rendimientos: \n{rendimientos[0]}')
#***************************************************************************
