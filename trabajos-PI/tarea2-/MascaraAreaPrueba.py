import cv2
import numpy as np
import tkinter as Tk
from tkinter.filedialog import askopenfilename

def cargar_video():
    file_path = askopenfilename(filetypes=[("Video files", "*.mp4")])
    return file_path

# Cargar el archivo de video
video_path = cargar_video()
if not video_path:
    print("No se seleccionó ningún archivo de video.")
    exit()

# Captura de video
capture = cv2.VideoCapture(video_path)
if not capture.isOpened():
    print("Error al abrir el video")
    exit()

# Leer el primer frame para usarlo como referencia
ret, first_frame = capture.read()
if not ret:
    print("Error al leer el primer frame")
    capture.release()
    exit()

# Crear una máscara basada en el primer frame
mask = np.zeros(first_frame.shape[:2], dtype="uint8")

# Define las coordenadas de las cuatro esquinas del rectángulo irregular
# [x, y] = [columna, fila]
#puntos = np.array([[481, 466], [742, 457], [226, 703], [1146, 668]])
#correccion de puntos el orden es: superior izquierda, superior derecha, inferior derecha, inferior izquierda
puntos = np.array([[481, 466], [742, 457], [1206, 681], [153, 697]])

# Rellenar el polígono (rectángulo irregular) en la máscara
cv2.fillPoly(mask, [puntos], 255)

# Aplicar la misma máscara a todos los frames siguientes
while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    # Aplicar la máscara al frame
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

    # Mostrar el resultado
    cv2.imshow('Masked Video', masked_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
