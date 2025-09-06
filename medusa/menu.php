<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menú Principal</title>
    <style>
        body {
            background-image: url('imagenes/fondomenu.jpg'); 
            background-size: cover;
            background-position: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        
        .top-bar {
            background-color: #333; 
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }
        
        .btn {
            background-color: #007BFF; 
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            font-size: 16px;
        }

        .menu-btn {
            font-size: 24px;
            color: white;
            background: none;
            border: none;
            cursor: pointer;
        }

        .logo {
            height: 50px;
        }
        
        .submenu {
            display: none;
            background-color: #444;
            position: absolute;
            right: 20px;
            top: 60px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            width: 200px; 
            padding: 10px;
        }

        .submenu a {
            display: block;
            padding: 15px 20px;
            color: white;
            text-decoration: none;
        }

        .submenu a:hover {
            background-color: #555;
        }

        .submenu-usuarios, .submenu-proveedor, .submenu-producto, .submenu-ventas, .submenu-clientes {
            display: none;
            background-color: #555;
            margin-top: 5px;
            border-radius: 5px;
        }
        
        .submenu-usuarios a, .submenu-proveedor a, .submenu-producto a, .submenu-ventas a, .submenu-clientes a {
            padding: 10px 15px;
            color: white;
            text-decoration: none;
        }

        .submenu-usuarios a:hover, .submenu-proveedor a:hover, .submenu-producto a:hover, .submenu-ventas a:hover, .submenu-clientes a:hover {
            background-color: #666;
        }
        
        .carousel {
            width: 80%;
            max-width: 600px;
            overflow: hidden;
            position: relative;
            margin: 50px auto 0;
            text-align: center;
        }
        .carousel img {
            width: 100%;
            position: absolute;
            left: 100%; 
            transition: transform 1s ease-in-out;
            opacity: 0; 
        }
        .carousel img.active {
            left: 0; 
            opacity: 1;
            transform: translateX(0); 
            position: static;
        }
        .product-name {
            color: white;
            font-size: 20px;
            margin-top: 10px;
        }
    </style>
</head>

<body>
    <div class="top-bar">
        <button class="btn" onclick="window.location.href='cerrarsesion.php'">Regresar</button>
        <img src="imagenes/logomenu.png" alt="Logo" class="logo">
        <button class="menu-btn" onclick="toggleSubMenu()">&#9776;</button>
    </div>

    <div class="submenu" id="submenu">
        <!-- Usuarios -->
        <a href="#" class="submenu-btn" onclick="toggleUsuarioSubMenu()">Usuarios</a>
        <div class="submenu-usuarios" id="submenu-usuarios">
            <a href="consulta.php" class="submenu-btn">Consultar Usuarios</a>
            <a href="agregar_usuario.php" class="submenu-btn">Registrar Usuarios</a>
        </div>

        <!-- Proveedores -->
        <a href="#" class="submenu-btn" onclick="toggleProveedorSubMenu()">Proveedores</a>
        <div class="submenu-proveedor" id="submenu-proveedor">
            <a href="agregar_proveedor.php" class="submenu-btn">Agregar Proveedor</a>
            <a href="consulta_proveedor.php" class="submenu-btn">Consultar Proveedor</a>
        </div>

        <!-- Productos -->
        <a href="#" class="submenu-btn" onclick="toggleProductoSubMenu()">Productos</a>
        <div class="submenu-producto" id="submenu-producto">
            <a href="agregar_producto.php" class="submenu-btn">Agregar Producto</a>
            <a href="consultar_producto.php" class="submenu-btn">Consultar Productos</a>
        </div>

        <!-- Ventas -->
        <a href="#" class="submenu-btn" onclick="toggleVentasSubMenu()">Ventas</a>
        <div class="submenu-ventas" id="submenu-ventas">
            <a href="insertar_venta.php" class="submenu-btn">Insertar Venta</a>
            <a href="consulta_ventas.php" class="submenu-btn">Consultar Ventas</a>
            <a href="update_venta.php" class="submenu-btn">Actualizar Ventas</a>
        </div>

        <!-- Clientes -->
        <a href="#" class="submenu-btn" onclick="toggleClientesSubMenu()">Clientes</a>
        <div class="submenu-clientes" id="submenu-clientes">
            <a href="carrito.php" class="submenu-btn">Carrito</a>
            <a href="procesar_pago.php" class="submenu-btn">Procesar Pago</a>
        </div>
    </div>

    <div class="carousel">
        <img src="imagenes/producto1.jpg" alt="Producto 1" class="active" data-name="Producto 1">
        <img src="imagenes/producto2.jpg" alt="Producto 2" data-name="Producto 2">
        <img src="imagenes/producto3.jpg" alt="Producto 3" data-name="Producto 3">
        <div class="product-name" id="product-name">Producto 1</div>
    </div>

    <script>
        function toggleSubMenu() {
            var submenu = document.getElementById('submenu');
            submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
        }

        function toggleUsuarioSubMenu() {
            var submenuUsuarios = document.getElementById('submenu-usuarios');
            submenuUsuarios.style.display = submenuUsuarios.style.display === 'block' ? 'none' : 'block';
        }

        function toggleProveedorSubMenu() {
            var submenuProveedor = document.getElementById('submenu-proveedor');
            submenuProveedor.style.display = submenuProveedor.style.display === 'block' ? 'none' : 'block';
        }

        function toggleProductoSubMenu() {
            var submenuProducto = document.getElementById('submenu-producto');
            submenuProducto.style.display = submenuProducto.style.display === 'block' ? 'none' : 'block';
        }

        function toggleVentasSubMenu() {
            var submenuVentas = document.getElementById('submenu-ventas');
            submenuVentas.style.display = submenuVentas.style.display === 'block' ? 'none' : 'block';
        }

        function toggleClientesSubMenu() {
            var submenuClientes = document.getElementById('submenu-clientes');
            submenuClientes.style.display = submenuClientes.style.display === 'block' ? 'none' : 'block';
        }

        let currentIndex = 0;
        const images = document.querySelectorAll('.carousel img');
        const productName = document.getElementById('product-name');
        const totalImages = images.length;

        setInterval(() => {
            const nextIndex = (currentIndex + 1) % totalImages;
            
            images[currentIndex].style.transform = 'translateX(-100%)';
            images[currentIndex].classList.remove('active');

            images[nextIndex].style.transform = 'translateX(0)';
            images[nextIndex].classList.add('active');

            productName.textContent = images[nextIndex].getAttribute('data-name');

            currentIndex = nextIndex;
        }, 5000); 
    </script>
</body>
</html>
