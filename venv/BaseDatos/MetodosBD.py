
from  sqlite3 import dbapi2
from sqlite3.dbapi2 import Connection, Cursor
from Clases import Vendedores


class MetodosBD:


    #Metddos comunes
    def conectar(self):
        """
        Función que conecta la base de datos
        :return: cursor
        """

        MetodosBD.bbdd = dbapi2.connect("BaseAlberto.db")
        cursor = MetodosBD.bbdd.cursor()

        return cursor

    def cerrar(self):
        """
        Función que cierra la base de datos
        :return: Nothing
        """
        try:
            MetodosBD.bbdd.close()
        except dbapi2.DatabaseError as erroSQL:
            print("Error al cierre de conexión: "+str(erroSQL))

    #Metodos Ventana Login


    def autentificar_login(self,nombre,password):
        """
        Metodo que verifica que el usuario y la contraseña recibidos están en la base de datos
        :param nombre: Text
        :param password: Text
        :return: Una condición de verdadero o falso dependiendo de que encuentre el usuario
        """
        try:

            cursor = MetodosBD.conectar(self)

            resultados=cursor.execute("select count(*) from Usuarios where Nombre=? and Password=?",(nombre,password)).fetchall()
            MetodosBD.cerrar(self)
            #print("Usuarios encontracdos = "+str(resultados[0][0])+ " Clase MetodosBD ")

            if(resultados[0][0]>0):
                return True
            else:
                return False

        except dbapi2.DatabaseError as errorAutentificar:
            print("Error en la consulta: " + str(errorAutentificar))


    def comprobar_tipo(self,nombre):
        """
        Comprueba la categoría del vendedor, hay 2 clases, Jefe de zona que pueden modificar otros
        vendedores o empleados que solo pueden modificar seguros
        :param nombre: Text
        :return: Retorna 3 valores Id del vendedor, su categoría(tipo) y su nombre
        """

        try:
            cursor = MetodosBD.conectar(self)

            datos=cursor.execute("select Id,Tipo,Nombre from Vendedores where Nombre='"+nombre+"'").fetchall()

            #print("Datos ID y Categoría de vendedor " + str(datos)+" Clase MetodosBD")
            MetodosBD.cerrar(self)
            return datos


        except dbapi2.DatabaseError as errorTipo:
            print("Error al comprobar el tipo: " + str(errorTipo))


    #Metodos ventana Ventanas

    #Metodo para agregar un nuevo vendedor a la base de datos
    def insert_vendedor(self,accion,dni,tipo,nombre,apellidos,telf,zona,nacionalidad,fecha,ventas):
        """
        Metodo para insertar en la base de datos, la variable acción se utiliza para que con un botón
        dependiendo del texto que tenga puedas o insertar o modificar un vendedor.
        Por defecto a todos los vendedores nuevos le pone la contraseá 1234, que luego cuando se
        logueen ellos puedan cambiar
        :param accion: Text
        :param dni: Text
        :param tipo: Text
        :param nombre: Text
        :param apellidos: Text
        :param telf: Text
        :param zona: Text
        :param nacionalidad: Text
        :param fecha: Text
        :param ventas: Float
        :return: Nothing
        """

        self.vbtnAdd = "Dar de alta"

        if  self.vbtnAdd==accion:
            self.password="1234"
            try:
                cursor= MetodosBD.conectar(self)
                cursor.execute("INSERT INTO Vendedores (Tipo, Dni, Nombre, Apellidos, Telf, Zona, Nacionalidad, Fecha,Ventas) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)",
                (tipo,dni,nombre,apellidos,telf,zona,nacionalidad,fecha,ventas))
                MetodosBD.bbdd.commit()
                MetodosBD.cerrar(self)

                MetodosBD.insert_user_password(self,accion,nombre,self.password)

            except dbapi2.DatabaseError as errorInserccionVendedor:
                print("Error al insertar: " + str(errorInserccionVendedor))


        else:

            try:

                cursor = MetodosBD.conectar(self)
                cursor.execute("UPDATE Vendedores SET Tipo=?, Dni=?, Nombre=?, Apellidos=?, Telf=?, Zona=?, Nacionalidad=?, Fecha=?,Ventas=? WHERE Dni=?",
                (tipo, dni, nombre, apellidos, telf, zona, nacionalidad, fecha, ventas,dni))
                MetodosBD.bbdd.commit()
                MetodosBD.cerrar(self)


            except dbapi2.DatabaseError as errorModificacionVendedor:
                print("Error al modificar: " + str(errorModificacionVendedor))



    #Metodo para eliminar un vendedor de la base de datos

    def borrar_vendedor(self,dni):
        """
        Metodo para eliminar un vendedor de la base de datos, recibe como parametro de busca el Dni
        del vendedor
        :param dni: Text
        :return: Nothing
        """

        try:

            cursor=MetodosBD.conectar(self)
            cursor.execute("DELETE from Vendedores where Dni='"+dni+"'").fetchall()
            MetodosBD.bbdd.commit()
            MetodosBD.cerrar(self)

        except dbapi2.DatabaseError as errorBorrarVend:
            print("Error al comprobar el tipo: " + str(errorBorrarVend))

    # Metodo para listar los vendedores
    def listar_vendedores(self):
        """
        Metodo que lista todos los vendedores de la base de datos y toda su información
        :return: Una lista con toda la informacion de todos los vendedores
        """

        try:
            cursor=MetodosBD.conectar(self)
            resultados=cursor.execute("SELECT * from Vendedores")
            vendedores= resultados.fetchall()
            MetodosBD.cerrar(self)

            return vendedores

        except dbapi2.DatabaseError as errorListarVendedores:
            print("Error al comprobar el tipo: " + str(errorListarVendedores))

    #Metodo para listar los Dnis de los vendedores
    def listar_dni_vendedores(self):
        """
         Metodo que recupera todos los DNIs de los vendedores de la base de datos
        :return: Una lista con todos los DNIs de todos los vendedores
        """
        try:
            cursor = MetodosBD.conectar(self)
            resultados = cursor.execute("SELECT Dni from Vendedores")
            dniVendedores = resultados.fetchall()
            MetodosBD.cerrar(self)

            return dniVendedores

        except dbapi2.DatabaseError as errorListarDniVendedores:
            print("Error al comprobar el tipo: " + str(errorListarDniVendedores))

    #Metodo para listar los Dnis de los vendedores
    def listar_id_vendedores(self):
        """
        Metodo con tres funciones primero recupera los Id de los vendedores
        luego recorre esos Id cada Id lo envía a otro medodo que con ese Id sabe que cuantos seguros
        vendio y el total que lleva ganado y por último actualiza la información de los vendedores
        :return:
        """
        try:
            cursor = MetodosBD.conectar(self)
            resultados = cursor.execute("SELECT Id from Vendedores")
            idVendedores = resultados.fetchall()

            for idRegistro in idVendedores:
                resultado= MetodosBD.sumar_seguros(self,idRegistro)
                idV = str(idRegistro[0])
                try:

                    cursor2 = MetodosBD.conectar(self)
                    cursor2.execute(
                        "UPDATE Vendedores SET Ventas=? WHERE Id=?",
                        (resultado, idV))
                    MetodosBD.bbdd.commit()
                    MetodosBD.cerrar(self)


                except dbapi2.DatabaseError as errorModificacionVentas:
                    print("Error al modificar: " + str(errorModificacionVentas))

            MetodosBD.cerrar(self)



        except dbapi2.DatabaseError as errorListarIdVendedores:
            print("Error al comprobar el tipo: " + str(errorListarIdVendedores))


    #Metodo para buscar los datos de un vendedor a partir de su DNI
    def buscar_vendedor(self,dni):

        try:

            cursor=MetodosBD.conectar(self)
            if not dni==None:
                resultados =cursor.execute("SELECT * from Vendedores where Dni='"+dni+"'")
                datos=tuple(resultados.fetchall())
                return datos

            MetodosBD.cerrar(self)



        except dbapi2.DatabaseError as errorBuscarVendedor:
            print("Error al comprobar el tipo: " + str(errorBuscarVendedor))
        # Metodo para buscar los datos de un vendedor a partir de su DNI

    def buscar_vendedor_id(self, id):

        try:

            cursor = MetodosBD.conectar(self)
            if not id == None:
                resultados = cursor.execute("SELECT Nombre from Vendedores where Id='" + id + "'")
                datos = tuple(resultados.fetchall())

                return datos[0][0]

            MetodosBD.cerrar(self)



        except dbapi2.DatabaseError as errorBuscarVendedor:
            print("Error al comprobar el tipo: " + str(errorBuscarVendedor))

    # Metodo para buscar los datos de un vendedor a partir de su nombre
    def buscar_vendedor_nombre(self,nombre):

        try:

            cursor=MetodosBD.conectar(self)
            if not nombre==None:


                resultados =cursor.execute("SELECT * from Vendedores where Nombre LIKE'"+nombre+"%'")
                datos=tuple(resultados.fetchall())
                return datos



            MetodosBD.cerrar(self)



        except dbapi2.DatabaseError as errorBuscarVendedor:
            print("Error al comprobar el tipo: " + str(errorBuscarVendedor))

    # Metodos ventana Seguros

    # Metodo para agregar un nuevo seguro a la base de datos

    def insert_seguros(self,idSeguro, accion, seguro, idVendedor, dniCliente,nombreCliente,apellidosCliente, tiempo, coste, fecha):
        self.vbtnAdd = "Añadir seguro"

        if self.vbtnAdd == accion:

            try:
                cursor = MetodosBD.conectar(self)
                cursor.execute(
                    "INSERT INTO Seguros (Seguro, IdVendedor, DniCliente,NombreCliente,ApellidosCliente, Tiempo, Coste, Fecha) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (seguro, idVendedor, dniCliente,nombreCliente,apellidosCliente, tiempo, coste, fecha))
                MetodosBD.bbdd.commit()
                MetodosBD.cerrar(self)

            except dbapi2.DatabaseError as errorInserccionSeguro:
                print("Error al insertar: " + str(errorInserccionSeguro))


        else:

            try:

                cursor = MetodosBD.conectar(self)
                cursor.execute(
                    "UPDATE Seguros SET Seguro=?, IdVendedor=?, DniCLiente=?, NombreCliente=?,ApellidosCliente=?, Tiempo=?, Coste=?, Fecha=? WHERE Id=?",
                    (seguro, idVendedor, dniCliente,nombreCliente,apellidosCliente, tiempo, coste, fecha, idSeguro))
                MetodosBD.bbdd.commit()
                MetodosBD.cerrar(self)


            except dbapi2.DatabaseError as errorModificacionSeguro:
                print("Error al modificar: " + str(errorModificacionSeguro))

    # Metodo para eliminar un seguro de la base de datos

    def borrar_Seguro(self, idSeguro):

        try:

            cursor = MetodosBD.conectar(self)
            cursor.execute("DELETE from Seguros where Id='" + idSeguro + "'").fetchall()
            MetodosBD.bbdd.commit()
            MetodosBD.cerrar(self)

        except dbapi2.DatabaseError as errorBorrarSeguro:
            print("Error al comprobar el tipo: " + str(errorBorrarSeguro))

    # Metodo para listar los Seguros

    def listar_seguros(self):
        try:
            cursor = MetodosBD.conectar(self)
            resultados = cursor.execute("SELECT * from Seguros")
            seguros = tuple(resultados.fetchall())
            MetodosBD.cerrar(self)

            return seguros

        except dbapi2.DatabaseError as errorListarVendedores:
            print("Error al comprobar el tipo: " + str(errorListarVendedores))

        # Metodo para listar los Ids de los Seguros

    def listar_id_seguros(self):
        try:
            cursor = MetodosBD.conectar(self)
            resultados = cursor.execute("SELECT Id from Seguros")
            idSeguros = tuple(resultados.fetchall())
            MetodosBD.cerrar(self)

            return idSeguros

        except dbapi2.DatabaseError as errorListarIdSeguros:
            print("Error al comprobar el tipo: " + str(errorListarIdSeguros))

        # Metodo para buscar los datos de un seguro a partir de su Id

    def buscar_seguros(self, id):

        try:

            cursor = MetodosBD.conectar(self)
            if not id == None:
                resultados = cursor.execute("SELECT * from Seguros where Id='" + id + "'")
                datos = tuple(resultados.fetchall())
                return datos

            MetodosBD.cerrar(self)



        except dbapi2.DatabaseError as errorBuscarSeguro:
            print("Error al comprobar el tipo: " + str(errorBuscarSeguro))

    # Metodo para buscar los datos de un cliente a partir de su nombre

    def buscar_seguro_nombre_cliente(self, nombre):

        try:

            cursor = MetodosBD.conectar(self)
            if not nombre == None:
                resultados = cursor.execute("SELECT * from Seguros where NombreCliente LIKE'" + nombre + "%'")
                datos = tuple(resultados.fetchall())
                return datos

            MetodosBD.cerrar(self)



        except dbapi2.DatabaseError as errorBuscarVendedor:
            print("Error al comprobar el tipo: " + str(errorBuscarVendedor))

    def sumar_seguros(self,idVendedor):
        self.sumaT=0
        try:

            idV=str(idVendedor[0])
            cursor = MetodosBD.conectar(self)

            resultados = cursor.execute("SELECT Coste from Seguros where IdVendedor='" + idV + "'")
            datos = tuple(resultados.fetchall())

            for dato in datos:
                self.sumaT = self.sumaT+dato[0]

            return   self.sumaT

            MetodosBD.cerrar(self)



        except dbapi2.DatabaseError as errorSumarSeguros:
            print("Error al sumar seguros: " + str(errorSumarSeguros))

    # Metodos Ventana Configuracion

    def insert_user_password(self,accion,nombre,password):
        self.vbtnAdd = "Dar de alta"

        if self.vbtnAdd == accion:

            try:
                cursor = MetodosBD.conectar(self)
                cursor.execute(
                    "INSERT INTO Usuarios (Nombre, Password) VALUES (?, ?)",
                    (nombre,password))
                MetodosBD.bbdd.commit()
                MetodosBD.cerrar(self)

            except dbapi2.DatabaseError as errorInserccionSeguro:
                print("Error al insertar: " + str(errorInserccionSeguro))


        else:

            try:

                cursor = MetodosBD.conectar(self)
                cursor.execute(
                    "UPDATE Usuarios SET Password=? WHERE Nombre=?",
                    (password, nombre))
                MetodosBD.bbdd.commit()
                MetodosBD.cerrar(self)


            except dbapi2.DatabaseError as errorModificacionPassword:
                print("Error al modificar: " + str(errorModificacionPassword))