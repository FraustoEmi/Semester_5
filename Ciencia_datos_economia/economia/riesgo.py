import numpy as np

precios = np.array([100,101.5,99.8,100.6,
                    102.0,101.2,103.0],dtype=float)

return_simple = precios[1:] / precios[:-1] - 1

returns_log = np.log(precios[1:] / precios[:-1])

vol_d_simple = np.std(return_simple, ddof=1)
vol_d_log    = np.std(returns_log,  ddof=1)

print(f'Volatibilidad Diaria simple {vol_d_simple*100:0.2f}%')
print(f'Volatibilidad Diaria Logaritmica {vol_d_log*100:0.2f}%')

