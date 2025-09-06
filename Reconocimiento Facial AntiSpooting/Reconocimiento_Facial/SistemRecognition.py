import cv2
import face_recognition as fr
import numpy as np
import mediapipe as mp
import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import imutils
import math
import csv
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure, ConnectionFailure

# Configuración mejorada de MongoDB
MONGO_URI = "mongodb+srv://uconfortasist:Udl8Q0APE93vt3BB@cluster0.g6qne.mongodb.net/UConfortAsist?retryWrites=true&w=majority"
DATABASE_NAME = "UConfortAsist"
COLLECTION_NAME = "asistencias"

mpDraw = mp.solutions.drawing_utils
ConfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1)
FacemeshObject = mp.solutions.face_mesh
FaceMesh = FacemeshObject.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)
FaceObject = mp.solutions.face_detection
detector = FaceObject.FaceDetection(min_detection_confidence=0.6, model_selection=1)


# Función para conectar a MongoDB
def conectar_mongo():
    try:
        cliente = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            socketTimeoutMS=30000,
            connectTimeoutMS=30000
        )

        # Verificación activa de la conexión
        cliente.admin.command('ping')
        print("✓ Conexión a MongoDB establecida correctamente")

        db = cliente[DATABASE_NAME]
        return db[COLLECTION_NAME]

    except ServerSelectionTimeoutError:
        messagebox.showerror("Error MongoDB", "Tiempo de espera agotado al conectar")
        return None
    except OperationFailure as err:
        messagebox.showerror("Error MongoDB", f"Error de autenticación: {err}")
        return None
    except Exception as e:
        messagebox.showerror("Error MongoDB", f"Error de conexión: {str(e)[:100]}")
        return None


# Función para enviar un CSV a MongoDB
def insertar_en_mongo(matricula, grupo, ciclo_escolar):
    try:
        # Crear el documento con la estructura exacta solicitada
        documento = {
            "matricula": matricula,
            "grupo": grupo,
            "ciclo_escolar": ciclo_escolar,
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "tipo_asistencia": "normal"
        }

        # Conectar a MongoDB
        collection = conectar_mongo()
        if collection is None:
            return False

        # Insertar documento
        resultado = collection.insert_one(documento)

        if resultado.inserted_id:
            print(f"✓ Documento insertado con ID: {resultado.inserted_id}")
            # Verificación adicional
            doc_insertado = collection.find_one({"_id": resultado.inserted_id})
            if doc_insertado:
                print("✓ Verificación exitosa - Documento encontrado:")
                print(doc_insertado)
                return True
        return False

    except Exception as e:
        print(f"✗ Error al insertar: {e}")
        return False


