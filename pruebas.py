from pynput.keyboard import Key, Controller
import keyboard
import time

keyboard_controller = Controller()

def on_key_press(e):
    print(f'Tecla presionada: {e.name}')
    
    if e.name in [f'num{i}' for i in range(10)]:
        # Enviar a Chrome
        keyboard_controller.press(e)
        keyboard_controller.release(e)
        
        # Enviar a tu aplicación (si tienes un campo de entrada)
        current_text = self.imput.text()
        self.imput.setText(current_text + e.name[-1])  # Asumimos que e.name tiene el formato numX
        self.imput.setFocus()  # Asegúrate de que el foco esté en el campo de entrada

# Iniciar el listener
keyboard.on_press(on_key_press)
keyboard.wait('esc')  # Cambia 'esc' por cualquier tecla que desees para detener
