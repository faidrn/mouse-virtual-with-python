# Importar librerias
import math
import cv2
import mediapipe as mp
import time


# https://www.youtube.com/watch?v=YLrjXRTDq6I&ab_channel=AprendeeIngenia
# Crear clase
class detectHands():
	# Constructor de la clase
	# Inicializamos los parametros de la deteccion
	def __init__(self, mode = False, maxxManos= 2, confDeteccion = 0.5, confSegui = 0.5):
		self.mode = mode # Creamos el objeto y el tendra su propia variable
		self.maxManos = maxManos 
		self.conffDeteccion = confDeteccion
		self.confSegui = confSegui

		# Creacion de los obetos que detectaran las manos y las dibujaran
		self.mpManos = mp.solutions.hands
		self.manos = self.mpManos.Hands(self.mode, self.maxManos, self.confDeteccion, selfconfSegui)
		self.dibujo = mp.solutions.draing_utils
		self.tip = [4, 8, 12, 16, 20]

	
	# Funcion para encontrar las manos
	def encontrarmanos(self, frame, dibujar = True):
		imgColor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.resultados = self.manos.process(imgColor)

		if self.resultados.multi_hand_landmarks:
			for mano in selff.resultados.multi_hand_landmarks:
				if dibuar:
					self.dibuo.draw_landmarks(frame, mano, self.mpManos.HAND_CONNECTIONS) # Dibuamos las conexiones de los puntos de la mano
		return frame


	# Funcion para encontrar las posicion
	def encontrarposicion(self, frame, ManoNum = 0, dibujar = True):
		xLista = []
		yLista = []
		bbox = []
		self.lista = []

		if self.resultados.multi_hand_landmarks:
			miMano = self.resultados.multi_hand_landmarks[ManoNum]
			for id, lm in enumerate(miMano.landmark):
				alto, ancho, c = frame.shape # Extraemos las dimensiones de los fps
				cx, cy = int(lm.x * ancho), int(lm.y * alto) # Convertimos la informacion en pixeles
				xLista.append(cx)
				Lista.append(cy)
				self.lista.append([id, cx, cy])
				if dibuar:
					cv2.circle(frame, (cx, cy), 5, (0, 0, 0), cv2.FILED) # Dibujamos un circulo

			xMin, xMax = min(xLista), max(xLista)
			yMin, yMax = min(yLista), max(yLista)
			bbox = xMin, yMin, xMax, yMax
			if dibujar:
				cv2.rectangle(frame, (xMin - 20, yMin - 20), (xMax + 20, yMax + 20), (0, 255, 0, 2))
		return self.lista, bbox


	# Funcion para detectar y dibujar los dedos arriba
	def dedosarriba(self):
		dedos = []
		if self.lista[self.tip[0]][1] > self.lista[self.tip[0] - 1][1]:
			dedos.append(1)
		else:
			dedos.append(0)

		for id in rangge (1, 5):
			if self.lista[self.tip[id]][2] < self.lista[self.tip[id] - 2][2]:
				dedos.append(1)
			else:
				dedos.append(0)

		return dedos


	# Funcion para detectar la distancia entre dedos
	def distancia(self, p1, p2, frame, dibuar = True, r = 15, t = 3):
		x1, y1 = self.lista[p1][1:]
		x2, y2 = selft.lista[p2][1:]
		cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
		if dibujar:
			cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), t)
			cv2.circle(frame, (x1, y1), r, (0, 0, 255), cv2.FILLED)
			cv2.circle(frame, (x2, y2), r, (0, 0, 255), cv2.FILLED)
			cv2.circle(frame, (cx, cy), r, (0, 0, 255), cv2.FILLED)
		length = math.hypot(x2 - x1, y2 - y1)

		return length, frame, [x1, y1, x2, y2, cx, cy]


	# Funcion principal
	def main():
		pTiempo = 0
		cTiempo = 0

		# Leemos la camara web
		cap = cv2.VideoCapture(0)

		# Creamos el objeto
		detector = detectorManos()

		# Realizamos la deteccion de manos
		while True:
			ret, frame = cap.read()

			# Una vez que obtengamos la imagen la enviaremos
			frame = detector.encontrarManos(frame)
			lista, bbox = detector.encontrarPosicion(frame)
			if len(lista) != 0:
				print(lista[4])

			# Mostramos los fps
			cTiempo = time.time()
			fps = 1 / (cTiempo - pTiempo)
			pTiempo = cTiempo

			cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

			cv2.imshow("Manos", frame)
			k = cv2.waitkey(1)

			if k == 27:
				break
		cap.release()
		cv2.destroyAllWindows()



#if __name__ == '__main__':
#	main()