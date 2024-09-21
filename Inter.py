import numpy as np
from scipy.interpolate import interp1d

# Datos originales
numero_viento_0 = [0, 1, 2, 3, 4]
valor_0 = [0, 3, 5, 8, 16]

numero_viento_45 = [0, 1, 2, 3, 4]
valor_45 = [0, 6, 11, 18, 26]

# Grados entre los que interpolaremos
grados = [0, 45]
grados_objetivo = [22, 23, 24, 25]

# Interpolación entre los grados 0° y 45° para obtener el valor correspondiente al grado 22°, 23°, 24°, 25°
interpolador = interp1d(grados, np.vstack([valor_0, valor_45]), axis=0)

# Calcular los valores interpolados para los grados objetivo
valores_interpolados = interpolador(grados_objetivo)

print(valores_interpolados)

range(0:51)
