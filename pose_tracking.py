# frameworks 
# from cProfile import run
# from unittest import result
import cv2 # opencv
import mediapipe as mp
import math


class poseTracking():

    # Initialize the parameters of the pose tracking
    def __init__(self, static_image_mode = False, model_complexity = 0):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        

		# Objets to detect and drawing the pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        # self.extremities = [muñeca mano izquierda, right wrist, left foot index, right foot index]
        self.controller = [0, 15, 16, 27, 28]



    # Method to detect the pose
    def detect_pose(self, frame):
        with self.mp_holistic.Holistic(
            self.static_image_mode, 
            self.model_complexity
        ) as holistic:

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(frame_rgb)

        return results


    #### SEE THE POSE LANDMARKS ###
    
    # Face
    # color=(black, green, red)
    def get_landmarks_face(self, frame, results):
        self.mp_drawing.draw_landmarks(frame, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION, 
            self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1), 
            self.mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 1)) 


    # LEFT HAND
    def get_landmarks_left_hand(self, frame, results):
        self.mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, 
            self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=1), 
            self.mp_drawing.DrawingSpec(color = (0, 255, 0), thickness = 2))

    
    # RIGHT HAND
    def get_landmarks_right_hand(self, frame, results):
        self.mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, 
            self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=1), 
            self.mp_drawing.DrawingSpec(color = (57, 143, 0), thickness = 2))


    # POSE
    def get_landmarks_pose(self, frame, results):
        self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS, 
            self.mp_drawing.DrawingSpec(color=(128, 0, 255), thickness=2, circle_radius=1), 
            self.mp_drawing.DrawingSpec(color = (255, 255, 255), thickness = 2))

    
    def get_pose_coordinates(self, frame, results, dibujar = True):
        x_list = []
        y_list = []
        self.list_coordinates_nose = []

        for id, file in enumerate(frame):
            height, width, c = frame.shape # Extraemos las dimensiones de los fps
            
            if not results.pose_landmarks:
                continue
            # print(
            #     f'Nose coordinates: ('
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].x * width}, '
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].y * height})'
            # )
            # coordinate_x, coordinate_y = self.get_nose_coordinates(results, height, width)
            coordinate_x = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].x * width)
            coordinate_y = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].y * height) # Convertimos la informacion en pixeles
            x_list.append(coordinate_x)
            y_list.append(coordinate_y)
            self.list_coordinates_nose.append([id, coordinate_x, coordinate_y])
            if dibujar:
                cv2.circle(frame, (coordinate_x, coordinate_y), 5, (0, 0, 0), cv2.FILLED) # Dibujamos un circulo

        return self.list_coordinates_nose


    def get_right_hand_coordinates(self, frame, results, dibujar = True):
        x_list = []
        y_list = []
        self.list_coordinates_right_hand = []

        for id, file in enumerate(frame):
            height, width, c = frame.shape # Extraemos las dimensiones de los fps
            
            if not results.pose_landmarks:
                continue
            # print(
            #     f'Right Wrist coordinates: ('
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST].x * width}, '
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST].y * height})'
            # )
            coordinate_x = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST].x * width)
            coordinate_y = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST].y * height) # Convertimos la informacion en pixeles
            x_list.append(coordinate_x)
            y_list.append(coordinate_y)
            self.list_coordinates_right_hand.append([id, coordinate_x, coordinate_y])
            if dibujar:
                cv2.circle(frame, (coordinate_x, coordinate_y), 5, (0, 0, 0), cv2.FILLED) # Dibujamos un circulo

        return self.list_coordinates_right_hand
        

    def get_left_hand_coordinates(self, frame, results, dibujar = True):
        x_list = []
        y_list = []
        self.list_coordinates_left_hand = []

        for id, file in enumerate(frame):
            height, width, c = frame.shape # Extraemos las dimensiones de los fps
            
            if not results.pose_landmarks:
                continue
            # print(
            #     f'Left Wrist coordinates: ('
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_WRIST].x * width}, '
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_WRIST].y * height})'
            # )
            coordinate_x = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_WRIST].x * width)
            coordinate_y = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_WRIST].y * height) # Convertimos la informacion en pixeles
            x_list.append(coordinate_x)
            y_list.append(coordinate_y)
            self.list_coordinates_left_hand.append([id, coordinate_x, coordinate_y])
            if dibujar:
                cv2.circle(frame, (coordinate_x, coordinate_y), 5, (0, 0, 0), cv2.FILLED) # Dibujamos un circulo

        return self.list_coordinates_left_hand
        

    def get_right_foot_coordinates(self, frame, results, dibujar = True):
        x_list = []
        y_list = []
        self.list_coordinates_right_foot = []

        for id, file in enumerate(frame):
            height, width, c = frame.shape # Extraemos las dimensiones de los fps
            
            if not results.pose_landmarks:
                continue
            # print(
            #     f'Right ankle coordinates: ('
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_ANKLE].x * width}, '
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_ANKLE].y * height})'
            # )
            coordinate_x = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_ANKLE].x * width)
            coordinate_y = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_ANKLE].y * height) # Convertimos la informacion en pixeles
            x_list.append(coordinate_x)
            y_list.append(coordinate_y)
            self.list_coordinates_right_foot.append([id, coordinate_x, coordinate_y])
            if dibujar:
                cv2.circle(frame, (coordinate_x, coordinate_y), 5, (0, 0, 0), cv2.FILLED) # Dibujamos un circulo

        return self.list_coordinates_right_foot


    def get_left_foot_coordinates(self, frame, results, dibujar = True):
        x_list = []
        y_list = []
        self.list_coordinates_left_foot = []

        for id, file in enumerate(frame):
            height, width, c = frame.shape # Extraemos las dimensiones de los fps
            
            if not results.pose_landmarks:
                continue
            # print(
            #     f'Left ankle coordinates: ('
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_ANKLE].x * width}, '
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_ANKLE].y * height})'
            # )
            coordinate_x = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_ANKLE].x * width)
            coordinate_y = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_ANKLE].y * height) # Convertimos la informacion en pixeles
            x_list.append(coordinate_x)
            y_list.append(coordinate_y)
            self.list_coordinates_left_foot.append([id, coordinate_x, coordinate_y])
            if dibujar:
                cv2.circle(frame, (coordinate_x, coordinate_y), 5, (0, 0, 0), cv2.FILLED) # Dibujamos un circulo

        return self.list_coordinates_left_foot


    def get_nose_coordinates(self, results, height, width):
        coordinate_x = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].x * width)
        coordinate_y = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].y * height) # Convertimos la informacion en pixeles

        return coordinate_x, coordinate_y


    # Funcion para detectar la distancia entre dedos
    def range_between_nose_and_hands(self, point_nose, point_hand, frame, dibujar = True, r = 15, t = 3):
    # def range_between_nose_and_hands(self, point_nose, point_right_hand, point_left_hand, frame, dibujar = True, r = 15, t = 3):
        nose_x, nose_y = self.list_coordinates_nose[point_nose][1:]
        hand_x, hand_y = self.list_coordinates_left_hand[point_hand][1:]
        # right_hand_x, right_hand_y = self.list_coordinates_right_hand[point_right_hand][1:]
        # left_hand_x, left_hand_y = self.list_coordinates_left_hand[point_left_hand][1:]
        # cx, cy = (nose_x + right_hand_x) // 2, (nose_y + right_hand_y) // 2
        if dibujar:
            cv2.line(frame, (nose_x, nose_y), (hand_x, hand_y), (0, 0, 255), t)
            # cv2.line(frame, (nose_x, nose_y), (right_hand_x, right_hand_y), (0, 0, 255), t)
            # cv2.line(frame, (nose_x, nose_y), (left_hand_x, left_hand_y), (0, 0, 255), t)
            cv2.circle(frame, (nose_x, nose_y), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (hand_x, hand_y), r, (0, 0, 255), cv2.FILLED)
            # cv2.circle(frame, (right_hand_x, right_hand_y), r, (0, 0, 255), cv2.FILLED)
            # cv2.circle(frame, (left_hand_x, left_hand_y), r, (0, 0, 255), cv2.FILLED)
            # cv2.circle(frame, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(hand_x - nose_x, hand_y - nose_y)
        # length = math.hypot(right_hand_x - nose_x, right_hand_y - nose_y, left_hand_x - nose_x, left_hand_y - nose_y)
        # print(length)
        return length


    def get_movements(self):
    # def get_movements(self, face_x, face_y, right_hand_x, right_hand_y, left_hand_x, left_hand_y, right_foot_x, right_foot_y):
        # Check if user is not moving
        # print(f'face: {face_x}, {face_y} - rh: {right_hand_x}, {right_hand_y}')
        # Si posicion actual mano es mayor a la anterior
        #     agrego 1, lo q indica q hubo movimiento
        # Si no
        #     agrego 0, no hubo 
        movements = []
        # print(self.list_coordinates_left_hand)
        # print(len(self.list_coordinates_left_hand))
        print(f'{self.list_coordinates_left_hand[len(self.list_coordinates_left_hand) - 1][1]} - {self.list_coordinates_left_hand[0][1]}')
        if self.list_coordinates_left_hand[self.controller[1]][1] > self.list_coordinates_left_hand[self.controller[1] - 1][1]:
            movements.append(1)
        else:
            movements.append(0)

        if self.list_coordinates_right_hand[self.controller[2]][1] > self.list_coordinates_right_hand[self.controller[2] - 1][1]:
            movements.append(1)
        else:
            movements.append(0)
        
        if self.list_coordinates_left_foot[self.controller[3]][1] > self.list_coordinates_left_foot[self.controller[3] - 1][1]:
            movements.append(1)
        else:
            movements.append(0)

        if self.list_coordinates_right_foot[self.controller[4]][1] > self.list_coordinates_right_foot[self.controller[4] - 1][1]:
            movements.append(1)
        else:
            movements.append(0)
                
        return movements


def run():
    # Read the web cam
    # 0 = Camara del pc
    # 1 = camara externa
    cap = cv2.VideoCapture(1)
    detector = poseTracking()

    # Realizamos la deteccion de manos
	# leer video de entrada
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
                
        # Deteccion
        results = detector.detect_pose(frame)
            
        # visualizar los landmarks del cuerpo en general
        detector.get_landmarks_pose(frame, results)
        detector.get_pose_coordinates(frame, results)
        # detector.get_landmarks_face(frame, results)
        detector.get_landmarks_left_hand(frame, results)
        detector.get_landmarks_right_hand(frame, results)
        detector.get_right_hand_coordinates(frame, results)
        detector.get_left_hand_coordinates(frame, results)
        detector.get_right_foot_coordinates(frame, results)
        detector.get_left_foot_coordinates(frame, results)
        # detector.range_between_nose_and_hands(0, 16, 15, frame)
        
        

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
	run()
#     # https://noemioocc.github.io/posts/Mostrar-la-webCam-o-reproducir-un-video-openCV-python/