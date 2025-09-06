import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

cv2.namedWindow('Detección de manos', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Detección de manos', WINDOW_WIDTH, WINDOW_HEIGHT)

def detect_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    thumb_y = thumb_tip.y
    index_y = index_tip.y
    middle_y = middle_tip.y
    ring_y = ring_tip.y
    pinky_y = pinky_tip.y

    # Amor y Paz (dedos índice y dedo medio levantados, todos los demas doblados)
    if (index_y < middle_y and middle_y < ring_y and middle_y < pinky_y and ring_y > pinky_y):      
        return "Amor y Paz"

    # Puño cerrado (todos los dedos doblados)
    if (index_y > middle_y and middle_y > ring_y and ring_y > pinky_y):      
        return "Puño cerrado"

    # Pulgar arriba
    if thumb_y < index_y and thumb_y < middle_y and thumb_y < ring_y and thumb_y < pinky_y:
        return "Pulgar arriba"

    # Pulgar abajo
    if thumb_y > index_y and thumb_y > middle_y and thumb_y > ring_y and thumb_y > pinky_y:
        return "Pulgar abajo"

    # Mano abierta
    if (index_y < middle_y and middle_y < ring_y and ring_y < pinky_y):
        return "Mano abierta"

    # OK (dedos índice y pulgar formando un círculo)
    thumb_index_distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
    if thumb_index_distance < 0.05:  
        return "OK"

    return "Desconocido"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo capturar el video")
        break

    frame_resized = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))

    rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            
            # Dibuja los landmarks y conexiones de la mano
            mp_drawing.draw_landmarks(
                frame_resized, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            # Detecta gesto
            gesture = detect_gesture(hand_landmarks)
            print(f"Gesto detectado: {gesture}")

    cv2.imshow('Detección de manos', frame_resized)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
