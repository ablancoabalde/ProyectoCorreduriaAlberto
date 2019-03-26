Proyecto Correduría de seguros Alberto
**************************************

Este proyecto intenta simular una gestión de una correduría, que incluye Vendedores y Seguros en su Base de Datos.


Listado de Clases
=================

-BaseDatos
	1.MetodosBD
-Clases
	1.Login
	2.Main
	3.Vendedores
	4.Seguros
	5.Configuración
	6.TablaVendedores
	7.TablaSeguros

Login
-----

El login es el portal de entrada de la Aplicación tiene varios usuarios con sus respectivas contraseñas, pero como prueba podemos usar el usuario admin y contraseña 1234 para ver como jefe de zona o usuario luis y contraseña 1234 para verla como empleado.

Main
----

El main es el navegador hacia las 2 o 3 opciones de manejo que tiene el programa, estas opciones vienen dadas según el tipo del empleado que se loguea. Desde aquí podemos ir a la ventana Vendedores, que administra los vendedores, Seguros que administra los seguros y la Configuración, que administra a los Usuarios.

Vendedores
----------

En esta ventana podemos Insertar nuevos vendedores cubriendo todos los datos del nuevo vendedor, podemos Modificar datos cargando primero un vendedor, buscandolo a traves del desplegable, podemos Eliminar una vendedor, un botón que abre otra ventana que muestra una tabla de vendedores y un botón cerrar que te regresa a la ventana Main.

Seguros
-------
En esta ventana podemos Insertar nuevos seguros cubriendo todos los datos del nuevo seguro, podemos Modificar datos cargando primero un seguro, buscandolo a traves del desplegable, podemos Eliminar una seguro, un botón que abre otra ventana que muestra una tabla de seguros y un botón cerrar que te regresa a la ventana Main.

Configuración
-------------

En esta ventana Modificamos la contraseña del usuario que está registrado.

TablaVendedores
---------------

En esta ventana hacemos consultas sobre la base de datos para encontrar vendedores, ya seá buscandolos por el campo nombre, por el dni o mostrando todos. Tambien generamos un pdf con las ventas de los Vendedores. Y un botón cerrar que vuelve a la ventana Vendedores

TablaSeguros
---------------

En esta ventana hacemos consultas sobre la base de datos para encontrar seguros, ya seá buscandolos por el campo nombre, por el Id del seguro o mostrando todos. Tambien generamos un pdf tras selecionar de la tabla un cliente que simula una factura. Y un botón cerrar que vuelve a la ventana Seguros

Imagenes
--------

Estas imagenes son para la ventana Login

.. figure:: _static/user.png
   :align: center

.. figure:: _static/passw.png
   :align: center
