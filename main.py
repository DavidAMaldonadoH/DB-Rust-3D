import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

from ui_main import Ui_MainWindow

from analyzer.parser import parser
from util.Error import ERRORS_
from util.Generator import Generator
from util.Scope import Scope
from util.Symbol import SYMBOLS


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Configuracion
        self.setUpIcons()
        self.setUpNavBar()
        self.setUpReportesBar()
        self.setUpTables()

        self.show()

    def compilar(self):
        input = self.ui.editor.toPlainText()
        self.ui.console.clear()
        SYMBOLS.clear()
        ERRORS_.clear()
        output: str = ""
        ast = parser.parse(input, tracking=True)
        g_scope = Scope(None, "Global")
        generator = Generator()

        generator.addImprimir()
        generator.addPrintFalse()
        generator.addPrintTrue()
        generator.addModule()
        generator.addAbsolute()
        generator.addSquareRoot()

        for node in ast:
            node.execute(g_scope, generator)

        output += "#include <stdio.h>\n"
        output += "double stack[100000];\n"
        output += "double heap[100000];\n"
        output += "double P;\n"
        output += "double H;\n"
        if len(generator.getTemps()) > 0:
            output += "double "

        for (i, tmp) in enumerate(generator.getTemps()):
            if i < len(generator.getTemps()) - 1:
                output += tmp + ", "
            else:
                output += tmp

        if len(generator.getTemps()) > 0:
            output += ";\n\n"

        # output += "void main() {"

        self.ui.console.append(output)

        for line in generator.code:
            self.ui.console.append(line)

        # self.ui.console.append("\treturn;\n}\n")

    def setUpIcons(self):
        self.setWindowIcon(QtGui.QIcon("./assets/user-astronaut-solid.svg"))
        self.ui.btn_editor.setIcon(QtGui.QIcon("./assets/code-solid.svg"))
        self.ui.btn_compilar.setIcon(QtGui.QIcon("./assets/circle-play-solid.svg"))
        self.ui.btn_reportes.setIcon(QtGui.QIcon("./assets/file-lines-solid.svg"))
        self.ui.btn_acerca_de.setIcon(QtGui.QIcon("./assets/circle-info-solid.svg"))

    def setUpNavBar(self):
        # Editor Page
        self.ui.btn_editor.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_1)
        )

        # Compilar
        self.ui.btn_compilar.clicked.connect(lambda: self.compilar())

        # Reportes Page
        self.ui.btn_reportes.clicked.connect(lambda: self.reportesAction())

        # Acerca de Page
        self.ui.btn_acerca_de.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
        )

    def setUpReportesBar(self):
        # Simbolos Page
        self.ui.btn_simbolos.clicked.connect(lambda: self.simbolosAction())

        # Errores Page
        self.ui.btn_errores.clicked.connect(lambda: self.erroresAction())

        # Bases Page
        self.ui.btn_bases.clicked.connect(lambda: self.basesAction())

        # Tablas Page
        self.ui.btn_tablas.clicked.connect(lambda: self.tablasAction())

    def setUpTables(self):
        afont = QtGui.QFont()
        afont.setFamily("Hack Nerd Font")
        afont.setPointSize(10)

        # Tabla Simbolos
        header1 = self.ui.table_simbolos.horizontalHeader()
        header1.setSectionResizeMode(0, QHeaderView.Stretch)
        header1.setSectionResizeMode(1, QHeaderView.Stretch)
        header1.setSectionResizeMode(2, QHeaderView.Stretch)
        header1.setSectionResizeMode(3, QHeaderView.Stretch)
        header1.setSectionResizeMode(4, QHeaderView.Stretch)
        header1.setSectionResizeMode(5, QHeaderView.Stretch)
        header1.setFont(afont)

        # Tabla Errores
        header2 = self.ui.table_errores.horizontalHeader()
        header2.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(1, QHeaderView.Stretch)
        header2.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header2.setFont(afont)

        # Tabla Bases
        header3 = self.ui.table_bases.horizontalHeader()
        header3.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header3.setSectionResizeMode(1, QHeaderView.Stretch)
        header3.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header3.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header3.setFont(afont)

        # Tabla Tablas
        header4 = self.ui.table_tablas.horizontalHeader()
        header4.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header4.setSectionResizeMode(1, QHeaderView.Stretch)
        header4.setSectionResizeMode(2, QHeaderView.Stretch)
        header4.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header4.setFont(afont)

    def setSymbols(self):
        self.ui.table_simbolos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ui.table_simbolos.setRowCount(len(SYMBOLS))
        for i, symbol in enumerate(SYMBOLS):
            self.ui.table_simbolos.setItem(i, 0, QTableWidgetItem(symbol["name"]))
            self.ui.table_simbolos.setItem(i, 1, QTableWidgetItem(symbol["type"]))
            self.ui.table_simbolos.setItem(i, 2, QTableWidgetItem(symbol["type2"]))
            self.ui.table_simbolos.setItem(i, 3, QTableWidgetItem(symbol["scope"]))
            self.ui.table_simbolos.setItem(
                i, 4, QTableWidgetItem(str(symbol["position"]))
            )
            self.ui.table_simbolos.setItem(i, 5, QTableWidgetItem(symbol["params"]))
            self.ui.table_simbolos.setItem(i, 6, QTableWidgetItem(symbol["size"]))

    def reportesAction(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        self.setSymbols()

    def simbolosAction(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_4)
        self.setSymbols()

    def erroresAction(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_5)
        self.ui.table_errores.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ui.table_errores.setRowCount(len(ERRORS_))
        for i, err in enumerate(ERRORS_):
            self.ui.table_errores.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.ui.table_errores.setItem(i, 1, QTableWidgetItem(err.description))
            self.ui.table_errores.setItem(i, 2, QTableWidgetItem(err.env))
            self.ui.table_errores.setItem(i, 3, QTableWidgetItem(str(err.line)))
            self.ui.table_errores.setItem(i, 4, QTableWidgetItem(str(err.column)))
            self.ui.table_errores.setItem(i, 5, QTableWidgetItem(err.time))

    def basesAction(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_6)
        self.ui.table_bases.setEditTriggers(QTableWidget.NoEditTriggers)

    def tablasAction(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_7)
        self.ui.table_tablas.setEditTriggers(QTableWidget.NoEditTriggers)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
