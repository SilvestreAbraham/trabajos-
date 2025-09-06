<?php
require 'conexion1.php';  // Asegúrate de que este archivo esté configurado correctamente

// Consulta a la tabla 'venta' para obtener los registros
$sql = "SELECT id, cliente, producto, cantidad, total, fecha FROM venta";
$resultado = $conexion->query($sql);
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Consulta de Ventas</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
        }
        .container {
            width: 80%;
            margin: 30px auto;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        td {
            background-color: #f9f9f9;
        }
        .btn-edit, .btn-delete {
            padding: 5px 10px;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .btn-edit {
            background-color: #e91e63;  /* Rosa */
        }
        .btn-delete {
            background-color: #f44336;  /* Rojo */
        }
        .btn-edit:hover, .btn-delete:hover {
            opacity: 0.8;
        }
        .no-records {
            text-align: center;
            font-size: 18px;
            margin-top: 50px;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Ventas Registradas</h1>

        <?php
        // Verificamos si hay resultados
        if ($resultado->num_rows > 0) {
            echo '<table>';
            echo '<tr><th>ID</th><th>Cliente</th><th>Producto</th><th>Cantidad</th><th>Total</th><th>Fecha</th><th>Acciones</th></tr>';
            
            // Mostramos los registros
            while ($fila = $resultado->fetch_assoc()) {
                echo '<tr>';
                echo '<td>' . htmlspecialchars($fila['id']) . '</td>';
                echo '<td>' . htmlspecialchars($fila['cliente']) . '</td>';
                echo '<td>' . htmlspecialchars($fila['producto']) . '</td>';
                echo '<td>' . htmlspecialchars($fila['cantidad']) . '</td>';
                echo '<td>' . htmlspecialchars($fila['total']) . '</td>';
                echo '<td>' . htmlspecialchars($fila['fecha']) . '</td>';
                echo '<td>
                        <a href="update_venta.php?id=' . htmlspecialchars($fila['id']) . '" class="btn-edit">Editar</a>
                        <a href="delete_venta.php?id=' . htmlspecialchars($fila['id']) . '" class="btn-delete" onclick="return confirm(\'¿Estás seguro de eliminar esta venta?\');">Eliminar</a>
                      </td>';
                echo '</tr>';
            }
            
            echo '</table>';
        } else {
            echo '<p class="no-records">No hay ventas registradas.</p>';
        }

        // Cerramos la conexión
        $conexion->close();
        ?>
    </div>

</body>
</html>
