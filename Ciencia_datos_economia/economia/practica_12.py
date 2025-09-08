import pandas as pd
import numpy as np

#EMILIO FRAUSTO ORTIZ
precios = pd.Series([100,105,102,107,110])

rendimientos = ((np.log(precios)).pct_change()).dropna()

print(f'LogRetorno: \n{rendimientos}')