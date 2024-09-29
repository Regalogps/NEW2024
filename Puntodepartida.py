import numpy as np
from scipy.interpolate import interp1d
import pandas as pd

class InterpoladorViento:
    def __init__(self, viento_existentes, valores_existentes, nombres_columnas):
        self.viento_existentes = viento_existentes
        self.valores_existentes = valores_existentes
        self.nombres_columnas = nombres_columnas
        self.df_total = None

    def generar_dataframe(self, viento_existentes_1, valor_exis_1, viento_faltantes, df_total=None, nombre_columna="Valor"):
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

        # Redondear a un decimal
        df_total[nombre_columna] = df_total[nombre_columna].round(1) # .astype(int) esto le quita el 0 adicional  -   # .round(1) le deja un decimal mas exacto

        return df_total


    def crear_dataframe_total(self):
        # Definir el rango completo y los valores faltantes
        rango_completo = list(range(0, 51))
        viento_faltantes = [num for num in rango_completo if num not in self.viento_existentes]

        for i, nombre_columna in enumerate(self.nombres_columnas):
            if i == 0:
                self.df_total = self.generar_dataframe(self.viento_existentes, self.valores_existentes[i], viento_faltantes, nombre_columna=nombre_columna)
            else:
                if nombre_columna == "(12:22)":
                    excep_1 = [0, 2, 5, 6, 15, 16, 21, 40, 41, 50]
                    excep_1_ = [num for num in rango_completo if num not in excep_1]
                    self.df_total = self.generar_dataframe(excep_1, self.valores_existentes[i], excep_1_, self.df_total, nombre_columna=nombre_columna)
                else:
                    self.df_total = self.generar_dataframe(self.viento_existentes, self.valores_existentes[i], viento_faltantes, self.df_total, nombre_columna=nombre_columna)


# Numero de vientos del wind chart original: 0, 5, 6, 10...
viento_existentes_1 = [0,  2, 5, 6, 10, 11, 15, 16, 20, 21, 25, 26, 30, 31, 35, 36, 40, 41, 45, 46, 50]

valores_existentes = [
                        # VIENTO EN CONTRA:
                      [0, -3, 8, 9, 16, 18, 22, 25, 31, 32, 38, 40, 47, 49, 55, 57, 61, 63, 68, 70, 75],                      # 6:45
                      [0, 4, 10, 12, 19, 22, 27, 29, 36, 38, 45, 47, 57, 59, 66, 68, 76, 77, 85, 87, 95],                     # 7:30
                      [0, 3, 9, 11, 18, 21, 28, 30, 38, 40, 49, 51, 62, 64, 75, 77, 89, 90, 103, 105, 115],                   # 8:15
                      [0, 1, 8, 9, 15, 18, 24, 26, 36, 37, 46, 48, 61, 63, 75, 80, 93, 96, 113, 120, 139],                    # 9:00
                      [0, 3, 5, 5, 10, 12, 16, 18, 25, 26, 33, 35, 47, 60, 63, 66, 82, 87, 110, 118, 152],                    # 9:45
                      [0, 1, 1, 2, 4, 6, 6, 7, 10, 11, 15, 17, 24, 25, 33, 37, 50, 52, 70, 80, 112],                          # 10:30
                      [0, 0, -2, -2, -4, -4, -6, -6, -8, -8, -8, -10, -8, -8, -6, -6, -5, 0, 0, 2, 10],                       # 11:15
                      [0, -1, -4, -4, -7, -8, -11, -12, -15, -16, -19, -20, -23, -23, -26, -27, -29, -30, -32, -33, -36],     # 11:37
                      [0, -2, -5, -6, -10, -12, -17, -20, -23, -24, -28, -30, -35, -36, -42, -43, -48, -49, -54, -55, -62],   # 12:00

                        # VIENTO A FAVOR:
                      [0, 1, 3, 3, 5, 6, 8, 9, 12, 12, 14, 15, 20, 21, 23, 25, 28, 30, 32, 32, 35],                           # 6:45   -  5:15
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 3, 3, 4, 4, 5, 5, 6, 6, 7],                                        # 7:30   -  4:30
                      [0, -1, -4, -4, -6, -7, -9, -10, -12, -13, -14, -14, -15, -15, -16, -16, -18, -18, -20, -20, -22],      # 8:15   -  3:45
                      [0, -2, -6, -7, -11, -13, -17, -18, -22, -23, -25, -28, -30, -31, -35, -36, -40, -40, -44, -44, -46],   # 9:00   -  3:00
                      [0, -2, -6, -7, -18, -19, -23, -24, -30, -32, -37, -39, -42, -45, -49, -50, -56, -57, -62, -65, -67],   # 9:45   -  2:15
                      [0, 2, -7, -8, -17, -20, -25, -27, -34, -35, -42, -44, -49, -51, -57, -59, -66, -67, -75, -78, -82],    # 10:30  -  1:30
                      [0, -2, -7, -8, -15, -17, -23, -24, -31, -33, -39, -41, -47, -48, -55, -57, -65, -66, -74, -76, -83],   # 11:15  -  12:45
                      [0, -2, -5, -6, -20, -23, -30, -62, -64, -84],                                                          # 11:37  -  12:22

                     ]

nombres_columnas = ["(6:45)", "(7:30)", "(8:15)", "(9:00)", "(9:45)", "(10:30)", "(11:15)", "(11:37)", "(12:00)",
                    "(5:15)", "(4:30)", "(3:45)", "(3:00)", "(2:15)", "(1:30)",  "(12:45)", "(12:22)"]

# Instanciar la clase
dataframe_original = InterpoladorViento(viento_existentes_1, valores_existentes, nombres_columnas)

# Crear DataFrame completo
dataframe_original. crear_dataframe_total()


print(dataframe_original.df_total.to_string(index=False))