import yfinance as yf
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#Estraer datos de yahoo finance con yfinance
data = yf.download('BTC-USD', start='2024-01-01', end='2025-09-01')

#Calcula el retorno porcentual o simple diario a partir del precio de cierre
data['Retorno'] = data['Close'].pct_change()

data['LogRetorno'] = np.log(data['Close'] / data['Close'].shift(1))

plt.plot(data['Retorno'], label='retornos simples')
plt.plot(data['LogRetorno'], label='retornos logaritmicos')
plt.title('Comparacion de rendimientos')
plt.xlabel('Fecha')
plt.ylabel('USD')
plt.grid()
plt.show()

sns.histplot(data['LogRetorno'].dropna(),bins=50,kde=True,color='green')
sns.histplot(data['Retorno'].dropna(),bins=50,kde=True,color='blue')
plt.title('Distribucion de rendimientos')
plt.xlabel('Rendimiento Diario')
plt.grid()
plt.show()