# Función para guardar datos en CSV
def save_to_csv(nombre, matricula, grupo, ciclo, filename):
    data = {
        "Nombre": [nombre.upper()],
        "Matricula": [matricula.upper()],
        "Grupo": [grupo.upper()],
        "Ciclo": [ciclo.upper()]
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


# Función para guardar datos en CSV y MongoDB
def save_data(nombre, matricula, grupo, ciclo):
    # Guardar en CSV (manteniendo el formato original)
    filename = f"{OutFolderPathUser}/{matricula}.csv"
    save_to_csv(nombre, matricula, grupo, ciclo, filename)  # Esta función puede mantenerse igual

    # Enviar a MongoDB con el nuevo formato
    if insertar_en_mongo(matricula, grupo, ciclo):
        print("Datos guardados en CSV y MongoDB correctamente")
    else:
        print("Datos guardados solo en CSV (fallo MongoDB)")


# Función para profile
def Profile():
    global step, conteo, UserName, OutFolderPathUser

    # Reset Variables
    conteo = 0
    step = 0

    # Crear la ventana de perfil
    pantalla4 = Toplevel(pantalla)
    pantalla4.title("PROFILE")
    pantalla4.geometry("1280x720")

    # Fondo de la ventana
    bc = Label(pantalla4, image=imagenbc, text="Nuevo")
    bc.place(x=0, y=0, relheight=1, relwidth=1)

    # Ruta del archivo CSV
    csv_filename = f"{OutFolderPathUser}/{UserName}.csv"
    img_path = f"{OutFolderPathFace}/{UserName}.png"

    # Frame para mensajes de MongoDB
    mongo_frame = Frame(pantalla4, bg="#f5f5f5", bd=1, relief=SOLID, highlightbackground="#4a6baf",
                        highlightthickness=1)
    mongo_frame.place(x=400, y=620, width=480, height=50)

    # Verificar si el archivo CSV existe
    if os.path.isfile(csv_filename):
        try:
            # Leer datos del CSV
            with open(csv_filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Saltar encabezados
                InfoUser = next(reader)  # Leer datos

                if len(InfoUser) >= 4:
                    nombre = InfoUser[0]
                    matricula = InfoUser[1]
                    grupo = InfoUser[2]
                    ciclo = InfoUser[3]

                    # Mostrar datos en la ventana (sin cambios)
                    texto1 = Label(pantalla4, text=f"BIENVENIDO {nombre}", font=("Arial", 18, "bold"), bg="#f8f9fa",
                                   fg="#2c3e50")
                    texto1.place(x=500, y=50)

                    texto2 = Label(pantalla4, text=f"Matrícula: {matricula}", font=("Arial", 14), bg="#f8f9fa",
                                   fg="#34495e")
                    texto2.place(x=500, y=100)

                    texto3 = Label(pantalla4, text=f"Grupo: {grupo}", font=("Arial", 14), bg="#f8f9fa", fg="#34495e")
                    texto3.place(x=500, y=150)

                    texto4 = Label(pantalla4, text=f"Ciclo Escolar: {ciclo}", font=("Arial", 14), bg="#f8f9fa",
                                   fg="#34495e")
                    texto4.place(x=500, y=200)

                    # Mostrar la imagen del usuario (sin cambios)
                    lblimage = Label(pantalla4, bg="#ecf0f1", bd=2, relief=SOLID, highlightbackground="#4a6baf",
                                     highlightthickness=2)
                    lblimage.place(x=490, y=250, width=300, height=300)

                    if os.path.isfile(img_path):
                        try:
                            ImgUser = cv2.imread(img_path)
                            if ImgUser is not None:
                                ImgUser = cv2.cvtColor(ImgUser, cv2.COLOR_BGR2RGB)
                                ImgUser = cv2.resize(ImgUser, (300, 300))
                                ImgUser = Image.fromarray(ImgUser)
                                IMG = ImageTk.PhotoImage(image=ImgUser)
                                lblimage.configure(image=IMG)
                                lblimage.image = IMG
                            else:
                                messagebox.showerror("Error", "No se pudo cargar la imagen del usuario.")
                        except Exception as e:
                            messagebox.showerror("Error", f"Error al procesar imagen: {str(e)}")
                    else:
                        messagebox.showerror("Error", f"No se encontró la imagen del usuario en: {img_path}")

                    # Intento de conexión a MongoDB con los nuevos parámetros
                    try:
                        # Mostrar estado de conexión
                        lbl_loading = Label(mongo_frame, text="Conectando a MongoDB...", font=("Arial", 12),
                                            bg="#f5f5f5", fg="#4a6baf")
                        lbl_loading.pack(pady=10)
                        pantalla4.update()

                        # Insertar en MongoDB solo los campos requeridos
                        if insertar_en_mongo(matricula, grupo, ciclo):
                            lbl_loading.destroy()
                            lbl_success = Label(mongo_frame, text="✓ Datos enviados correctamente", font=("Arial", 12),
                                                bg="#e8f5e9", fg="#2e7d32")
                            lbl_success.pack(fill=BOTH, expand=True)
                        else:
                            lbl_loading.destroy()
                            lbl_error = Label(mongo_frame, text="✗ Error al enviar datos", font=("Arial", 12),
                                              bg="#ffebee", fg="#c62828")
                            lbl_error.pack(fill=BOTH, expand=True)

                    except Exception as e:
                        lbl_loading.destroy()
                        lbl_error = Label(mongo_frame, text=f"✗ Error: {str(e)[:30]}...", font=("Arial", 10),
                                          bg="#ffebee", fg="#c62828")
                        lbl_error.pack(fill=BOTH, expand=True)
                        print(f"Error completo en MongoDB: {e}")

                else:
                    messagebox.showerror("Error", "El archivo CSV no tiene el formato correcto.")
        except StopIteration:
            messagebox.showerror("Error", "El archivo CSV está vacío.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo CSV: {e}")
    else:
        messagebox.showerror("Error", f"No se encontró el archivo CSV del usuario en: {csv_filename}")

    # Botón de cerrar
    btn_cerrar = Button(pantalla4, text="CERRAR", font=("Arial", 14, "bold"), command=lambda: Close_Window(pantalla4),
                        bg="#e74c3c", fg="white", width=18, height=1, activebackground="#c0392b", relief=RAISED, bd=3)
    btn_cerrar.place(x=530, y=570)


# Función de close window
def Close_Window(window):
    global step, conteo

    # Reset Variables
    conteo = 0
    step = 0
    window.destroy()
    cap.release()


# Función código de rostros
def Code_Face(images):
    listacod = []

    for img in images:
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Mejoramos la detección con parámetros ajustados
        face_locations = fr.face_locations(img, model="hog")
        face_encodings = fr.face_encodings(img, face_locations, num_jitters=2)

        if len(face_encodings) > 0:
            listacod.append(face_encodings[0])
        else:
            print("No se detectó ningún rostro - Intensificando búsqueda...")
            # Segundo intento con diferentes parámetros
            face_locations = fr.face_locations(img, model="cnn")
            face_encodings = fr.face_encodings(img, face_locations)
            if len(face_encodings) > 0:
                listacod.append(face_encodings[0])

    return listacod


# login biometric funcion
def Log_Biometric():
    global pantalla2, conteo, parpadeo, img_info, step, lblVideo, RegUser, FaceCode, cap

    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        frame = imutils.resize(frame, width=1280)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameSave = frameRGB.copy()

        # Si es correcta
        if ret == True:
            # Inference
            res = FaceMesh.process(frameRGB)

            # List Results
            px = []
            py = []
            lista = []
            r = 5
            t = 3

            # Resultados
            if res.multi_face_landmarks:
                # Iteramos
                for rostros in res.multi_face_landmarks:

                    # Draw Face Mesh
                    mpDraw.draw_landmarks(frame, rostros, mp.solutions.face_mesh.FACEMESH_TESSELATION, ConfigDraw, ConfigDraw)

                    # Extract KeyPoints
                    for id, puntos in enumerate(rostros.landmark):

                        # Info IMG
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])

                        # 468 KeyPoints
                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            longitud1 = math.hypot(x2 - x1, y2 - y1)

                            # Ojo Izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            longitud2 = math.hypot(x4 - x3, y4 - y3)

                            # Parietal Derecho
                            x5, y5 = lista[139][1:]
                            # Parietal Izquierdo
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha
                            x7, y7 = lista[70][1:]
                            # Ceja Izquierda
                            x8, y8 = lista[300][1:]

                            # Face Detect
                            faces = detector.process(frameRGB)

                            if faces.detections is not None:
                                for face in faces.detections:

                                    # bboxInfo - "id","bbox","score","center"
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if score > confThreshold:
                                        # Coordenates
                                        xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, anc, alt = int(xi * an), int(yi * al), int(anc * an), int(alt * al)

                                        # Width
                                        offsetan = (offsetx / 100) * an
                                        xi = int(xi - int(offsetan / 2))
                                        anc = int(anc + offsetan)
                                        xf = xi + anc

                                        # Height
                                        offsetal = (offsety / 100) * al
                                        yi = int(yi - offsetal)
                                        alt = int(alt + offsetal)
                                        yf = yi + alt

                                        # Error < 0
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if anc < 0: anc = 0
                                        if alt < 0: alt = 0

                                        # Steps
                                        if step == 0:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, anc, alt), (255, 0, 255), 2)
                                            # IMG Step0
                                            als0, ans0, c = img_step0.shape
                                            frame[50:50 + als0, 50:50 + ans0] = img_step0

                                            # IMG Step1
                                            als1, ans1, c = img_step1.shape
                                            frame[50:50 + als1, 1030:1030 + ans1] = img_step1

                                            # IMG Step2
                                            als2, ans2, c = img_step2.shape
                                            frame[270:270 + als2, 1030:1030 + ans2] = img_step2

                                            # Condiciones
                                            if x7 > x5 and x8 < x6:
                                                alch, anch, c = img_check.shape
                                                frame[165:165 + alch, 1105:1105 + anch] = img_check

                                                # Cont Parpadeos
                                                if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:
                                                    conteo = conteo + 1
                                                    parpadeo = True

                                                elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:
                                                    parpadeo = False

                                                # Parpadeos
                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070, 375),
                                                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                                                if conteo >= 3:
                                                    # IMG check
                                                    alch, anch, c = img_check.shape
                                                    frame[385:385 + alch, 1105:1105 + anch] = img_check

                                                    # Ojos abiertos
                                                    if longitud1 > 15 and longitud2 > 15:
                                                        # Cut
                                                        cut = frameSave[yi:yf, xi:xf]
                                                        # Save Image Without Draw
                                                        cv2.imwrite(f"{OutFolderPathFace}/{RegUser}.png", cut)

                                                        step = 1
                                            else:
                                                conteo = 0

                                        if step == 1:
                                            cv2.rectangle(frame, (xi, yi, anc, alt), (0, 255, 0), 2)

                                            alli, anli, c = img_liche.shape
                                            frame[50:50 + alli, 50:50 + anli] = img_liche
                                            Close_Window(pantalla2)
                                            pantalla.mainloop()
                                            break

                                    # circulo
                            cv2.circle(frame, (x7, y7), 2, (255, 0, 0), cv2.FILLED)
                            cv2.circle(frame, (x8, y8), 2, (255, 0, 0), cv2.FILLED)

            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, Log_Biometric)

        else:
            cap.release()
            Close_Window(pantalla2)
            cap = None


