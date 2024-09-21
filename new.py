import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPolygon, QTransform, QMouseEvent
import math

class Ruleta(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0  # Ángulo inicial de la flecha
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ruleta con Flecha delgada')
        self.setGeometry(100, 100, 400, 400)

        # Cuadro de texto para mostrar el ángulo actual
        self.resultado = QLineEdit(self)
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.resultado)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # Dibujar la ruleta
        self.drawRuleta(painter, rect)

        # Dibujar la flecha
        self.drawFlecha(painter, rect)

    def drawRuleta(self, painter, rect):
        painter.setRenderHint(QPainter.Antialiasing)

        # Configuraciones de la ruleta
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 3

        # Dibujar el círculo de la ruleta
        painter.setBrush(QBrush(QColor(200, 200, 255)))
        painter.setPen(QPen(Qt.black, 2))
        painter.drawEllipse(center, radius, radius)

    def drawFlecha(self, painter, rect):
        painter.setRenderHint(QPainter.Antialiasing)

        # Configuración de la flecha delgada
        center = rect.center()
        radius = min(rect.width(), rect.height()) // 3
        length_flecha = radius - 10  # Longitud de la flecha
        angle_rads = math.radians(self.angle)

        # Puntos de la flecha delgada (similar a una manecilla de reloj)
        end_x = center.x() + length_flecha * math.cos(angle_rads)
        end_y = center.y() - length_flecha * math.sin(angle_rads)

        painter.setPen(QPen(Qt.red, 4))  # Flecha delgada y roja
        painter.drawLine(center, QPoint(int(end_x), int(end_y)))

    def mousePressEvent(self, event: QMouseEvent):
        center = self.rect().center()

        # Obtener la posición del clic
        click_x = event.x() - center.x()
        click_y = center.y() - event.y()

        # Calcular el ángulo en radianes y convertir a grados
        self.angle = math.degrees(math.atan2(click_y, click_x))
        if self.angle < 0:
            self.angle += 360

        # Actualizar la flecha y el cuadro de texto
        self.resultado.setText(f"Ángulo: {self.angle:.2f}°")
        self.update()  # Redibuja la flecha

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ruleta = Ruleta()
    ruleta.show()
    sys.exit(app.exec_())
