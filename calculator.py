import numpy as np
from scipy.interpolate import interp1d
import pandas as pd

# Datos originales
numero_viento =     [0,  2, 5, 6, 10, 11, 15, 16, 20, 21, 25, 26, 30, 31, 35, 36, 40, 41, 45, 46, 50]

# Datos interpolados
numeros_faltantes = [1, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19, 22, 23, 24, 27, 28, 29, 32, 33, 34, 37, 38, 39, 42, 43, 44, 47, 48, 49]


def nuevos_valores(df, lista):

   # Crear la interpolación basada en los datos originales
    result_interpolacion = interp1d(df['Viento'], lista,  kind='linear', fill_value='extrapolate')

    valores_interpolados = result_interpolacion(numeros_faltantes)



  

    df['Valor 1'] = valores_interpolados  # Agregar la columna con los nuevos valores proporcionados

    return df


# Crear DataFrame para datos originales
cuadro_inicial = pd.DataFrame({
    'Viento': numero_viento,
})

# Lista de pesos nuevos
valor_6_45 =    [0, -3, 8, 9, 16, 18, 22, 25, 31, 32, 38, 40, 47, 49, 55, 57, 61, 63, 68, 70, 75]

# Llamando a la funcion
frame = nuevos_valores(cuadro_inicial, valor_6_45)

print(frame.to_string(index=False))