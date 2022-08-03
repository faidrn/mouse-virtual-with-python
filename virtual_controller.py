# frameworks 
# from cProfile import run
# from unittest import result
from operator import length_hint
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


    def drawing_pose(self, frame):
        # Drawing the landmarks of the pose
        self.detector.get_landmarks_pose(frame, self.results)
        # Face
        # self.detector.get_landmarks_face(frame, self.results)
        # Drawing the right hand
        self.detector.get_landmarks_right_hand(frame, self.results)
        # Drawing the left hand
        self.detector.get_landmarks_left_hand(frame, self.results)


    def get_face_position(self, frame):
        self.list_position_face = self.detector.get_pose_coordinates(frame, self.results)
        # print(self.list_position_face)


    def get_right_hand_position(self, frame):
        self.list_position_right_hand = self.detector.get_right_hand_coordinates(frame, self.results)


    def get_left_hand_position(self, frame):
        self.list_position_left_hand = self.detector.get_left_hand_coordinates(frame, self.results)

    
    def get_right_foot_position(self, frame):
        self.list_position_right_foot = self.detector.get_right_foot_coordinates(frame, self.results)



    def get_left_foot_position(self, frame):
        self.list_position_left_foot = self.detector.get_left_foot_coordinates(frame, self.results)


    # def stop_position(self, face_x, face_y, right_hand_x, right_hand_y, left_hand_x, left_hand_y):
    def is_player_get_moving(self, frame):
        # Check if player is moving
        # 0 = lh    1 = rh  2 = lf      3 = rf
        # movements = self.detector.get_movements()
        length_left_hand = self.detector.range_between_nose_and_hands(0, 15, frame) #Nos entrega la distancia entre el punto 8 y 12
        # print(movements)
        print(length_left_hand)

        # if movements[0]

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
        virtual_controller_object.drawing_pose(frame)

        virtual_controller_object.get_face_position(frame)
        virtual_controller_object.get_right_hand_position(frame)
        virtual_controller_object.get_left_hand_position(frame)
        virtual_controller_object.get_right_foot_position(frame)
        virtual_controller_object.get_left_foot_position(frame)
        # virtual_controller_object.play_game(frame)
         
        # Get the positions of the nose, hands and feet
        if len(virtual_controller_object.list_position_face) != 0:
            # face_x, face_y = virtual_controller_object.list_position_face[0][1:]
            # right_hand_x, right_hand_y = virtual_controller_object.list_position_right_hand[16][1:]
            # left_hand_x, left_hand_y = virtual_controller_object.list_position_left_hand[15][1:]
            # right_foot_x, right_foot_y = virtual_controller_object.list_position_right_foot[28][1:]
            # left_foot_x, left_foot_y = virtual_controller_object.list_position_left_foot[27][1:]
            # print(f'x: {left_hand_x} y: {left_hand_y}')

            # Check if player is moving
            virtual_controller_object.is_player_get_moving(frame)


        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    virtual_controller_object.cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
	run()