from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QRadioButton, QHBoxLayout, QLabel, QMainWindow, QGraphicsView, QGraphicsScene, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QRectF, QStandardPaths

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ventana Personalizada')
        self.setGeometry(100, 100, 200, 200)  # Tamaño inicial de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)  # Sin barra de título ni bordes

        # Widget central y su layout (usando QGridLayout en lugar de QVBoxLayout)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Barra de botones
        self.button_bar = QWidget()
        self.button_bar_layout = QHBoxLayout(self.button_bar)
        self.button_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.button_bar_layout.setSpacing(0)
        self.layout.addWidget(self.button_bar, 0, 0, 1, 2)  # Coloca la barra en la fila 0, columna 0-2

        self.button_bar.setStyleSheet("background-color: #2C2C2C;")  # Color plomo oscuro (hex #2C2C2C)



        # Añadir un espaciador a la izquierda para empujar los botones a la derecha
        spacer = QSpacerItem(15, 15, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_bar_layout.addItem(spacer)


        # Boton minimizar
        self.minimize_button = QPushButton('-')
        self.minimize_button.setFixedSize(15, 15)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.minimize_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            text-align: center;
            border: none;
        """)  # Estilo del botón minimizar

        self.button_bar_layout.addWidget(self.minimize_button)

        # Boton cerrar
        self.close_button = QPushButton('x')
        self.close_button.setFixedSize(15, 15)
        self.close_button.clicked.connect(self.close)

        self.close_button.setStyleSheet("""
            background-color: #f44336;
            color: white;
            font-weight: bold;
            text-align: center;
            border: none;
        """)  # Estilo del botón cerrar

        self.button_bar_layout.addWidget(self.close_button)

        # Widget para el reloj
        self.clock_widget = QWidget()
        self.clock_layout = QGridLayout(self.clock_widget)  # Usar QGridLayout para el reloj
        self.clock_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.clock_widget, 1, 0, 1, 2)  # Coloca el reloj en la fila 1, columna 0-2

        # Crear la escena y la vista
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.clock_layout.addWidget(self.view, 0, 0, 1, 1)  # Añadir la vista al layout del reloj

        # Dibujar el círculo y los radio buttons
        #self.draw_circle_and_buttons()

    """def draw_circle_and_buttons(self):
        # Ajustar el tamaño de la imagen
        diameter = 150  # Diámetro del círculo
        pixmap = QPixmap(diameter, diameter)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(0, 0, diameter, diameter)
        painter.end()

        # Añadir la imagen a la escena
        self.scene.addPixmap(pixmap)

        # Añadir los radio buttons sobre el círculo
        self.radio_button_1 = QRadioButton("1")
        self.radio_button_1.setStyleSheet("background-color: transparent;")  # Fondo transparente
        self.clock_layout.addWidget(self.radio_button_1, 0, 0)  # Posición de la hora 1

        self.radio_button_2 = QRadioButton("2")
        self.radio_button_2.setStyleSheet("background-color: transparent;")  # Fondo transparente
        self.clock_layout.addWidget(self.radio_button_2, 0, 1)  # Posición de la hora 2

        # Exportar la imagen al escritorio
        self.export_image(pixmap)

    def export_image(self, pixmap):
        file_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation) + "/circle_image.png"
        pixmap.save(file_path)
        print(f"Imagen exportada a: {file_path}")"""

app = QApplication([])
window = CustomWindow()
window.show()
app.exec_()
