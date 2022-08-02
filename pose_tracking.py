# frameorks 
# from cProfile import run
# from unittest import result
import cv2 # opencv
import mediapipe as mp


class poseTracking():

    # Initialize the parameters of the pose tracking
    def __init__(self, static_image_mode = False, model_complexity = 0):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        

		# Objets to detect and drawing the pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        # self.extremities = [muñeca mano izquierda, right wrist, left foot index, right foot index]
        # self.extremities = [15, 16, 31, 32]



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
        list_coordinates = []

        for idx, file in enumerate(frame):
            height, width, c = frame.shape # Extraemos las dimensiones de los fps
            
            if not results.pose_landmarks:
                continue
            # print(
            #     f'Nose coordinates: ('
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].x * width}, '
            #     f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].y * height})'
            # )
            coordinate_x = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].x * width)
            coordinate_y = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].y * height) # Convertimos la informacion en pixeles
            x_list.append(coordinate_x)
            y_list.append(coordinate_y)
            list_coordinates.append([id, coordinate_x, coordinate_y])
            if dibujar:
                cv2.circle(frame, (coordinate_x, coordinate_y), 5, (0, 0, 0), cv2.FILLED) # Dibujamos un circulo

        return list_coordinates


    def get_hands_coordinates(self, frame, results, hand, dibujar = True):
        x_list = []
        y_list = []
        list_coordinates = []

        for idx, file in enumerate(frame):
            height, width, c = frame.shape # Extraemos las dimensiones de los fps
            
            if not results.pose_landmarks:
                continue
            print(
                f'Wrist coordinates: ('
                f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST].x * width}, '
                f'{results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST].y * height})'
            )
            coordinate_x = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST].x * width)
            coordinate_y = int(results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_WRIST].y * height) # Convertimos la informacion en pixeles
            x_list.append(coordinate_x)
            y_list.append(coordinate_y)
            list_coordinates.append([id, coordinate_x, coordinate_y])
            if dibujar:
                cv2.circle(frame, (coordinate_x, coordinate_y), 5, (0, 0, 0), cv2.FILLED) # Dibujamos un circulo

        return list_coordinates


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
        detector.get_hands_coordinates(frame, results, 0)
        
        

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
	run()
#     # https://noemioocc.github.io/posts/Mostrar-la-webCam-o-reproducir-un-video-openCV-python/