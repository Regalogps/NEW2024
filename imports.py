import numpy as np  # Biblioteca para operaciones numéricas
from scipy.interpolate import interp1d  # Función para interpolaciones unidimensionales
import pandas as pd  # Biblioteca para manipulación de datos en DataFrames


# Importaciones de módulos estándar
import sys  # Importa el módulo sys para manejar funciones del sistema
import math  # Importa el módulo math para funciones matemáticas

# Importaciones de PyQt5
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QHBoxLayout, QSizeGrip,
                             QSpacerItem, QSizePolicy, QMainWindow, QGraphicsView, QLabel, QVBoxLayout, QLineEdit, QStackedLayout, QStyle)

# Componentes de interfaz gráfica                           
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QBrush, QMouseEvent, QIntValidator
from PyQt5.QtCore import Qt, QPoint, QPointF, QRect, QTimer, pyqtSignal, QObject # Importa clases de PyQt5 para el manejo de eventos y puntos

import pyautogui
from pynput import keyboard
import pygetwindow as gw

# DataFrame
from dataframe import InterpoladorViento, InterpoladorDataFrame, crear_df_completo

# Importa las clases CuadrosTexto y Reloj desde sus módulos respectivos
from reloj import Reloj  # Clase Reloj desde el archivo reloj.py
from imput import CuadrosTexto  # Clase CuadrosTexto desde el archivo cuadros_texto.py