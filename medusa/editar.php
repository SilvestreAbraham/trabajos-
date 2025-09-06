<?php

require 'conexion1.php';

$usuario = [];

if (isset($_GET['id']) && !empty($_GET['id'])) {

    $id = $_GET['id'];

    $sql = "SELECT * FROM usuarios WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    if ($stmt === false) {
        die('Error al preparar la consulta: ' . $conexion->error);
    }

    $stmt->bind_param("i", $id);
    $stmt->execute();
    $resultado = $stmt->get_result();

    if ($resultado->num_rows > 0) {
        $usuario = $resultado->fetch_assoc();
    }
}

if (empty($usuario)) {
    
    echo "Usuario no encontrado, redirigiendo...";
    header("Refresh: 3; url=consulta.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Usuario</title>
    <style>
        body {
            background-image: url('ruta/a/tu/fondo.jpg');
            background-size: cover;
            font-family: Arial, sans-serif;
            color: #fff;
        }

        .form-container {
            width: 50%;
            margin: 50px auto;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
        }

        input[type="text"], input[type="email"], input[type="number"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            margin: 10px 0;
            cursor: pointer;
            border-radius: 5px;
        }

        .btn-back {
            background-color: #2196F3;
            padding: 10px 20px;
            text-decoration: none;
            color: white;
            border-radius: 5px;
            position: absolute;
            top: 20px;
            left: 20px; 
            z-index: 10;
        }
    </style>
</head>
<body>

<a href="consulta.php" class="btn-back">Regresar</a>

<div class="form-container">
    <h2>Editar Usuario</h2>
    <form action="editar_proceso.php" method="POST">
        
        <input type="hidden" name="id" value="<?php echo isset($usuario['id']) ? htmlspecialchars($usuario['id']) : ''; ?>">

        <label for="nombre">Nombre:</label>
        <input type="text" name="nombre" id="nombre" value="<?php echo isset($usuario['nombre']) ? htmlspecialchars($usuario['nombre']) : ''; ?>" required>

        <label for="email">Email:</label>
        <input type="email" name="email" id="email" value="<?php echo isset($usuario['email']) ? htmlspecialchars($usuario['email']) : ''; ?>" required>

        <label for="edad">Edad:</label>
        <input type="number" name="edad" id="edad" value="<?php echo isset($usuario['edad']) ? htmlspecialchars($usuario['edad']) : ''; ?>" required>

        <label for="direccion">Dirección:</label>
        <input type="text" name="direccion" id="direccion" value="<?php echo isset($usuario['direccion']) ? htmlspecialchars($usuario['direccion']) : ''; ?>" required>

        <input type="submit" value="Actualizar">
    </form>
</div>

</body>
</html>