def Sign_Biometric():
    global LogUser, LogPass, OutFolderPath, cap, lblVideo, pantalla3, FaceCode, clases, images, pantalla2, step, parpadeo, conteo, UserName, RegUser

    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        frame = imutils.resize(frame, width=1280)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frameSave = frameRGB.copy()

        # Si es correcta
        if ret == True:
            # Inference
            res = FaceMesh.process(frameRGB)

            # List Results
            px = []
            py = []
            lista = []
            r = 5
            t = 3

            # Resultados
            if res.multi_face_landmarks:
                # repetimos
                for rostros in res.multi_face_landmarks:
                    # Draw Face Mesh
                    mpDraw.draw_landmarks(frame, rostros, mp.solutions.face_mesh.FACEMESH_TESSELATION, ConfigDraw,
                                          ConfigDraw)

                    # Extract KeyPoints
                    for id, puntos in enumerate(rostros.landmark):

                        # Info IMG
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])

                        # 468 KeyPoints
                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            longitud1 = math.hypot(x2 - x1, y2 - y1)

                            # Ojo Izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            longitud2 = math.hypot(x4 - x3, y4 - y3)

                            # Parietal Derecho y izquierdo
                            x5, y5 = lista[139][1:]
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha y izquierda
                            x7, y7 = lista[70][1:]
                            x8, y8 = lista[300][1:]

                            # Face Detect
                            faces = detector.process(frameRGB)

                            if faces.detections is not None:
                                for face in faces.detections:

                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if score > confThreshold:
                                        # Coordenates
                                        xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, anc, alt = int(xi * an), int(yi * al), int(anc * an), int(alt * al)

                                        # Width
                                        offsetan = (offsetx / 100) * an
                                        xi = int(xi - int(offsetan / 2))
                                        anc = int(anc + offsetan)
                                        xf = xi + anc

                                        # Height
                                        offsetal = (offsety / 100) * al
                                        yi = int(yi - offsetal)
                                        alt = int(alt + offsetal)
                                        yf = yi + alt

                                        # Error < 0
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if anc < 0: anc = 0
                                        if alt < 0: alt = 0

                                        # Steps
                                        if step == 0:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, anc, alt), (255, 0, 255), 2)
                                            # IMG Step0
                                            als0, ans0, c = img_step0.shape
                                            frame[50:50 + als0, 50:50 + ans0] = img_step0

                                            # IMG Step1
                                            als1, ans1, c = img_step1.shape
                                            frame[50:50 + als1, 1030:1030 + ans1] = img_step1

                                            # IMG Step2
                                            als2, ans2, c = img_step2.shape
                                            frame[270:270 + als2, 1030:1030 + ans2] = img_step2

                                            # Condiciones
                                            if x7 > x5 and x8 < x6:
                                                alch, anch, c = img_check.shape
                                                frame[165:165 + alch, 1105:1105 + anch] = img_check

                                                # Cont Parpadeos
                                                if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:
                                                    conteo = conteo + 1
                                                    parpadeo = True

                                                elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:
                                                    parpadeo = False

                                                # Parpadeos
                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070, 375),
                                                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                                                if conteo >= 3:
                                                    # IMG check
                                                    alch, anch, c = img_check.shape
                                                    frame[385:385 + alch, 1105:1105 + anch] = img_check

                                                    # Ojos abiertos
                                                    if longitud1 > 15 and longitud2 > 15:
                                                        step = 1

                                            else:
                                                conteo = 0

                                        if step == 1:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, anc, alt), (0, 255, 0), 2)
                                            # IMG check Liveness
                                            alli, anli, c = img_liche.shape
                                            frame[50:50 + alli, 50:50 + anli] = img_liche

                                            try:
                                                faces = fr.face_locations(frameRGB)
                                                facescod = fr.face_encodings(frameRGB, faces)

                                                if len(facescod) == 0:
                                                    # Mensaje de error en la interfaz
                                                    error_frame = Frame(pantalla3, bg="#FFEBEE", bd=2, relief=SOLID, highlightbackground="#C62828", highlightthickness=2)
                                                    error_frame.place(x=400, y=620, width=480, height=60)
                                                    Label(error_frame, text=" NO SE DETECTO NINGUN ROSTRO", font=("Arial", 14, "bold"), bg="#FFEBEE", fg="#C62828").pack(pady=10)
                                                    pantalla3.after(3000, error_frame.destroy)
                                                    step = 0
                                                    conteo = 0
                                                    continue

                                                for facecod, faceloc in zip(facescod, faces):
                                                    Match = fr.compare_faces(FaceCode, facecod)
                                                    simi = fr.face_distance(FaceCode, facecod)
                                                    min = np.argmin(simi)

                                                    if Match[min]:
                                                        UserName = clases[min].upper()
                                                        Profile()
                                                        Close_Window(pantalla3)
                                                        pantalla.mainloop()
                                                        break
                                                    else:
                                                        # Mensaje de rostro no reconocido
                                                        error_frame = Frame(pantalla3, bg="#FFEBEE", bd=2, relief=SOLID, highlightbackground="#C62828", highlightthickness=2)
                                                        error_frame.place(x=400, y=620, width=480, height=60)
                                                        Label(error_frame, text="✗ ROSTRO NO REGISTRADO", font=("Arial", 14, "bold"), bg="#FFEBEE", fg="#C62828").pack(pady=10)
                                                        pantalla3.after(3000, error_frame.destroy)
                                                        step = 0
                                                        conteo = 0
                                                        continue

                                            except Exception as e:
                                                print(f"Error en reconocimiento: {str(e)}")
                                                # Mensaje de error genérico
                                                error_frame = Frame(pantalla3, bg="#FFEBEE", bd=2, relief=SOLID, highlightbackground="#C62828", highlightthickness=2)
                                                error_frame.place(x=300, y=620, width=680, height=80)
                                                Label(error_frame, text=" ERROR DE RECONOCIMIENTO:\nNO SE ENCONTRARON COINCIDENCIAS O ALUMNO NO REGISTRADO", font=("Arial", 12, "bold"), bg="#FFEBEE", fg="#C62828", wraplength=650, justify="center").pack(pady=12)

                                                pantalla3.after(3000, lambda: [error_frame.destroy(), pantalla3.destroy(), cap.release()])
                                                step = 0
                                                conteo = 0

                            # Circulos en cejas
                            cv2.circle(frame, (x7, y7), 2, (255, 0, 0), cv2.FILLED)
                            cv2.circle(frame, (x8, y8), 2, (255, 0, 0), cv2.FILLED)

            # Convertir la imagen y actualizar
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, Sign_Biometric)

        else:
            if cap is not None:
                cap.release()
            pantalla3.destroy()


