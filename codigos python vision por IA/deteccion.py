import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    results = model(frame, stream=True)  

    for r in results:
        
        for box in r.boxes:
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = f"{model.names[cls_id]} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("YOLOv8 - Detección de Objetos", frame)

    if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
        break

cap.release()
cv2.destroyAllWindows()