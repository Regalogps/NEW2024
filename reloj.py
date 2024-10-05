from imports import *
# ordenar sus importaciones

# Define una clase llamada Reloj que hereda de QWidget
class Reloj(QWidget):
    def __init__(self, inst_recibida=None):
        super().__init__()  # Llama al constructor de la clase base (QWidget)

        self.hora = 0       # Inicializa la hora en 3
        self.minuto = 0     # Inicializa los minutos en 0

        self.invertir_hora = False

        hora_actual = self.actualizar_hora_minuto(0, 0)        # Simula un clic en el centro y guarda la hora en reposo de la manecilla

        self.cuadros = inst_recibida                           # Guarda la instancia recibida en una variable
        self.cuadros .actualizar_hora(hora_actual)             # Llama a su metodo para actualizar la hora en reposo de la manecilla
        

    # Método que se llama cada vez que se necesita repintar la ventana
    def paintEvent(self, event):
        #print("____0____paintEvent")

        painter = QPainter(self)                            # Crea un objeto QPainter para dibujar en la ventana
        rect = self.rect()

        outer_radius = self.drawReloj(painter, rect)        # Llama al método para dibujar el reloj
        self.drawManecillas(painter, rect, outer_radius)  # Llama al método para dibujar las manecillas


    # Método para dibujar el reloj
    def drawReloj(self, painter, rect):
        #print("_____1____drawReloj")

        painter.setRenderHint(QPainter.Antialiasing)                # Habilita el suavizado de bordes
        painter.fillRect(rect, QColor(21, 21, 21))                  # Color de fondo contenedor (código RGB)

        center = rect.center()                                      # Obtiene el centro del área de dibujo
        outer_radius = min(rect.width(), rect.height() ) // 2 - 5   # Calcula el radio del círculo exterior (1/5 del tamaño mínimo del rectángulo)
        inner_radius = outer_radius * 3.7 // 5                      # Calcula el radio del círculo interior (4/5 del radio exterior)

        painter.setBrush(QBrush(QColor(42, 49, 59)))                # Establece el color de fondo del reloj
        painter.setPen(QPen(Qt.black, 1))                           # Establece el color y grosor del borde del reloj
        painter.drawEllipse(center, outer_radius, outer_radius)     # Dibuja el círculo exterior centrado

        # Cambia el color de las líneas de división
        painter.setPen(QPen(QColor(255, 215, 0), 2))                # Cambia el color a dorado y el grosor a 2 para las líneas de división

        # Divide el círculo exterior en 8 partes
        for i in range(8):
            angle = 2 * math.pi * i / 8                             # Calcula el ángulo correspondiente a la división i
            x = center.x() + outer_radius * math.cos(angle)         # Calcula la coordenada x del borde del círculo exterior
            y = center.y() + outer_radius * math.sin(angle)         # Calcula la coordenada y del borde del círculo exterior
            painter.drawLine(center, QPointF(x, y))                 # Dibuja una línea desde el centro hasta el borde del círculo exterior

        painter.setPen(QPen(Qt.black, 1))                           # Reestablece el color y grosor del lápiz para el círculo interior
        painter.drawEllipse(center, inner_radius, inner_radius)     # Dibuja el círculo interior centrado

        return outer_radius


    # Método para dibujar las manecillas del reloj
    def drawManecillas(self, painter, rect, outer_radius):
        #print("____2____drawManecillas")
        
        painter.setRenderHint(QPainter.Antialiasing)                    # Habilita el suavizado de bordes

        center = rect.center()                                          # Obtiene el centro del área de dibujo
        radius = min(rect.width(), rect.height()) // 2                  # Calcula el radio del reloj

        # Dibujar manecilla de la hora
        hour_angle = (self.hora % 12 + self.minuto / 60) * 30                               # Calcula el ángulo de la manecilla de la hora

        #-------------------------------------------------------------------------------------------------------
        # INVERTIR MANECILLA DE LA HORA
        if self.invertir_hora:
            hour_angle = (360 - hour_angle) % 360  # Refleja el ángulo respecto a 180°

        #-------------------------------------------------------------------------------------------------------

        hour_length = outer_radius                                                          # Longitud de la manecilla de la hora
        hour_end_x = center.x() + hour_length * math.cos(math.radians(hour_angle - 90))     # Calcula la posición final x
        hour_end_y = center.y() + hour_length * math.sin(math.radians(hour_angle - 90))     # Calcula la posición final y

        painter.setPen(QPen(Qt.red, 3))                                                     # Establece el color y grosor de la manecilla de la hora
        painter.drawLine(center, QPoint(int(hour_end_x), int(hour_end_y)))                  # Dibuja la manecilla de la hora

        # Dibujar manecilla del minuto
        minute_angle = self.minuto * 6                                                          # Calcula el ángulo de la manecilla de los minutos
        minute_length = radius * 0.0                                                            # Longitud de la manecilla de los minutos
        minute_end_x = center.x() + minute_length * math.cos(math.radians(minute_angle - 90))   # Calcula la posición final x
        minute_end_y = center.y() + minute_length * math.sin(math.radians(minute_angle - 90))   # Calcula la posición final y

        painter.setPen(QPen(Qt.red, 4))                                                         # Establece el color y grosor de la manecilla de los minutos
        painter.drawLine(center, QPoint(int(minute_end_x), int(minute_end_y)))                  # Dibuja la manecilla de los minutos


    # Método que se llama al hacer clic en la ventana
    def mousePressEvent(self, event: QMouseEvent):
        #print("mouseveneto...")
        center = self.rect().center()                                                           # Obtiene el centro del área de dibujo

        # Obtener la posición del clic en relación con el centro
        click_x = event.x() - center.x()                                                        # Calcula la posición x del clic
        click_y = center.y() - event.y()                                                        # Calcula la posición y del clic
        
        hora_nueva = self.actualizar_hora_minuto(click_x, click_y)   # La llamada desde mousePressEvent a este metodo es para hallar la hora nueva
        #                                                            # Hora nueva despues del click
        #print("hora nueva  ", hora_nueva)
        self.cuadros .actualizar_hora(hora_nueva)     # Actualiza la hora actual en la class CuadroTexto() cuando se da click en la ventana
        self.cuadros .event_resultado()               # Actualiza el cuadro de lectura (resultado) con el valor que hay en la fila que hay en imput 
        #                                             # y con el valor que tiene la manecilla para hallar la columna
        self.update()



    # 1.1 Metodo para hallar la hora en reposo(inicio) de la manecilla pasandole (0,0)
    # 1.2 Metodo para hallar la nueva hora al hacer click en la ventana
    def actualizar_hora_minuto(self, click_x, click_y):
        #print("actualizar hora y minuto: ", click_x, click_y)

        #------------------------------------------------------------------
        # INVERTIR HORARIO:
        def calcular_angulo_inverso(angle_new):
            if self.invertir_hora:
                print("Hora invertida: Activado")
                # Invertir el ángulo respecto a 90°
                angle_new = (180 - angle_new) % 360
                
            else:
                print("Hora invertida: Desactivado")

            return angle_new
                
        #------------------------------------------------------------------    


        # Calcular el ángulo del clic
        angle = (math.degrees(math.atan2(-click_y, click_x)) + 360) % 360

        angle = calcular_angulo_inverso(angle)

        # Calcular la hora y minuto desde el ángulo
        self.hora = int((angle // 30) % 12)  # Cada 30 grados representa 1 hora
        self.minuto = int((angle % 30) * 2)  # Cada grado adicional representa 2 minutos

        # Ajustar para que 0 grados sea 3:00
        self.hora = (self.hora + 3) % 12
        self.hora = 12 if self.hora == 0 else self.hora  # Mostrar 0 en lugar de 12

        #print("hora: ",self.hora, "minuto: ", self.minuto)

        #----------------------------------------------------------------------
        if self.hora == 12:  # Si la hora es 12, lo cambia para que sea '00' en lugar de '12'
            hora_formateada = "00"
        else:
            hora_formateada = f"{self.hora:02d}"

            # Generar el nombre de la columna
        columna = f"({hora_formateada}:{self.minuto:02d})"
        #----------------------------------------------------------------------
        return columna
