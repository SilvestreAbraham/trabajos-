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
    $password = $_POST['password'];
    $nombre = $_POST['nombre'];
    $edad = $_POST['edad'];
    $email = $_POST['email'];
    $direccion = $_POST['direccion'];

    $sql = "INSERT INTO usuarios (id, password, nombre, edad, email, direccion) 
            VALUES ('$id', '$password', '$nombre', '$edad', '$email', '$direccion')";

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
    <title>Agregar Usuario</title>
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

        input[type="text"], input[type="password"], input[type="number"], input[type="email"], textarea {
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
        <h2>Agregar Usuario</h2>
        <form action="agregar_usuario.php" method="POST">
            <input type="text" name="id" placeholder="ID" required><br>
            <input type="password" name="password" placeholder="Contraseña" required><br>
            <input type="text" name="nombre" placeholder="Nombre" required><br>
            <input type="number" name="edad" placeholder="Edad" required><br>
            <input type="email" name="email" placeholder="Email" required><br>
            <textarea name="direccion" placeholder="Dirección" required></textarea><br>
            <input type="submit" value="Guardar Usuario">
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

