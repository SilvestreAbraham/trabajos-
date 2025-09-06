<?php
require 'conexion1.php';

if (isset($_GET['id'])) {
    $id = $_GET['id'];
    
    $sql = "DELETE FROM usuarios WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    $stmt->bind_param("i", $id);
    $stmt->execute();

    header("Location: consulta.php");
    exit();
} else {
    echo 'ID no válido.';
}
?>
