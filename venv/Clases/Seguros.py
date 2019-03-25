import gi
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from BaseDatos import MetodosBD
from Clases import TablaSeguros,Main



class seguros(Gtk.Window):

    def __init__(self, initTipo, initId, initNombre):
        """
        Recibe la catergoría, el Id y el Nombre del Vendedor que inicio sesión
        :param initTipo: Text
        :param initId: Int
        :param initNombre: Text
        """

        Gtk.Window.__init__(self, title="Seguros "+str(initNombre))
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Obtengo la fecha local para luego metarla en el campo Fecha
        self.localTime=time.strftime("%d-%m-%Y",time.gmtime())
        print("Hora local: ",str(self.localTime)+" Clase Vendedores")

        boxV = Gtk.Box(spacing=20, orientation=Gtk.Orientation.VERTICAL)

        # Variables de uso común
        self.vbtnAdd = "Añadir seguro"
        self.vbtnUpdate = "Modificar datos"
        self.vbtnRefresh = "Fecha actual"
        self.vbtnRemove = "Eliminar seguro"
        self.vbtnClean = "Limpiar"
        self.vbtnVerTabla = "Consultar Seguros"
        self.vbtnCerrar = "Cerrar"
        self.tipo=initTipo
        self.id=initId
        self.nombre = initNombre

        # Creamos los Frames para separar contextos
        frameInsertar = Gtk.Frame()
        frameInsertar.set_label("Añadir venta de un seguro")

        frameBorrar = Gtk.Frame()
        frameBorrar.set_label("Eliminar Seguro")

        frameConsultar = Gtk.Frame()
        frameConsultar.set_label("Consultar Seguros")

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
        self.lblCargarValores = Gtk.Label("Cargar Datos de Seguros: ")
        self.lblIdVendedor = Gtk.Label("Id Vendedor: ")
        self.lblDniCliente = Gtk.Label("Dni Cliente: ")
        self.lblNombreCliente = Gtk.Label("Nombre Cliente: ")
        self.lblApellidosCliente = Gtk.Label("Apellidos Cliente: ")
        self.lblTipoSeguro = Gtk.Label("Tipo de Seguro: ")
        self.lblCoste = Gtk.Label("Coste: ")
        self.lblTiempo = Gtk.Label("Tiempo activo: ")
        self.lblFecha = Gtk.Label("Fecha: ")

        # GridRemove
        self.lblBaja = Gtk.Label("Id Seguro: ")

        # Entrys

        # GridADD
        self.txtIdVendedor = Gtk.Entry()
        self.txtIdVendedor.set_text(str(self.id))
        self.txtIdVendedor.set_editable(False)
        self.txtDniCliente = Gtk.Entry()
        self.txtNombreCliente= Gtk.Entry()
        self.txtApellidoCliente = Gtk.Entry()
        self.txtTipoSeguro = Gtk.Entry()
        self.txtCoste = Gtk.Entry()
        self.txtTiempo = Gtk.Entry()
        self.txtFecha = Gtk.Entry()
        self.txtFecha.set_editable(False)

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
        self.cbIdSeguroAdd = Gtk.ComboBoxText()
        self.cbIdSeguroAdd.set_entry_text_column(0)
        self.cbIdSeguroAdd.connect("changed", self.update_seguro)

        # GridRemove
        self.cbIdSeguroRemove = Gtk.ComboBoxText()
        self.cbIdSeguroRemove.set_entry_text_column(0)

        # Cargamos los DNIs de los clientes en los ComboBox
        cmbBoXAdd = seguros.actualizar_cmbId(self)
        cmbBoXRemove = seguros.actualizar_cmbId(self)


        # Agregamos el label, comboBox y botón al GridRemove
        self.gridRemove.attach(self.lblBaja, 0, 0, 1, 1)
        self.gridRemove.attach(self.cbIdSeguroRemove, 1, 0, 1, 1)
        self.gridRemove.attach(self.btnRemove, 4, 1, 1, 1)

        # Agregamos labels, comboBox, entrys, botones y el GridCheckBox al GridAdd
        gridAdd.attach(self.lblCargarValores, 0, 0, 1, 1)
        gridAdd.attach(self.cbIdSeguroAdd, 1, 0, 1, 1)
        gridAdd.attach(self.btnClean, 2, 0, 1, 1)
        gridAdd.attach(self.lblIdVendedor, 0, 1, 1, 1)
        gridAdd.attach(self.txtIdVendedor, 0, 2, 1, 1)
        gridAdd.attach(self.lblDniCliente, 0, 3, 1, 1)
        gridAdd.attach(self.txtDniCliente, 0, 4, 1, 1)
        gridAdd.attach(self.lblNombreCliente, 1, 3, 1, 1)
        gridAdd.attach(self.txtNombreCliente, 1, 4, 1, 1)
        gridAdd.attach(self.lblApellidosCliente, 2, 3, 1, 1)
        gridAdd.attach(self.txtApellidoCliente, 2, 4, 1, 1)
        gridAdd.attach(self.lblTipoSeguro, 0, 5, 1, 1)
        gridAdd.attach(self.txtTipoSeguro, 0, 6, 1, 1)
        gridAdd.attach(self.lblCoste, 1,5, 1, 1)
        gridAdd.attach(self.txtCoste, 1, 6, 1, 1)
        gridAdd.attach(self.lblTiempo, 2, 5, 1, 1)
        gridAdd.attach(self.txtTiempo, 2, 6, 1, 1)
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


    """
    Metodo que recoge los datos introducidos por pantalla y los envía a otro Metodo 
    de la Clase MetodoBD para su insercción en la base de datos
    """

    def on_add_clicked(self, control):
        """
        Función que llama otros metodos para validar la insercción de los datos, primero se
        autentifica que los Entrys estén llenos. Luego se llama al metodo insertar de la Clase
        MetodosBD, se actualizan los comboBox y por último se llama al metodo limpiar para limpiar Entrys
        :param control: Button
        :return: Nothing
        """


        # Envio texto de Botón para que en el Metodo de la Clase MetodoBD insertar
        # sepa si tiene que insertar o modificar
        accion = self.btnAdd.get_label()

        #dni = self.txtIdVendedor.get_text()
        dniCliente = self.txtDniCliente.get_text()
        nombreCliente=self.txtNombreCliente.get_text()
        apellidoCliente=self.txtApellidoCliente.get_text()
        seguro = self.txtTipoSeguro.get_text()
        coste = self.txtCoste.get_text()
        tiempo = self.txtTiempo.get_text()
        idSeguro=self.cbIdSeguroAdd.get_active_text()

        # Metodo para validar la entrada de texto que devuelve un Boolean
        condicion = seguros.on_autentificar(self, dniCliente,nombreCliente,apellidoCliente, seguro, coste, tiempo)

        if condicion:
            # Metodo que inserta o modifica un vendedor en la base de datos
            MetodosBD.MetodosBD.insert_seguros(self,idSeguro, accion, seguro, self.id, dniCliente,nombreCliente,apellidoCliente, tiempo, coste, str(self.localTime))


            # Metodo que refresca los Combobox
            seguros.actualizar_cmbId(self)

            # Medoto que limpia las cajas de texto
            seguros.on_limpiar(self, control)

    # Metodo que valida que todas los Entry tengan contenido y devuelve un boolean
    def on_autentificar(self, dniCliente,nombreCliente,apellidoCliente, seguro, coste,tiempo):
        """
        Valida que la Entry tenga contenido
        :param dniCliente: Text
        :param nombreCliente: Text
        :param apellidoCliente: Text
        :param seguro: Text
        :param coste: Int
        :param tiempo: Int
        :return: Variable booleana
        """
        condicion = True

        if dniCliente == '':
            self.txtDniCliente.set_placeholder_text("Inserte DNI")
            condicion = False
        elif nombreCliente == '':
            self.txtNombreCliente.set_placeholder_text("Inserte Nombre")
            condicion = False
        elif apellidoCliente == '':
            self.txtApellidoCliente.set_placeholder_text("Inserte Apellidos")
            condicion = False
        elif seguro == '':
            self.txtTipoSeguro.set_placeholder_text("Inserte tipo de seguro")
            condicion = False
        elif coste == '':
            self.txtCoste.set_placeholder_text("Inserte Precio")
            condicion = False
        elif tiempo == '':
            self.txtTiempo.set_placeholder_text("Inserte Tiempo de seguro")
            condicion = False

        return condicion

    # Metodo que tras elegir un Dni del ComboBOx manda el Dni a un metodo
    # de la Clase MetodosBD que busca el Id y devuelve los datos de este
    def update_seguro(self, control):
        """
        Metodo que tras elegir un Dni del ComboBOx manda el Dni a un metodo
        de la Clase MetodosBD que busca el Id y devuelve los datos de este
        :param control: Button
        :return: Nothing
        """

        # Sacamos el texto seleccionado del ComboBox
        idSelect = self.cbIdSeguroAdd.get_active_text()

        # Condición para que sí no hay nada seleccionado en el Combox no haga una consula en vacío
        if not idSelect == None:
            # Al selecionar el ComboBox el Programa Sobreentiende que vas a hacer una Modificación
            # y cambia el nombre al botónAdd
            self.btnAdd.set_label(self.vbtnUpdate)

            # Metodo de la Clase MetodosBD que busca el Dni seleccionado y devuelve los datos
            datos = MetodosBD.MetodosBD.buscar_seguros(self, idSelect)

            # Metodo que muestra los datos por pantalla
            seguros.on_mostrarDatos(self, datos)

    # Metodo que separa los datos recogidos y luego los guarda en sus respectivos Entrys
    def on_mostrarDatos(self, datos):
        """
        Metodo que separa los datos recogidos y luego los guarda en sus respectivos Entrys
        :param datos: Lista de datos
        :return: Nothing
        """
        self.txtDniCliente.set_text(datos[0][3])
        self.txtNombreCliente.set_text(datos[0][4])
        self.txtApellidoCliente.set_text(datos[0][5])
        self.txtTipoSeguro.set_text(datos[0][1])
        self.txtCoste.set_text(str(datos[0][7]))
        self.txtTiempo.set_text(str(datos[0][6]))
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
    def actualizar_cmbId(self):
        """
        Metodo que refresca la información de los Combobox
        :return: Nothing
        """

        # Eliminamos primero todos los datos de los comboBox
        self.cbIdSeguroAdd.remove_all()
        self.cbIdSeguroRemove.remove_all()

        # Metodo de la clase MetodosBd que devuelve el Dni de todos los usuarios
        ids = MetodosBD.MetodosBD.listar_id_seguros(self)

        for rexistro in ids:
            self.cbIdSeguroAdd.append_text(str(rexistro[0]))
            self.cbIdSeguroRemove.append_text(str(rexistro[0]))

    # Metodo que envia el Dni seleccionado a un Metodo de la Clase MetodosBD y elimina de
    # la base de datos al seguro
    def on_remove_clicked(self, control):
        """
        Metodo que envia el Dni seleccionado a un Metodo de la Clase MetodosBD y elimina de
        la base de datos al seguro, luego llama al metodo recarga los ComboBox y
        al de limpiar los Entrys
        :param control: Button
        :return: Nothin
        """

        # Recogemos el valor del ComboBox
        idBaja = self.cbIdSeguroRemove.get_active_text()
        # Lo enviamos al metodo de la Clase MetodosBD
        MetodosBD.MetodosBD.borrar_Seguro(self, idBaja)
        # Metodo que refresca los Combobox
        seguros.actualizar_cmbId(self)
        # Medoto que limpia las cajas de texto
        seguros.on_limpiar(self, control)

    # Medoto que limpia las cajas de texto
    def on_limpiar(self, control):
        """
        Medoto que limpia las cajas de texto
        :param control: Button
        :return: Nothing
        """

        self.btnAdd.set_label(self.vbtnAdd)
        self.txtDniCliente.set_text("")
        self.txtNombreCliente.set_text("")
        self.txtApellidoCliente.set_text("")
        self.txtTipoSeguro.set_text("")
        self.txtCoste.set_text("")
        self.txtTiempo.set_text("")
        self.txtFecha.set_text("")

        self.txtIdVendedor.set_placeholder_text("")
        self.txtDniCliente.set_placeholder_text("")
        self.txtNombreCliente.set_placeholder_text("")
        self.txtApellidoCliente.set_placeholder_text("")
        self.txtTipoSeguro.set_placeholder_text("")
        self.txtCoste.set_placeholder_text("")
        self.txtTiempo.set_placeholder_text("")


    # Metodo que abre la Clase Main y se oculta a sí mista
    def on_cerrar_clicked(self, Button):
        """
        Metodo para navegar a la ventana Main
        :param Button: Button
        :return: Nothing
        """
        main = Main.Main(self.tipo, self.id,self.nombre)
        self.set_visible(False)

    # Metodo que abre la Clase TablaVendedores y se oculta a sí mista
    def on_tabla_vendedores_clicked(self, Button):
        """
        Metodo para navegar a la ventana TablaSeguros
        :param Button: Button
        :return: Nothing
        """
        tablaseguros = TablaSeguros.tablaSeguros(self.tipo, self.id,self.nombre)
        self.set_visible(False)


if __name__ == "__main__":
    seguros()
    Gtk.main()