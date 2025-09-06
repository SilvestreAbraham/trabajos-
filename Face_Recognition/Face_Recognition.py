import tkinter as tk
from tkinter import messagebox
import cv2
import os
import csv
from datetime import datetime, timedelta
import face_recognition as fr
import numpy as np
import random
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure, ConnectionFailure

# MongoDB config
MONGO_URI = "mongodb+srv://uconfortasist:Udl8Q0APE93vt3BB@cluster0.g6qne.mongodb.net/UConfortAsist?retryWrites=true&w=majority"
DATABASE_NAME = "UConfortAsist"
COLLECTION_NAME = "asistencias"

# Crear carpetas si no existen
os.makedirs("alumnos", exist_ok=True)
os.makedirs("csv_registros", exist_ok=True)

registro_reciente = {}


def conectar_mongo():
    try:
        cliente = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            socketTimeoutMS=30000,
            connectTimeoutMS=30000
        )
        cliente.admin.command('ping')
        print("✓ Conexion a MongoDB establecida correctamente")
        db = cliente[DATABASE_NAME]
        return db[COLLECTION_NAME]
    except ServerSelectionTimeoutError:
        print("Error: Tiempo de espera agotado al conectar a MongoDB")
        return None
    except OperationFailure as err:
        print(f"Error de autenticacion: {err}")
        return None
    except Exception as e:
        print(f"Error de conexion: {str(e)[:100]}")
        return None


def insertar_asistencia_mongo(matricula, nombre_completo, grupo, ciclo_escolar):
    try:
        documento = {
            "matricula": matricula,
            "nombre_completo": nombre_completo,
            "grupo": grupo,
            "ciclo_escolar": ciclo_escolar,
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "hora": datetime.now().strftime("%H:%M:%S"),
            "tipo_asistencia": "normal"
        }

        collection = conectar_mongo()
        if collection is None:
            return False

        resultado = collection.insert_one(documento)
        if resultado.inserted_id:
            print(f" Asistencia registrada para {nombre_completo} (Matrícula: {matricula})")
            return True
        return False
    except Exception as e:
        print(f" Error al insertar asistencia: {e}")
        return False


def guardar_csv(nombre, apellido_paterno, apellido_materno, contacto, matricula, grupo, ciclo):

    nombre_archivo = f"{apellido_paterno}_{apellido_materno}_{nombre}"
    filename = f"csv_registros/{nombre_archivo}.csv"
    now = datetime.now()

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["matricula", "nombre", "apellido_paterno", "apellido_materno", "grupo", "ciclo_escolar", "contacto", "fecha"])
        writer.writerow(
            [matricula, nombre, apellido_paterno, apellido_materno, grupo, ciclo, contacto, now.strftime('%Y-%m-%d')])

    return filename


def codrostros(images):
    listacod = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cod = fr.face_encodings(img)
        if cod:
            listacod.append(cod[0])
    return listacod


def horario(nombre_completo):
    ahora = datetime.now()

    if nombre_completo in registro_reciente:
        if ahora - registro_reciente[nombre_completo] < timedelta(hours=1):
            print(f"⏱ Registro reciente para {nombre_completo}, ignorado.")
            return

    registro_reciente[nombre_completo] = ahora

    try:
        # Buscar información del alumno en el CSV correspondiente
        csv_path = None
        for archivo in os.listdir("csv_registros"):
            if nombre_completo in archivo:
                csv_path = f"csv_registros/{archivo}"
                break

        if csv_path and os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                reader = csv.DictReader(file)
                alumno_info = next(reader)

                # Enviar a MongoDB solo cuando se toma asistencia
                insertar_asistencia_mongo(
                    matricula=alumno_info.get('matricula', ''),
                    nombre_completo=nombre_completo,
                    grupo=alumno_info.get('grupo', ''),
                    ciclo_escolar=alumno_info.get('ciclo_escolar', '')
                )

        # Guardar el CSV local
        with open('Asistencia.csv', 'a') as h:
            fecha = ahora.strftime('%Y-%m-%d')
            hora = ahora.strftime('%H:%M:%S')
            h.write(f'{nombre_completo},{fecha},{hora}\n')

    except Exception as e:
        print(f" Error en asistencia: {e}")


