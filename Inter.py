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
        try:
            result = interp1d(viento_existentes_1, valor_exis_1, kind='linear', fill_value='extrapolate')
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
            df_total[nombre_columna] = df_total[nombre_columna].round(1)

            return df_total
        except ValueError as e:
            print(f"Error al interpolar los valores para {nombre_columna}: {e}")
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

    def completar_columnas(self, total_columnas=720):
        # Obtener las columnas existentes
        columnas_actuales = len(self.df_total.columns) - 1  # Restamos 1 porque la columna 'Viento' no cuenta
        columnas_faltantes = total_columnas - columnas_actuales

        if columnas_faltantes <= 0:
            print("Ya tienes el número necesario de columnas o más.")
            return self.df_total

        # Añadir columnas interpoladas adicionales hasta llegar a 720
        for i in range(columnas_faltantes):
            nueva_columna = f"Columna_extra_{i + 1}"
            valores_extra = np.random.random(len(self.df_total))  # Generar valores aleatorios para las columnas extra
            self.df_total[nueva_columna] = valores_extra

        return self.df_total


# Definir los datos originales
viento_existentes_1 = [0, 2, 5, 6, 10, 11, 15, 16, 20, 21, 25, 26, 30, 31, 35, 36, 40, 41, 45, 46, 50]

valores_existentes = [
    [0, -3, 8, 9, 16, 18, 22, 25, 31, 32, 38, 40, 47, 49, 55, 57, 61, 63, 68, 70, 75],
    [0, 4, 10, 12, 19, 22, 27, 29, 36, 38, 45, 47, 57, 59, 66, 68, 76, 77, 85, 87, 95],
    [0, 3, 9, 11, 18, 21, 28, 30, 38, 40, 49, 51, 62, 64, 75, 77, 89, 90, 103, 105, 115],
    [0, 1, 8, 9, 15, 18, 24, 26, 36, 37, 46, 48, 61, 63, 75, 80, 93, 96, 113, 120, 139],
    [0, 3, 5, 5, 10, 12, 16, 18, 25, 26, 33, 35, 47, 60, 63, 66, 82, 87, 110, 118, 152],
    [0, 1, 1, 2, 4, 6, 6, 7, 10, 11, 15, 17, 24, 25, 33, 37, 50, 52, 70, 80, 112],
    [0, 0, -2, -2, -4, -4, -6, -6, -8, -8, -8, -10, -8, -8, -6, -6, -5, 0, 0, 2, 10],
    [0, -1, -4, -4, -7, -8, -11, -12, -15, -16, -19, -20, -23, -23, -26, -27, -29, -30, -32, -33, -36],
    [0, -2, -5, -6, -10, -12, -17, -20, -23, -24, -28, -30, -35, -36, -42, -43, -48, -49, -54, -55, -62]
]

nombres_columnas = ["(6:45)", "(7:30)", "(8:15)", "(9:00)", "(9:45)", "(10:30)", "(11:15)", "(11:37)", "(12:00)"]

# Instanciar la clase
dataframe_original = InterpoladorViento(viento_existentes_1, valores_existentes, nombres_columnas)

# Crear DataFrame completo
dataframe_original.crear_dataframe_total()

# Completar hasta 720 columnas
df_final = dataframe_original.completar_columnas(720)

# Imprimir el resultado
print(df_final.to_string(index=False))
