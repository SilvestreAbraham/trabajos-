import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0) 

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

cv2.namedWindow('Pose Detection with Square', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Pose Detection with Square', WINDOW_WIDTH, WINDOW_HEIGHT)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_resized = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT), interpolation=cv2.INTER_LINEAR)
    
    rgb_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    
    results = pose.process(rgb_frame)
    
    if results.pose_landmarks:
        
        mp_drawing.draw_landmarks(frame_resized, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        landmarks = results.pose_landmarks.landmark
        h, w, _ = frame_resized.shape
        
        xs = [landmark.x for landmark in landmarks if landmark.visibility > 0.5]
        ys = [landmark.y for landmark in landmarks if landmark.visibility > 0.5]
        
        if xs and ys:  
            min_x, max_x = int(min(xs) * w), int(max(xs) * w)
            min_y, max_y = int(min(ys) * h), int(max(ys) * h)
            
            cv2.rectangle(frame_resized, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)
    
    cv2.imshow('Pose Detection with Square', frame_resized)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()