# funcion Sign
def Sign():
    global LogUser, LogPass, OutFolderPath, cap, lblVideo, pantalla3, FaceCode, clases, images, parpadeo, conteo, step

    # DB Faces
    images = []
    clases = []
    lista = os.listdir(OutFolderPathFace)

    for lis in lista:
        imgdb = cv2.imread(f'{OutFolderPathFace}/{lis}')
        images.append(imgdb)
        clases.append(os.path.splitext(lis)[0])

    # Face Code
    FaceCode = Code_Face(images)

    # 3° Ventana
    pantalla3 = Toplevel(pantalla)
    pantalla3.title("LOGIN BIOMETRIC")
    pantalla3.geometry("1280x720")

    # Video
    lblVideo = Label(pantalla3)
    lblVideo.place(x=0, y=0)

    # Elegimos la cámara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)
    parpadeo = False
    conteo = 0
    step = 0
    Sign_Biometric()


# funcion Login
def Log():
    global RegName, RegUser, RegPass, RegCiclo, InputNameReg, InputUserReg, InputPassReg, InputCicloReg, cap, lblVideo, pantalla2, parpadeo, conteo, step

    # Obtenemos los valores y los convertimos a mayúsculas
    RegName = InputNameReg.get().strip()  # .strip() para eliminar espacios en blanco
    RegUser = InputUserReg.get().strip()
    RegPass = InputPassReg.get().strip()
    RegCiclo = InputCicloReg.get().strip()

    if len(RegName) == 0 or len(RegUser) == 0 or len(RegPass) == 0 or len(RegCiclo) == 0:
        # Info incompleta
        print(" FORMULARIO INCOMPLETO ")
        messagebox.showerror("Error", "Por favor, complete todos los campos.")
    else:
        # Checka usuario
        UserList = os.listdir(PathUserCheck)

        # Nombre se usuario
        UserName = []

        for lis in UserList:
            # Extrae usuario
            User = lis
            User = User.split('.')

            # guardar
            UserName.append(User[0])

        # Checa nombre (comparando en mayúsculas para evitar duplicados)
        if RegUser.upper() in [user.upper() for user in UserName]:
            # Registred
            print("USUARIO REGISTRADO ANTERIORMENTE")
            messagebox.showerror("Error", "El usuario ya está registrado.")
        else:
            # No Registrado - Guardamos los datos convertidos a mayúsculas
            save_data(RegName, RegUser, RegPass, RegCiclo)

            # Clean
            InputNameReg.delete(0, END)
            InputUserReg.delete(0, END)
            InputPassReg.delete(0, END)
            InputCicloReg.delete(0, END)

            # Ventana principal
            pantalla2 = Toplevel(pantalla)
            pantalla2.title("SIGN UP BIOMETRIC")
            pantalla2.geometry("1280x720")

            # Video
            lblVideo = Label(pantalla2)
            lblVideo.place(x=0, y=0)

            # Elegimos la camara
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(3, 1280)
            cap.set(4, 720)
            parpadeo = False
            conteo = 0
            step = 0
            Log_Biometric()


