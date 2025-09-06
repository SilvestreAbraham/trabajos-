<?php
require 'conexion1.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $producto = $_POST['producto'];
    $cantidad = $_POST['cantidad'];
    $precio = $_POST['precio'];
    $fecha = date('Y-m-d');

    $sql = "INSERT INTO ventas (producto, cantidad, precio, fecha) VALUES (?, ?, ?, ?)";
    $stmt = $conexion->prepare($sql);
    $stmt->bind_param('sids', $producto, $cantidad, $precio, $fecha);

    if ($stmt->execute()) {
        echo "<script>alert('Venta registrada exitosamente'); window.location.href='consulta_ventas.php';</script>";
    } else {
        echo "<script>alert('Error al registrar la venta');</script>";
    }

    $stmt->close();
    $conexion->close();
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Insertar Venta</title>
    <style>
        body {
            background-image: url('imagenes/fondo.jpg');
            background-size: cover;
            color: #fff;
            font-family: Arial, sans-serif;
        }
        .form-container {
            width: 40%;
            margin: 100px auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            text-align: center;
        }
        input, button {
            margin: 10px 0;
            padding: 10px;
            width: 90%;
            border: none;
            border-radius: 5px;
        }
        button {
            background: #4CAF50;
            color: #fff;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Registrar Nueva Venta</h2>
        <form method="POST">
            <input type="text" name="producto" placeholder="Producto" required>
            <input type="number" name="cantidad" placeholder="Cantidad" required>
            <input type="number" name="precio" placeholder="Precio" step="0.01" required>
            <button type="submit">Registrar Venta</button>
        </form>
    </div>
</body>
</html>
