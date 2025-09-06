<?php
require 'conexion1.php';

if (isset($_POST['id']) && !empty($_POST['id'])) {
    $id = $_POST['id'];
    $nombre = $_POST['nombre'];
    $empresa = $_POST['empresa'];
    $fecha_compra = $_POST['fecha_compra'];
    $fecha_caducidad = $_POST['fecha_caducidad'];
    $precio = $_POST['precio'];

    if (isset($_FILES['imagen']) && $_FILES['imagen']['error'] == 0) {
        $imagen_nombre = $_FILES['imagen']['name'];
        $imagen_tmp = $_FILES['imagen']['tmp_name'];
        $imagen_destino = 'imagenes/productos/' . $imagen_nombre;
        
        move_uploaded_file($imagen_tmp, $imagen_destino);
    } else {
        $imagen_nombre = $_POST['imagen_actual']; 
    }

    $sql = "UPDATE productos SET nombre = ?, empresa = ?, fecha_compra = ?, fecha_caducidad = ?, precio = ?, imagen = ? WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    if ($stmt === false) {
        die('Error al preparar la consulta: ' . $conexion->error);
    }

    $stmt->bind_param("ssssisi", $nombre, $empresa, $fecha_compra, $fecha_caducidad, $precio, $imagen_nombre, $id);
    $stmt->execute();

    header("Location: consulta_productos.php");
    exit();
} else {
    echo 'Datos del producto no válidos.';
}
?>