# path
OutFolderPathUser = 'DataBase/Users'
PathUserCheck = 'DataBase/Users'
OutFolderPathFace = 'DataBase/Faces'

# leer imagenes (read img)
img_check = cv2.imread('SetUp/check.png')
img_check = cv2.cvtColor(img_check, cv2.COLOR_BGR2RGB)
img_step0 = cv2.imread('SetUp/Step0.png')
img_step0 = cv2.cvtColor(img_step0, cv2.COLOR_BGR2RGB)
img_step1 = cv2.imread('SetUp/Step1.png')
img_step1 = cv2.cvtColor(img_step1, cv2.COLOR_BGR2RGB)
img_step2 = cv2.imread('SetUp/Step2.png')
img_step2 = cv2.cvtColor(img_step2, cv2.COLOR_BGR2RGB)
img_liche = cv2.imread('SetUp/LivenessCheck.png')
img_liche = cv2.cvtColor(img_liche, cv2.COLOR_BGR2RGB)

# info list
info = []

# variables
parpadeo = False
conteo = 0
muestra = 0
step = 0

# offset's
offsety = 15
offsetx = 10

# umbral de deteccion (Threshold)
confThreshold = 0.6
blurThreshold = 15

# herramienta de dibujo (tool draw)
mpDraw = mp.solutions.drawing_utils
ConfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

