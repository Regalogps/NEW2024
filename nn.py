import cv2
import numpy as np
import pytesseract
import tkinter as tk
from mss import mss
import os

# Inicializa el número previo como una cadena vacía
previous_text = ""
last_capture_path = "last_capture.png"  # Archivo donde se almacenará la última captura

# Configuración de Tesseract-OCR (asegúrate de que la ruta a tesseract esté bien)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para obtener texto de una imagen
def detect_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 6')
    return text.strip()

# Eliminar la última captura
def delete_last_capture():
    if os.path.exists(last_capture_path):
        os.remove(last_capture_path)
        print("Última captura eliminada.")

# Función para tomar una captura de pantalla y revisar si hay un nuevo número
def capture_screen():
    global previous_text

    with mss() as sct:
        # Define las dimensiones de la ventana de captura
        monitor = {"top": window.winfo_y(), "left": window.winfo_x(), "width": window.winfo_width(), "height": window.winfo_height()}
        sct_img = sct.grab(monitor)

        img = np.array(sct_img)

        # Detecta texto en la imagen
        text = detect_text(img)
        
        if text and text != previous_text:
            delete_last_capture()  # Elimina la última captura solo si hay un nuevo número
            previous_text = text
            cv2.imwrite(last_capture_path, img)  # Guarda la nueva captura
            # Reemplaza caracteres no ASCII por '?'
            print(f'Nuevo numero detectado: {text.encode("ascii", "replace").decode()}')
        else:
            print('No se detecto un número nuevo o no hay numero.')

    window.after(1000, capture_screen)  # Vuelve a capturar cada segundo

# Función para mover la ventana
def start_move(event):
    window.x = event.x
    window.y = event.y

def stop_move(event):
    window.x = None
    window.y = None

def on_motion(event):
    x = (event.x_root - window.x)
    y = (event.y_root - window.y)
    window.geometry(f"+{x}+{y}")

# Crear la ventana principal
window = tk.Tk()
window.title("Captura de pantalla de números")
window.geometry("100x100")
window.attributes("-topmost", True)  # Hace que la ventana esté siempre en primer plano

# Hacer que la ventana se pueda mover
window.bind('<ButtonPress-1>', start_move)
window.bind('<B1-Motion>', on_motion)

# Define las dimensiones de la transparencia (solo el centro)
frame = tk.Frame(window, bg='black')
frame.pack(fill=tk.BOTH, expand=tk.YES, padx=5, pady=5)

# Establece el fondo transparente
window.attributes("-transparentcolor", "black")  # Define el color que será transparente

# Iniciar la captura
capture_screen()            

# Iniciar el bucle de la ventana
window.mainloop()
