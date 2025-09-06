import flet as ft
import time
import numpy as np

def funcion_activacion(x):
    return 1 if x >= 0 else 0

def entrenar_neurona(X, y, page, epoca, valor_x1, valor_x2, valor_w1, valor_w2, valor_bias, valor_y, tasa_aprendizaje=0.1, epocas=100):
    n_caracteristicas = X.shape[1]
    pesos = np.zeros(n_caracteristicas)
    bias = 0

    for ep in range(epocas):
        epoca.value = f"Epoca: {ep + 1}"
        pesos_actualizados = False

        for i in range(X.shape[0]):
            valor_x1.value = str(X[i][0])
            valor_x2.value = str(X[i][1])
            valor_w1.value = f"* {pesos[0]:.2f}"
            valor_w2.value = f"* {pesos[1]:.2f}"
            valor_bias.value = f"Bias: {bias:.2f}"
            
            z = np.dot(pesos, X[i]) + bias
            y_pred = funcion_activacion(z)
            error = y[i] - y_pred

            if error != 0:
                pesos += tasa_aprendizaje * error * X[i]
                bias += tasa_aprendizaje * error
                pesos_actualizados = True

            valor_y.value = str(y_pred)
            page.update()
            time.sleep(0.7)

        if not pesos_actualizados:
            epoca.value = "Convergencia alcanzada"
            page.update()
            break

    return pesos, bias

# Datos de compuertas lógicas
datos_AND = {
    "X": np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
    "y": np.array([0, 0, 0, 1])
}

datos_OR = {
    "X": np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
    "y": np.array([0, 1, 1, 1])
}

def predecir(input_1, input_2, pesos, bias):
    X_input = np.array([input_1, input_2])
    z = np.dot(pesos, X_input) + bias
    return funcion_activacion(z)

def main(page: ft.Page):
    page.title = "Perceptrón Simple"
    page.window_width = 750  
    page.window_height = 800  
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    imagen_neurona = ft.Image(src="neurona.png", width=700, height=650)  
    
    epoca = ft.Text(value="Epoca: 0", size=30)
    valor_x1 = ft.Text(value="0", size=30)
    valor_w1 = ft.Text(value="* 0.10", size=30)
    valor_x2 = ft.Text(value="0", size=30)
    valor_w2 = ft.Text(value="* 0.00", size=30)
    valor_bias = ft.Text(value="Bias: -0.20", size=25)
    valor_y = ft.Text(value="0", size=30)
    
    boton_entrenar = ft.ElevatedButton("Entrenar AND", width=150, height=40)
    boton_entrenar_or = ft.ElevatedButton("Entrenar OR", width=150, height=40)
    
    input_1 = ft.TextField(value="1", width=60, height=40, text_size=20)
    input_2 = ft.TextField(value="1", width=60, height=40, text_size=20)
    prediccion_text = ft.Text(value="Prediction: 0", size=30)
    empty_text = ft.Text(value="Emptyer", size=20)

    main_stack = ft.Stack([
        imagen_neurona,
        
        ft.Container(epoca, left=40, top=30),
        ft.Container(valor_x1, left=50, top=190),
        ft.Container(valor_w1, left=75, top=190),
        ft.Container(valor_x2, left=210, top=185),
        ft.Container(valor_w2, left=235, top=185),
        ft.Container(valor_bias, left=240, top=270),
        ft.Container(valor_y, left=600, top=150),
        ft.Container(boton_entrenar, left=500, top=30),
        ft.Container(boton_entrenar_or, left=500, top=80),
        ft.Container(input_1, left=50, top=550),
        ft.Container(input_2, left=210, top=550),
        ft.Container(prediccion_text, left=450, top=550),
        ft.Container(empty_text, left=350, top=600)

    ], width=700, height=700)

    page.add(main_stack)

    # Variables para almacenar pesos entrenados
    pesos_entrenados = None
    bias_entrenado = None

    def entrenar_and(e):
        nonlocal pesos_entrenados, bias_entrenado
        pesos_entrenados, bias_entrenado = entrenar_neurona(
            datos_AND["X"], datos_AND["y"], page, epoca, valor_x1, valor_x2, 
            valor_w1, valor_w2, valor_bias, valor_y
        )
        actualizar_prediccion()

    def entrenar_or(e):
        nonlocal pesos_entrenados, bias_entrenado
        pesos_entrenados, bias_entrenado = entrenar_neurona(
            datos_OR["X"], datos_OR["y"], page, epoca, valor_x1, valor_x2, 
            valor_w1, valor_w2, valor_bias, valor_y
        )
        actualizar_prediccion()

    def actualizar_prediccion(e=None):
        if pesos_entrenados is not None and bias_entrenado is not None:
            try:
                in1 = int(input_1.value)
                in2 = int(input_2.value)
                pred = predecir(in1, in2, pesos_entrenados, bias_entrenado)
                prediccion_text.value = f"Prediction: {pred}"
                page.update()
            except ValueError:
                prediccion_text.value = "Prediction: Error"
                page.update()

    # Asignación de eventos
    boton_entrenar.on_click = entrenar_and
    boton_entrenar_or.on_click = entrenar_or
    input_1.on_change = actualizar_prediccion
    input_2.on_change = actualizar_prediccion

ft.app(target=main)