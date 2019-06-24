# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.browseButton = QtWidgets.QToolButton(self.centralwidget)
        self.browseButton.setObjectName("browseButton")
        self.gridLayout.addWidget(self.browseButton, 0, 2, 1, 1)
        self.browseFile = QtWidgets.QLineEdit(self.centralwidget)
        self.browseFile.setObjectName("browseFile")
        self.gridLayout.addWidget(self.browseFile, 0, 1, 1, 1)
        self.OutputText_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.OutputText_2.setObjectName("OutputText_2")
        self.gridLayout.addWidget(self.OutputText_2, 1, 0, 1, 3)
        self.generateSummary = QtWidgets.QPushButton(self.centralwidget)
        self.generateSummary.setObjectName("generateSummary")
        self.gridLayout.addWidget(self.generateSummary, 3, 1, 1, 1)
        self.internet_status = QtWidgets.QLabel(self.centralwidget)
        self.internet_status.setAlignment(QtCore.Qt.AlignCenter)
        self.internet_status.setObjectName("internet_status")
        self.gridLayout.addWidget(self.internet_status, 2, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuPreference = QtWidgets.QMenu(self.menubar)
        self.menuPreference.setObjectName("menuPreference")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuPreference.addAction(self.actionSettings)
        self.menubar.addAction(self.menuPreference.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Automatic Text Summarization"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.generateSummary.setText(_translate("MainWindow", "Generate Summary"))
        #self.internet_status.setText(_translate("MainWindow", ""))
        self.menuPreference.setTitle(_translate("MainWindow", "Preference"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))


