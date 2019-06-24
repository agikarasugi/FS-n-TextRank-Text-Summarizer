# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settings_menu(object):
    def setupUi(self, settings_menu):
        settings_menu.setObjectName("settings_menu")
        settings_menu.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(settings_menu)
        self.buttonBox.setGeometry(QtCore.QRect(90, 240, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(settings_menu)
        self.label.setGeometry(QtCore.QRect(20, 110, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.algorithm = QtWidgets.QComboBox(settings_menu)
        self.algorithm.setGeometry(QtCore.QRect(250, 110, 111, 21))
        self.algorithm.setObjectName("algorithm")
        self.label_2 = QtWidgets.QLabel(settings_menu)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(settings_menu)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.language = QtWidgets.QComboBox(settings_menu)
        self.language.setGeometry(QtCore.QRect(250, 70, 111, 22))
        self.language.setObjectName("language")
        self.sen_count = QtWidgets.QLineEdit(settings_menu)
        self.sen_count.setGeometry(QtCore.QRect(250, 30, 113, 22))
        self.sen_count.setObjectName("sen_count")
        self.metric = QtWidgets.QComboBox(settings_menu)
        self.metric.setGeometry(QtCore.QRect(250, 150, 111, 21))
        self.metric.setObjectName("metric")
        self.label_4 = QtWidgets.QLabel(settings_menu)
        self.label_4.setGeometry(QtCore.QRect(20, 150, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(settings_menu)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.graph = QtWidgets.QComboBox(settings_menu)
        self.graph.setGeometry(QtCore.QRect(250, 190, 111, 21))
        self.graph.setObjectName("graph")

        self.retranslateUi(settings_menu)
        self.buttonBox.accepted.connect(settings_menu.accept)
        self.buttonBox.rejected.connect(settings_menu.reject)
        QtCore.QMetaObject.connectSlotsByName(settings_menu)

    def retranslateUi(self, settings_menu):
        _translate = QtCore.QCoreApplication.translate
        settings_menu.setWindowTitle(_translate("settings_menu", "Settings"))
        self.label.setText(_translate("settings_menu", "Algorithm"))
        self.label_2.setText(_translate("settings_menu", "Sentence Count(For Output)"))
        self.label_3.setText(_translate("settings_menu", "Language"))
        self.label_4.setText(_translate("settings_menu", "Distance Metric"))
        self.label_5.setText(_translate("settings_menu", "Graph Model"))


