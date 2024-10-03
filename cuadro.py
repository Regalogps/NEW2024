from imports import *

class CuadrosTexto(QWidget):
    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.df = df                # Recibe el DataFrame desde la clase Reloj
        self.hora_actual = None     # Variable que guarda la hora siempre
        self.initUI()

    # Método para configurar la interfaz gráfica de los cuadros de texto
    def initUI(self):
        # Crear el campo de texto para mostrar la fuerza del viento
        self.resultado = QLineEdit(self)  # Crea un campo de texto para mostrar la hora              -
        self.resultado.setReadOnly(True)  # Establece el campo como de solo lectura                  -
        self.resultado.setAlignment(Qt.AlignCenter)  # Alinea el texto al centro  
        self.resultado.setFixedHeight(25)  # Establece una altura fija de 40 píxeles
        self.resultado.setText("0.0")
        self.resultado.setStyleSheet(
        """
        font-size: 17px; 
        font-weight: bold; 
        color: #c8c8c8; 
        background-color: #1c1d22; 
        border: 1px solid black; 
        border-radius: 4px; 
        text-align: center;
        """
        )

        # Crear el campo de texto para la entrada de vientos
        self.imput = CustomLineEdit(self)
        self.imput.setAlignment(Qt.AlignCenter) 
        self.imput.setFixedHeight(25)
        self.imput.setStyleSheet(
        """
        font-size: 17px; 
        font-weight: bold; 
        color: #c8c8c8; 
        background-color: red; 
        border: 1px solid black; 
        border-radius: 4px; 
        text-align: center;
        """
        )

        # Crear validador para permitir solo números de 2 dígitos (entre 0 y 99)
        validator = QIntValidator(0, 50, self)
        self.imput.setValidator(validator)
        
        # Conectar el evento de texto modificado
        self.imput.textChanged .connect(self.imput_textchanged)
        # Instalar el event filter para la entrada de vientos (self.imput)
        self.imput .installEventFilter(self)


        # Crear un layout vertical
        layout = QVBoxLayout()
        layout .addWidget(self.resultado)           # Añade el campo de texto al layout
        layout .addWidget(self.imput)               # Añade el campo de texto de entrada al layout
        layout .setContentsMargins(30, 0, 30, 10)  # Establecer márgenes (izquierda, arriba, derecha, abajo)
        self.setLayout(layout)                      # Establece el layout en el widget

        self.imput.setFocusPolicy(Qt.StrongFocus)  # Permitir que reciba el foco
        self.imput.setFocus()

    # Método que ctualiza el resultado con el valor actual de entrada del input y la manecilla / SE LLAMA AUTOMATICAMENTE CUANDO ESCRIBIMOS EN IMPUT
    def imput_textchanged(self):
        #print("ESCRIBIE")

        valor_imput = self.imput.text()  # Obtiene el texto de imput

        # Evitar posicionar el cursor manualmente
        cursor_position = self.imput.cursorPosition()
        longitud_texto = len(valor_imput)

        # Evitar que se ingrese el número "0"
        if valor_imput == "0":
            self.imput.setText("")  # Borra el "0" si lo ingresan
            return  # Salimos para evitar más procesamiento


        if valor_imput .isdigit():  # Verifica si es un número
            fila = int(valor_imput)
            
            if 0 <= fila < len(self.df):  # Verifica si la fila está dentro del rango
                valor = self.df.loc[fila, self.hora_actual] # Obtiene el valor de la fila seleccionada
                self.resultado.setText(str(valor))  # Actualiza el resultado

            else:
                self.resultado.setText("Fila fuera de rango")
                self.imput.setText(valor_imput[:-1]) 
        else:
            self.resultado.setText("0.0")  # Limpia el resultado si no es un número



    # Metodo actualiza el cuadro de lectura (resultado) con el valor que hay en la fila que hay en imput y con el valor que tiene la manecilla para hallar la columna
    def event_resultado(self):
            print("EVENT RESULTADO__CLASE CUADRO")

            #----------------------------------------------------------------------
            # CONSIGUE LA HORA Y LA COLUMNA DEL DATAFRAME

            imput_valor = self.imput.text()  # Obtiene el texto del QLineEdit
            reloj_valor = self.hora_actual  # Obtiene el valor del reloj ejem: (04:45)

            if reloj_valor in self.df.columns:

                if imput_valor .isdigit() and int(imput_valor) <= 50:  # Verifica si es un número3

                    numero_fila = int(imput_valor)                  # Obtiene el valor actual del cuadro de entrada imput
                    valor = self.df.loc[numero_fila, reloj_valor]   # fila y nombre de columna

                    # Mostrar el valor en el QLineEdit o QLabel
                    self.resultado.setText(f"{valor}")

                else:
                    self.resultado.setText("0.0")
            else:
                # Si la columna no existe, mostrar un mensaje de error o algo por el estilo
                self.resultado.setText("Horario no encontrado")
            #----------------------------------------------------------------------
            self.imput.setFocus()
            #self.update()  # Llama a update si necesitas repintar


    # Metodo para actualizar columna hija con el valor de columna padre / se accese desde la clase Reloj
    def actualizar_hora(self, hora_reloj):
        #print(" Actualizando columna hijo:", self.hora_actual)
        self.hora_actual = hora_reloj  # Guarda el valor de columna para usarlo más tarde



# Nueva clase que hereda de QLineEdit para sobreescribir mousePressEvent
class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)  # Llama al evento original de QLineEdit
        self.setCursorPosition(len(self.text()))  # Mueve el cursor al final del texto