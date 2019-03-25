import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Clases import Main
from BaseDatos import MetodosBD

class configuracion(Gtk.Window):

    def __init__(self, initTipo, initId, initNombre):
        """
        Recibe la catergoría, el Id y el Nombre del Vendedor que inicio sesión
        :param initTipo: Text
        :param initId: Int
        :param initNombre: Text
        """

        Gtk.Window.__init__(self, title="Configuración " +str(initNombre))
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        boxV = Gtk.Box(spacing=0, orientation=Gtk.Orientation.VERTICAL)
        # Variables de uso común
        self.tipo1 = "Jefe de zona"
        self.tipo=initTipo
        self.id=initId
        self.nombre = initNombre
        self.vbtnAdd = "Modificar datos"

        # Creamos los Frames para separar contextos
        frameInsertar = Gtk.Frame()
        frameInsertar.set_label("Datos Usuarios")

        # Creamos los Grids
        gridtop = Gtk.Grid()
        gridtop.set_column_spacing(10)

        # Labels

        # GridTop
        self.lblNombre = Gtk.Label("Nombre: ")
        self.lblPassword = Gtk.Label("Password: ")

        # Entrys

        # GridTop
        self.txtNombre = Gtk.Entry()
        self.txtNombre.set_text(self.nombre)
        self.txtNombre.set_editable(False)
        self.txtPassword = Gtk.Entry()

        # Botones

        # GridAdd
        self.btnAdd = Gtk.Button(label=self.vbtnAdd)
        self.btnAdd.connect("clicked", self.on_add_clicked)

        # GridCerrar
        self.btnCerrar = Gtk.Button(label="Cerrar Sesión")
        self.btnCerrar.connect("clicked", self.on_cerrar_clicked)

        # Agregamos labels, comboBox, entrys, botones y el GridCheckBox al GridAdd
        gridtop.attach(self.lblNombre, 0, 0, 1, 1)
        gridtop.attach(self.txtNombre, 1, 0, 1, 1)
        gridtop.attach(self.lblPassword, 0, 1, 1, 1)
        gridtop.attach(self.txtPassword, 1, 1, 1, 1)
        gridtop.attach(self.btnAdd, 2, 2, 1, 1)

        # Agregamos contenido a los Frames
        frameInsertar.add(gridtop)

        boxV.add(frameInsertar)
        boxV.add(self.btnCerrar)

        self.add(boxV)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def on_add_clicked(self, control):
        """
        Función que llama otros metodos para validar la insercción de los datos, primero se
        autentifica que los Entrys estén llenos. Luego se llama al metodo insertar de la Clase
        MetodosBD y por último se llama al metodo limpiar para limpiar Entrys
        :param control: Button
        :return: Nothing
        """

        # Envio texto de Botón para que en el Metodo de la Clase MetodoBD insertar
        # sepa si tiene que insertar o modificar
        accion = self.btnAdd.get_label()

        # dni = self.txtIdVendedor.get_text()
        nombre = self.txtNombre.get_text()
        password = self.txtPassword.get_text()


        # Metodo para validar la entrada de texto que devuelve un Boolean
        condicion = configuracion.on_autentificar(self,password)

        if condicion:
            # Metodo que inserta o modifica un vendedor en la base de datos
            MetodosBD.MetodosBD.insert_user_password(self, accion,nombre,password)

            # Medoto que limpia las cajas de texto
            configuracion.on_limpiar(self, control)

        # Metodo que valida que todas los Entry tengan contenido y devuelve un boolean

    def on_autentificar(self,password):
        """
        Valida que la Entry tenga contenido
        :param password: Text
        :return: Variable booleana
        """
        condicion = True

        if password == '':
            self.txtNombreCliente.set_placeholder_text("Inserte password")
            condicion = False


        return condicion

    # Medoto que limpia las cajas de texto
    def on_limpiar(self, control):
        """
        Metodo que limpia los Entrys
        :param control: Button
        :return: Nothing
        """


        self.txtPassword.set_text("")
        self.txtPassword.set_placeholder_text("")



    def on_cerrar_clicked(self,Button):
        """
        Metodo para navegar a la ventana Main
        :param Button: Button
        :return: Nothing
        """
        main=Main.Main(self.tipo, self.id,self.nombre )
        self.set_visible(False)


if __name__ == "__main__":
    configuracion()
    Gtk.main()
