import pandas as pd
import numpy as np

# Definir la clase para manejar la generación de columnas intermedias e interpolación
class InterpoladorDataFrame:
    def __init__(self, df):
        #Inicializa la clase con un DataFrame
        self.df = df

    def generar_rango_horario(self, start_time, end_time):
        """Genera un rango de tiempo en minutos entre dos horas"""
        start =      pd .to_datetime(start_time, format="(%H:%M)")          # Conviernte el formato cadena en un objeto de tiempo 
        end =        pd .to_datetime(end_time,   format="(%H:%M)")          # Conviernte el formato cadena en un objeto de tiempo 
        time_range = pd .date_range (start=start, end=end, freq='T').time   # Frecuencia en minutos ('T')
        return time_range 

    def generar_columnas_intermedias(self, columnas_horario):
        """Genera columnas intermedias entre las horas especificadas"""
        new_columns = {}

        for i in range(len(columnas_horario) - 1):
            # Obtener el rango de horas entre dos columnas consecutivas
            rango_horario = self.generar_rango_horario(columnas_horario[i], columnas_horario[i+1])

            # Generar las columnas intermedias
            for time in rango_horario[1:-1]:  # Ignorar la primera y última hora
                time_str = time.strftime("(%H:%M)")  # Formato de 24 horas
                new_columns[time_str] = [np.nan] * len(self.df)  # Inicializar con NaN
        
        # Agregar las nuevas columnas al DataFrame usando pd.concat para eficiencia
        new_df = pd.DataFrame(new_columns)
        self.df = pd.concat([self.df, new_df], axis=1)
        
        # Ordenar el DataFrame según los nombres de las columnas
        self.df = self.df.reindex(sorted(self.df.columns, key=lambda x: pd.to_datetime(x.strip('()'), format='%H:%M')), axis=1)

    def interpolar_datos(self):
        """Realiza la interpolación lineal en el DataFrame"""
        self.df.interpolate(method='linear', axis=1, inplace=True)

    def obtener_dataframe(self):
        """Devuelve el DataFrame final"""
        return self.df


# Ejemplo de uso:

# Crear un DataFrame de ejemplo con varias columnas con datos
data = {
    "(00:00)": np.random.rand(20),  # Columna (12:00)
    "(01:10)": np.random.rand(20),   # Columna (1:10)
    "(03:00)": np.random.rand(20),   # Columna (3:00)
    "(04:25)": np.random.rand(20),   # Columna (4:25)
    "(06:55)": np.random.rand(20)    # Columna (4:25)
}
df = pd.DataFrame(data)

# Crear una instancia de la clase, pasando el DataFrame como argumento
interpolador = InterpoladorDataFrame(df)

# Definir las columnas horarias que ya tienen datos
columnas_horario = ["(00:00)", "(01:10)", "(03:00)", "(04:25)", "(06:55)"]

# Generar las columnas intermedias
interpolador.generar_columnas_intermedias(columnas_horario)

# Realizar la interpolación en las nuevas columnas
interpolador.interpolar_datos()

# Obtener el DataFrame final con las columnas intermedias e interpoladas
df_resultante = interpolador.obtener_dataframe()

# Mostrar el DataFrame resultante
print(f"Total de columnas en el DataFrame: {df_resultante.shape[1]}")
print(df_resultante)
