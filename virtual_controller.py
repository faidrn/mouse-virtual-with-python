# frameorks 
# from cProfile import run
# from unittest import result
from re import A
import cv2 # opencv
import mediapipe as mp
import pyautogui # framework to use the keyboard
from pose_tracking import poseTracking
import math



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


    def get_face(self, frame):
        self.detector.get_landmarks_face(frame, self.results)
        # Get positions of the face to convert to pixels
        self.list_position_face = []
        if self.results.face_landmarks:
            face = self.results.face_landmarks.landmark
            self.list_position_face, bbox_face = self.get_positions(frame, face)

        # if len(self.list_position_face) != 0:
        #     self.x_face, self.y_face = self.list_position_face[0][1:]                  # Get the coordinates of the face, 0 = nose
        


    def right_hand(self, frame):
        # Drawing the right hand
        self.detector.get_landmarks_right_hand(frame, self.results)
        # list_positions, bbox = self.get_position_right_hand(frame)
        # print(f'lista: {list_positions} - bbox: {bbox}')

        # Get positions of the hand to convert to pixels
        self.list_position_right_hand = []
        self.x_right_hand = 0
        # self.results.right_hand_landmarks => get the axis x, y and z
        if self.results.right_hand_landmarks:
            right_hand = self.results.right_hand_landmarks.landmark
            self.list_position_right_hand, bbox_right_hand = self.get_positions(frame, right_hand)

        if len(self.list_position_right_hand) != 0:
            self.x_right_hand, self.y_right_hand = self.list_position_right_hand[16][1:]                  # Get the coordinates of the right hand, 16 = right wrist

        if self.x_right_hand > 0:
            pyautogui.press("f")



    def left_hand(self, frame):
        # Drawing the left hand
        self.detector.get_landmarks_left_hand(frame, self.results)


    def drawing_pose(self, frame):
        self.detector.get_landmarks_pose(frame, self.results)

    
    def right_foot(self):
        pass


    def left_foot(self):
        pass


    def get_positions(self, frame, body_part):
        x_list = []
        y_list = []
        bbox = []
        list_positions = []

        for id, lm in enumerate(body_part):
            height, width, c = frame.shape # We extract the dimensions of the fps
            coordinate_x, coordinate_y = int(lm.x * width), int(lm.y * height) # We convert the information into pixels
            x_list.append(coordinate_x)
            y_list.append(coordinate_y)
            list_positions.append([id, coordinate_x, coordinate_y])

        xMin, xMax = min(x_list), max(x_list)
        yMin, yMax = min(y_list), max(y_list)
        bbox = xMin, yMin, xMax, yMax

        return list_positions, bbox


    # def get_distances(self, point_face, point_right_hand, point_left_hand):
    #     x_face, y_face = self.list_position_face[point_face][1:]
    #     x_right_hand, y_right_hand = self.list_position_right_hand[point_right_hand][1:]
    #     # cx, cy = (x_face + x_right_hand) // 2, (y_face + y_right_hand) // 2

    #     length = math.hypot(x_right_hand - x_face, y_right_hand - y_face)
    #     print(length)
    #     # return length

    
    # def play_game(self, frame):
    #     self.get_pose(frame) # Go first always
    #     self.get_face(frame)
    #     self.drawing_pose(frame)
    #     self.right_hand(frame)
        
    #     self.get_distances(0, 16, 15)


def run():
    
    virtual_controller_object = virtualController(1)
    # Doing the body (in this case hands and feet) detection 
	# Read the video input 
    while True:
        ret, frame = virtual_controller_object.cap.read()
        if ret == False:
            break
                
        # Detection
        virtual_controller_object.get_pose(frame) # Go first always
        virtual_controller_object.get_face(frame)
        virtual_controller_object.drawing_pose(frame)
        virtual_controller_object.right_hand(frame)
        # virtual_controller_object.play_game(frame)
         
        

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    virtual_controller_object.cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
	run()