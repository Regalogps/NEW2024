import numpy as np
from scipy.interpolate import interp1d
import pandas as pd

# Definir la función escalable
def generar_dataframe(viento_existentes_1, valor_exis_1, viento_faltantes, df_total=None, nombre_columna="Valor"):
    # Interpolar los valores faltantes
    result = interp1d(viento_existentes_1, valor_exis_1 , kind='linear', fill_value='extrapolate')
    valores_interpolados = result(viento_faltantes)

    # Crear DataFrame para datos existentes
    df_existente = pd.DataFrame({
        'Viento': viento_existentes_1,
        nombre_columna: valor_exis_1 
    })

    # Crear DataFrame para datos interpolados
    df_interpolados = pd.DataFrame({
        'Viento': viento_faltantes,
        nombre_columna: valores_interpolados
    })

    # Unir los dos DataFrames y ordenar por la columna 'Viento'
    df_nuevo = pd.concat([df_existente, df_interpolados]).sort_values(by='Viento').reset_index(drop=True)

    # Si ya existe un DataFrame, unimos las nuevas columnas
    if df_total is not None:
        df_total = pd.merge(df_total, df_nuevo, on='Viento', how='outer').sort_values(by='Viento').reset_index(drop=True)
    else:
        df_total = df_nuevo

    # Crear nueva columna con valores redondeados (sin decimales)
    df_total[f' {nombre_columna}'] = df_total[nombre_columna].round().astype(int)

    # Crear nueva columna con valores con máximo 2 decimales
    df_total[f'  {nombre_columna}'] = np.around(df_total[nombre_columna], decimals=1)
    # Renombrar la columna
    df_total = df_total.rename(columns={f'  {nombre_columna}': 'dec.'})

    return df_total

# Variables de ejemplo (estas ya las tienes definidas)
viento_existentes_1 = [0,  2, 5, 6, 10, 11, 15, 16, 20, 21, 25, 26, 30, 31, 35, 36, 40, 41, 45, 46, 50]

# Definir el rango completo
rango_completo = list(range(0, 51))  # Esto incluye todos los números del 0 al 50
# Encontrar los números faltantes
viento_faltantes = [num for num in rango_completo if num not in viento_existentes_1]

# Conjuntos de valores para pasar a la función
list_valour = [
    [0, -3, 8, 9, 16, 18, 22, 25, 31, 32, 38, 40, 47, 49, 55, 57, 61, 63, 68, 70, 75], 
    [0, 4, 10, 12, 19, 22, 27, 29, 36, 38, 45, 47, 57, 59, 66, 68, 76, 77, 85, 87, 95],
    # ... añade más conjuntos de valores aquí
]

lista_names = ["(6:45)", "(7:30)", "(8:15)", "(9:00)", "(9:45)", "(10:30)", "(11:15)", "(11:37)", "(12:00)"]

# Inicializar el DataFrame total
df_total = None

# Bucle para iterar sobre las listas de valores y nombres
for valor_exis, nombre_columna in zip(list_valour, lista_names):
    df_total = generar_dataframe(viento_existentes_1, valor_exis, viento_faltantes, df_total, nombre_columna=nombre_columna)

    # Eliminar la columna original si es necesario (opcional)
    df_total = df_total.drop(columns=[nombre_columna])

# Mostrar el DataFrame final
print(df_total.to_string(index=False))
