<?php
// Inicia la sesión si estás usando sesiones para pasar los datos
session_start();

// Obtener datos del cliente de la URL
$numero_tarjeta = isset($_GET['numero_tarjeta']) ? $_GET['numero_tarjeta'] : 'No disponible';
$banco = isset($_GET['banco']) ? $_GET['banco'] : 'No disponible';
$fecha_vencimiento = isset($_GET['fecha_vencimiento']) ? $_GET['fecha_vencimiento'] : 'No disponible';
$cvv = isset($_GET['cvv']) ? $_GET['cvv'] : 'No disponible';

// Supongamos que los productos están en la sesión
// Si no, se pueden obtener desde la base de datos si se almacena en ella
if (isset($_SESSION['carrito']) && !empty($_SESSION['carrito'])) {
    $productos = $_SESSION['carrito'];
} else {
    $productos = []; // Si no hay productos en el carrito, mostrar vacío
}

// Calcular el total
$total = 0;
foreach ($productos as $producto) {
    // Si 'nombre', 'cantidad' o 'precio' no existen, se les da un valor predeterminado
    $nombre = isset($producto['nombre']) ? $producto['nombre'] : 'Producto desconocido';
    $cantidad = isset($producto['cantidad']) ? $producto['cantidad'] : 0;
    $precio = isset($producto['precio']) ? $producto['precio'] : 0;

    $subtotal = $cantidad * $precio;
    $total += $subtotal;  // Acumulamos el total
}

?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Factura</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }

        .factura-container {
            background-color: white;
            margin: 30px auto;
            padding: 20px;
            width: 80%;
            max-width: 800px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .factura-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }

        .factura-header img {
            width: 50px;
            height: 50px;
            margin-right: 20px;
        }

        .factura-header h1 {
            font-size: 24px;
            margin: 10px 0;
        }

        .factura-header p {
            font-size: 14px;
            margin: 5px 0;
        }

        .table-container {
            width: 100%;
            margin: 20px 0;
            border-collapse: collapse;
        }

        .table-container th, .table-container td {
            padding: 8px;
            text-align: left;
            border: 1px solid #ddd;
        }

        .table-container th {
            background-color: #f2f2f2;
        }

        .total {
            font-size: 18px;
            font-weight: bold;
            text-align: right;
            margin-top: 20px;
        }

        .button {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            margin: 20px auto;
            border-radius: 5px;
            text-align: center;
            text-decoration: none;
        }

        .button:hover {
            background-color: #45a049;
        }

        .qr-code {
            width: 150px;  /* Ajusta el tamaño del QR a 150px de ancho */
            height: 150px; /* Ajusta el tamaño del QR a 150px de alto */
            float: right;  /* Si deseas que el QR se alinee a la derecha */
        }
    </style>
</head>
<body>
    <div class="factura-container">
        <div class="factura-header">
            <!-- Logo movido a la izquierda y menos arriba -->
            <img src="imagenes/logofactura.png" alt="Logo"> <!-- Aquí puedes poner el logo -->
            <div>
                <h1>Factura MEDUSA SA DE CV</h1>
                <p>Fecha: <?php echo date('Y-m-d'); ?></p>
            </div>
        </div>

        <div class="cliente-info">
            <p><strong>Cliente:</strong> <?php echo $numero_tarjeta; ?></p>
            <p><strong>Banco:</strong> <?php echo $banco; ?></p>
        </div>

        <div class="table-container">
            <table>
                <tr>
                    <th>Producto</th>
                    <th>Cantidad</th>
                    <th>Precio Unitario</th>
                    <th>Subtotal</th>
                </tr>
                <?php
                // Mostrar los productos dinámicamente
                foreach ($productos as $producto) {
                    // Asignamos valores predeterminados si el producto no tiene datos completos
                    $nombre = isset($producto['nombre']) ? $producto['nombre'] : 'Producto desconocido';
                    $cantidad = isset($producto['cantidad']) ? $producto['cantidad'] : 0;
                    $precio = isset($producto['precio']) ? $producto['precio'] : 0;
                    $subtotal = $cantidad * $precio;

                    echo "<tr>";
                    echo "<td>" . htmlspecialchars($nombre) . "</td>";
                    echo "<td>" . htmlspecialchars($cantidad) . "</td>";
                    echo "<td>$" . number_format($precio, 2) . "</td>";
                    echo "<td>$" . number_format($subtotal, 2) . "</td>";
                    echo "</tr>";
                }
                ?>
            </table>
        </div>

        <div class="total">
            <p>A pagar: $<?php echo number_format($total, 2); ?></p>
        </div>

        <div class="qr-code">
            <!-- Aquí puedes agregar un código QR con un enlace, por ejemplo -->
            <img src="imagenes/qrfactura.png" alt="QR Code">
        </div>

        <a href="menu.php" class="button">Finalizar y Regresar al Menú</a>
    </div>
</body>
</html>
