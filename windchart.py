from imports import *
# ordenar sus importaciones

class CustomWindow(QMainWindow):
    def __init__(self):  # Método constructor de la clase
        super().__init__()  # Llama al constructor de la clase base (QMainWindow)

        self.df = crear_df_completo()   # DataFrame

        # Estado para saber si la ventana está en foco
        self.focus_window = True

        # Inicializar variables para el movimiento de la ventana1
        self.dragging = False                       # Variable para verificar si se está arrastrando la ventana
        self.drag_position = None                   # Almacena la posición del mouse durante el arrastre

        self.setWindowTitle('W.ChartEpiC')                                      # Establece el título de la ventana
        self.setGeometry(0, 0, 195, 200)                                        # Establece la posición y tamaño de la ventana (x, y, ancho, alto)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)   # Configura la ventana sin barra de título ni bordes


        # WIDGET CREATE: Contenedor global, barra de botones, los botones y el espaciador
        self.create_widget()
        # WIDGET CREATE: Instancias (QlineEdits, Reloj)
        self.create_instancias()

        # Metodo para redimensionar la ventana
        self.widget_resize()


#----------------------- ALGORITMO DE ENTRADA DE DATOS AL IMBOX------------------------

        # Está conectando la señal focus_signal (que emite un valor booleano indicando si el widget ha ganado o perdido el foco) 
        # al método (detect_focus_imput) Esto significa que cada vez que la señal focus_signal sea emitida (cuando el foco cambia),
        # se ejecutará automáticamente el método "detect_focus_imput"
        self.inst_cuadros .imput .focus_signal.connect(self.detect_focus_imput)

        # Iniciar el listener del teclado
        self.start_keyboard_listener()
    

    def detect_focus_imput(self, has_focus):
        #print("detect_focus_imput")
        active_window = gw.getActiveWindow()
        #print("gw.getActiveWindow():",active_window)

        if has_focus:
            #print("__Imput: FOCO")
            self.focus_window = True

            if active_window.title != 'W.ChartEpiC':
                print(f"Ventana activa: {active_window.title}")
                self.inst_cuadros .imput.clearFocus()
                #self.focus_window = False
            
        else:
            #print("__Imput: SIN FOCO")
            self.focus_window = False
            

    def start_keyboard_listener(self):
        # Listener de teclado utilizando pynput
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()


    def on_key_press(self, key):
        #print("entrada de fatos")
        try:
            # Solo capturamos teclas si la ventana NO está en foco (es decir,     si escribes en Chrome u otra app)
            if not self.focus_window:
                #print("APK SIN FOCO")
                current_text = self.inst_cuadros.imput.text()  # Obtiene el texto actual del QLineEdit # tal vez poner esto en if adentro
                
                # Detectar teclas del teclado numérico (num1-num9)
                if isinstance(key, keyboard.KeyCode):  # Comprueba si la tecla es un código de tecla
                    if 96 <= key.vk <= 105:  # Verifica si el código virtual está en el rango de num0 a num9
                        num_char = str(key.vk - 96)  # Convierte el código a número (0-9)
                        new_text = current_text + num_char  # Crea el nuevo texto agregando el número
                        self.inst_cuadros.imput.setText(new_text)  # Establece el nuevo texto en el QLineEdit
                    
                # Filtrar la tecla espacio
                elif key == keyboard.Key.space:  # Comprueba si se ha presionado la tecla "Espacio"
                    #print("space")
                    pass
                
                elif key == keyboard.Key.backspace:  # Comprueba si se ha presionado la tecla "Retroceso"
                    self.inst_cuadros.imput.setText("")
                    #self.inst_cuadros.imput.setText(current_text[:-1])  # Elimina el último carácter del texto actual
        
        except AttributeError:
            print(f"Tecla especial presionada: {key}")  # Manejo de errores para teclas especiales
   


 #----------------------- ALGORITMO DE ENTRADA DE DATOS AL IMBOX------------------------F I N 
 
    # WIDGET CREATE: Contenedor global, barra de botones, los botones y el espaciador
    def create_widget(self):

        # CONTENEDOR GLOBAL DE LA VENTANA:
        self.central_widget = QWidget()                                             # Crea un widget central para contener todos los demás widgets
        #self.central_widget.setStyleSheet("background-color: black;")              # Cambia el color de fondo del contenedor padre
        self.setCentralWidget(self.central_widget)                                  # Establece el widget central en la ventana

        # ORGANIZADOR GLOBAL DE LA VENTANA: "( QGridLayout )" 
        self.layout = QGridLayout(self.central_widget)                              # Crea un layout en cuadrícula para organizar los widgets en el widget central
        self.layout .setContentsMargins(0, 0, 0, 0)                                 # Establece márgenes de 0 para el layout (sin espacio alrededor)
        self.layout .setSpacing(0)                                                  # Establece el espacio entre widgets en el layout a 0

        # CONTENEDOR QUE ACTUARA COMO BARRA DE BOTONES: (-  x):
        # ORGANIZADOR DE ESPACIOS: "( QHBoxLayout )"
        self.barra_gestor = QWidget()                                               # Barra de botones
        self.layout_2 = QHBoxLayout(self.barra_gestor)                              # Organizador horizontal para la barra de botones
        self.layout_2 .setContentsMargins(0, 0, 0, 0)                               # Establece márgenes de 0 para la barra de botones
        self.layout_2 .setSpacing(0)                                                # Establece el espacio entre botones en la barra a 0


    #--------------------------------------------------------------------------
        # BOTON BLOQUEO REDIMENSIONAR:
        icono = QApplication.style().standardIcon(QStyle.SP_DockWidgetCloseButton)

        self.resize_button = QPushButton()                                          # Crea un botón con el texto "-"
        self.resize_button.setIcon(icono)                                           # Establece el icono en el botón
        self.resize_button.setFixedSize(15, 15)                                     # Fija el tamaño del botón
        self.resize_button.clicked.connect(self.button_resize_active)               # Conecta el clic del botón a la función
        self.resize_button.setStyleSheet("background-color: #2C2C2C;  text-align: center;  border: none;")
        self.layout_2 .addWidget(self.resize_button)                                # Añade el botón resize al layout de la barra de botones
    #--------------------------------------------------------------------------

        
        # TITULO DE LA BARRA DE BOTONES:
        self.titulo_barra = QLabel(" Wind Chart Ns")                                            # Crea un QLabel con el texto del título
        self.titulo_barra .setStyleSheet("background-color: #333333;  color: white;  font-size: 09px;  font-weight: bold;  font-family: 'Helvetica', Arial, sans-serif;")
        self.titulo_barra .setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)          # Establece la política de tamaño para que se expanda
        self.titulo_barra .setCursor(Qt.ClosedHandCursor)
        self.layout_2 .addWidget(self.titulo_barra)                                             # Añade el QLabel al organizador de la barra de botones

        # ESPACIADOR: Empuja los botones(- x) a la derecha
        #spacer = QSpacerItem(15, 15, QSizePolicy.Expanding, QSizePolicy.Minimum)    # Crea un espaciador que ocupará el espacio disponible
        #self.layout_2 .addItem(spacer)                                              # Añade el espaciador al organizador de la barra de botones

        # AGREGA LA BARRA DE BOTONES AL ORGANIZADOR GLOBAL DE LA VENTANA:
        self.layout       .addWidget(self.barra_gestor, 0, 0, 1, 2)                 # Agrega la barra de botones al organizador de la ventana, fila 0, ocupando 2 columnas
        self.barra_gestor .setStyleSheet("background-color: #2C2C2C;")              # Establece el color de fondo de la barra de botones
        self.barra_gestor .setFixedHeight(15)                                       # Fija la altura de la barra de botones en píxeles


        # BOTON MINIMIZAR
        self.minimize_button = QPushButton('-')                                     # Crea un botón con el texto "-"
        self.minimize_button.setFixedSize(15, 15)                                   # Fija el tamaño del botón a 30x30 píxeles
        self.minimize_button.clicked.connect(self.showMinimized)                    # Conecta el clic del botón a la función para minimizar la ventana
        self.minimize_button.setStyleSheet("background-color: #4CAF50;  color: white;  font-weight: bold;  text-align: center;  border: none;")
        self.layout_2 .addWidget(self.minimize_button)                              # Añade el botón minimizar al layout de la barra de botones

        # BOTON CLOSE
        self.close_button = QPushButton('x')                                        # Crea un botón con el texto "x"
        self.close_button.setFixedSize(15, 15)                                      # Fija el tamaño del botón a 30x30 píxeles
        self.close_button.clicked.connect(self.close)                               # Conecta el clic del botón a la función para cerrar la ventana
        self.close_button.setStyleSheet("background-color: #f44336;  color: white;  font-weight: bold;  text-align:  center; border: none; ")
        self.layout_2 .addWidget(self.close_button)                                 # Añade el botón cerrar al layout de la barra de botones

    def create_instancias(self):
        # CONTENEDOR DE LAS INSTANCIAS: (Reloj, QlineEdits)
        self.container_instancias = QWidget()                                       # Contenedor del reloj y los cuadros de entrada
        self.container_instancias .setStyleSheet("background-color: #151515;")      # Establece el color de fondo del reloj y los cuadros de entrada

        self.layout_10 = QVBoxLayout(self.container_instancias)                     # Crea el organizador Vertical
        self.layout_10.setContentsMargins(0, 0, 0, 0)                               # Eliminar márgenes
        self.layout_10.setSpacing(0)                                                # Eliminar el espacio entre widgets
        self.layout   .addWidget(self.container_instancias, 1, 0, 1, 2)             # Coloca el contenedor en la fila 1


        # INSTANCIAS:
        self.inst_cuadros = CuadrosTexto(self.df)
        self.inst_cuadros .setCursor(Qt.ClosedHandCursor)
        self.inst_reloj   = Reloj(self.inst_cuadros)
        
        self.inst_reloj .setMinimumSize(140, 140)                           # Establece un tamaño mínimo adecuado para el reloj
        # Línea fina usando QWidget
        linea = QWidget()
        linea.setFixedHeight(1)                                             # Establecer la altura de la línea
        linea.setStyleSheet("background-color: #1c1d22;")                   # Color de la línea

        # AGREGA LAS INSTANCIAS AL CONTENEDOR:
        self.layout_10 .addWidget(self.inst_reloj)
        self.layout_10 .addWidget(linea)
        self.layout_10 .addWidget(self.inst_cuadros)

        self.inst_cuadros .imput.setFocus()                                 # Establece el foco en imput al ejecutar x 1ra vez


    # Eventos para mover la ventana
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and self.resize_grip.isVisible():
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False


    def widget_resize(self):
        # Agregar un punto de control para redimensionar la ventana
        self.resize_grip = QSizeGrip(self)  # Crea un tamaño de agarre
        self.resize_grip .setFixedSize(10, 10)  # Fija el tamaño del agarre
        self.resize_grip .setStyleSheet("background-color: #151515;")  # Color para hacerlo visible
        self.layout.addWidget(self.resize_grip, 1, 1, Qt.AlignBottom | Qt.AlignRight)  # Coloca en la esquina inferior derecha

    def button_resize_active(self):

        if self.resize_grip.isVisible():                # Si el grip de redimensionar está visible (habilitado)
            self.titulo_barra .setCursor(Qt.ArrowCursor)
            self.inst_cuadros .setCursor(Qt.ArrowCursor)

            #print("Redimensionar desactivado")
            self.resize_grip.hide()                     # Oculta el grip para deshabilitar el redimensionamiento
            self.setFixedSize(self.size())              # Bloquea el tamaño actual de la ventana
            self.titulo_barra .setStyleSheet("background-color: #333333;  color: red;  font-size: 09px;  font-weight: bold;  font-family: 'Helvetica', Arial, sans-serif;")
            
        else:
            self.titulo_barra .setCursor(Qt.ClosedHandCursor)
            self.inst_cuadros .setCursor(Qt.ClosedHandCursor)

            #print("Redimensionar activado")
            self.resize_grip.show()                     # Muestra el grip para habilitar el redimensionamiento
            self.setMinimumSize(140, 200)               # Establece un tamaño mínimo de ventana
            self.setMaximumSize(16777215, 16777215)     # Permite redimensionar libremente
            self.titulo_barra .setStyleSheet("background-color: #333333;  color: white;  font-size: 09px;  font-weight: bold;  font-family: 'Helvetica', Arial, sans-serif;")


    def closeEvent(self, event):
        # Al cerrar la ventana, detener el listener
        self.listener.stop()
        event.accept()


# Inicialización de la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec_())
