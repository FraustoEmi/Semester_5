import pandas as pd

#EMILIO FRAUSTO ORTIZ
precios = pd.Series([100,105,102,107,110])

rendimiento = (precios.pct_change()).dropna()
    
print(f'Rendimientos: \n{rendimiento}')