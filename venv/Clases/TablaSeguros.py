import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from BaseDatos import MetodosBD
from Clases import Seguros
from reportlab.pdfgen import canvas


class tablaSeguros(Gtk.Window):

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


        self.boxV = Gtk.Box(spacing=20, orientation=Gtk.Orientation.VERTICAL)

        # Variables de uso común
        self.vbtnBuscar="Buscar"
        self.vbtnMostrarTodo="Mostrar Todo"
        self.vbtnFacturas = "Generar factura PDF"
        self.vbtnCerrar= "Cerrar"
        self.tipo=initTipo
        self.id=initId
        self.nombre = initNombre

        # Creamos los Frames para separar contextos
        frameTabla= Gtk.Frame()
        frameTabla.set_label("Tabla")

        # Creamos los Grids
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(10)
        self.gridTabla = Gtk.Grid()
        self.gridTabla.set_column_spacing(10)
        self.gridCerrar = Gtk.Grid()
        self.gridCerrar.set_column_spacing(10)

        # Labels

        #Grid
        self.lblId = Gtk.Label("ID: ")
        self.lblNombre = Gtk.Label("Nombre Cliente: ")

        #GridCerrar
        self.lblFactura = Gtk.Label("Realizar factura PDF: ")

        #Entrys

        #Grid
        self.txtNombre = Gtk.Entry()
        self.txtNombre.connect("changed", self.on_consultaTxt_clicked)

        # ComboBox

        # Grid
        self.cbIdBuscar = Gtk.ComboBoxText()
        self.cbIdBuscar.set_entry_text_column(0)

        # Botones

        # Grid

        self.btnConsultar = Gtk.Button(self.vbtnBuscar)
        self.btnConsultar.connect("clicked", self.on_consultaCB_clicked)
        self.btnMostrar = Gtk.Button(self.vbtnMostrarTodo)
        self.btnMostrar.connect("clicked", self.on_mostrar_click)

        # GridCerrar
        self.btnCerrar = Gtk.Button(self.vbtnCerrar)
        self.btnCerrar.connect("clicked", self.on_cerrar_clicked)
        self.btnFactura = Gtk.Button(self.vbtnFacturas)
        self.btnFactura.connect("clicked", self.on_crearPdf_click)

        #Tabla Vendedores
        #self.columnas = ["IdSeguro","Seguro" "IdVendedor","Dni Cliente", "Nombre", "Apellidos", "Tiempo", "Coste", "Fecha"]
        self.modelo = Gtk.ListStore(int, str, int, str,str, str, int, float, str)
        #self.axenda = []
        self.vista = Gtk.TreeView(model=self.modelo)

        self.seleccion = self.vista.get_selection()
        self.seleccion.connect("changed", self.on_selection_changed)

        self.celdaTexto = Gtk.CellRendererText()
        """ Con esto otro hacemos que la vista se actualice"""
        self.celdaTexto.connect("edited", self.on_celdaText_edited, self.modelo)

        """Agregamos sroll a la tabla"""
        self.scrollTree = Gtk.ScrolledWindow(hexpand=True,vexpand=True)
        self.scrollTree.add_with_viewport(self.vista)
        """Agregamos la función de ordenar según la categoría que pinchemos"""
        self.columnaId=Gtk.TreeViewColumn('Id Seguro',self.celdaTexto,text=0)
        self.columnaId.set_sort_column_id(0)
        self.vista.append_column(self.columnaId)

        self.columnaSeguro=Gtk.TreeViewColumn('Seguro', self.celdaTexto, text=1)
        self.columnaSeguro.set_sort_column_id(1)
        self.vista.append_column(self.columnaSeguro)

        self.columnaIdVendedor=Gtk.TreeViewColumn('Id Vendedor', self.celdaTexto, text=2)
        self.columnaIdVendedor.set_sort_column_id(2)
        self.vista.append_column(self.columnaIdVendedor)

        self.columnaDniCliente=Gtk.TreeViewColumn('Dni Cliente', self.celdaTexto, text=3)
        self.columnaDniCliente.set_sort_column_id(3)
        self.vista.append_column(self.columnaDniCliente)

        self.columnaNombre=Gtk.TreeViewColumn('Nombre', self.celdaTexto, text=4)
        self.columnaNombre.set_sort_column_id(4)
        self.vista.append_column(self.columnaNombre)

        self.columnaApellidos=Gtk.TreeViewColumn('Apellidos', self.celdaTexto, text=5)
        self.columnaApellidos.set_sort_column_id(5)
        self.vista.append_column(self.columnaApellidos)

        self.columnaTiempo=Gtk.TreeViewColumn('Tiempo', self.celdaTexto, text=6)
        self.columnaTiempo.set_sort_column_id(6)
        self.vista.append_column(self.columnaTiempo)

        self.columnaCoste=Gtk.TreeViewColumn('Coste', self.celdaTexto, text=7)
        self.columnaCoste.set_sort_column_id(7)
        self.vista.append_column(self.columnaCoste)

        self.columnaFecha=Gtk.TreeViewColumn('Fecha',self.celdaTexto,text=8)
        self.columnaFecha.set_sort_column_id(8)
        self.vista.append_column(self.columnaFecha)


        # Agregamos labels,,ComboBox, botones al Grid 1
        self.grid.attach(self.lblNombre, 0, 0, 1, 1)
        self.grid.attach(self.txtNombre, 1, 0, 1, 1)
        self.grid.attach(self.lblId, 0, 1, 1, 1)
        self.grid.attach(self.cbIdBuscar, 1, 1, 1, 1)
        self.grid.attach(self.btnConsultar, 2, 1, 1, 1)
        self.grid.attach(self.btnMostrar, 3, 1, 1, 1)

        # Agregamos labels,,ComboBox, botones al GridCerrar
        self.gridCerrar.attach(self.btnCerrar, 0, 0, 2, 1)
        self.gridCerrar.attach(self.lblFactura, 2, 0, 1, 1)
        self.gridCerrar.attach(self.btnFactura, 3, 0, 1, 1)

        # Cargamos el DNI de los clientes en un ComboBox
        cmbBoXAdd = tablaSeguros.actualizar_cmbId(self)

        frameTabla.add(self.scrollTree)
        self.gridTabla.add(frameTabla)

        self.boxV.add(self.grid)
        self.boxV.add(self.gridTabla)
        self.boxV.add(self.gridCerrar)
        self.add(self.boxV)


        self.connect("destroy", Gtk.main_quit)
        self.show_all()

        # Metodo que refresca la información de los Combobox

    def actualizar_cmbId(self):
        """
        Metodo que refresca la información de los Combobox
        :return: Nothing
        """

        # Eliminamos primero todos los datos de los comboBox
        self.cbIdBuscar.remove_all()


        # Metodo de la clase MetodosBd que devuelve el Dni de todos los usuarios
        ids = MetodosBD.MetodosBD.listar_id_seguros(self)

        for rexistro in ids:
            self.cbIdBuscar.append_text(str(rexistro[0]))



    def on_celdaText_edited(self,control,punteiro,texto, modelo):
        """
        Metodo que permite seleccionar el TreeView para obtener los datos
        :param control: TreeView
        :param punteiro: Posición
        :param texto: Text
        :param modelo: Formato de la tabla
        :return: Nothing
        """
        modelo[punteiro][0]=texto


    def on_mostrar_click(self, control):
        """
        Muestra la información sacada todos los seguros de la base de datos en el TreeView
        :param control: Button
        :return: Nothing
        """
        # self.columnas = ["IdSeguro","Seguro" "IdVendedor","Dni Cliente", "Nombre", "Apellidos", "Tiempo", "Coste", "Fecha"]

        self.modelo.clear()
        datos = MetodosBD.MetodosBD.listar_seguros(self)
        tamañoDatos=len(datos)
        for i in range(tamañoDatos):

            d1=datos[i][0]
            d2=datos[i][1]
            d3=datos[i][2]
            d4=datos[i][3]
            d5=datos[i][4]
            d6=datos[i][5]
            d7=datos[i][6]
            d8=datos[i][7]
            d9=datos[i][8]
            self.modelo.append([d1, d2, d3, d4, d5, d6, d7, d8, d9])


    def on_consultaCB_clicked(self,control):
        """
        Muestra la información sacada de la base de datos buscada por Iden el TreeView
        :param control: Button
        :return: Nothing
        """

        idSelect = self.cbIdBuscar.get_active_text()

        if not idSelect == None:
            self.modelo.clear()
            datos = MetodosBD.MetodosBD.buscar_seguros(self,idSelect)

            d1 = datos[0][0]
            d2 = datos[0][1]
            d3 = datos[0][2]
            d4 = datos[0][3]
            d5 = datos[0][4]
            d6 = datos[0][5]
            d7 = datos[0][6]
            d8 = datos[0][7]
            d9 = datos[0][8]
            self.modelo.append([d1, d2, d3, d4, d5, d6, d7, d8, d9])

    def on_consultaTxt_clicked(self, control):
        """
        Muestra la información sacada de la base de datos por el nombre del Cliente en el TreeView
        :param control: Button
        :return: Nothing
        """

        self.modelo.clear()
        nombreSelect = self.txtNombre.get_text()

        if not nombreSelect == None and not nombreSelect=='':

            datos = MetodosBD.MetodosBD.buscar_seguro_nombre_cliente(self, nombreSelect)
            tamañoDatos = len(datos)
            for i in range(tamañoDatos):
                d1 = datos[i][0]
                d2 = datos[i][1]
                d3 = datos[i][2]
                d4 = datos[i][3]
                d5 = datos[i][4]
                d6 = datos[i][5]
                d7 = datos[i][6]
                d8 = datos[i][7]
                d9 = datos[i][8]
                self.modelo.append([d1, d2, d3, d4, d5, d6, d7, d8, d9])
        else:
            self.modelo.clear()

    def on_selection_changed(self,seleccion):
        """
        Metodo que recoge todos los valores seleccionados en variables al pinchar en el TreeView
        :param seleccion: TreeView
        :return: Variable booleana
        """
    #["IdSeguro","Seguro" "IdVendedor","Dni Cliente", "Nombre", "Apellidos", "Tiempo", "Coste", "Fecha"]
        condicion= True
        modelo, punteiro = seleccion.get_selected()
        if punteiro is not None:
            self.sltIdVendedor = (str(modelo[punteiro][2]))
            self.sltNomVendedor=MetodosBD.MetodosBD.buscar_vendedor_id(self,self.sltIdVendedor)
            self.sltDniCliente=(modelo[punteiro][3])
            self.sltNomCliente=(modelo[punteiro][4])
            self.sltApellCliente=((modelo[punteiro][5]))
            self.sltSeguro=(modelo[punteiro][1])
            self.sltTiempo = (str(modelo[punteiro][6]))
            self.sltCoste = (str(modelo[punteiro][7]))
            self.sltFecha = (modelo[punteiro][8])
            condicion = True

        else:
            condicion = False

        return condicion


    def on_crearPdf_click(self,control):
        """
        Metodo que crea un Pdf simulando una Factura, con la información del vendedor y del cliente
        :param control: Button
        :return: Nothing
        """


        if  tablaSeguros.on_selection_changed(self,self.seleccion):

            aux = canvas.Canvas("Factura" +self.sltNomCliente+ ".pdf")
            obxetoTexto = aux.beginText()
            obxetoTexto.setFont("Courier-Bold", 14)
            obxetoTexto.setTextOrigin(100, 800)

            titulo ='Factura Correduría de Seguros'

            obxetoTexto.textLines(titulo)
            obxetoTexto.moveCursor(0, 80)

            obxetoTexto.setFont("Courier", 10)

            texto = ['Id del Vendedor: ' + self.sltIdVendedor +
                      '     Vendedor: ' + self.sltNomVendedor,
                     'Dni Cliente: ' + self.sltDniCliente,
                     'Nombre titular: ' + self.sltNomCliente + ' ' + self.sltApellCliente,
                     'Seguro de: ' + self.sltSeguro +
                     '      Tiempo del seguro: ' + self.sltTiempo + ' meses ',
                     'Coste del seguro: ' + self.sltCoste + ' euros ' +
                     '      A día de: ' + self.sltFecha]

            for linha in texto:

                obxetoTexto.textOut(linha)
                obxetoTexto.moveCursor(0,40)


            obxetoTexto.setFillGray(0.5)

            aux.drawText(obxetoTexto)

            aux.showPage()

            aux.save()
        else:
            messageDialog = Gtk.MessageDialog(parent=self, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.WARNING,
                                              buttons=Gtk.ButtonsType.OK, message_format="Seleccione un Cliente")
            response = messageDialog.run()
            if (response == Gtk.ResponseType.OK):
                messageDialog.destroy()



    def on_cerrar_clicked(self,Button):
        """
        Metodo para navegar a la ventana Seguros
        :param Button: Button
        :return: Nothing
        """
        seguros = Seguros.seguros(self.tipo, self.id,self.nombre)
        self.set_visible(False)




if __name__ == "__main__":
    tablaSeguros()
    Gtk.main()