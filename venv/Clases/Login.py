import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from BaseDatos import MetodosBD
from Clases import Main



class Login(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Seguros")
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        grid = Gtk.Grid()

        boxV = Gtk.Box(spacing=0, orientation=Gtk.Orientation.VERTICAL)


        '''Creando elementos'''
        #Label
        self.lblLogin = Gtk.Label(label="App tu Seguro", margin=20)
        # Imagenes
        self.imgUsu = Gtk.Image(margin_bottom=40)
        self.imgUsu.set_from_file("Images/user.png")
        self.imgPass = Gtk.Image(margin_bottom=40)
        self.imgPass.set_from_file("Images/passw.png")
        #Cajas de texto
        self.txtNombre = Gtk.Entry()
        self.txtPassword =Gtk.Entry()
        self.txtPassword.set_visibility(False)
        #Botón
        self.btnInicio=Gtk.Button(label="Iniciar")
        self.btnInicio.connect("clicked",self.on_iniciar_clicked)

        '''Añadiendo elementos a la Box'''
        boxV.add(self.lblLogin)
        boxV.pack_start(self.imgUsu,True,True,0)
        boxV.pack_start(self.txtNombre, True, True, 0)
        boxV.add(self.imgPass)
        boxV.add(self.txtPassword)
        boxV.add(self.btnInicio)


        self.add(boxV)

        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def on_iniciar_clicked(self,button):

        encontrado=MetodosBD.MetodosBD.autentificar_login(self,self.txtNombre.get_text(),self.txtPassword.get_text())

        if(encontrado==True):
            datos = MetodosBD.MetodosBD.comprobar_tipo(self, self.txtNombre.get_text())

            tipo = datos[0][1]
            id = datos[0][0]
            nombre=datos[0][2]
            main= Main.Main(tipo,id,nombre)
            self.set_visible(False)
        else:
            Login.on_limpiar(self)
            messageDialog=Gtk.MessageDialog(parent=self,flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.WARNING,buttons=Gtk.ButtonsType.OK,message_format="Usuario no encontrado")
            response=messageDialog.run()
            if(response==Gtk.ResponseType.OK):
                messageDialog.destroy()

    def on_limpiar(self):
        self.txtNombre.set_text("")
        self.txtPassword.set_text("")


if __name__ == "__main__":
    Login()
    Gtk.main()
