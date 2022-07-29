# frameorks 
from unittest import result
import cv2 # opencv
import mediapipe as mp
import pyautogui # Libreria que nos va a permitir manipular el teclado


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
    model_complexity = 0) as holistic:

    # leer video de entrada
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
            
        # Deteccion
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(frame_rgb)
        
        # visualizar los landmarks del cuerpo en general
        # FACE
        # dibujamos los puntos y las conexiones del rostro
        # mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1) => dibujamos los puntos y les damos un color y un grosor
        # thickness => GROSOR DE LINEA
        mp_drawing.draw_landmarks(frame, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1), 
            mp_drawing.DrawingSpec(color = (0, 128, 255), thickness = 2)) 
        
        # LEFT HAND
        mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=1), 
            mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2)) 

        # RIGHT HAND
        mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1), 
            mp_drawing.DrawingSpec(color = (57, 143, 0), thickness = 2)) 

        # POSE
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
            mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1), 
            mp_drawing.DrawingSpec(color = (255, 255, 255), thickness = 2)) 


        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()