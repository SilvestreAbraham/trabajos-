<?php
require 'conexion1.php';  

$sql = "SELECT id, nombre, empresa, fecha_compra, fecha_caducidad, precio FROM productos"; 
$resultado = $conexion->query($sql); 
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consulta de Productos</title>
    <style>
        body {
            background-image: url('imagenes/fondoconsulta.jpg');
            background-size: cover;
            background-position: center;
            font-family: Arial, sans-serif;
            color: #fff;
            margin: 0;
        }

        .top-bar {
            background-color: #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }
        .menu-btn {
            font-size: 24px;
            color: white;
            background: none;
            border: none;
            cursor: pointer;
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

        table {
            width: 80%;
            margin: 80px auto 20px;  
            border-collapse: collapse;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 8px;
        }
        th, td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ddd;
        }
        th {
            background-color: #444;
        }
        td {
            background-color: #333;
        }
        .btn {
            text-decoration: none;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 5px;
            color: #fff;
        }
        .btn-edit {
            background-color: #e91e63;  
        }
        .btn-delete {
            background-color: #f44336;  
        }
    </style>
</head>
<body>

    <div class="top-bar">
        <img src="imagenes/logomenu.png" alt="Logo" class="logo">
        <button class="menu-btn" onclick="toggleSubMenu()">&#9776;</button>
    </div>

    <div class="submenu" id="submenu">
        <a href="menu.php" class="submenu-btn">Regresar al Menú</a>
    </div>

    <?php
    if ($resultado->num_rows > 0) {
        echo '<table>';
        echo '<tr><th>ID</th><th>Nombre</th><th>Empresa</th><th>Fecha de Compra</th><th>Fecha de Caducidad</th><th>Precio</th><th>Acciones</th></tr>';

        while ($fila = $resultado->fetch_assoc()) {
            echo '<tr>';
            echo '<td>' . htmlspecialchars($fila['id']) . '</td>';
            echo '<td>' . htmlspecialchars($fila['nombre']) . '</td>';
            echo '<td>' . htmlspecialchars($fila['empresa']) . '</td>';
            echo '<td>' . htmlspecialchars($fila['fecha_compra']) . '</td>';
            echo '<td>' . htmlspecialchars($fila['fecha_caducidad']) . '</td>';
            echo '<td>' . htmlspecialchars($fila['precio']) . '</td>';
            echo '<td>
                    <a href="editar_producto.php?id=' . htmlspecialchars($fila['id']) . '" class="btn btn-edit">Editar</a> 
                    <a href="eliminar_producto.php?id=' . htmlspecialchars($fila['id']) . '" class="btn btn-delete" onclick="return confirm(\'¿Estás seguro de eliminar este producto?\');">Eliminar</a>
                  </td>';
            echo '</tr>';
        }

        echo '</table>';
    } else {
        echo '<p style="text-align: center; margin-top: 50px;">No se encontraron registros.</p>';
    }

    $conexion->close();
    ?>

    <script>
        function toggleSubMenu() {
            var submenu = document.getElementById('submenu');
            submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
        }
    </script>

</body>
</html>
