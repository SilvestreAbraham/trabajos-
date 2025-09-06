<?php
$host = 'localhost';
$usuario = 'root'; 
$clave = 'utc'; 
$basedatos = 'medusa'; 

$conexion = new mysqli($host, $usuario, $clave, $basedatos);

if ($conexion->connect_error) {
    die('Conexión fallida: ' . $conexion->connect_error);
}
?>
