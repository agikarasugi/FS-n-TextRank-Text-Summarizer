import sys
from main_ui import Ui_MainWindow
from settings import Ui_settings_menu
from PyQt5 import QtCore, QtGui, QtWidgets
from textrank import TextRank
from check_connection import check_internet
from article import get_text
from frequency_summarizer import fs


class SettingsWindow (QtWidgets.QDialog, Ui_settings_menu):
    def __init__(self, alg, lang, count, met, graph, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent

        # list of items from the combo box
        self.algorithm.addItems(['FS', 'TextRank'])
        self.language.addItems(['indonesian', 'english'])
        self.metric.addItems(
            ['cosine', 'euclidean', 'jenshan', 'hamming', 'log'])
        self.graph.addItems(['PageRank', 'HITS'])

        # set initial value
        self.algorithm.setCurrentIndex(self.algorithm.findText(alg))
        self.language.setCurrentIndex(self.language.findText(lang))
        self.metric.setCurrentIndex(self.metric.findText(met))
        self.graph.setCurrentIndex(self.graph.findText(graph))
        self.sen_count.setText(str(count))
        self.sen_count.setValidator(QtGui.QIntValidator())

        # metric_and graph visibility
        self.metric_graph_visibility()

        # save changes when ok button clicked
        self.buttonBox.accepted.connect(self.button_accept)

        # hide metric option if selected algorithm is not text rank
        self.algorithm.currentTextChanged.connect(self.metric_graph_visibility)

    def button_accept(self):
        self.parent.set_algorithm = str(self.algorithm.currentText())
        self.parent.set_language = str(self.language.currentText())
        self.parent.set_count = self.sen_count.text()
        self.parent.set_metric = str(self.metric.currentText())
        self.parent.set_graph = str(self.graph.currentText())

    def metric_graph_visibility(self):
        if self.algorithm.currentText() != 'TextRank':
            self.metric.setVisible(False)
            self.label_4.setVisible(False)

            self.graph.setVisible(False)
            self.label_5.setVisible(False)
        else:
            self.metric.setVisible(True)
            self.label_4.setVisible(True)
            self.graph.setVisible(True)
            self.label_5.setVisible(True)


class MainWindow (QtWidgets.QMainWindow, Ui_MainWindow, QtWidgets.QSizePolicy):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.url = None
        self.text = None
        self.file_path = ''
        self.thread = QtCore.QThread()
        self.out = ''

        # initial value for settings parameters
        self.set_algorithm = 'FS'
        self.set_language = 'indonesian'
        self.set_count = '10'
        self.set_metric = 'cosine'
        self.set_graph = 'PageRank'

        # add input mode combo box list
        self.comboBox.addItems(['File', 'URL'])

        # initial value for input mode
        self.comboBox.setCurrentIndex(self.comboBox.findText('File'))

        # list action
        self.browseButton.clicked.connect(self.browse_files)
        self.actionSettings.triggered.connect(self.open_settings)
        self.comboBox.currentTextChanged.connect(self.input_list)
        self.browseFile.setReadOnly(True)
        self.browseFile.textChanged.connect(self.bf_textchanged)

        # start thread for checking internet connection
        self.inet = Internet(self)
        self.thread = QtCore.QThread()
        self.inet.moveToThread(self.thread)
        self.thread.start()
        self.inet.run()

        # start summarization thread
        self.generateSummary.clicked.connect(self.summarize)

    def summarize(self):
        'change text and disable summary button'
        self.generateSummary.setDisabled(True)
        self.generateSummary.setText('Generating Summary...')

        # start summarizaton thread
        self.sum_thread = SumT(self)
        self.thread2 = QtCore.QThread()
        self.sum_thread.moveToThread(self.thread2)
        self.thread2.start()

        # run method after thread started
        self.thread2.started.connect(self.sum_thread.summary)

        # output summarization after thread is finished
        self.thread2.finished.connect(self.output_text)
        self.thread2.quit()

    def bf_textchanged(self):
        self.file_path = str(self.browseFile.text())

    def input_list(self):
        # retain size when hidden
        size_retain = self.browseButton.sizePolicy()
        size_retain.setRetainSizeWhenHidden(True)
        self.browseButton.setSizePolicy(size_retain)

        if str(self.comboBox.currentText()) == 'URL':
            self.browseButton.setVisible(False)
            self.browseFile.setReadOnly(False)
        else:
            self.browseButton.setVisible(True)
            self.browseFile.setReadOnly(True)

        self.browseFile.setText('')
        self.file_path = ''

    def browse_files(self):
        temp = self.file_path
        self.file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Browse Files')[
            0]
        if self.file_path == '':
            self.file_path = temp
        self.browseFile.setText(self.file_path)

    def open_settings(self):
        d = SettingsWindow(self.set_algorithm, self.set_language,
                           self.set_count, self.set_metric, self.set_graph, self)
        d.exec_()

    def output_text(self):
        self.OutputText_2.setPlainText('')

        for sentence in self.out:
            self.OutputText_2.appendPlainText(sentence)

        # re-enable the generate summary button
        self.generateSummary.setDisabled(False)
        self.generateSummary.setText('Generate Summary')


class Internet(QtCore.QObject):

    def __init__(self, parent):
        super(Internet, self).__init__()
        self.parent = parent
        self.timer = QtCore.QTimer()

    def update_connection_status(self):
        if (check_internet() == True):
            self.parent.internet_status.setStyleSheet('color: green')
            self.parent.internet_status.setText('ONLINE')
        else:
            self.parent.internet_status.setStyleSheet('color: red')
            self.parent.internet_status.setText('OFFLINE')

    def run(self):
        # add timer to check internet connection
        self.timer.timeout.connect(self.update_connection_status)
        self.timer.start(1000)


class SumT(QtCore.QObject):

    def __init__(self, parent):
        super(SumT, self).__init__()
        self.parent = parent

    def summary(self):
        if self.parent.file_path != '':
            out = None

            if str(self.parent.comboBox.currentText()) == 'File':
                self.parent.text = open(self.parent.file_path, 'r').read()
            elif str(self.parent.comboBox.currentText()) == 'URL':
                if str(self.parent.internet_status.text()) == 'OFFLINE':
                    return
                self.parent.text = get_text(self.parent.file_path)

            if self.parent.set_algorithm == 'FS':
                out = fs(self.parent.text, self.parent.set_language,
                         int(self.parent.set_count))
            elif self.parent.set_algorithm == 'TextRank':
                tr = TextRank(self.parent.text, int(self.parent.set_count),
                              self.parent.set_language, self.parent.set_metric, self.parent.set_graph)
                out = tr.summarize()

            self.parent.out = out


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ats = MainWindow()
    ats.show()

    sys.exit(app.exec_())
