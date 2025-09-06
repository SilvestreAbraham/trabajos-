<?php
session_start();

// Verificar si la sesión del carrito existe
if (!isset($_SESSION['carrito'])) {
    $_SESSION['carrito'] = [];
}

// Agregar al carrito si el formulario es enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $producto = $_POST['producto'];
    $cantidad = $_POST['cantidad'];
    $precio = $_POST['precio'];
    $total = $cantidad * $precio;  // Calcular el total de la venta
    $cliente = $_SESSION['username']; // El cliente es el usuario actual (debe estar en la sesión)
    
    // Agregar el producto al carrito
    $_SESSION['carrito'][] = [
        'producto' => $producto,
        'cantidad' => $cantidad,
        'precio' => $precio,
        'total' => $total
    ];
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Carrito de Compras</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f7f7f7;
        }
        table {
            width: 70%;
            margin: 20px auto;
            border-collapse: collapse;
            background: #fff;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th {
            background: #333;
            color: #fff;
        }
        button {
            padding: 8px 12px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <h1 style="text-align: center;">Carrito de Compras</h1>
    
    <!-- Formulario para agregar productos al carrito -->
    <form method="POST" style="text-align: center;">
        <input type="text" name="producto" placeholder="Producto" required>
        <input type="number" name="cantidad" placeholder="Cantidad" required>
        <input type="number" step="0.01" name="precio" placeholder="Precio" required>
        <button type="submit">Agregar al Carrito</button>
    </form>

    <!-- Si el carrito tiene productos, se muestran en una tabla -->
    <?php if (!empty($_SESSION['carrito'])): ?>
        <table>
            <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Precio</th>
                <th>Total</th>
            </tr>
            <?php foreach ($_SESSION['carrito'] as $item): ?>
                <tr>
                    <td><?= htmlspecialchars($item['producto']) ?></td>
                    <td><?= htmlspecialchars($item['cantidad']) ?></td>
                    <td>$<?= number_format($item['precio'], 2) ?></td>
                    <td>$<?= number_format($item['total'], 2) ?></td>
                </tr>
            <?php endforeach; ?>
        </table>
        
        <!-- Botón para procesar el pago -->
        <div style="text-align: center;">
            <a href="procesar_pago.php" style="text-decoration: none; color: white; background: #007BFF; padding: 10px 20px; border-radius: 5px;">Procesar Pago</a>
        </div>
    <?php endif; ?>
</body>
</html>
