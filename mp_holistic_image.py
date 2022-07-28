# frameorks 
from unittest import result
import cv2 # opencv
import mediapipe as mp


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

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

    # Input image
    image = cv2.imread("./assets/images/woman.jpg")
    # opencv lee la imagen en bgr, la convertimos a rgb
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # realizamos las detecciones con holistic.process
    results = holistic.process(image_rgb)

    ### OUTPUTS ###
    """
    pose_landmarks: obtenemos las coordenadas (x, y, z), junto con visibility, q es un valor entre 0 y 1, q 
        indica la probabilidad q el punto de referencia sea visible, presente y no ocluido en la imagen
    pose_world_landmarks: devuelve una lista de los puntos de referencia de postura, en donde cada punto 
        consta de las coordenadas x, y, z (coordenadas 3D del mundo real en metros) con el origen en el 
        centro de las caderas, tambien devuelve visibility q es similar a pose landmarks
    face_landmarks: obtenemos 468 puntos de referencia con sus coordenadas x, y, z
    left_hand_landmarks: lista con los 21 puntos de referencia de la mano izquierda con sus coordenadas x, y, z
    right_hand_landmarks: lista con los 21 puntos de referencia de la mano derecha con sus coordenadas x, y, z
    """

    # FACE
    # dibujamos los puntos y las conexiones del rostro
    # mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1) => dibujamos los puntos y les damos un color y un grosor
    # thickness => GROSOR DE LINEA
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
        mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1), 
        mp_drawing.DrawingSpec(color = (0, 128, 255), thickness = 2)) 
    
    # LEFT HAND
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=1), 
        mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 2)) 

    # RIGHT HAND
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1), 
        mp_drawing.DrawingSpec(color = (57, 143, 0), thickness = 2)) 

    # POSE
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1), 
        mp_drawing.DrawingSpec(color = (255, 255, 255), thickness = 2)) 
    
    
    # https://www.youtube.com/watch?v=djoI_s-qPJ0&ab_channel=OMES
    


    # visualizar la imagen de entrada
    cv2.imshow("Image", image)
    # ver todos los puntos de la postura de la persona dibujados en el espacio
        # Plot: puntos de referencia y conexiones en matplotlib 3D
    mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)
    cv2.waitKey(0)
cv2.destroyAllWindows()
