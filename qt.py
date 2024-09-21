from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

app = QApplication([])

# Crear una ventana principal
window = QWidget()
window.setWindowTitle('Ejemplo de Layout')

# Crear un layout vertical
layout = QVBoxLayout()

# Crear algunos botones
button1 = QPushButton('Botón 1')
button2 = QPushButton('Botón 2')
button3 = QPushButton('Botón 3')

# Agregar los botones al layout
layout.addWidget(button1)
layout.addWidget(button2)
layout.addWidget(button3)

# Aplicar el layout a la ventana
window.setLayout(layout)

# Mostrar la ventana
window.show()

app.exec_()
