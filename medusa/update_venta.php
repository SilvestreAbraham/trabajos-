<?php
require 'conexion1.php';  // Incluye la conexión a la base de datos

// Verifica si se ha recibido el parámetro 'id' desde la URL
if (isset($_GET['id'])) {
    $id = $_GET['id'];  // Obtener el ID de la venta que se desea editar

    // Consulta para obtener los datos de la venta con el ID especificado
    $sql = "SELECT * FROM venta WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    $stmt->bind_param('i', $id);
    $stmt->execute();
    $resultado = $stmt->get_result();

    // Si se encuentra la venta con ese ID
    if ($resultado->num_rows > 0) {
        $venta = $resultado->fetch_assoc(); // Obtener los datos de la venta
    } else {
        echo "<script>alert('Venta no encontrada'); window.location.href='consulta_ventas.php';</script>";
        exit;
    }
} else {
    echo "<script>alert('No se proporcionó un ID válido'); window.location.href='consulta_ventas.php';</script>";
    exit;
}

// Procesar la actualización si se envía el formulario
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $producto = $_POST['producto'];
    $cantidad = $_POST['cantidad'];
    $total = $_POST['total'];
    $fecha = $_POST['fecha'];

    // Consulta para actualizar la venta
    $sql_update = "UPDATE venta SET producto = ?, cantidad = ?, total = ?, fecha = ? WHERE id = ?";
    $stmt_update = $conexion->prepare($sql_update);
    $stmt_update->bind_param('siisi', $producto, $cantidad, $total, $fecha, $id);

    if ($stmt_update->execute()) {
        echo "<script>alert('Venta actualizada exitosamente'); window.location.href='consulta_ventas.php';</script>";
    } else {
        echo "<script>alert('Error al actualizar la venta');</script>";
    }
    $stmt_update->close();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Actualizar Venta</title>
    <style>
        body {
            background-image: url('imagenes/fondousuarios.jpg');
            background-size: cover;
            background-position: center;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
        }

        .top-bar {
            background-color: #333;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            box-sizing: border-box;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
        }

        .top-bar img {
            height: 50px;
        }

        .menu-btn {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
        }

        .form-container {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2em;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
            width: 80%;
            max-width: 600px;
            margin-top: 80px;
        }

        input[type="text"], input[type="number"], input[type="date"], input[type="submit"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }

        input[type="submit"]:hover {
            background-color: #45a049;
        }

        /* Submenu styles */
        .submenu {
            display: none;
            background-color: #444;
            position: absolute;
            right: 20px;
            top: 60px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            width: 180px;
            padding: 10px;
        }

        .submenu a {
            display: block;
            padding: 15px 20px;
            color: white;
            text-decoration: none;
        }

        .submenu a:hover {
            background-color: #555;
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <img src="imagenes/logomenu.png" alt="Logo">
        <button class="menu-btn" onclick="toggleSubMenu()">&#9776;</button>
    </div>

    <div class="submenu" id="submenu">
        <a href="menu.php">Regresar al Menú</a>
    </div>

    <div class="form-container">
        <h2>Actualizar Venta</h2>
        <form method="POST">
            <label for="producto">Producto:</label>
            <input type="text" name="producto" value="<?php echo htmlspecialchars($venta['producto']); ?>" required><br>

            <label for="cantidad">Cantidad:</label>
            <input type="number" name="cantidad" value="<?php echo htmlspecialchars($venta['cantidad']); ?>" required><br>

            <label for="total">Total:</label>
            <input type="number" step="0.01" name="total" value="<?php echo htmlspecialchars($venta['total']); ?>" required><br>

            <label for="fecha">Fecha:</label>
            <input type="date" name="fecha" value="<?php echo htmlspecialchars($venta['fecha']); ?>" required><br>

            <input type="submit" value="Actualizar Venta">
        </form>
    </div>

    <script>
        // Función para alternar la visibilidad del submenu
        function toggleSubMenu() {
            var submenu = document.getElementById('submenu');
            submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
        }
    </script>
</body>
</html>
