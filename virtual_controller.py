# frameorks 
from cProfile import run
from unittest import result
import cv2 # opencv
import mediapipe as mp
import pyautogui # framework to use the keyboard
from pose_tracking import poseTracking


class virtualController():
    def __init__(self, camera = 0):
        # Read the web cam
        # 0 = Pc Camera
        # 1 = External camera
        self.cap = cv2.VideoCapture(camera)
        
        self.detector = poseTracking()


    def get_pose(self, frame):
        # Detect and drawing the pose
        self.results = self.detector.detect_pose(frame)



    def right_hand(self, frame):
        # Drawing the right hand
        self.detector.get_landmarks_right_hand(frame, self.results)
        self.get_position_right_hand(frame)


    def left_hand(self, frame):
        # Drawing the left hand
        self.detector.get_landmarks_left_hand(frame, self.results)


    def drawing_pose(self, frame):
        self.detector.get_landmarks_pose(frame, self.results)

    
    def right_foot(self):
        pass


    def left_foot(self):
        pass


    def get_position_right_hand(self, frame, ManoNum = 0, dibujar = True):
        x_list = []
        y_list = []
        bbox = []
        self.list = []

        # self.results.right_hand_landmarks => get the axis x, y and z
        if self.results.right_hand_landmarks:
            right_hand = self.results.right_hand_landmarks
        #     for id, landmark in enumerate(right_hand.landmark):
        #         alto, ancho, c = frame.shape # Extraemos las dimensiones de los fps
        #         cx, cy = int(landmark.x * ancho), int(landmark.y * alto) # Convertimos la informacion en pixeles
        #         x_list.append(cx)
        #         y_list.append(cy)
        #         self.list.append([id, cx, cy])
        #         if dibujar:
        #             cv2.circle(frame, (cx, cy), 5, (0, 0, 0), cv2.FILLED) # Dibujamos un circulo

        #     xMin, xMax = min(x_list), max(x_list)
        #     yMin, yMax = min(y_list), max(y_list)
        #     bbox = xMin, yMin, xMax, yMax
        #     if dibujar:
        #         cv2.rectangle(frame, (xMin - 20, yMin - 20), (xMax + 20, yMax + 20), (0, 255, 0), 2)
        # return self.list, bbox


def run():
    
    virtual_controller_object = virtualController(1)
    # Doing the body (in this case hands and feet) detection 
	# Read the video input 
    while True:
        ret, frame = virtual_controller_object.cap.read()
        if ret == False:
            break
                
        # Detection
        virtual_controller_object.get_pose(frame)
        virtual_controller_object.drawing_pose(frame)
        virtual_controller_object.right_hand(frame)
            
        # visualizar los landmarks del cuerpo en general
        # detector.get_landmarks_face(frame, results)
        # detector.get_landmarks_left_hand(frame, results)
        # detector.get_landmarks_pose(frame, results)
        

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    virtual_controller_object.cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
	run()