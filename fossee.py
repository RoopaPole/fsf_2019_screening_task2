import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QFileDialog, \
    QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import  QRect, Qt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
TABLE_FIXED_HEIGHT = 500
TABLE_FIXED_WIDTH= 700
data = pd.DataFrame()

class MainFrame(QMainWindow):
    FrameList = []
    flag = 0
    global fileName
    imageTitle = 'rj'
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window'
        self.left = 50
        self.top = 50
        self.width = 1500
        self.height = 1500
        self.setScreen()
        loadUi('Screen.ui', self)
        self.actionLoad.triggered.connect(self.load_csv_file)
        self.menuEdit.triggered.connect(self.edit_data)
        self.actionPlot_Data.triggered.connect(self.plot)
        self.menuAdd_Data.triggered.connect(self.add_data)
        self.save_plot.triggered.connect(self.saveAsPNG)
    def setScreen(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    def add_data(self):
        if(data.empty):
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!")
        else:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            QMessageBox.about(self, "Add Data", "Empty row is Added to The Table You can Add the data now!!!")

    def edit_data(self):
        if (data.empty):
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!")
        else:
            other = MainFrame()
            MainFrame.FrameList.append(other)
            other.editTable()
            other.layout = QVBoxLayout()
            other.layout.addWidget(other.tableWidget)
            other.setLayout(other.layout)
            other.show()
            self.destroy()
    def editTable(self):
        df = data.shape
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.tableWidget = QTableWidget(centralWidget)
        self.tableWidget.setRowCount(df[0])
        self.tableWidget.setColumnCount(df[1])
        list = data.values
        column_names = data.columns
        for i in range(0, 1):
            for j in range(0, len(column_names)):
                item = QTableWidgetItem(column_names[j])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)

        for i in range(1, df[0]):
            for j in range(0, df[1]):
                value = str(list[i][j])
                item = QTableWidgetItem(value)
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setFixedHeight(TABLE_FIXED_HEIGHT)
        self.tableWidget.setFixedWidth(TABLE_FIXED_WIDTH)
    def on_click_scatter(self):
        self.flag=1
        self.imageTitle ='Scatter Plot'
        plt.title(self.imageTitle)
        text1 = str(self.comboBox1.currentText())
        text2 = str(self.comboBox2.currentText())
        plt.xlabel(text1)
        plt.ylabel(text2)
        if(text1 =='please select column1' and text2 =='please select column2'):
            QMessageBox.about(self, "Plotting", "Select Columns first")
        elif (text1 =='please select column1' ):
            QMessageBox.about(self, "Plotting", "Select Column1")
        elif (text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Column2")
        elif(text1 == text2):
            QMessageBox.about(self, "Plotting", "x-axis and y-axis should not be same please select different!!!")
        else:
            x_axis = data[text1].values
            y_axis = data[text2].values
            plt.scatter(x_axis,y_axis)
            plt.savefig("plottedImage")
            plt.show()
    def on_click_scatter_smooth(self):
        self.flag=1
        self.imageTitle ='Scatter Plot With Smooth Lines'
        plt.title(self.imageTitle)
        
        text1 = str(self.comboBox1.currentText())
        text2 = str(self.comboBox2.currentText())
        plt.xlabel(text1)
        plt.ylabel(text2)
        if (text1 == 'please select column1' and text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Columns first")
        elif (text1 == 'please select column1'):
            QMessageBox.about(self, "Plotting", "Select Column1")
        elif (text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Column2")
        elif (text1 == text2):
            QMessageBox.about(self, "Plotting", "x-axis and y-axis should not be same please select different!!!")
        else:
            x_axis = data[text1]
            y_axis = data[text2]
            x_smooth = np.linspace(x_axis.min(), x_axis.max(),500)
           # f = interp1d(x_axis, y_axis,kind='quadratic')
            #y_smooth = f(x_smooth)
            y_smooth = spline(x_axis,y_axis,x_smooth)
            plt.scatter(x_axis,y_axis)
            plt.plot(x_smooth, y_smooth)
            plt.savefig("plottedImage")
            plt.show()


    def on_click_lines(self):
        self.flag=1
        self.imageTitle='Line Plot'
        plt.title(self.imageTitle)
        global data
        text1 = str(self.comboBox1.currentText())
        text2= str(self.comboBox2.currentText())
        plt.xlabel(text1)
        plt.ylabel(text2)
        if (text1 == 'please select column1' and text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Columns first")
        elif (text1 == 'please select column1'):
            QMessageBox.about(self, "Plotting", "Select Column1")
        elif (text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Column2")
        elif (text1 == text2):
            QMessageBox.about(self, "Plotting", "x-axis and y-axis should not be same please select different!!!")
        else:
            x_axis= data[text1].values
            y_axis= data[text2].values
            plt.plot(x_axis,y_axis)
            plt.savefig("plottedImage")
            plt.show()
    def saveAsPNG(self,plt):
        if (not data.empty):
            if(self.flag==0):
                QMessageBox.about(self, 'Important', "please plot first!!")
            else:
               QMessageBox.about(self, 'Save As PNG', self.imageTitle+ " "+"is saved to your folder you can check over there")

        else:
            QMessageBox.about(self, 'Important', "Please Load Data First !!!")
    def plot(self):
        if (data.empty):
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!")
        else:
            other = MainFrame()
            MainFrame.FrameList.append(other)
            centralWidget = QWidget(other)
            other.setCentralWidget(centralWidget)
            other.comboBox1= QComboBox(centralWidget)
            other.comboBox1.setGeometry(QRect(3, 3, 600, 31))
            other.comboBox1.setObjectName(("comboBox1"))
            dimension=data.shape
            columns = list(data.head(0))
            other.comboBox1.addItem('please select column1')
            for i in range (0,dimension[1]):
                 other.comboBox1.addItem(columns[i])

            other.comboBox2 = QComboBox(centralWidget)
            other.comboBox2.setGeometry(QRect(610, 3, 600, 31))
            other.comboBox2.setObjectName(("comboBox2"))
            other.comboBox2.addItem('please select column2')
            for i in range (0,dimension[1]):
                    other.comboBox2.addItem(columns[i])

            button1= QPushButton('scatter points',other)
            button1.move(100, 70)
            button1.clicked.connect(other.on_click_scatter)
            button2= QPushButton('scatter points with smooth lines', other)
            button2.resize(200, 32)
            button2.move(300, 70)
            button2.clicked.connect(other.on_click_scatter_smooth)
            button3= QPushButton(' lines', other)
            button3.move(600, 70)
            button3.clicked.connect(other.on_click_lines)
            other.show()
            self.destroy()
    def load_csv_file(self):
        options = QFileDialog.Options()
        options= QFileDialog.DontUseNativeDialog
        self.fileName= QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                       "Python Files (*.csv)", options=options)

        global data
        data=pd.read_csv(self.fileName[0])#reading csv file from the path and storing it into data

        self.size=data.shape
        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.show()


    def createTable(self):
        df=data.shape
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.tableWidget = QTableWidget(centralWidget)
        self.tableWidget.setRowCount(df[0])
        self.tableWidget.setColumnCount(df[1])
        list=data.values
        column_names = data.columns
        for i in range(0,1):
            for j in range(0,len(column_names)):
                item = QTableWidgetItem(column_names[j])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)
        for i in range(1, df[0]):
            for j in range(0, df[1]):
                value = str(list[i][j])
                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setFixedHeight(TABLE_FIXED_HEIGHT)
        self.tableWidget.setFixedWidth(TABLE_FIXED_WIDTH)

if __name__ == '__main__':
    application = QApplication(sys.argv)
    start= MainFrame()
    start.show()
    sys.exit(application.exec())
