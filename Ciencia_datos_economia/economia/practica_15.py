#EMILIO FRAUSTO ORTIZ
import yfinance as yf
import pandas as pd
import math

data = yf.download('BTC-USD', start='2019-01-01', end='2021-09-01')

data['Retorno'] = data['Close'].pct_change()
rendimiento_promedio = data['Retorno'].mean()

Volatibilidad_diaria = data['Retorno'].std()

Volatibilidad_anual = data['Retorno'].std() * (math.sqrt(252))

print(f'Rendimiento diario:            {rendimiento_promedio:0.2%}')
print(f'Volatibilidad diaria:          {Volatibilidad_diaria:0.2%}')
print(f'Volatibilidad anual:           {Volatibilidad_anual:0.2%}')


