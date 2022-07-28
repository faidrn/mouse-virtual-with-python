# frameorks 
from unittest import result
import cv2 # opencv
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture("./assets/images/video.mp4")
### Settings options ###
"""
static_image_mode: por defecto es False => (en False trata a las imagenes de entrada como video, detectando 
    a la persona mas prominente. En True, la deteccion de las personas corre en todas las imagenes, es mejor 
    usarlo en imagenes no relacionadas)
model_complexity: por defecto es 1 => (puede tomar valores de 0, 1 o 2,  corresponden a la compleijidad del modelo
    pose landmark. Entre mas alto el valor, mas lento el movimiento en el video)
smooth_landmarks: por defecto es True => (Si es true se filtra los puntos de referencia de la postura a traves 
    de diferentes imagenes de entrada para reducir la fluctuaciones, es ignorado cuando static_image_mode es true)
min_detection_confidence: por defecto es 0.5 => (valor minimo de confianza de la deteccion de la persona, para que 
    la deteccion sea considerada correcta)
min_tracking_confidence: por defecto es 0.5 => (valor minimo de confianza del modelo de seguimiento de puntos de 
    referencia para q los pose landmarks se consideren rastreados con exito, de lo contrario la deteccion de 
    la persona se invocara en la siguiente entrada. Es ignorado si static_image_mode es true)
"""

with mp_holistic.Holistic(
    static_image_mode = False, 
    model_complexity = 1) as holistic:

    # leer video de entrada
    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
