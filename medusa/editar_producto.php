<?php
require 'conexion1.php';

$producto = [];

if (isset($_GET['id']) && !empty($_GET['id'])) {
    $id = $_GET['id'];

    // Consulta para obtener los datos del producto
    $sql = "SELECT * FROM productos WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    if ($stmt === false) {
        die('Error al preparar la consulta: ' . $conexion->error);
    }

    $stmt->bind_param("i", $id);
    $stmt->execute();
    $resultado = $stmt->get_result();

    if ($resultado->num_rows > 0) {
        $producto = $resultado->fetch_assoc();
    }
}

if (empty($producto)) {
    echo "Producto no encontrado, redirigiendo...";
    header("Refresh: 3; url=consulta_producto.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Producto</title>
    <style>
        body {
            background-image: url('imagenes/fondoeditarproveedor.jpg'); 
            background-size: cover;
            font-family: Arial, sans-serif;
            color: #fff;
            margin: 0;
            padding: 0;
        }

        .header-bar {
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
            position: fixed;
            width: 100%;
            top: 0;
            left: 0;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .menu-btn {
            cursor: pointer;
            padding: 10px;
            font-size: 24px;
            display: inline-block;
            color: white;
            margin-left: 1250px;
        }

        .menu-btn:hover {
            background-color: #575757;
            border-radius: 5px;
        }

        .menu-btn span {
            display: block;
            width: 30px;
            height: 3px;
            background-color: white;
            margin: 6px 0;
        }

        .menu-dropdown {
            display: none;
            position: absolute;
            background-color: #333;
            min-width: 200px;
            top: 50px;
            right: 20px;
            z-index: 1000;
        }

        .menu-dropdown a {
            padding: 10px;
            text-decoration: none;
            color: white;
            display: block;
        }

        .menu-dropdown a:hover {
            background-color: #575757;
        }

        .form-container {
            width: 60%;
            margin: 100px auto;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 10px;
        }

        input[type="text"], input[type="email"], input[type="number"], input[type="date"], input[type="file"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #ddd;
            box-sizing: border-box;
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

        .menu-btn.active + .menu-dropdown {
            display: block;
        }

    </style>
</head>
<body>

    <div class="header-bar">
        <div class="menu-btn" onclick="toggleMenu()">
            <span></span>
            <span></span>
            <span></span>
        </div>
        <div class="menu-dropdown">
            <a href="menu.php">Regresar al Menú</a>
        </div>
    </div>

    <div class="form-container">
        <h2>Editar Producto</h2>
        <form action="editar_producto_proceso.php" method="POST" enctype="multipart/form-data">
            <input type="hidden" name="id" value="<?php echo isset($producto['id']) ? htmlspecialchars($producto['id']) : ''; ?>">

            <label for="nombre">Nombre:</label>
            <input type="text" name="nombre" id="nombre" value="<?php echo isset($producto['nombre']) ? htmlspecialchars($producto['nombre']) : ''; ?>" required>

            <label for="empresa">Empresa:</label>
            <input type="text" name="empresa" id="empresa" value="<?php echo isset($producto['empresa']) ? htmlspecialchars($producto['empresa']) : ''; ?>" required>

            <label for="fecha_compra">Fecha de Compra:</label>
            <input type="date" name="fecha_compra" id="fecha_compra" value="<?php echo isset($producto['fecha_compra']) ? htmlspecialchars($producto['fecha_compra']) : ''; ?>" required>

            <label for="fecha_caducidad">Fecha de Caducidad:</label>
            <input type="date" name="fecha_caducidad" id="fecha_caducidad" value="<?php echo isset($producto['fecha_caducidad']) ? htmlspecialchars($producto['fecha_caducidad']) : ''; ?>" required>

            <label for="precio">Precio:</label>
            <input type="number" name="precio" id="precio" value="<?php echo isset($producto['precio']) ? htmlspecialchars($producto['precio']) : ''; ?>" required>

            <label for="imagen">Imagen del Producto:</label>
            <input type="file" name="imagen" id="imagen">

            <input type="submit" value="Actualizar">
        </form>
    </div>

    <script>
        function toggleMenu() {
            const menu = document.querySelector('.menu-btn');
            menu.classList.toggle('active');
        }
    </script>

</body>
</html>