# para la maya del rostro
FacemeshObject = mp.solutions.face_mesh
FaceMesh = FacemeshObject.FaceMesh(max_num_faces=1)

# detector de rostros
FaceObject = mp.solutions.face_detection
detector = FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)

# ventana principal
pantalla = Tk()
pantalla.title("RECONOCIMIENTO FACIAL SYSTEM")
pantalla.geometry("1280x720")

# fondo
imagenF = PhotoImage(file='./SetUp/Inicio.png')
background = Label(image=imagenF, text="Inicio")
background.place(x=0, y=0, relheight=1, relwidth=1)

# fondo 2
imagenbc = PhotoImage(file='./SetUp/Back2.png')

# Entrada de texto registro con nombre
InputNameReg = Entry(pantalla)
InputNameReg.place(x=110, y=260)

# Usuario
InputUserReg = Entry(pantalla)
InputUserReg.place(x=110, y=370)

# Contraseña
InputPassReg = Entry(pantalla)
InputPassReg.place(x=110, y=480)

# Ciclo Escolar
InputCicloReg = Entry(pantalla)
InputCicloReg.place(x=110, y=590)

# botones
# botton sign
imagenBR = PhotoImage(file='./SetUp/BtSing.png')
BtReg = Button(pantalla, text="Registro", image=imagenBR, height="40", width="200", command=Log)
BtReg.place(x=400, y=580)

# botton login
imagenBL = PhotoImage(file='./SetUp/BtLogin.png')
BtSign = Button(pantalla, text="Inicio", image=imagenBL, height="40", width="200", command=Sign)
BtSign.place(x=900, y=580)

pantalla.mainloop()