import gi
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from BaseDatos import MetodosBD
from Clases import TablaVendedores, Main


class vendedores(Gtk.Window):

    def __init__(self, initTipo, initId, initNombre):
        """
        Recibe la catergoría, el Id y el Nombre del Vendedor que inicio sesión
        :param initTipo: Text
        :param initId: Int
        :param initNombre: Text
        """

        Gtk.Window.__init__(self, title="Vendedores " + str(initNombre))
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Obtengo la fecha local para luego metarla en el campo Fecha
        self.localTime = time.strftime("%d-%m-%Y", time.gmtime())
        print("Hora local: ", str(self.localTime) + " Clase Vendedores")

        MetodosBD.MetodosBD.listar_id_vendedores(self)

        boxV = Gtk.Box(spacing=20, orientation=Gtk.Orientation.VERTICAL)

        # Variables de uso común
        self.tipo1 = "Jefe de zona"
        self.tipo2 = "empleado"
        self.estado = ""
        self.vbtnAdd = "Dar de alta"
        self.vbtnUpdate = "Modificar datos"
        self.vbtnRefresh = "Fecha actual"
        self.vbtnRemove = "Dar de baja"
        self.vbtnClean = "Limpiar"
        self.vbtnVerTabla = "Consultar Vendedores"
        self.vbtnCerrar = "Cerrar"
        self.tipo = initTipo
        self.id = initId
        self.nombre = initNombre

        # Creamos los Frames para separar contextos
        frameInsertar = Gtk.Frame()
        frameInsertar.set_label("Dar de alta Vendedor  o Modificar")

        frameBorrar = Gtk.Frame()
        frameBorrar.set_label("Dar de baja Vendedor")

        frameConsultar = Gtk.Frame()
        frameConsultar.set_label("Consultar Vendedores")

        # Creamos los Grids
        gridtop = Gtk.Grid()
        gridtop.set_column_spacing(10)

        gridRight = Gtk.Grid()
        gridRight.set_column_spacing(40)

        gridAdd = Gtk.Grid()
        gridAdd.set_column_spacing(10)
        gridAdd.set_row_spacing(10)

        self.gridVerTabla = Gtk.Grid()
        self.gridVerTabla.set_column_spacing(40)
        self.gridVerTabla.set_row_spacing(40)

        self.gridCheckBox = Gtk.Grid()
        self.gridCheckBox.set_column_spacing(10)

        self.gridRemove = Gtk.Grid()
        self.gridRemove.set_column_spacing(40)
        self.gridRemove.set_row_spacing(40)

        # Labels

        # GridADD
        self.lblCargarValores = Gtk.Label("Cargar Datos de vendedor: ")
        self.lblDni = Gtk.Label("DNI: ")
        self.lblNombre = Gtk.Label("Nombre: ")
        self.lblApellidos = Gtk.Label("Apellidos: ")
        self.lblTelf = Gtk.Label("Teléfono de contacto: ")
        self.lblZona = Gtk.Label("Zona de trabajo: ")
        self.lblNacionalidad = Gtk.Label("Nacionalidad: ")
        self.lblFecha = Gtk.Label("Fecha: ")

        # GridRemove
        self.lblBaja = Gtk.Label("DNI vendedor: ")

        # Entrys

        # GridADD
        self.txtDni = Gtk.Entry()
        self.txtNombre = Gtk.Entry()
        self.txtApellidos = Gtk.Entry()
        self.txtTelf = Gtk.Entry()
        self.txtZona = Gtk.Entry()
        self.txtNacionalidad = Gtk.Entry()
        self.txtFecha = Gtk.Entry()
        self.txtFecha.set_editable(False)

        # RadioButton Alojado en GridCheck
        self.rbJefe = Gtk.RadioButton(label=self.tipo1)
        self.rbJefe.connect("toggled", self.on_opcion_clicked, self.rbJefe)
        self.rbJefe.set_active(False)
        self.rbEmpleado = Gtk.RadioButton.new_with_label_from_widget(self.rbJefe, label=self.tipo2)

        # Botones

        # gridAdd
        self.btnAdd = Gtk.Button(label=self.vbtnAdd)
        self.btnAdd.connect("clicked", self.on_add_clicked)
        self.btnClean = Gtk.Button(label=self.vbtnClean)
        self.btnClean.connect("clicked", self.on_limpiar)
        self.btnRefreshTime = Gtk.Button(label=self.vbtnRefresh)
        self.btnRefreshTime.connect("clicked", self.on_refreshTime)

        # gridRemove
        self.btnRemove = Gtk.Button(label=self.vbtnRemove)
        self.btnRemove.connect("clicked", self.on_remove_clicked)

        # gridTabla
        self.btnVerTabla = Gtk.Button(label=self.vbtnVerTabla)
        self.btnVerTabla.connect("clicked", self.on_tabla_vendedores_clicked)

        # GridCerrar
        self.btnCerrar = Gtk.Button(self.vbtnCerrar)
        self.btnCerrar.connect("clicked", self.on_cerrar_clicked)

        # ComboBox

        # GridAdd
        self.cbDniAdd = Gtk.ComboBoxText()
        self.cbDniAdd.set_entry_text_column(0)
        self.cbDniAdd.connect("changed", self.update_vendedor)

        # GridRemove
        self.cbDniRemove = Gtk.ComboBoxText()
        self.cbDniRemove.set_entry_text_column(0)

        # Cargamos los DNIs de los clientes en los ComboBox
        cmbBoXAdd = vendedores.actualizar_cmbDni(self)
        cmbBoXRemove = vendedores.actualizar_cmbDni(self)

        # Agregamos el RadioButton al GridCheckBox
        self.gridCheckBox.attach(self.rbJefe, 1, 0, 1, 1)
        self.gridCheckBox.attach(self.rbEmpleado, 2, 0, 1, 1)

        # Agregamos el label, comboBox y botón al GridRemove
        self.gridRemove.attach(self.lblBaja, 0, 0, 1, 1)
        self.gridRemove.attach(self.cbDniRemove, 1, 0, 1, 1)
        self.gridRemove.attach(self.btnRemove, 4, 1, 1, 1)

        # Agregamos labels, comboBox, entrys, botones y el GridCheckBox al GridAdd
        gridAdd.attach(self.lblCargarValores, 0, 0, 1, 1)
        gridAdd.attach(self.cbDniAdd, 1, 0, 1, 1)
        gridAdd.attach(self.btnClean, 2, 0, 1, 1)
        gridAdd.attach(self.lblDni, 0, 1, 1, 1)
        gridAdd.attach(self.txtDni, 0, 2, 1, 1)
        gridAdd.attach(self.gridCheckBox, 2, 2, 1, 1)
        gridAdd.attach(self.lblNombre, 0, 3, 1, 1)
        gridAdd.attach(self.txtNombre, 0, 4, 1, 1)
        gridAdd.attach(self.lblApellidos, 1, 3, 1, 1)
        gridAdd.attach(self.txtApellidos, 1, 4, 1, 1)
        gridAdd.attach(self.lblTelf, 2, 3, 1, 1)
        gridAdd.attach(self.txtTelf, 2, 4, 1, 1)
        gridAdd.attach(self.lblZona, 0, 5, 1, 1)
        gridAdd.attach(self.txtZona, 0, 6, 1, 1)
        gridAdd.attach(self.lblNacionalidad, 1, 5, 1, 1)
        gridAdd.attach(self.txtNacionalidad, 1, 6, 1, 1)
        gridAdd.attach(self.lblFecha, 0, 7, 1, 1)
        gridAdd.attach(self.txtFecha, 0, 8, 1, 1)
        gridAdd.attach(self.btnRefreshTime, 1, 8, 1, 1)
        gridAdd.attach(self.btnAdd, 2, 9, 1, 1)

        # Agregamos botón al GridTabla
        self.gridVerTabla.attach(self.btnVerTabla, 2, 0, 1, 1)

        # Agregamos los frames y el btnCerrar al GridRight
        gridRight.attach(frameBorrar, 0, 0, 1, 1)
        gridRight.attach(frameConsultar, 0, 1, 1, 2)
        gridRight.attach(self.btnCerrar, 0, 4, 1, 2)

        # Agregamos contenido a los Frames
        frameInsertar.add(gridAdd)
        frameBorrar.add(self.gridRemove)
        frameConsultar.add(self.gridVerTabla)

        # Agregamos los frames y un grid a un gridTop
        gridtop.add(frameInsertar)
        gridtop.add(gridRight)

        # Agregamos el contenido a la caja
        boxV.add(gridtop)

        self.add(boxV)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    # Metodo para almacenar en una variable que RadioButon está activo
    def on_opcion_clicked(self, control, ch1):
        res = ch1.get_active() == True
        if res:

            self.estado = self.tipo1

        else:

            self.estado = self.tipo2

        print(self.estado)

    """
    Metodo que recoge los datos introducidos por pantalla y los envía a otro Metodo 
    de la Clase MetodoBD para su insercción en la base de datos
    """

    def on_add_clicked(self, control):
        """
        Función que llama otros metodos para validar la insercción de los datos, primero se
        autentifica que los Entrys estén llenos. Luego se llama al metodo insertar de la Clase
        MetodosBD se actualizan los comboBox y por último se llama al metodo limpiar para limpiar Entrys
        :param control: Button
        :return: Nothing
        """

        vendedores.on_opcion_clicked(self, control, self.rbJefe)
        # Envio texto de Botón para que en el Metodo de la Clase MetodoBD insertar
        # sepa si tiene que insertar o modificar
        accion = self.btnAdd.get_label()

        dni = self.txtDni.get_text()
        nom = self.txtNombre.get_text()
        apellidos = self.txtApellidos.get_text()
        telf = self.txtTelf.get_text()
        zona = self.txtZona.get_text()
        nacio = self.txtNacionalidad.get_text()

        # Valor inicial de ventas de un Vendedor
        ventas = 0

        # Metodo para validar la entrada de texto que devuelve un Boolean
        condicion = vendedores.on_autentificar(self, dni, nom, apellidos, telf, zona, nacio)

        if condicion:
            # Metodo que inserta o modifica un vendedor en la base de datos
            MetodosBD.MetodosBD.insert_vendedor(self, accion, dni, self.estado, nom, apellidos, telf, zona, nacio,
                                                str(self.localTime), ventas)

            # Metodo que refresca los Combobox
            vendedores.actualizar_cmbDni(self)

            # Medoto que limpia las cajas de texto
            vendedores.on_limpiar(self, control)

    # Metodo que valida que todas los Entry tengan contenido y devuelve un boolean
    def on_autentificar(self, dni, nom, apellidos, telf, zona, nacion):
        """
        Valida que la Entry tenga contenido
        :param dni: Text
        :param nom: Text
        :param apellidos: Text
        :param telf: Text
        :param zona: Text
        :param nacion: Text
        :return: Variable booleana
        """
        condicion = True

        if dni == '':
            self.txtDni.set_placeholder_text("Inserte DNI")
            condicion = False
        elif nom == '':
            self.txtNombre.set_placeholder_text("Inserte Nombre")
            condicion = False
        elif apellidos == '':
            self.txtApellidos.set_placeholder_text("Inserte Apellidos")
            condicion = False
        elif telf == '':
            self.txtTelf.set_placeholder_text("Inserte Telefono")
            condicion = False
        elif zona == '':
            self.txtZona.set_placeholder_text("Inserte Zona")
            condicion = False
        elif nacion == '':
            self.txtNacionalidad.set_placeholder_text("Inserte Nacionalidad")
            condicion = False

        return condicion

    # Metodo que tras elegir un Dni del ComboBOx manda el Dni a un metodo
    # de la Clase MetodosBD que busca el Dni y devuelve los datos de este
    def update_vendedor(self, control):
        """
        Metodo que tras elegir un Dni del ComboBOx manda el Dni a un metodo
        de la Clase MetodosBD que busca el Dni y devuelve los datos de este
        :param control: Button
        :return: Nothing
        """

        # Sacamos el texto seleccionado del ComboBox
        dniSelect = self.cbDniAdd.get_active_text()

        # Condición para que sí no hay nada seleccionado en el Combox no haga una consula en vacío
        if not dniSelect == None:
            # Al selecionar el ComboBox el Programa Sobreentiende que vas a hacer una Modificación
            # y cambia el nombre al botónAdd
            self.btnAdd.set_label(self.vbtnUpdate)

            # Metodo de la Clase MetodosBD que busca el Dni seleccionado y devuelve los datos
            datos = MetodosBD.MetodosBD.buscar_vendedor(self, dniSelect)

            # Metodo que muestra los datos por pantalla
            vendedores.on_mostrarDatos(self, datos)

    # Metodo que separa los datos recogidos y luego los guarda en sus respectivos Entrys
    def on_mostrarDatos(self, datos):
        """
        Metodo que separa los datos recogidos y luego los guarda en sus respectivos Entrys
        :param datos: Lista de datos
        :return: Nothing
        """

        # Condición que cambia los estados de los RadioButons
        if datos[0][1] == self.tipo1:

            self.rbJefe.set_active(True)
        else:

            self.rbEmpleado.set_active(True)

        self.txtDni.set_text(datos[0][2])
        self.txtNombre.set_text(datos[0][3])
        self.txtApellidos.set_text(datos[0][4])
        self.txtTelf.set_text(datos[0][5])
        self.txtZona.set_text(datos[0][6])
        self.txtNacionalidad.set_text(datos[0][7])
        self.txtFecha.set_text(datos[0][8])

    # Metodo que recarga el valor de la fecha en el Entry Fecha
    def on_refreshTime(self, control):
        """
        Metodo que recarga el valor de la fecha en el Entry Fecha
        :param control: Button
        :return: Noting
        """

        self.txtFecha.set_text(str(self.localTime))

    # Metodo que refresca la información de los Combobox
    def actualizar_cmbDni(self):
        """
        Metodo que refresca la información de los Combobox
        :return: Nothing
        """

        # Eliminamos primero todos los datos de los comboBox
        self.cbDniAdd.remove_all()
        self.cbDniRemove.remove_all()

        # Metodo de la clase MetodosBd que devuelve el Dni de todos los usuarios
        dnis = MetodosBD.MetodosBD.listar_dni_vendedores(self)

        for rexistro in dnis:
            self.cbDniAdd.append_text(rexistro[0])
            self.cbDniRemove.append_text(rexistro[0])

    # Metodo que envia el Dni seleccionado a un Metodo de la Clase MetodosBD y elimina de
    # la base de datos al vendedor
    def on_remove_clicked(self, control):
        """
        Metodo que envia el Dni seleccionado a un Metodo de la Clase MetodosBD y elimina de
        la base de datos al vendedor, luego llama al metodo recarga los ComboBox y
        al de limpiar los Entrys
        :param control: Button
        :return: Nothin
        """

        # Recogemos el valor del ComboBox
        dniBaja = self.cbDniRemove.get_active_text()
        # Lo enviamos al metodo de la Clase MetodosBD
        MetodosBD.MetodosBD.borrar_vendedor(self, dniBaja)
        # Metodo que refresca los Combobox
        vendedores.actualizar_cmbDni(self)
        # Medoto que limpia las cajas de texto
        vendedores.on_limpiar(self, control)

    # Medoto que limpia las cajas de texto
    def on_limpiar(self, control):
        """
        Medoto que limpia las cajas de texto
        :param control: Button
        :return: Nothing
        """

        self.btnAdd.set_label(self.vbtnAdd)
        self.txtDni.set_text("")
        self.txtNombre.set_text("")
        self.txtApellidos.set_text("")
        self.txtTelf.set_text("")
        self.txtZona.set_text("")
        self.txtNacionalidad.set_text("")
        self.txtFecha.set_text("")
        self.txtDni.set_placeholder_text("")
        self.txtNombre.set_placeholder_text("")
        self.txtApellidos.set_placeholder_text("")
        self.txtTelf.set_placeholder_text("")
        self.txtZona.set_placeholder_text("")
        self.txtNacionalidad.set_placeholder_text("")

    # Metodo que abre la Clase Main y se oculta a sí mista
    def on_cerrar_clicked(self, Button):
        """
        Metodo para navegar a la ventana Main
        :param Button: Button
        :return: Nothing
        """
        main = Main.Main(self.tipo, self.id, self.nombre)
        self.set_visible(False)

    # Metodo que abre la Clase TablaVendedores y se oculta a sí mista
    def on_tabla_vendedores_clicked(self, Button):
        """
        Metodo para navegar a la ventana TablaVendedores
        :param Button: Button
        :return: Nothing
        """
        tablavendedores = TablaVendedores.tablaVendedores(self.tipo, self.id, self.nombre)
        self.set_visible(False)


if __name__ == "__main__":
    vendedores()
    Gtk.main()
