import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor

class Reloj(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Reloj con Circunferencias Concéntricas')
        self.setGeometry(100, 100, 400, 400)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        self.drawCircunferencias(painter, rect)

    def drawCircunferencias(self, painter, rect):
        painter.setRenderHint(QPainter.Antialiasing)  # Habilita el suavizado de bordes para un mejor acabado visual
        center = rect.center()  # Obtiene el centro del área de dibujo desde el rectángulo

        outer_radius = min(rect.width(), rect.height()) // 5  # Calcula el radio del círculo exterior (1/5 del tamaño mínimo del rectángulo)
        inner_radius = outer_radius * 4 // 5  # Calcula el radio del círculo interior (4/5 del radio exterior)

        painter.setBrush(QBrush(QColor(42, 49, 59)))  # Establece el color de fondo del reloj
        painter.setPen(QPen(Qt.black, 1))  # Establece el color y grosor del borde del reloj
        painter.drawEllipse(center, outer_radius, outer_radius)  # Dibuja el círculo exterior centrado

        # Cambia el color de las líneas de división
        painter.setPen(QPen(QColor(255, 215, 0)))  # Cambia el color a rojo y el grosor a 2 para las líneas de división

        # Divide el círculo exterior en 8 partes
        for i in range(8):
            angle = 2 * math.pi * i / 8  # Calcula el ángulo correspondiente a la división i
            x = center.x() + outer_radius * math.cos(angle)  # Calcula la coordenada x del borde del círculo exterior
            y = center.y() + outer_radius * math.sin(angle)  # Calcula la coordenada y del borde del círculo exterior
            painter.drawLine(center, QPointF(x, y))  # Dibuja una línea desde el centro hasta el borde del círculo exterior

        painter.setPen(QPen(Qt.black, 1))  # Reestablece el color y grosor del lápiz para el círculo interior
        painter.drawEllipse(center, inner_radius, inner_radius)  # Dibuja el círculo interior centrado



if __name__ == '__main__':
    app = QApplication(sys.argv)
    reloj = Reloj()
    reloj.show()
    sys.exit(app.exec_())
