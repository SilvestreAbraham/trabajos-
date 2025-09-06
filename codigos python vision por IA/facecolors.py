import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

WHITE = (255, 255, 255)  

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

cv2.namedWindow('Malla Facial', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Malla Facial', WINDOW_WIDTH, WINDOW_HEIGHT)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image_resized = cv2.resize(image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results = face_mesh.process(image_rgb)
    image_rgb.flags.writeable = True
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            
            mp_drawing.draw_landmarks(
                image=image_bgr,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(
                    color=WHITE, thickness=1, circle_radius=1))

            landmarks = face_landmarks.landmark
            img_h, img_w, _ = image_bgr.shape

            min_x = min(lm.x for lm in landmarks)
            max_x = max(lm.x for lm in landmarks)
            min_y = min(lm.y for lm in landmarks)
            max_y = max(lm.y for lm in landmarks)

            center_x = int((min_x + max_x) * img_w / 2)
            center_y = int((min_y + max_y) * img_h / 2)
            radius = int(max(max_x - min_x, max_y - min_y) * img_w / 2 * 0.8)

            width = int((max_x - min_x) * img_w)
            height = int((max_y - min_y) * img_h)
            aspect_ratio = width / height if height != 0 else 0

            left_eye_idx = 33  
            right_eye_idx = 263  

            left_eye = landmarks[left_eye_idx]
            right_eye = landmarks[right_eye_idx]

            left_eye_point = np.array([left_eye.x * img_w, left_eye.y * img_h])
            right_eye_point = np.array([right_eye.x * img_w, right_eye.y * img_h])

            eye_distance = np.linalg.norm(left_eye_point - right_eye_point)

            print(f"\nMetricas del rostro detectado ")
            print(f"Centro: ({center_x}, {center_y})")
            print(f"Radio aproximado: {radius}")
            print(f"Ancho del rostro: {width} px")
            print(f"Alto del rostro: {height} px")
            print(f"Relación ancho/alto: {aspect_ratio:.2f}")
            print(f"Distancia entre ojos: {eye_distance:.2f} px")

    cv2.imshow('Malla Facial', image_bgr)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()