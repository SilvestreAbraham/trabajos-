<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro Exitoso</title>
    <style>
        body {
            background-image: url('imagenes/fondoregistroexitoso.jpg');
            background-size: cover;
            background-position: center;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .message-container {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2em;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
            text-align: center;
            width: 80%;
            max-width: 600px;
        }
        .btn-container {
            display: flex;
            justify-content: space-between; 
            margin-top: 20px;
            gap: 30px; 
        }
        .btn {
            background-color: #007BFF; 
            color: white;
            padding: 15px 20px; 
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-size: 18px;
            width: 45%; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); 
        }
        .btn:hover {
            background-color: #0056b3; 
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3); 
        }
    </style>
</head>
<body>

    <div class="message-container">
        <h2>¡Registro Exitoso!</h2>
        <p>Ha Sido Registrado Correctamente.</p>
        
        <div class="btn-container">
            <a href="agregar_usuario.php" class="btn">Volver a Ingresar otro Registro</a>
            <a href="menu.php" class="btn">Regresar al Menú</a>
        </div>
    </div>

</body>
</html>

