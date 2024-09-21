from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QRadioButton, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QMainWindow, QGraphicsView, QGraphicsScene, QLabel, QVBoxLayout)
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QRect, QStandardPaths

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ventana Personalizada')
        self.setGeometry(100, 100, 180, 180)  # Tamaño inicial de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)  # Sin barra de título ni bordes

        # Widget central y su layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal de la ventana
        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Barra de botones
        self.button_bar = QWidget()
        self.button_bar_layout = QHBoxLayout(self.button_bar)
        self.button_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.button_bar_layout.setSpacing(0)

        # Añadir la barra de botones al layout principal
        self.layout.addWidget(self.button_bar, 0, 0, 1, 2)  # Fila 0, columna 0, ocupa 1x1 celda

        # Color y altura de la barra de botones
        self.button_bar.setStyleSheet("background-color: #2C2C2C;")
        self.button_bar.setFixedHeight(15)  # Altura ajustada de la barra de botones

        # Espaciador para empujar los botones a la derecha
        spacer = QSpacerItem(15, 15, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_bar_layout.addItem(spacer)

        # Botón minimizar
        self.minimize_button = QPushButton('-')
        self.minimize_button.setFixedSize(15, 15)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.minimize_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            text-align: center;
            border: none;
        """)
        self.button_bar_layout.addWidget(self.minimize_button)

        # Botón cerrar
        self.close_button = QPushButton('x')
        self.close_button.setFixedSize(15, 15)
        self.close_button.clicked.connect(self.close)
        self.close_button.setStyleSheet("""
            background-color: #f44336;
            color: white;
            font-weight: bold;
            text-align: center;
            border: none;
        """)
        self.button_bar_layout.addWidget(self.close_button)




        # Widget para la imagen
        self.image_widget = QLabel()
        self.pixmap = QPixmap('C:/Users/REGALOGPS/Desktop/np/ciculo.png')  # Reemplaza con la ruta de tu imagen
        self.image_widget.setPixmap(self.pixmap)
        self.image_widget.setScaledContents(True)
        self.layout.addWidget(self.image_widget, 1, 0, 1, 2)  # Coloca la imagen en la fila 1, columna 0-2

        # Layout para los widgets sobre la imagen
        self.overlay_layout = QVBoxLayout()
        self.overlay_layout.setContentsMargins(0, 0, 0, 0)
        self.overlay_widget = QWidget(self.image_widget)
        self.overlay_widget.setLayout(self.overlay_layout)
        self.overlay_widget.setGeometry(QRect(0, 0, self.pixmap.width(), self.pixmap.height()))

        # Añadir botones y radio buttons sobre la imagen
        self.radio_button_1 = QRadioButton("Option 1")
        self.radio_button_2 = QRadioButton("Option 2")

        self.overlay_layout.addWidget(self.radio_button_1)
        self.overlay_layout.addWidget(self.radio_button_2)

        # Establecer el tamaño y posición de los widgets en la imagen
        self.radio_button_1.move(50, 50)  # Cambia las coordenadas según sea necesario
        self.radio_button_2.move(50, 100)  # Cambia las coordenadas según sea necesario





        # Inicializar variables para el movimiento de la ventana
        self.dragging = False
        self.drag_position = None

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

app = QApplication([])
window = CustomWindow()
window.show()
app.exec_()
