"""
Class to make motion detection
"""

# Frameworks
# import numpy as np
import cv2


class MotionDetection():
    

    def get_motion(self):
        # Capturar video
        cap = cv2.VideoCapture(1)

        # Call motion detector
        # history: tamaño del historico
        # dist2Threshold: umbral de la distancia al cuadrado entre el pixel y la muestra para decidir si un pixel esta cerca de esa muestra
        # detectShadows: con un valor verdadero detecta las sombras

        mov = cv2.createBackgroundSubtractorKNN(history = 500, dist2Threshold = 400, detectShadows = False)

        # To disable OpenCL
        cv2.ocl.setUseOpenCL(False)

        while (True):
            ret, frame = cap.read()

            # If video is not read Ok, to close (exit)
            if not ret:
                break

            # Apply the detector
            mascara = mov.apply(frame)

            # Make a copy to detect the contourns
            contornos = mascara.copy()

            # Looking for contourns
            con, jerarquia = cv2.findContours(contornos, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # To pass by the contourns
            for c in con:
                # Delete noise
                if cv2.contourArea(c) < 2500: # si el movimiento es menor a 1500px no se detecta (ejemplo mosca)
                    continue

                if cv2.contourArea(c) >= 2500:
                    # Get the limits of the contourn 
                    (x, y, w, h) = cv2.boundingRect(c)

                    # Drawing the rectangle
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, '()'.format('Movimiento'), (x, y - 5), 1, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
                    # aqui llama la alarma

            # Show the cam, mask and contourns
            cv2.imshow('Alarma inactiva', frame)
            cv2.imshow('Umbral', mascara)
            cv2.imshow('Contornos', contornos)

            k = cv2.waitKey(5)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


def run():
    motion_detector = MotionDetection()
    motion_detector.get_motion()


if __name__ == '__main__':
    run()