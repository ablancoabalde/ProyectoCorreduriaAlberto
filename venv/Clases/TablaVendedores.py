import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from BaseDatos import MetodosBD
from Clases import Vendedores

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.graphics.charts.piecharts import Pie


class tablaVendedores(Gtk.Window):

    def __init__(self, initTipo, initId, initNombre):
        """
        Recibe la catergoría, el Id y el Nombre del Vendedor que inicio sesión
        :param initTipo: Text
        :param initId: Int
        :param initNombre: Text
        """

        Gtk.Window.__init__(self, title="Tabla Seguros "+str(initNombre))
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)


        self.boxV = Gtk.Box(spacing=20, orientation=Gtk.Orientation.VERTICAL)

        # Variables de uso común
        self.vbtnBuscar="Buscar"
        self.vbtnMostrarTodo="Mostrar Todo"
        self.vbtnEstadisticas = "Generar PDF"
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
        self.lblDni = Gtk.Label("DNI: ")
        self.lblNombre = Gtk.Label("Nombre: ")

        #GridCerrar
        self.lblEstadisticas = Gtk.Label("Realizar PDF de Ventas: ")

        #Entrys

        #Grid
        self.txtNombre = Gtk.Entry()
        self.txtNombre.connect("changed", self.on_consultaTxt_clicked)

        # ComboBox

        # Grid
        self.cbDniBuscar = Gtk.ComboBoxText()
        self.cbDniBuscar.set_entry_text_column(0)

        # Botones

        # Grid

        self.btnConsultar = Gtk.Button(self.vbtnBuscar)
        self.btnConsultar.connect("clicked", self.on_consultaCB_clicked)
        self.btnMostrar = Gtk.Button(self.vbtnMostrarTodo)
        self.btnMostrar.connect("clicked", self.on_mostrar_click)

        # GridCerrar
        self.btnCerrar = Gtk.Button(self.vbtnCerrar)
        self.btnCerrar.connect("clicked", self.on_cerrar_clicked)
        self.btnEstadisticas = Gtk.Button(self.vbtnEstadisticas)
        self.btnEstadisticas.connect("clicked", self.on_crearPdf_click)

        #Tabla Vendedores
        #self.columnas = ["DNI","Tipo" "Nombre","Apellidos", "Telefono", "Zona", "Nacionalidad", "Fecha", "Ventas"]
        self.modelo = Gtk.ListStore(str, str, str, str,str, str, str, str, float)
        #self.axenda = []
        self.vista = Gtk.TreeView(model=self.modelo)


        self.celdaTexto = Gtk.CellRendererText()
        """ Con esto otro hacemos que la vista se actualice"""
        self.celdaTexto.connect("edited", self.on_celdaText_edited, self.modelo)

        """Agregamos la función de ordenar según la categoría que pinchemos"""
        self.scrollTree = Gtk.ScrolledWindow(hexpand=True,vexpand=True)
        self.scrollTree.add_with_viewport(self.vista)

        self.columnaDni=Gtk.TreeViewColumn('DNI',self.celdaTexto,text=0)
        self.columnaDni.set_sort_column_id(0)
        self.vista.append_column(self.columnaDni)

        self.columnaTipo=Gtk.TreeViewColumn('Cargo',self.celdaTexto,text=1)
        self.columnaTipo.set_sort_column_id(1)
        self.vista.append_column(self.columnaTipo)

        self.columnaNombre=Gtk.TreeViewColumn('Nombre',self.celdaTexto,text=2)
        self.columnaNombre.set_sort_column_id(2)
        self.vista.append_column(self.columnaNombre)

        self.columnaApellidos=Gtk.TreeViewColumn('Apellidos',self.celdaTexto,text=3)
        self.columnaApellidos.set_sort_column_id(3)
        self.vista.append_column(self.columnaApellidos)

        self.columnaTelf=Gtk.TreeViewColumn('Telefono',self.celdaTexto,text=4)
        self.columnaTelf.set_sort_column_id(4)
        self.vista.append_column(self.columnaTelf)

        self.columnaZona=Gtk.TreeViewColumn('Zona',self.celdaTexto,text=5)
        self.columnaZona.set_sort_column_id(5)
        self.vista.append_column(self.columnaZona)

        self.columnaNacio=Gtk.TreeViewColumn('Nacionalidad',self.celdaTexto,text=6)
        self.columnaNacio.set_sort_column_id(6)
        self.vista.append_column(self.columnaNacio)

        self.columnaFecha=Gtk.TreeViewColumn('Fecha',self.celdaTexto,text=7)
        self.columnaFecha.set_sort_column_id(7)
        self.vista.append_column(self.columnaFecha)

        self.columnaVentas=Gtk.TreeViewColumn('Ventas',self.celdaTexto,text=8)
        self.columnaVentas.set_sort_column_id(8)
        self.vista.append_column(self.columnaVentas)




        # Agregamos labels,,ComboBox, botones al Grid 1
        self.grid.attach(self.lblNombre, 0, 0, 1, 1)
        self.grid.attach(self.txtNombre, 1, 0, 1, 1)
        self.grid.attach(self.lblDni, 0, 1, 1, 1)
        self.grid.attach(self.cbDniBuscar, 1, 1, 1, 1)
        self.grid.attach(self.btnConsultar, 2, 1, 1, 1)
        self.grid.attach(self.btnMostrar, 3, 1, 1, 1)

        # Agregamos labels,,ComboBox, botones al GridCerrar
        self.gridCerrar.attach(self.btnCerrar, 0, 0, 2, 1)
        self.gridCerrar.attach(self.lblEstadisticas, 2, 0, 1, 1)
        self.gridCerrar.attach(self.btnEstadisticas, 3, 0, 1, 1)

        # Cargamos el DNI de los clientes en un ComboBox
        cmbBoXAdd = tablaVendedores.actualizar_cmbDni(self)

        frameTabla.add(self.scrollTree)
        self.gridTabla.add(frameTabla)

        self.boxV.add(self.grid)
        self.boxV.add(self.gridTabla)
        self.boxV.add(self.gridCerrar)
        self.add(self.boxV)


        self.connect("destroy", Gtk.main_quit)
        self.show_all()



    def actualizar_cmbDni(self):
        """
        Metodo que refresca la información de los Combobox
        :return: Nothing
        """

        self.cbDniBuscar.remove_all()
        dnis= MetodosBD.MetodosBD.listar_dni_vendedores(self)
        for rexistro in dnis:

            self.cbDniBuscar.append_text(rexistro[0])


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
        Muestra la información sacada todos los vendedores de la base de datos en el TreeView
        :param control: Button
        :return: Nothing
        """

        self.modelo.clear()
        datos = MetodosBD.MetodosBD.listar_vendedores(self)
        tamañoDatos=len(datos)
        for i in range(tamañoDatos):
            d1=datos[i][2]
            d2=datos[i][1]
            d3=datos[i][3]
            d4=datos[i][4]
            d5=datos[i][5]
            d6=datos[i][6]
            d7=datos[i][7]
            d8=datos[i][8]
            d9=datos[i][9]
            self.modelo.append([d1, d2, d3, d4, d5, d6, d7, d8, d9])


    def on_consultaCB_clicked(self,control):
        """
        Muestra la información sacada de la base de datos sacada por el Dni en el TreeView
        :param control: Button
        :return: Nothing
        """

        dniSelect = self.cbDniBuscar.get_active_text()

        if not dniSelect == None:
            self.modelo.clear()
            datos = MetodosBD.MetodosBD.buscar_vendedor(self,dniSelect)

            d1 = datos[0][2]
            d2 = datos[0][1]
            d3 = datos[0][3]
            d4 = datos[0][4]
            d5 = datos[0][5]
            d6 = datos[0][6]
            d7 = datos[0][7]
            d8 = datos[0][8]
            d9 = datos[0][9]
            self.modelo.append([d1, d2, d3, d4, d5, d6, d7, d8, d9])

    def on_consultaTxt_clicked(self, control):
        """
        Muestra la información sacada de la base de datos por el nombre del Vendedor en el TreeView
        :param control: Button
        :return: Nothing
        """

        self.modelo.clear()
        nombreSelect = self.txtNombre.get_text()

        if not nombreSelect == None and not nombreSelect=='':

            datos = MetodosBD.MetodosBD.buscar_vendedor_nombre(self, nombreSelect)
            tamañoDatos = len(datos)
            for i in range(tamañoDatos):
                d1 = datos[i][2]
                d2 = datos[i][1]
                d3 = datos[i][3]
                d4 = datos[i][4]
                d5 = datos[i][5]
                d6 = datos[i][6]
                d7 = datos[i][7]
                d8 = datos[i][8]
                d9 = datos[i][9]
                self.modelo.append([d1, d2, d3, d4, d5, d6, d7, d8, d9])
        else:
            self.modelo.clear()

    def on_crearPdf_click(self,control):
        """
        Metodo que crea un pdf que contiene una gráfica con las ventas de los vendedores
        :param control: Button
        :return: Nothing
        """
        guion = []

        d = Drawing(500, 300)
        grafica = VerticalBarChart()
        # Posiciona el grafico en la hoja
        grafica.x = 0
        grafica.y = -250
        # Tamaño del gráfico
        grafica.height = 500
        grafica.width = 500
        # Color de la info de las barras
        grafica.strokeColor = colors.black
        # Valores min y max alcanzables en la barra
        grafica.valueAxis.valueMin = 0
        grafica.valueAxis.valueMax = 4000
        # Saltos de valores
        grafica.valueAxis.valueStep = 100
        # Muestra donde se va a colocar el texto
        # los valores son como una rosa de los vientos(center,n,nw,w,sw,s,se,ene)
        grafica.categoryAxis.labels.boxAnchor = 'n'
        # Ángulo con el que se muestra el texto
        grafica.categoryAxis.labels.angle = 25
        # Espaciado entre las los grupos de barras
        grafica.groupSpacing = 10

        # Llamada al metodo para recuperar toda la información de todos los vendedores
        datosBD = MetodosBD.MetodosBD.listar_vendedores(self)
        # Obtengo el valor de cuantos vendedores están registrados
        tamañoDatos = len(datosBD)

        # Creamos las listas vacías
        valoresVentas = []
        listIdVendedores = []
        # Recorremos el tamaño para que i vaya desde 0 hasta el max de vendedores guardados
        for i in range(tamañoDatos):
            # Recupero los datos que necesito en este caso IdVendedor y las ventas de este
            d0 = datosBD[i][0]
            d9 = datosBD[i][9]
            # Almacenamos la info en las listas
            valoresVentas.append(d9)
            listIdVendedores.append(str(d0))

        # Introducimos los valores de venta para que las muestre en barra
        # la convierto en una lista para que funcione
        grafica.data = [valoresVentas]
        # Introduzco los valores de Id del vendedor para que muestre el id de cada uno
        grafica.categoryAxis.categoryNames =listIdVendedores

        d.add(grafica)

        guion.append(d)

        doc = SimpleDocTemplate("GráficaVentaVendedores.pdf", pagesize=A4)

        doc.build(guion)

    def on_cerrar_clicked(self,Button):
        """
        Metodo para navegar a la ventana Vendedores
        :param Button: Button
        :return: Nothing
        """
        vendedores = Vendedores.vendedores(self.tipo, self.id,self.nombre)
        self.set_visible(False)




if __name__ == "__main__":
    tablaVendedores()
    Gtk.main()
