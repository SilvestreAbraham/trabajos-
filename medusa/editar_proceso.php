<?php

require 'conexion1.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    $id = $_POST['id'];
    $nombre = $_POST['nombre'];
    $email = $_POST['email'];
    $edad = $_POST['edad'];
    $direccion = $_POST['direccion'];

    $sql = "UPDATE usuarios SET nombre = ?, email = ?, edad = ?, direccion = ? WHERE id = ?";

    $stmt = $conexion->prepare($sql);

    if ($stmt === false) {
        die('Error al preparar la consulta: ' . $conexion->error);
    }

    $stmt->bind_param("ssisi", $nombre, $email, $edad, $direccion, $id);

    if ($stmt->execute()) {
       
        echo "<script>alert('Actualización exitosa');</script>";
        echo "<script>window.location = 'consulta.php';</script>";
    } else {
       
        echo "<script>alert('Error al actualizar los datos');</script>";
    }

    $stmt->close();
}

$conexion->close();
?>
