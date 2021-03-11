#!/usr/bin/python


from PyQt5.QtWidgets import (QWidget, QSlider, QHBoxLayout,
                             QLabel, QApplication, QVBoxLayout, QCheckBox, QLineEdit, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import sys
import sqlite3 as sql
from functools import partial


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.modulName = 'ContoursConfig'
        self.ConfigID = 7
        self.conDB = self.connectDB()
        self.cur, config = self.getConfig(self.conDB, self.modulName)
        self.slider = self.buildParaModuls(config)

        self.window = QWidget()
        self.window.setLayout(self.slider)
        self.window.show()

    def connectDB(self, pathDB = 'configs/Config.db'):

        print('Connect to DB: ' + pathDB + '...', end=' ')
        try:
            con = sql.connect(pathDB)
            con.row_factory = sql.Row
            #cur = con.cursor()
            print('CONNECTED')
            return con
        except:
            print('FAILD')
            sys.exit()

    def getDbParameter(self, paraModul):
        self.cur.execute("SELECT %s FROM %s WHERE ConfigID=%i" % (paraModul, self.modulName, self.ConfigID))
        val = self.cur.fetchone()[0]
        return val

    def setDbParameter(self, paraName, val, label=0):
        if label is 0:
            pass
        else:
            label.setText(str(val))
        sqlexe = "UPDATE %s SET %s=%s WHERE ConfigID=%i" % (self.modulName, paraName, val, self.ConfigID)
        print(sqlexe)
        self.cur.execute(sqlexe)
        self.conDB.commit()
        return 1

    def getCurParameter(self, cur,  paramName):
        parameters = cur.fetchone()
        param = parameters[paramName]
        return param


    def getConfig(self, con, modulName):
        print('Get config index for: ' + modulName + '...', end=' ')
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT*FROM %s " % (modulName, ))
        config = list(map(lambda x: x[0], cur.description))
        if config is None:
            print('FAILD')
            print('Modul '+modulName+' not found')
            sys.exit()
        else:
            print("DONE")
        return cur, config
    def getParameterList(self, attribute, nameParameter):

        sqlExe = "SELECT %s FROM Parameter WHERE Name='%s'" % (attribute, nameParameter)
        print(sqlExe)
        self.cur.execute(sqlExe)
        val = self.cur.fetchone()[0]
        return val

    def buildParaModuls(self, config):
        config = config[2:]
        layout = QVBoxLayout()
        for paraModul in config:
            if paraModul.find('_')<0:
                paraNames = []
                for para in config:
                    if para.find(paraModul+'_')>=0:
                        paraNames.append(para)

                layout.addLayout(self.buildSliderSection(paraModul, paraNames))
            else:
                pass
        return layout


    def buildSliderSection(self,paraModul, paraNames):
        layout = QVBoxLayout()

        # Label
        label = QLabel(paraModul)
        # Checkbox
        checkbox = QCheckBox('Enable')
        checkbox.setChecked(self.getDbParameter(paraModul))
        checkbox.stateChanged.connect(lambda: self.setDbParameter(paraModul, int(checkbox.isChecked())))
        # Slider
        sliderParaModul = self.buildSider(paraNames)
        
        # Generate Layout
        layout.addWidget(label)
        layout.addWidget(checkbox)
        layout.addLayout(sliderParaModul)

        return layout

    def checkboxCallback(self,paraModul,test):
        print(paraModul)
        print(test)
        self.setDbParameter(paraModul, test)

    def buildSider(self,paraNames):
        layout = QVBoxLayout()
        for paraName in paraNames:
            slider = self.generateSlider(paraName)
            label = QLabel(paraName)
            layout.addLayout(slider)
        return layout


    def generateSlider(self,paraName):
        hbox = QHBoxLayout()

        try:
            valDB = int(self.getDbParameter(paraName))
        except:
            valDB = self.getDbParameter(paraName)

        if isinstance(valDB, int):
            labelVal = QLabel(str(valDB))
            labelVal.setFont(QtGui.QFont("Sanserif", 15))

            paraSlider = QSlider(Qt.Horizontal, self)
            paraSlider.setGeometry(30, 40, 200, 30)
            paraSlider.setMinimum(int(self.getParameterList('SliderMin', paraName)))
            paraSlider.setMaximum(int(self.getParameterList('SliderMax', paraName)))
            paraSlider.setSliderPosition(valDB)
            paraSlider.valueChanged.connect(lambda: self.setDbParameter(paraName, int(paraSlider.value()), labelVal))

            label = QLabel(paraName)
            label.setFont(QtGui.QFont("Sanserif", 15))




            hbox.addWidget(labelVal)
            hbox.addWidget(paraSlider)
            hbox.addWidget(label)
        else:
            textBox = QLineEdit()
            textBox.resize(200, 30)
            textBox.setText(valDB)
            textBox.editingFinished.connect(lambda: self.setDbParameter(paraName, "'"+textBox.text()+"'"))

            hbox.addWidget(textBox)



        return hbox


    def initUI(self):

        hbox = QHBoxLayout()

        sld = QSlider(Qt.Horizontal, self)
        sld.setRange(0, 100)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setPageStep(5)

        sld.valueChanged.connect(self.updateLabel)

        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)

        hbox.addWidget(sld)
        hbox.addSpacing(15)
        hbox.addWidget(self.label)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QSlider')
        self.show()

    def updateLabel(self, value):

        self.label.setText(str(value))


def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()