def registrar_datos():
    nombre = entry_nombre.get().strip().upper()
    apellido_paterno = entry_appat.get().strip().upper()
    apellido_materno = entry_apmat.get().strip().upper()
    matricula = entry_matricula.get().strip().upper()
    grupo = entry_grupo.get().strip().upper()
    ciclo = entry_ciclo.get().strip().upper()
    contacto = entry_contacto.get().strip()

    if not nombre or not apellido_paterno or not apellido_materno or not matricula or not grupo or not ciclo:
        messagebox.showerror("Error", "Por favor, complete todos los campos obligatorios.")
        return

    def tomar_foto(ventana_registro):
        cap = cv2.VideoCapture(0)
        rostro_detectado = False

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = fr.face_locations(frame_rgb)
            codigos = fr.face_encodings(frame_rgb, faces)

            for (top, right, bottom, left), cod in zip(faces, codigos):
                rostro_detectado = True

                ancho = right - left
                alto = bottom - top
                margen_x = int(ancho * 0.25)
                margen_y = int(alto * 0.25)
                left_exp = max(0, left - margen_x)
                top_exp = max(0, top - margen_y)
                right_exp = min(frame.shape[1], right + margen_x)
                bottom_exp = min(frame.shape[0], bottom + margen_y)

                color = (0, 255, 0) if cod is not None else (0, 165, 255)
                cv2.rectangle(frame, (left_exp, top_exp), (right_exp, bottom_exp), color, 3)

            if rostro_detectado:
                cv2.putText(frame, "Presiona ENTER para guardar", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            cv2.imshow("Captura de rostro", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == 13 and rostro_detectado:
                nombre_archivo = f"{apellido_paterno}_{apellido_materno}_{nombre}"
                filename = f"alumnos/{nombre_archivo}.jpg"
                cv2.imwrite(filename, frame)
                guardar_csv(nombre, apellido_paterno, apellido_materno, contacto, matricula, grupo, ciclo)
                messagebox.showinfo("Registro exitoso", f"{nombre} fue registrado correctamente.")
                break

        cap.release()
        cv2.destroyAllWindows()
        ventana_foto.destroy()
        ventana_registro.destroy()

    ventana_foto = tk.Toplevel(root)
    ventana_foto.title("Captura de Foto")
    ventana_foto.geometry("700x500")
    ventana_foto.configure(bg="#ffffff")
    tomar_foto(reg)


def ventana_registro():
    global reg, entry_nombre, entry_appat, entry_apmat, entry_contacto, entry_matricula, entry_grupo, entry_ciclo
    reg = tk.Toplevel(root)
    reg.title("Registrar Nuevo Alumno")
    reg.geometry("700x650+300+50")
    reg.configure(bg="#f5f5f5")

    frame = tk.Frame(reg, bg="#f5f5f5")
    frame.pack(expand=True, padx=20, pady=20)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=3)

    etiquetas = [
        ("Nombre:", 0),
        ("Apellido Paterno:", 1),
        ("Apellido Materno:", 2),
        ("Matrícula:", 3),
        ("Grupo:", 4),
        ("Ciclo Escolar:", 5),
        ("Contacto (Opcional):", 6)
    ]

    entradas = []

    for texto, fila in etiquetas:
        tk.Label(frame, text=texto, font=("Arial", 12), bg="#f5f5f5", fg="#003366", anchor="e").grid(row=fila, column=0, padx=10, pady=10, sticky="e")

        entrada = tk.Entry(frame, font=("Arial", 12), width=30)
        entrada.grid(row=fila, column=1, padx=10, pady=10, sticky="we")
        entradas.append(entrada)

    entry_nombre, entry_appat, entry_apmat, entry_matricula, entry_grupo, entry_ciclo, entry_contacto = entradas

    btn_tomar_foto = tk.Button(frame, text="Tomar Foto", command=registrar_datos, font=("Arial", 14), bg="#4CAF50", fg="white", width=20, height=2)
    btn_tomar_foto.grid(row=7, column=0, columnspan=2, pady=20, padx=10, sticky="s")


def tomar_asistencia():
    path = 'alumnos'
    images = []
    clases = []
    lista = os.listdir(path)

    for lis in lista:
        imgdb = cv2.imread(f'{path}/{lis}')

        if imgdb is not None:
            images.append(imgdb)
            # El nombre del archivo sin extensión es el nombre completo
            clases.append(os.path.splitext(lis)[0])

    rostroscod = codrostros(images)
    cap = cv2.VideoCapture(0)
    comp1 = 100

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame2 = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        faces = fr.face_locations(rgb)
        facescod = fr.face_encodings(rgb, faces)

        for facecode, faceloc in zip(facescod, faces):
            comparacion = fr.compare_faces(rostroscod, facecode)
            simi = fr.face_distance(rostroscod, facecode)
            min = np.argmin(simi)

            if comparacion[min]:
                nombre_completo = clases[min]
                print(f" Reconocido: {nombre_completo}")
                yi, xf, yf, xi = [v * 4 for v in faceloc]
                indice = comparacion.index(True)

                if comp1 != indice:
                    r, g, b = random.randrange(0, 255, 50), random.randrange(0, 255, 50), random.randrange(0, 255, 50)
                    comp1 = indice

                centro_x = (xi + xf) // 2
                centro_y = (yi + yf) // 2
                radio = int(max((xf - xi), (yf - yi)) * 0.70)
                cv2.circle(frame, (centro_x, centro_y), radio, (r, g, b), 3)

                # Mostramos el nombre completo en la pantalla
                texto_x = centro_x - (len(nombre_completo) * 10) // 2
                texto_y = centro_y + radio + 30
                cv2.putText(frame, nombre_completo, (texto_x, texto_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (r, g, b), 2)

                horario(nombre_completo)

        cv2.imshow("Asistencia por Reconocimiento Facial", frame)

        if cv2.waitKey(5) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# Interfaz principal
root = tk.Tk()
root.title("Sistema de Asistencia con Reconocimiento Facial")
root.geometry("700x550+300+100")
root.configure(bg="#e6f2ff")

# Frame principal
main_frame = tk.Frame(root, bg="#e6f2ff")
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

titulo = tk.Label(main_frame, text="SISTEMA DE ASISTENCIA", font=("Arial Black", 20), bg="#e6f2ff", fg="#003366")
titulo.pack(pady=(20, 40))

# Botón para tomar asistencia
btn_asistencia = tk.Button(main_frame, text="Tomar Asistencia", font=("Arial", 14), width=25, height=2, bg="#ff5733", fg="white", command=tomar_asistencia)
btn_asistencia.pack(pady=20)

# Botón para registrar alumno
btn_registrar = tk.Button(main_frame, text="Registrar Alumno", font=("Arial", 14), width=25, height=2, bg="#0066cc", fg="white", command=ventana_registro)
btn_registrar.pack(pady=20)

root.mainloop()