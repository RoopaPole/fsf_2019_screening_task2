import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QFileDialog, \
    QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import  QRect, Qt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
from sklearn import preprocessing

TABLE_FIXED_HEIGHT = 650
TABLE_FIXED_WIDTH= 700
data = pd.DataFrame()

class MainFrame(QMainWindow):
    FrameList = []
    flag = 0
    global fileName
    imageTitle = 'rj'
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window'#title of the window
        self.left = 50
        self.top = 50
        self.width = 1500
        self.height = 1500
        self.setScreen()#calling setScreen function
        loadUi('Screen.ui', self)#loads the Screen.ui file
        self.actionLoad.triggered.connect(self.load_csv_file)#if we select Load option under File menu from main window then it connects to the load_csv_file function
        self.menuEdit.triggered.connect(self.edit_data)#if we select Edit data option under File menu from main window then it connects to the edit_data function
        self.actionPlot_Data.triggered.connect(self.plot)#if we select Plot option from main window then it connects to the plot function
        self.menuAdd_Data.triggered.connect(self.add_data)#if we select Add data option under File menu from main window then it connects to the add_data function
        self.save_plot.triggered.connect(self.saveAsPNG)#if we select Save as PNG option under File menu from main window then it connects to the saveAsPNG function
    def setScreen(self):
        self.setWindowTitle(self.title)#setting title for window
        self.setGeometry(self.left, self.top, self.width, self.height)#setting the geometry of the Window
    def add_data(self):
        if(data.empty):#checking for data is empty which indicates that csv file not loaded
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!")#raises message box
        else:
            rowCount = self.tableWidget.rowCount()#getting the row count of table
            self.tableWidget.insertRow(rowCount)#addig an empty row to the table
            QMessageBox.about(self, "Add Data", "Empty row is Added to The Table You can Add the data now!!!")#raising a message box

    def edit_data(self):
        if (data.empty):#checking for data is empty which indicates that csv file not loaded
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!")#raises message box
        else:
            other = MainFrame()#creating instance for MainFrame
            MainFrame.FrameList.append(other)
            other.editTable()#calling editTable function
            other.layout = QVBoxLayout()#creating instance for QVBoxLayout
            other.layout.addWidget(other.tableWidget)
            other.setLayout(other.layout)
            other.show()#displaying Frame
            self.destroy()
    def editTable(self):
        df = data.shape#df contains number of rows and columns
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
        plt.title(self.imageTitle)#setting title for scatter plot
        text1 = str(self.comboBox1.currentText())#getting the current selected item from the combobox1
        text2 = str(self.comboBox2.currentText())#getting the current selected item from the combobox2
        plt.xlabel(text1)#setting x lable to the plot
        plt.ylabel(text2)#setting y lable to the plot
        if(text1 =='please select column1' and text2 =='please select column2'):
            QMessageBox.about(self, "Plotting", "Select Columns first")
        elif (text1 =='please select column1' ):
            QMessageBox.about(self, "Plotting", "Select Column1")
        elif (text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Column2")
        elif(text1 == text2):
            QMessageBox.about(self, "Plotting", "x-axis and y-axis should not be same please select different!!!")
        else:
            x_axis = data[text1].values# all values from selected column1 are stored as list in x_axis
            y_axis = data[text2].values# all values from selected column2 are stored as list in y_axis
            plt.scatter(x_axis,y_axis)#plotting scatterplot
            plt.savefig("plottedImage")
            plt.show()#displaying the plot
    def on_click_scatter_smooth(self):
        self.flag=1
        self.imageTitle ='Scatter Plot With Smooth Lines'
        plt.title(self.imageTitle)#setting title for scatter plot with smooth line
        text1 = str(self.comboBox1.currentText())#getting the current selected item from the combobox1
        text2 = str(self.comboBox2.currentText())#getting the current selected item from the combobox2
        plt.xlabel(text1)#setting x lable to the plot
        plt.ylabel(text2)#setting y lable to the plot
        if (text1 == 'please select column1' and text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Columns first")
        elif (text1 == 'please select column1'):
            QMessageBox.about(self, "Plotting", "Select Column1")
        elif (text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Column2")
        elif (text1 == text2):
            QMessageBox.about(self, "Plotting", "x-axis and y-axis should not be same please select different!!!")
        else:
            x_axis = data[text1]# all values from selected column1 are stored as list in x_axis
            y_axis = data[text2]# all values from selected column2 are stored as list in y_axis
            x_smooth = np.linspace(x_axis.min(), x_axis.max(),500)#making smooth
            y_smooth = spline(x_axis,y_axis,x_smooth)#making smooth
            plt.scatter(x_axis,y_axis)#plotting scatte rplot
            plt.plot(x_smooth, y_smooth)#plotting a smooth line
            plt.savefig("plottedImage")
            plt.show()#displaying the plot


    def on_click_lines(self):
        self.flag=1
        self.imageTitle='Line Plot'
        plt.title(self.imageTitle)#setting title for linplot
        global data
        text1 = str(self.comboBox1.currentText())#getting the current selected item from the combobox1
        text2= str(self.comboBox2.currentText())#getting the current selected item from the combobox2
        plt.xlabel(text1)#setting x lable to the plot
        plt.ylabel(text2)#setting x lable to the plot
        if (text1 == 'please select column1' and text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Columns first")
        elif (text1 == 'please select column1'):
            QMessageBox.about(self, "Plotting", "Select Column1")
        elif (text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Column2")
        elif (text1 == text2):
            QMessageBox.about(self, "Plotting", "x-axis and y-axis should not be same please select different!!!")
        else:
            x_axis=data[text1].values # all values from selected column1 are stored as list in x_axis
            y_axis= data[text2].values# all values from selected column2 are stored as list in y_axis
            plt.plot(x_axis,y_axis)#plotting line plot
            plt.savefig("plottedImage")
            plt.show()#displaying the plot

    def saveAsPNG(self,plt):
        if (not data.empty):#checking for data is not empty which indicates that csv file loaded
            if(self.flag==0):
                QMessageBox.about(self, 'Important', "please plot first!!")
            else:
               QMessageBox.about(self, 'Save As PNG', self.imageTitle+ " "+"is saved to your folder you can check over there")

        else:
            QMessageBox.about(self, 'Important', "Please Load Data First !!!")#if csv file is not loaded message box will be raised
    def plot(self):
        if (data.empty):#checking for data is empty which indicates that cvs file not loaded
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!")#rainsing a message box
        else:
            other = MainFrame()#creating instance for Mainframe
            MainFrame.FrameList.append(other)
            centralWidget = QWidget(other)
            other.setCentralWidget(centralWidget)
            other.comboBox1= QComboBox(centralWidget)#creating combobox1
            other.comboBox1.setGeometry(QRect(3, 3, 600, 31))#setting geometry for combobox1
            other.comboBox1.setObjectName(("comboBox1"))
            dimension=data.shape
            columns = list(data.head(0))
            other.comboBox1.addItem('please select column1')#adding an item to the combobox1 and the item is please select column1
            for i in range (0,dimension[1]):
                 other.comboBox1.addItem(columns[i])#adding an item to the combobox1 and the item is column name from the dataset

            other.comboBox2 = QComboBox(centralWidget)#creating combobox2
            other.comboBox2.setGeometry(QRect(610, 3, 600, 31))#setting geometry for combobox1
            other.comboBox2.setObjectName(("comboBox2"))
            other.comboBox2.addItem('please select column2')#adding an item to the combobox2 and the item is please select column2
            for i in range (0,dimension[1]):
                    other.comboBox2.addItem(columns[i])#adding an item to the combobox2 and the item is column name from the dataset

            button1= QPushButton('scatter points',other)#creating a button with name Scatter points
            button1.move(100, 70)# setting button position in the frame
            button1.clicked.connect(other.on_click_scatter)#when the button is clicked then it goto the function on_click_scatter

            button2= QPushButton('scatter points with smooth lines', other)#creating a button with name Scatter points with smooth lines
            button2.resize(200, 32)# resizing the betton
            button2.move(300, 70)# setting button position in the frame
            button2.clicked.connect(other.on_click_scatter_smooth)#when the button is clicked then it goto the function on_click_scatter_smooth

            button3= QPushButton(' lines', other)#creating a button with name lines
            button3.move(600, 70)# setting button position in the frame
            button3.clicked.connect(other.on_click_lines)#when the button is clicked then it goto the function on_click_lines
            other.show()#displaying the window
            self.destroy()
    def load_csv_file(self):
        options = QFileDialog.Options()
        options= QFileDialog.DontUseNativeDialog
        self.fileName= QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                       "Python Files (*.csv)", options=options)

        global data
        data=pd.read_csv(self.fileName[0])#reading csv file from the path and storing it into data

        self.size=data.shape
        self.createTable()#calling th createTable function
        self.layout = QVBoxLayout()#creating instance for QVBoxLayout
        self.layout.addWidget(self.tableWidget)#tableWidget is added to the QVBoxLayout
        self.setLayout(self.layout)
        self.show()#displaying the window
    def createTable(self):#this function used to display the data in the form of table
        df=data.shape
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.tableWidget = QTableWidget(centralWidget)#tbaleWidget is the instance of QtableWidget
        self.tableWidget.setRowCount(df[0])#setting column count to tableWidget
        self.tableWidget.setColumnCount(df[1])#setting row count to tableWidget
        column_names = data.columns# getting column names from dataset
        for i in range(0,1):
            for j in range(0,len(column_names)):
                item = QTableWidgetItem(column_names[j])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)#disabling the editable option for column name
                self.tableWidget.setItem(i, j, item)#adding column name to the table in the i'th row and j'th column
        list=data.values#data values are stored into list as two dimensional array
        for i in range(1, df[0]):
            for j in range(0, df[1]):
                value = str(list[i][j])
                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled) #disabling the editable option for data item
                self.tableWidget.setItem(i, j, item) #adding data item to the table in the i'th row and j'th column
        self.tableWidget.resizeColumnsToContents() #table cells are resized  acording to the contents of dataset
        self.tableWidget.setFixedHeight(TABLE_FIXED_HEIGHT) #setting table height to be fixed with height 650
        self.tableWidget.setFixedWidth(TABLE_FIXED_WIDTH) #setting table width to be fixed with width 700

if __name__ == '__main__':#excecution starts from here
    application = QApplication(sys.argv)
    start= MainFrame()#creating  instance for main Frame
    start.show()#displaying the window
    sys.exit(application.exec())
