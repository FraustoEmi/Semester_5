#EMILIO FRAUSTO ORTIZ
import yfinance as yf
import pandas as pd
import numpy as np

data = yf.download('BTC-USD', start='2019-01-01', end='2021-09-01')

data['Retorno'] = data['Close'].pct_change()
data['LogRetorno'] = np.log(data['Close'].pct_change())

simple_mean = data['Retorno'].mean()
log_mean = data['LogRetorno'].mean()

simple_desv = np.std(data['Retorno'])
log_desv = np.std(data['LogRetorno'])

print(f'MEDIAS DE: SIMPLE:     {simple_mean:0.2%} LOG: {log_mean:0.2%}')
print(f'MEDIAS DE DESVIACION:  {simple_desv:0.2%} LOG: {log_desv:0.2%}')
