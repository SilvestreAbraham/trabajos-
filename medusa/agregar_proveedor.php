<?php
require 'conexion1.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    $id = $_POST['id']; 
    $nombre = $_POST['nombre'];
    $rfc = $_POST['rfc'];
    $telefono = $_POST['telefono'];
    $email = $_POST['email'];
    $direccion = $_POST['direccion'];

    $sql = "INSERT INTO proveedores (id, nombre, rfc, telefono, email, direccion) VALUES ('$id', '$nombre', '$rfc', '$telefono', '$email', '$direccion')";
    
    if ($conexion->query($sql) === TRUE) {
        echo "Proveedor agregado exitosamente";
    } else {
        echo "Error: " . $sql . "<br>" . $conexion->error;
    }

    $conexion->close();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agregar Proveedor</title>
    <style>
        body {
            background-image: url('imagenes/fondoagregarproveedor.jpg'); 
            background-size: cover;
            background-position: center;
            font-family: Arial, sans-serif;
            color: white;
            margin: 0;
        }

        .top-bar {
            background-color: #333;
            width: 100%;
            display: flex;
            justify-content: flex-start; 
            align-items: center;
            padding: 10px 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            position: fixed;
            top: 0;
            left: 0;
        }

        .menu-btn {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            margin-left: 1200px; 
        }

        .logo {
            height: 50px;
        }

        .submenu {
            display: none;
            background-color: #444;
            position: absolute;
            right: 20px;
            top: 60px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            width: 180px;
            padding: 10px;
        }

        .submenu a {
            display: block;
            padding: 15px 20px;
            color: white;
            text-decoration: none;
            text-align: center;
        }

        .submenu a:hover {
            background-color: #555;
        }

        .form-container {
            width: 40%;
            margin: 100px auto 50px; 
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }

        label {
            display: block;
            margin-top: 10px;
        }

        input[type="text"], input[type="email"], input[type="submit"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
            box-sizing: border-box;
        }

        input[type="submit"] {
            background-color: #007BFF;
            color: white;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

    <div class="top-bar">
        <img src="imagenes/logomenu.png" alt="Logo" class="logo">
        <button class="menu-btn" onclick="toggleSubMenu()">&#9776;</button>
    </div>

    <div class="submenu" id="submenu">
        <a href="menu.php">Regresar al Menú</a>
    </div>

    <div class="form-container">
        <h2>Agregar Proveedor</h2>
        <form method="POST" action="agregar_proveedor.php">
            <label for="id">ID:</label>
            <input type="text" name="id" required>

            <label for="nombre">Nombre:</label>
            <input type="text" name="nombre" required>

            <label for="rfc">RFC:</label>
            <input type="text" name="rfc" required>

            <label for="telefono">Teléfono:</label>
            <input type="text" name="telefono" required>

            <label for="email">Email:</label>
            <input type="email" name="email" required>

            <label for="direccion">Dirección:</label>
            <input type="text" name="direccion" required>

            <input type="submit" value="Agregar Proveedor">
        </form>
    </div>

    <script>
        function toggleSubMenu() {
            var submenu = document.getElementById('submenu');
            submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
        }
    </script>

</body>
</html>

