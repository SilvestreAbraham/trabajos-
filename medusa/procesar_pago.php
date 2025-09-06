<?php
// Incluye la conexión a la base de datos desde 'conexion1.php'
require_once 'conexion1.php'; // Asegúrate de que la ruta es correcta

// Paso 2: Procesar el formulario (solo si se envió un POST)
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Obtener los datos del formulario
    $numero_tarjeta = $_POST['numero_tarjeta'];
    $banco = $_POST['banco'];
    $fecha_vencimiento = $_POST['fecha_vencimiento'];
    $cvv = $_POST['cvv'];

    // Paso 3: Preparar y ejecutar la consulta para insertar los datos en la tabla 'tarjetas'
    $query = "INSERT INTO tarjetas (numero_tarjeta, banco, fecha_vencimiento, cvv) VALUES (?, ?, ?, ?)";
    $stmt = $conexion->prepare($query);

    // Verifica si la preparación de la consulta fue exitosa
    if ($stmt === false) {
        die("Error al preparar la consulta: " . $conexion->error);
    }

    // Enlazar los parámetros con los valores
    $stmt->bind_param("ssss", $numero_tarjeta, $banco, $fecha_vencimiento, $cvv);

    // Ejecutar la consulta
    if ($stmt->execute()) {
        // Redirigir a la página de factura después de la inserción exitosa
        header("Location: factura.php?numero_tarjeta=" . urlencode($numero_tarjeta) . "&banco=" . urlencode($banco));
        exit(); // Detener el script después de la redirección
    } else {
        // Si ocurre un error
        echo "Error al procesar el pago: " . $stmt->error;
    }

    // Cerrar la declaración
    $stmt->close();
}

// Paso 4: Cerrar la conexión a la base de datos al final
$conexion->close();
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procesar Pago</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        .form-container {
            background-color: white;
            margin: 30px auto;
            padding: 20px;
            width: 80%;
            max-width: 600px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        h1 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }

        input[type="text"], input[type="number"], input[type="password"], input[type="date"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 5px;
            width: 100%;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        .back-button {
            background-color: #007BFF;
            text-align: center;
            padding: 10px;
            margin-top: 20px;
            text-decoration: none;
            color: white;
            border-radius: 5px;
        }

        .back-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

    <div class="form-container">
        <h1>Procesar Pago</h1>

        <!-- Formulario para ingresar los datos de la tarjeta -->
        <form action="procesar_pago.php" method="POST">
            <label for="numero_tarjeta">Número de Tarjeta:</label>
            <input type="text" id="numero_tarjeta" name="numero_tarjeta" required placeholder="Número de tarjeta (sin espacios)" maxlength="16">

            <label for="banco">Banco:</label>
            <input type="text" id="banco" name="banco" required placeholder="Nombre del banco">

            <label for="fecha_vencimiento">Fecha de Vencimiento:</label>
            <input type="date" id="fecha_vencimiento" name="fecha_vencimiento" required>

            <label for="cvv">CVV:</label>
            <input type="password" id="cvv" name="cvv" required placeholder="CVV" maxlength="4">

            <button type="submit">Procesar Pago</button>
        </form>

        <!-- Enlace para regresar al carrito -->
        <a href="carrito.php" class="back-button">Regresar al Carrito</a>
    </div>

</body>
</html>