# frameorks 
from cProfile import run
from unittest import result
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


    # Method to detect the pose
    def detect_pose(self, frame):
        with self.mp_holistic.Holistic(self.static_image_mode, self.model_complexity) as holistic:

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
        detector.get_landmarks_face(frame, results)
        detector.get_landmarks_left_hand(frame, results)
        detector.get_landmarks_right_hand(frame, results)
        detector.get_landmarks_pose(frame, results)
        

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
	run()
    # https://noemioocc.github.io/posts/Mostrar-la-webCam-o-reproducir-un-video-openCV-python/