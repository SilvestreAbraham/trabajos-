from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
import os
import datetime
import random

app = Flask(__name__)

path = 'alumnos'
images = []
names = []
colores = {}

if not os.path.exists("Asistencia.csv"):
    with open("Asistencia.csv", "w") as f:
        f.write("Nombre,Fecha,Hora\n")

for file in os.listdir(path):
    img = cv2.imread(f"{path}/{file}")
    if img is not None:
        images.append(face_recognition.face_encodings(face_recognition.load_image_file(f"{path}/{file}"))[0])
        name = os.path.splitext(file)[0].upper()
        names.append(name)
        colores[name] = tuple(random.randint(50, 255) for _ in range(3))


def registrar_asistencia(nombre):
    now = datetime.datetime.now()
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")
    registro = f"{nombre},{fecha},{hora}\n"

    if not os.path.exists("Asistencia.csv"):
        with open("Asistencia.csv", "w") as f:
            f.write("Nombre,Fecha,Hora\n")

    with open("Asistencia.csv", "r+") as h:
        contenido = f.read()
        if nombre not in contenido:
            f.write(registro)
            print(f"{nombre} - {fecha} - {hora}")


def gen():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces_loc = face_recognition.face_locations(rgb)
        faces_enc = face_recognition.face_encodings(rgb, faces_loc)

        for enc, loc in zip(faces_enc, faces_loc):
            distancias = face_recognition.face_distance(images, enc)
            min_index = np.argmin(distancias)

            if distancias[min_index] < 0.5:
                nombre = names[min_index]
                registrar_asistencia(nombre)

                yi, xf, yf, xi = loc
                centro_x = (xi + xf) // 2
                centro_y = (yi + yf) // 2
                radio = int(max(xf - xi, yf - yi) * 0.65)

                color = colores[nombre]
                cv2.circle(frame, (centro_x, centro_y), radio, color, 3)
                cv2.putText(frame, nombre, (centro_x - 50, centro_y + radio + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


#Running on http://127.0.0.1:5000
