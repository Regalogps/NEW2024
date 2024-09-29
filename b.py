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

    # Crear nueva columna con valores redondeados (enteros)
    df_total[nombre_columna] = df_total[nombre_columna].round(1)   # .astype(int) esto le quita el 0 adicional  -   # .round(1) le deja un decimal mas exacto

    return df_total


# Ejemplo de uso
viento_existentes_1 = [0,  2, 5, 6, 10, 11, 15, 16, 20, 21, 25, 26, 30, 31, 35, 36, 40, 41, 45, 46, 50]
excep_1 = [0, 2, 5, 6, 15, 16, 21, 40, 41, 50]

# Definir el rango completo
rango_completo = list(range(0, 51))  # Esto incluye todos los números del 0 al 50

# Encontrar los números faltantes
viento_faltantes = [num for num in rango_completo if num not in viento_existentes_1]

# Lista de numeros de viento solo para la interpolacion del aire (12:22)
excep_1_ = [num for num in rango_completo if num not in excep_1]
#viento_faltantes = [1, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19, 22, 23, 24, 27, 28, 29, 32, 33, 34, 37, 38, 39, 42, 43, 44, 47, 48, 49]


# VIENTO EN CONTRA:
#valor_existentes_0  = [0, -3, 8, 9, 16, 18, 22, 25, 31, 32, 38, 40, 47, 49, 55, 57, 61, 63, 68, 70, 75]                     # 6:00

valor_exis_1  = [0, -3, 8, 9, 16, 18, 22, 25, 31, 32, 38, 40, 47, 49, 55, 57, 61, 63, 68, 70, 75]                      # 6:45
valor_exis_2  = [0, 4, 10, 12, 19, 22, 27, 29, 36, 38, 45, 47, 57, 59, 66, 68, 76, 77, 85, 87, 95]                     # 7:30
valor_exis_3  = [0, 3, 9, 11, 18, 21, 28, 30, 38, 40, 49, 51, 62, 64, 75, 77, 89, 90, 103, 105, 115]                   # 8:15
valor_exis_4  = [0, 1, 8, 9, 15, 18, 24, 26, 36, 37, 46, 48, 61, 63, 75, 80, 93, 96, 113, 120, 139]                    # 9:00
valor_exis_5  = [0, 3, 5, 5, 10, 12, 16, 18, 25, 26, 33, 35, 47, 60, 63, 66, 82, 87, 110, 118, 152]                    # 9:45
valor_exis_6  = [0, 1, 1, 2, 4, 6, 6, 7, 10, 11, 15, 17, 24, 25, 33, 37, 50, 52, 70, 80, 112]                          # 10:30
valor_exis_7  = [0, 0, -2, -2, -4, -4, -6, -6, -8, -8, -8, -10, -8, -8, -6, -6, -5, 0, 0, 2, 10]                       # 11:15
valor_exis_8  = [0, -1, -4, -4, -7, -8, -11, -12, -15, -16, -19, -20, -23, -23, -26, -27, -29, -30, -32, -33, -36]     # 11:37
valor_exis_9  = [0, -2, -5, -6, -10, -12, -17, -20, -23, -24, -28, -30, -35, -36, -42, -43, -48, -49, -54, -55, -62]   # 12:00

# VIENTO A FAVOR:
valor_exis_1_  = [0, 1, 3, 3, 5, 6, 8, 9, 12, 12, 14, 15, 20, 21, 23, 25, 28, 30, 32, 32, 35]                          # 6:45   -  5:15
valor_exis_2_  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 3, 3, 4, 4, 5, 5, 6, 6, 7]                                       # 7:30   -  4:30
valor_exis_3_  = [0, -1, -4, -4, -6, -7, -9, -10, -12, -13, -14, -14, -15, -15, -16, -16, -18, -18, -20, -20, -22]     # 8:15   -  3:45
valor_exis_4_  = [0, -2, -6, -7, -11, -13, -17, -18, -22, -23, -25, -28, -30, -31, -35, -36, -40, -40, -44, -44, -46]  # 9:00   -  3:00
valor_exis_5_  = [0, -2, -6, -7, -18, -19, -23, -24, -30, -32, -37, -39, -42, -45, -49, -50, -56, -57, -62, -65, -67]  # 9:45   -  2:15
valor_exis_6_  = [0, 2, -7, -8, -17, -20, -25, -27, -34, -35, -42, -44, -49, -51, -57, -59, -66, -67, -75, -78, -82]   # 10:30  -  1:30
valor_exis_7_  = [0, -2, -7, -8, -15, -17, -23, -24, -31, -33, -39, -41, -47, -48, -55, -57, -65, -66, -74, -76, -83]  # 11:15  -  12:45
valor_exis_8_  = [0, -2, -5, -6, -20, -23, -30, -62, -64, -84]                                                         # 11:37  -  12:22


list_valour = [valor_exis_1, valor_exis_2, valor_exis_3, valor_exis_4, 
               valor_exis_5, valor_exis_6, valor_exis_7, valor_exis_8, valor_exis_9,
               valor_exis_1_, valor_exis_2_, valor_exis_3_, valor_exis_4_,
               valor_exis_5_, valor_exis_6_, valor_exis_7_, valor_exis_8_]

lista_names = ["(6:45)", "(7:30)", "(8:15)", "(9:00)", "(9:45)", "(10:30)", "(11:15)", "(11:37)", "(12:00)",
               "(5:15)", "(4:30)", "(3:45)", "(3:00)", "(2:15)", "(1:30)",  "(12:45)", "(12:22)"]


# Llamar la función por primera vez
for i, valor in enumerate(lista_names):
    if i == 0:
        df_total = generar_dataframe(viento_existentes_1, list_valour[i] , viento_faltantes, nombre_columna=lista_names[i])
    else:
        if valor == "(12:22)":
            df_total = generar_dataframe(excep_1, list_valour[i] , excep_1_, df_total, nombre_columna=lista_names[i])
        else:
            df_total = generar_dataframe(viento_existentes_1, list_valour[i] , viento_faltantes, df_total, nombre_columna=lista_names[i])

# Eliminar la columna 'Valor' original
#for i in range(len(list_valour)):
   # df_total = df_total.drop(columns=[lista_names[i]])

# Esto elimina o quita de vision la columna con el calculo exacto con un decimal
#df_total = df_total.drop(columns="dec.")

# Mostrar el DataFrame original y final
print(df_total.to_string(index=False))


#______________________________________________________________________________________otro____________
# Lista para hallar (6:00) intervalo A
valor_a = df_total['(5:15)'].tolist()

# Lista para hallar (6:00) intervalo B
valor_b = df_total['(6:45)'].tolist()

# Grados entre los que interpolaremos
grados = [292.5, 247.5]

# Grados objetivos
grados_objetivo = [270]

# Interpolación entre los grados A y B para obtener el valor correspondiente a los grados x,x,x, etc
interpolador = interp1d(grados, np.vstack([valor_a, valor_b]), axis=0)

# Calcular los valores interpolados para los grados objetivo
valor_6_00 = interpolador(grados_objetivo)


print(valor_6_00)

print(df_total.columns)

#df_total['(6:00)'] = valores_interpolados

#________________________________________________________________________________________________________

# Esto muestra la columna Viento y una columna por nombre ademas de otra por indice
#print(df_total[['Viento', " (6:00)"]] .join(df_total.iloc[:, [-1]]) .to_string(index=False))
