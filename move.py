from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QMainWindow, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ventana Personalizada')
        self.setGeometry(100, 100, 200, 200)  # Tamaño inicial de la ventana
        self.setWindowFlags(Qt.FramelessWindowHint)  # Sin barra de título ni bordes

        # Widget central y su layout (usando QGridLayout en lugar de QVBoxLayout)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: blue;")  # Aplicar color al widget que contiene el layout
        #self.central_widget.setFixedHeight(20)

        self.layout = QGridLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        #self.layout.setStyleSheet("background-color: #4CAF50")

        # Barra de botones
        self.button_bar = QWidget()
        self.button_bar_layout = QHBoxLayout(self.button_bar)
        self.button_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.button_bar_layout.setSpacing(0)

        # Cambiar el color de fondo de la barra y ajustar la altura
        self.button_bar.setStyleSheet("background-color: #2C2C2C;")  # Color plomo oscuro (hex #2C2C2C)
        self.button_bar.setFixedHeight(15)  # Ajustar la altura de la barra a la altura de los botones

        # Añadir un espaciador a la izquierda para empujar los botones a la derecha
        spacer = QSpacerItem(15, 15, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.button_bar_layout.addItem(spacer)

        # Botones minimizar y cerrar
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

        # Añadir la barra de botones al layout principal
        self.layout.addWidget(self.button_bar, 0, 0, 1, 2)  # Coloca la barra en la fila 0, columna 0-2

        # Widget para el reloj
        self.clock_widget = QWidget()
        self.clock_layout = QGridLayout(self.clock_widget)  # Usar QGridLayout para el reloj
        self.clock_layout.setContentsMargins(0, 0, 0, 0)

        self.clock_widget.setStyleSheet("background-color: red;")

        self.layout.addWidget(self.clock_widget, 1, 0, 1, 2)  # Coloca el reloj en la fila 1, columna 0-2

        # Crear la escena y la vista
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.clock_layout.addWidget(self.view, 0, 0, 1, 1)  # Añadir la vista al layout del reloj

        # Inicializar variables para el movimiento de la ventana
        self.dragging = False
        self.drag_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton :
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
