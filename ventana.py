from imports import *
# ordenar sus importaciones

class CustomWindow(QMainWindow):
    def __init__(self):  # Método constructor de la clase
        super().__init__()  # Llama al constructor de la clase base (QMainWindow)

        self.df = crear_df_completo()

        # Inicializar variables para el movimiento de la ventana
        self.dragging = False  # Variable para verificar si se está arrastrando la ventana
        self.drag_position = None  # Almacena la posición del mouse durante el arrastre

        self.setWindowTitle('Ventana Personalizada')  # Establece el título de la ventana
        self.setGeometry(0, 0, 200, 250)  # Establece la posición y tamaño de la ventana (x, y, ancho, alto)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Configura la ventana sin barra de título ni bordes

        self.initUI()
        self.create_instancias()


        # Controlador de teclado para enviar teclas a Chrome
        self.keyboard_controller = Controller()

        # Iniciar el listener para el teclado
        keyboard.on_press(self.on_key_press)

        #self.init_keyboard_listener()  # Iniciar el listener aquí




        self.widget_resize()


    # Crea widget principales: contenedor global, barra de botones, los botones y el espaciador
    def initUI(self):
        # CREA EL CONTENEDOR GLOBAL EN LA VENTANA:

        self.central_widget = QWidget()                                     # Crea un widget central para contener todos los demás widgets
        self.central_widget.setStyleSheet("background-color: black;")       # Cambia el color de fondo del widget
        self.setCentralWidget(self.central_widget)                          # Establece el widget central en la ventana

        # CREA EL ORGANIZADOR  EN EL CONTENEDOR GLOBAL DE LA VENTANA: "( QGridLayout )" 

        self.layout = QGridLayout(self.central_widget)   # Crea un layout en cuadrícula para organizar los widgets en el widget central
        self.layout .setContentsMargins(0, 0, 0, 0)      # Establece márgenes de 0 para el layout (sin espacio alrededor)
        self.layout .setSpacing(0)                       # Establece el espacio entre widgets en el layout a 0

        # CREA EL CONTENEDOR QUE ACTUARA COMO BARRA DE BOTONES (-  x):
        # CREA SU ORGANIZADOR DE ESPACIOS: "( QHBoxLayout )"

        self.barra_gestor = QWidget()                               # Crea un widget que actuará como la barra de botones
        self.layout_2 = QHBoxLayout(self.barra_gestor)              # Crea un layout horizontal para la barra de botones
        self.layout_2 .setContentsMargins(0, 0, 0, 0)               # Establece márgenes de 0 para el layout de la barra de botones
        self.layout_2 .setSpacing(0)                                # Establece el espacio entre botones en la barra a 0
        

        # Agrega un QLabel como título
        self.titulo_barra = QLabel("  Wind Chart Ns")                                 # Crea un QLabel con el texto del título

        # Aplica estilos CSS al título
        self.titulo_barra .setStyleSheet("""
            color: white;
            font-size: 09px;
            font-weight: bold;
            font-family: 'Helvetica', Arial, sans-serif;
            background-color: #333333;
        """)
        self.layout_2 .addWidget(self.titulo_barra)                             # Añade el QLabel al layout de la barra


        # AGREGA LA BARRA DE BOTONES AL ORGANIZADOR GLOBAL DE LA VENTANA:
        self.layout       .addWidget(self.barra_gestor, 0, 0, 1, 2)                 # Agrega la barra de botones al layout en la fila 0, ocupando 2 columnas
        self.barra_gestor .setStyleSheet("background-color: #2C2C2C;")              # Establece el color de fondo de la barra de botones
        self.barra_gestor .setFixedHeight(15)                                       # Fija la altura de la barra de botones a 30 píxeles


        # Espaciador para empujar los botones a la derecha de la barra
        spacer = QSpacerItem(15, 15, QSizePolicy.Expanding, QSizePolicy.Minimum)  # Crea un espaciador que ocupará el espacio disponible
        self.layout_2 .addItem(spacer)  # Añade el espaciador al layout de la barra de botones

        # Botón para minimizar la ventana
        self.minimize_button = QPushButton('-')                     # Crea un botón con el texto "-"
        self.minimize_button.setFixedSize(15, 15)                   # Fija el tamaño del botón a 30x30 píxeles
        self.minimize_button.clicked.connect(self.showMinimized)    # Conecta el clic del botón a la función para minimizar la ventana
        self.minimize_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            text-align: center;
            border: none;
        """)
        self.layout_2 .addWidget(self.minimize_button)              # Añade el botón minimizar al layout de la barra de botones

        # Botón para cerrar la ventana
        self.close_button = QPushButton('x')                        # Crea un botón con el texto "x"
        self.close_button.setFixedSize(15, 15)                      # Fija el tamaño del botón a 30x30 píxeles
        self.close_button.clicked.connect(self.close)               # Conecta el clic del botón a la función para cerrar la ventana
        self.close_button.setStyleSheet("""
            background-color: #f44336;
            color: white;
            font-weight: bold;
            text-align: center;
            border: none;
        """)
        self.layout_2 .addWidget(self.close_button)                 # Añade el botón cerrar al layout de la barra de botones


    def create_instancias(self):
        # Crear un widget para contener el Reloj y el Cuadro de Texto
        self.contenedor_widgets = QWidget()
        self.layout_10 = QVBoxLayout(self.contenedor_widgets)
        self.layout_10.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes
        self.layout_10.setSpacing(0)  # Eliminar el espacio entre widgets
        self.layout.addWidget(self.contenedor_widgets, 1, 0, 1, 2)  # Coloca el contenedor en la fila 1

        # INSTANCIAS 
        self.inst_cuadros = CuadrosTexto(self.df)
        self.inst_reloj   = Reloj(self.inst_cuadros)
        self.inst_reloj.setMinimumSize(200, 200)  # Establece un tamaño mínimo adecuado para el reloj

        # Agrega el Reloj y el Cuadro de Texto al contenedor
        self.layout_10 .addWidget(self.inst_reloj)
        self.layout_10 .addWidget(self.inst_cuadros)

        self.inst_cuadros .imput.setFocus()



    def on_key_press(self, e):
        # Imprimir la tecla presionada
        print(f'Tecla presionada: {e.name}')

        # Verificar si la tecla pertenece al teclado numérico
        if e.name in [str(i) for i in range(10)]:
            print(f'Tecla presionada iff ....: {e.name}')
            # Enviar a Chrome
            self.keyboard_controller.press(e.name[-1])  # Extrae solo el número
            self.keyboard_controller.release(e.name[-1])
            # Simular la escritura del número en el input
            #pyautogui.typewrite(e.name[-1])  # Escribe el último carácter del nombre de la tecla

            # Enviar a tu aplicación (si tienes un campo de entrada)
            current_text = self.inst_cuadros .imput.text()
            self.inst_cuadros .imput.setText(current_text + e.name[-1])  # Asumimos que e.name tiene el formato numX
            self.inst_cuadros .setFocus()  # Asegúrate de que el foco esté en el campo de entrada




    def closeEvent(self, event):
        # Detener el listener de teclado al cerrar la ventana
        keyboard.unhook_all()
        event.accept()



    def widget_resize(self):
        # Agregar un punto de control para redimensionar la ventana
        self.resize_grip = QSizeGrip(self)  # Crea un tamaño de agarre
        self.resize_grip .setFixedSize(20, 20)  # Fija el tamaño del agarre
        self.resize_grip .setStyleSheet("background-color: black;")  # Color para hacerlo visible
        self.layout.addWidget(self.resize_grip, 1, 1, Qt.AlignBottom | Qt.AlignRight)  # Coloca en la esquina inferior derecha



    # Eventos para mover la ventana
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False


# Inicialización de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec_())
