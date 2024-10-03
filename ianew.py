
from imports import interp1d, np, pd


# Definir la clase para manejar la generación de columnas intermedias e interpolación
class InterpoladorDataFrame:

    def __init__(self, df):
        """Inicializa la clase con un DataFrame"""
        self.df = df

    def generar_rango_horario(self, start_time, end_time):
        """Genera un rango de tiempo en minutos entre dos horas"""
        start =      pd .to_datetime (start_time, format="(%H:%M)")
        end =        pd .to_datetime (end_time, format="(%H:%M)")
        time_range = pd .date_range  (start=start, end=end, freq='T').time  # Frecuencia en minutos ('T')
        
        return time_range

    def generar_columnas_intermedias(self, columnas_horario):
        """Genera columnas intermedias entre las horas especificadas"""
        new_columns = {}

        for i in range(len(columnas_horario) - 1):

            if columnas_horario[i] == 'Viento' or columnas_horario[i+1] == 'Viento':
                continue  # Saltar la columna 'Viento'
            
            # Obtener el rango de horas entre dos columnas consecutivas
            rango_horario = self.generar_rango_horario(columnas_horario[i], columnas_horario[i+1])

            # Generar las columnas intermedias
            for time in rango_horario[1:-1]:  # Ignorar la primera y última hora
                time_str = time.strftime("(%H:%M)")  # Formato de 24 horas
                new_columns[time_str] = [np.nan] * len(self.df)  # Inicializar con NaN

        # Agregar las nuevas columnas al DataFrame
        new_df = pd.DataFrame(new_columns)
        self.df = pd.concat([self.df, new_df], axis=1)
        
        # Ordenar el DataFrame según los nombres de las columnas (excluyendo 'Viento')
        columnas_a_ordenar = [col for col in self.df.columns if col != 'Viento']
        self.df = self.df.reindex(
            ['Viento'] + sorted(columnas_a_ordenar, key=lambda x: pd.to_datetime(x.strip('()'), format='%H:%M')),
            axis=1
        )
        

    def interpolar_datos(self):
        """Realiza la interpolación lineal en el DataFrame"""
        self.df.interpolate(method='linear', axis=1, inplace=True)

        # Aplicar el formato a todas las columnas excepto 'Viento', dejando solo un decimal
        columnas_a_redondear = [col for col in self.df.columns if col != 'Viento']
        self.df[columnas_a_redondear] = self.df[columnas_a_redondear].round(0)

    def obtener_dataframe(self):
        """Devuelve el DataFrame final"""
        return self.df


#-----------------------------------------------------------------------------------------------------------------------------------------------------

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
        df_total[nombre_columna] = df_total[nombre_columna].round(0) # .astype(int) esto le quita el 0 adicional  -   # .round(1) le deja un decimal mas exacto

        return df_total


    def crear_dataframe_total(self):
        # Definir el rango completo y los valores faltantes
        rango_completo = list(range(0, 51))
        viento_faltantes = [num for num in rango_completo if num not in self.viento_existentes]

        for i, nombre_columna in enumerate(self.nombres_columnas):
            if i == 0:
                self.df_total = self.generar_dataframe(self.viento_existentes, self.valores_existentes[i], viento_faltantes, nombre_columna=nombre_columna)
            else:
                if nombre_columna == "(00:22)":
                    excep_1 = [0, 2, 5, 6, 15, 16, 21, 40, 41, 50]
                    excep_1_ = [num for num in rango_completo if num not in excep_1]
                    self.df_total = self.generar_dataframe(excep_1, self.valores_existentes[i], excep_1_, self.df_total, nombre_columna=nombre_columna)
                else:
                    self.df_total = self.generar_dataframe(self.viento_existentes, self.valores_existentes[i], viento_faltantes, self.df_total, nombre_columna=nombre_columna)


    def agregar_valor_6_00(self, valor_a, valor_b, grados_a, grados_b, grados_objetivo, nueva_columna):
        # Creando dos listas del DataFrame para interporlar 
        valor_a = self.df_total[valor_a].tolist()
        valor_b = self.df_total[valor_b].tolist()

        # Crear interpolador entre los grados
        interpolador = interp1d([grados_a, grados_b], np.vstack([valor_a, valor_b]), axis=0)
        valor_6_00 = interpolador(grados_objetivo)

        # Añadir los valores interpolados al DataFrame como nueva columna
        self.df_total[nueva_columna] = valor_6_00.flatten()  # Convertir a 1D si es necesario


    def ordenar_dataframe(self):

        # Separar las columnas que representan horas de las que no
        columnas_hora = [col for col in self.df_total.columns if col.startswith('(') and col.endswith(')')]
        otras_columnas = [col for col in self.df_total.columns if col not in columnas_hora]
        
        # Ordenar las columnas de horas
        columnas_hora_ordenadas = sorted(columnas_hora, key=lambda x: pd .to_datetime(x.strip('()'), format='%H:%M'))
        
        # Reindexar el DataFrame con las columnas ordenadas y luego las otras columnas
        self.df_total = self.df_total.reindex(columns=otras_columnas + columnas_hora_ordenadas)
        
        # Mostrar el DataFrame

        #print(self.df_total.to_string(index=False))

