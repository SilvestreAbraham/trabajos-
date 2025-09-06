<?php
require 'conexion1.php'; 

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Recibimos los datos del formulario
    $id = $_POST['id'];
    $nombre = $_POST['nombre'];
    $rfc = $_POST['rfc'];
    $telefono = $_POST['telefono'];
    $email = $_POST['email'];
    $direccion = $_POST['direccion'];

    $sql = "UPDATE proveedores SET nombre = ?, rfc = ?, telefono = ?, email = ?, direccion = ? WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    $stmt->bind_param("sssssi", $nombre, $rfc, $telefono, $email, $direccion, $id);
    
    if ($stmt->execute()) {
        echo "Proveedor actualizado con éxito.";
    } else {
        echo "Error al actualizar el proveedor.";
    }

    $stmt->close();
}

$conexion->close();
?>
