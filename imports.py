import numpy as np  # Biblioteca para operaciones numéricas
from scipy.interpolate import interp1d  # Función para interpolaciones unidimensionales
import pandas as pd  # Biblioteca para manipulación de datos en DataFrames


# Importaciones de módulos estándar
import sys  # Importa el módulo sys para manejar funciones del sistema
import math  # Importa el módulo math para funciones matemáticas

# Importaciones de PyQt5
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QPushButton, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QMainWindow, QGraphicsView, QLabel, QVBoxLayout, QLineEdit)

# Componentes de interfaz gráfica                           
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QBrush, QMouseEvent
from PyQt5.QtCore import Qt, QPoint, QPointF   # Importa clases de PyQt5 para el manejo de eventos y puntos

# DataFrame
from ianew import df_completo