def crear_df_completo():

    # Numero de vientos del wind chart original: 0, 5, 6, 10...
    viento_existentes_1 = [0,  2, 5, 6, 10, 11, 15, 16, 20, 21, 25, 26, 30, 31, 35, 36, 40, 41, 45, 46, 50]

    valores_existentes = [
                        # VIENTO A FAVOR:
                      [0, -2, -5, -6, -10, -12, -17, -20, -23, -24, -28, -30, -35, -36, -42, -43, -48, -49, -54, -55, -62],             # 00:00
                      [0, -2, -5, -6, -20, -23, -30, -62, -64, -84],                                                          # 11:37  -  00:22
                      [0, -2, -7, -8, -15, -17, -23, -24, -31, -33, -39, -41, -47, -48, -55, -57, -65, -66, -74, -76, -83],   # 11:15  -  00:45
                      [0, 2, -7, -8, -17, -20, -25, -27, -34, -35, -42, -44, -49, -51, -57, -59, -66, -67, -75, -78, -82],    # 10:30  -  01:30
                      [0, -2, -6, -7, -18, -19, -23, -24, -30, -32, -37, -39, -42, -45, -49, -50, -56, -57, -62, -65, -67],   # 9:45   -  02:15
                      [0, -2, -6, -7, -11, -13, -17, -18, -22, -23, -25, -28, -30, -31, -35, -36, -40, -40, -44, -44, -46],   # 9:00   -  03:00
                      [0, -1, -4, -4, -6, -7, -9, -10, -12, -13, -14, -14, -15, -15, -16, -16, -18, -18, -20, -20, -22],      # 8:15   -  03:45
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 3, 3, 4, 4, 5, 5, 6, 6, 7],                                        # 7:30   -  04:30
                      [0, 1, 3, 3, 5, 6, 8, 9, 12, 12, 14, 15, 20, 21, 23, 25, 28, 30, 32, 32, 35],                           # 6:45   -  05:15

                        # VIENTO EN CONTRA:
                      [0, -3, 8, 9, 16, 18, 22, 25, 31, 32, 38, 40, 47, 49, 55, 57, 61, 63, 68, 70, 75],                                # 06:45
                      [0, 4, 10, 12, 19, 22, 27, 29, 36, 38, 45, 47, 57, 59, 66, 68, 76, 77, 85, 87, 95],                               # 07:30
                      [0, 3, 9, 11, 18, 21, 28, 30, 38, 40, 49, 51, 62, 64, 75, 77, 89, 90, 103, 105, 115],                             # 08:15
                      [0, 1, 8, 9, 15, 18, 24, 26, 36, 37, 46, 48, 61, 63, 75, 80, 93, 96, 113, 120, 139],                              # 09:00
                      [0, 3, 5, 5, 10, 12, 16, 18, 25, 26, 33, 35, 47, 60, 63, 66, 82, 87, 110, 118, 152],                              # 09:45
                      [0, 1, 1, 2, 4, 6, 6, 7, 10, 11, 15, 17, 24, 25, 33, 37, 50, 52, 70, 80, 112],                                    # 10:30
                      [0, 0, -2, -2, -4, -4, -6, -6, -8, -8, -8, -10, -8, -8, -6, -6, -5, 0, 0, 2, 10],                                 # 11:15
                      [0, -1, -4, -4, -7, -8, -11, -12, -15, -16, -19, -20, -23, -23, -26, -27, -29, -30, -32, -33, -36],               # 11:37
                      [0, -2, -5, -6, -10, -12, -17, -20, -23, -24, -28, -30, -35, -36, -42, -43, -48, -49, -54, -55, -61],             # 11:59
                     ]

    nombres_columnas = ["(00:00)", "(00:22)", "(00:45)", "(01:30)", "(02:15)", "(03:00)", "(03:45)", "(04:30)", "(05:15)",
                    "(06:45)", "(07:30)", "(08:15)", "(09:00)", "(09:45)", "(10:30)", "(11:15)", "(11:37)", "(11:59)"]


    # Instancia el primer DataFrame con los nombres de la columna de la lista llamada: "nombres_columnas" 
    df_original = InterpoladorViento(viento_existentes_1, valores_existentes, nombres_columnas)

    # Crear el 1er DataFrame 
    df_original. crear_dataframe_total()

    # Añadir el valor para las 6:00 al 1er DataFrame
    df_original .agregar_valor_6_00('(05:15)', '(06:45)', 292.5, 247.5, [270], "(06:00)")

    # Ordena las columnas en el 1er DataFrame 
    df_original .ordenar_dataframe()


    #___________________________________________________________________________________________

    # Crear una instancia de la clase, pasando el DataFrame como argumento
    interpolador = InterpoladorDataFrame(df_original .df_total)

    # Definir las columnas horarias que ya tienen datos
    columnas_horario = [col for col in df_original .df_total .columns if col != 'Viento']

    # Generar las columnas intermedias
    interpolador.generar_columnas_intermedias(columnas_horario)

    # Realizar la interpolación en las nuevas columnas
    interpolador.interpolar_datos()

    # Obtener el DataFrame final con las columnas intermedias e interpoladas

    df_completo = interpolador.obtener_dataframe()
    #print(df_completo)

    return df_completo

    # Mostrar el DataFrame resultante
    #print(f"Total de columnas en el DataFrame: {df_completo.shape[1]}")

if __name__ == "__main__":
    df_completo = crear_df_completo()
    #print(df_completo)