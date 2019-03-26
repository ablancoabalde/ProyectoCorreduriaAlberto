import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Clases import Vendedores
from Clases import Seguros
from Clases import Configuracion
from Clases import Login
from BaseDatos import MetodosBD

class Main(Gtk.Window):

    def __init__(self, initTipo, initId, initNombre):
        """
        Recibe la catergoría, el Id y el Nombre del Vendedor que inicio sesión
        :param initTipo: Text
        :param initId: Int
        :param initNombre: Text
        """

        Gtk.Window.__init__(self, title="Menu "+str(initNombre))
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        boxV = Gtk.Box(spacing=0, orientation=Gtk.Orientation.VERTICAL)
        # Variables de uso común
        self.tipo1 = "Jefe de zona"
        self.tipo = initTipo
        self.id = initId
        self.nombre = initNombre

        #Creación de botones
        self.btnVendedores = Gtk.Button(label="Vendedores")
        self.btnVendedores.connect("clicked", self.on_vendedores_clicked)
        self.btnSeguros = Gtk.Button(label="Seguros")
        self.btnSeguros.connect("clicked", self.on_seguros_clicked)
        self.btnConfig= Gtk.Button(label="Configuración")
        self.btnConfig.connect("clicked", self.on_configuracion_clicked)
        self.btnCerrar = Gtk.Button(label="Cerrar Sesión")
        self.btnCerrar.connect("clicked", self.on_cerrar_clicked)



        if( self.tipo==self.tipo1):

            boxV.add(self.btnVendedores)
            boxV.add(self.btnSeguros)
            boxV.add(self.btnConfig)
            boxV.add(self.btnCerrar)

        else:

            boxV.add(self.btnSeguros)
            boxV.add(self.btnConfig)
            boxV.add(self.btnCerrar)



        self.add(boxV)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def on_vendedores_clicked(self,Button):
        """
        Metodo para navegar a la ventana Vendedores
        :param Button: Button
        :return: Nothing
        """
        vendedores = Vendedores.vendedores(self.tipo, self.id,self.nombre)
        self.set_visible(False)

    def on_seguros_clicked(self,Button):
        """
        Metodo para navegar a la ventana Seguros
        :param Button: Button
        :return: Nothing
        """
        seguros = Seguros.seguros(self.tipo, self.id,self.nombre)
        self.set_visible(False)

    def on_configuracion_clicked(self,Button):
        """
        Metodo para navegar a la ventana Configuración
        :param Button: Button
        :return: Nothing
        """
        confi = Configuracion.configuracion(self.tipo, self.id,self.nombre)
        self.set_visible(False)

    def on_cerrar_clicked(self,Button):
        """
        Metodo para navegar a la ventana Login
        :param Button: Button
        :return: Nothing
        """
        login = Login.Login()
        self.set_visible(False)


if __name__ == "__main__":
    Main()
    Gtk.main()
