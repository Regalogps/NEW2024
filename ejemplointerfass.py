from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cambiar Cursor al Arrastrar')
        self.setGeometry(100, 100, 400, 300)
        
        # Establecer el cursor al iniciar
        self.setCursor(Qt.ClosedHandCursor)

        # Variables para el movimiento
        self.startPos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()  # Guardar la posición de inicio

    def mouseMoveEvent(self, event):
        if self.startPos is not None:
            # Calcular el movimiento
            self.move(self.pos() + event.pos() - self.startPos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = None  # Reiniciar la posición al soltar el botón

if __name__ == '__main__':
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    app.exec_()
