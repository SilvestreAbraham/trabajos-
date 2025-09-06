<?php
session_start();
if (isset($_SESSION['username'])) {
    header("Location: menu.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body {
            background-image: url('imagenes/medusas.jpg'); 
            background-size: cover;
            background-position: center;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
        }

        .container {
            display: flex;
            width: 60%;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }

        .image-container {
            width: 50%;
            background-image: url('imagenes/medusalogo.jpg'); /* Reemplaza con tu imagen */
            background-size: cover;
            background-position: center;
        }

        .login-container {
            width: 50%;
            padding: 4em 2em;  /* Aumenté el padding vertical */
            text-align: center;
            background-color: rgba(255, 255, 255, 0.8);
        }

        .login-container h2 {
            margin-bottom: 30px; /* Espaciado mayor */
            color: #333;
        }

        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 15px;  /* Aumenté el padding de los inputs */
            margin: 15px 0; /* Aumenté el margen vertical */
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px; /* Texto más grande */
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }

        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="image-container"></div> 
        <div class="login-container">
            <h2>Inicia Sesión Humano</h2>
            <form action="verificacion.php" method="POST">
                <input type="text" name="username" placeholder="Usuario" required><br>
                <input type="password" name="password" placeholder="Contraseña" required><br>
                <input type="submit" value="Login">
            </form>
        </div>
    </div>
</body>
</html>
