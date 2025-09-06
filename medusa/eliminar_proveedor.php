<?php
require 'conexion1.php';

if (isset($_GET['id'])) {
    $id = $_GET['id'];
    
    $sql = "DELETE FROM proveedores WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    
    if ($stmt === false) {
        die('Error al preparar la consulta: ' . $conexion->error);
    }
    
    $stmt->bind_param("i", $id);
    $stmt->execute();

    header("Location: consulta_proveedor.php");
    exit();
} else {
    echo 'ID no válido.';
}
?>
