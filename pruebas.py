from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from pynput import keyboard
import sys

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuración de la interfaz
        self.setWindowTitle("Captura de Teclas desde Chrome")
        self.setGeometry(100, 100, 400, 100)
        
        # Campo de entrada de texto
        self.input_field = QLineEdit(self)
        
        # Diseño
        layout = QVBoxLayout()
        layout.addWidget(self.input_field)
        self.setLayout(layout)
        
        # Estado para saber si la ventana está en foco
        self.in_focus = True
        
        # Conectar señal de foco
        self.input_field.focusInEvent = self.on_focus_in
        self.input_field.focusOutEvent = self.on_focus_out
        
        # Iniciar el listener del teclado
        self.start_keyboard_listener()
    
    def start_keyboard_listener(self):
        # Listener de teclado utilizando pynput
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
    
    def on_key_press(self, key):
        try:
            # Solo capturamos teclas si la ventana NO está en foco (es decir, si escribes en Chrome u otra app)
            if not self.in_focus:
                current_text = self.input_field.text()
                if hasattr(key, 'char') and key.char is not None:  # Comprobar si es una tecla de carácter
                    new_text = current_text + key.char
                    self.input_field.setText(new_text)
                elif key == keyboard.Key.space:
                    self.input_field.setText(current_text + ' ')
                elif key == keyboard.Key.backspace:
                    self.input_field.setText(current_text[:-1])
        except AttributeError:
            print(f"Tecla especial presionada: {key}")
    
    def on_focus_in(self, event):
        # Indica que la ventana está en foco
        self.in_focus = True
        super(QLineEdit, self.input_field).focusInEvent(event)
    
    def on_focus_out(self, event):
        # Indica que la ventana está fuera de foco
        self.in_focus = False
        super(QLineEdit, self.input_field).focusOutEvent(event)
    
    def closeEvent(self, event):
        # Al cerrar la ventana, detener el listener
        self.listener.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Iniciar la aplicación
    window = MyApp()
    window.show()
    
    # Ejecutar el evento de la aplicación
    sys.exit(app.exec_())
