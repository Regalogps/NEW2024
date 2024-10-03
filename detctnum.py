import keyboard

def on_key_press(e):
    # Imprimir la tecla presionada
    print(f'Tecla presionada: {e.name}')

# Iniciar el listener
keyboard.on_press(on_key_press)

# Mantener el programa en ejecución
keyboard.wait('esc')  # Cambia 'esc' por cualquier tecla que desees para detener
