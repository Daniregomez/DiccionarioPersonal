import sys


from pandas import DataFrame, ExcelWriter, read_excel

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, 
    QPushButton, QRadioButton, QHBoxLayout, 
    QVBoxLayout, QApplication, QGroupBox)

from PyQt5.QtCore import QTimer, Qt


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.dictionary_gui()


    def dictionary_gui(self):

        self.load_dates()

        # Elementos de la seccion de consulta-------------

        palabra = QLabel("Palabra:")
        self.a_trad = QLineEdit() 
        self.ing_spa = QRadioButton("Ingles a Español")
        self.spa_ing = QRadioButton("Español a Ingles")
        traduccion = QLabel("Traduccion")
        self.word = QLabel()


        v1 = QVBoxLayout()
        v1.addWidget(self.ing_spa)
        v1.addWidget(self.spa_ing)

        v2 = QVBoxLayout()
        v2.addWidget(palabra)
        v2.addWidget(self.a_trad)

        h1 = QHBoxLayout()
        h1.addStretch()
        h1.addWidget(traduccion)
        h1.addStretch()
        h1.addWidget(self.word)
        h1.addStretch()

        h2 = QHBoxLayout()
        h2.addStretch()
        h2.addLayout(v1)
        h2.addStretch()
        h2.addLayout(v2)
        h2.addStretch()

        sec_consulta = QVBoxLayout()
        sec_consulta.addLayout(h2)
        sec_consulta.addLayout(h1)

        consultar = QGroupBox("Consultar")
        consultar.setLayout(sec_consulta)


        # Elementos de la seccion de agregar---------------

        ing = QLabel("Ingles:")
        self.ing_word = QLineEdit()

        spa = QLabel("Español:")
        self.spa_word = QLineEdit()

        self.aceptar = QPushButton("Aceptar")
        self.sucess = QLabel()

        v3 = QVBoxLayout()
        v3.addWidget(ing)
        v3.addWidget(self.ing_word)

        v4 = QVBoxLayout()
        v4.addWidget(spa)
        v4.addWidget(self.spa_word)

        h_v34 = QHBoxLayout()
        h_v34.addStretch()
        h_v34.addLayout(v3)
        h_v34.addStretch()
        h_v34.addLayout(v4)
        h_v34.addStretch()

        h4 = QHBoxLayout()
        h4.addStretch()
        h4.addWidget(self.sucess)
        h4.addStretch()
        h4.addWidget(self.aceptar)
        
        sec_agregar = QVBoxLayout()

        sec_agregar.addLayout(h_v34)
        sec_agregar.addLayout(h4)

        agregar = QGroupBox("Agregar")
        agregar.setLayout(sec_agregar)


        # Texto informativo-----------------------------

        system = QLabel()

        h5 = QHBoxLayout()
        h5.addStretch()
        h5.addWidget(system)


        # Union de todos los elementos-------------------

        todo = QVBoxLayout()
        todo.addWidget(consultar)
        todo.addStretch()
        todo.addWidget(agregar)
        todo.addLayout(h5)

        self.setLayout(todo)
        self.setWindowTitle("Diccionario personal")
        self.setGeometry(300, 150, 350, 300)

        self.aceptar.clicked.connect(self.add_word)
        self.ing_spa.toggled.connect(self.mode)
        self.spa_ing.toggled.connect(self.mode)

        self.show()

    def mode(self):
        self.mode = self.sender().text()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:        
            """Funcion a realizar"""
            self.convert_word()
            

    def add_word(self):
        """
        Se agregan dos palabras a la df y se muestra un texto en la interfaz para confirmar que 
        se agrego exitosamente
        """

        # Se agrega una palabra y su traduccion a la df
        new_row = DataFrame([self.ing_word.text()], index=[self.spa_word.text()])
        new_row.rename(columns={0 : 'Ingles'}, inplace=True)

        self.df = (self.df.append(new_row)
                          .sort_index())

        # Indica con un texto cuando se registra una palabra y realiza una pequeña animacion
        self.count = 0
        self.timer = QTimer()
        self.sucess.setText("Registro exitoso")
        self.timer.timeout.connect(self.text)
        self.timer.start(1000)

        self.save_dates()
        
        print(self.df)


    def text(self):
        """
        Agrega al texto que indica un registro exitoso un punto al final, 
        despues de 3 puntos el texto desaparece
        """
        text = "Registro exitoso"
        self.sucess.setText(text + self.count * '.')
        self.count += 1

        if self.count == 5:
            self.timer.stop()
            self.sucess.setText('')


    def convert_word(self):

        try:
            if self.mode == "Ingles a Español":
                for w in self.df.index:
                    if self.df.loc[w, 'Ingles'] == self.a_trad.text():
                        self.word.setText(w)
                    else:
                        self.word.setText("La palabra buscada no esta registrada")

            else:
                self.word.setText(self.df.loc[self.a_trad.text(), "Ingles"])
        except:
            self.word.setText("La palabra buscada no esta registrada")


    def save_dates(self):
        writer = ExcelWriter('dictionary.xlsx')
        self.df.to_excel(writer,'Hoja1')
        writer.save()  


    def load_dates(self):
        self.df = read_excel('dictionary.xlsx', index_col=0)


app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
