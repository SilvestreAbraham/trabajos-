<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $conn = new mysqli("localhost", "root", "utc", "medusa");
    if ($conn->connect_error) {
        die("Conexión fallida: " . $conn->connect_error);
    }

    $id = $_POST['id'];
    $nombre = $_POST['nombre'];
    $empresa = $_POST['empresa'];
    $fecha_compra = $_POST['fecha_compra'];
    $fecha_caducidad = $_POST['fecha_caducidad'];
    $precio = $_POST['precio'];

    $sql = "INSERT INTO productos (id, nombre, empresa, fecha_compra, fecha_caducidad, precio) 
            VALUES ('$id', '$nombre', '$empresa', '$fecha_compra', '$fecha_caducidad', '$precio')";

    if ($conn->query($sql) === TRUE) {
        header("Location: registro_exitoso.php");
        exit();
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    $conn->close();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agregar Producto</title>
    <style>
        body {
            background-image: url('imagenes/fondoagregarproducto.jpg');
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
        }
        .menu-dropdown {
            display: none;
            position: absolute;
            background-color: #444;
            top: 60px;
            right: 20px;
            border-radius: 5px;
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
            z-index: 1000;
        }
        .menu-dropdown a {
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            display: block;
        }
        .menu-dropdown a:hover {
            background-color: #555;
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
        input[type="text"], input[type="date"], input[type="number"] {
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
    </style>
    <script>
        function toggleMenu() {
            var dropdown = document.getElementById("menuDropdown");
            dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
        }
    </script>
</head>
<body>
    <div class="top-bar">
        <img src="imagenes/logomenu.png" alt="Logo">
        <button class="menu-btn" onclick="toggleMenu()">&#9776;</button>
        <div class="menu-dropdown" id="menuDropdown">
            <a href="menu.php">Regresar al Menú</a>
        </div>
    </div>

    <div class="form-container">
        <h2>Agregar Producto</h2>
        <form action="agregar_producto.php" method="POST">
            <input type="text" name="id" placeholder="ID del Producto" required><br>
            <input type="text" name="nombre" placeholder="Nombre del Producto" required><br>
            <input type="text" name="empresa" placeholder="Empresa" required><br>
            <input type="date" name="fecha_compra" placeholder="Fecha de Compra" required><br>
            <input type="date" name="fecha_caducidad" placeholder="Fecha de Caducidad" required><br>
            <input type="number" step="0.01" name="precio" placeholder="Precio" required><br>
            <input type="submit" value="Guardar Producto">
        </form>
    </div>
</body>
</html>

