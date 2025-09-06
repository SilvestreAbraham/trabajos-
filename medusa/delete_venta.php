<?php
require 'conexion1.php';  // Incluye el archivo de conexión a la base de datos

// Verifica si se ha recibido el parámetro 'id' desde la URL
if (isset($_GET['id'])) {
    $id = $_GET['id'];  // Obtener el ID de la venta a eliminar

    // Preparamos la consulta para eliminar el registro con el ID proporcionado
    $sql = "DELETE FROM venta WHERE id = ?";
    $stmt = $conexion->prepare($sql);
    
    // Vinculamos el parámetro 'i' para el ID (entero)
    $stmt->bind_param('i', $id);

    // Ejecutamos la consulta
    if ($stmt->execute()) {
        // Si la eliminación fue exitosa, redirigimos a la página de consulta de ventas con un mensaje
        echo "<script>alert('Venta eliminada exitosamente'); window.location.href='consulta_ventas.php';</script>";
    } else {
        // Si hubo un error al eliminar, mostramos un mensaje de error
        echo "<script>alert('Error al eliminar la venta'); window.location.href='consulta_ventas.php';</script>";
    }

    // Cerramos la declaración y la conexión
    $stmt->close();
    $conexion->close();
} else {
    // Si no se proporcionó un ID, redirigimos al usuario
    echo "<script>alert('No se proporcionó un ID válido'); window.location.href='consulta_ventas.php';</script>";
}
?>
