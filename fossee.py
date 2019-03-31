import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QFileDialog, \
    QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import  QRect, Qt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline, interp1d
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
        self.title = 'PyQt5 simple window'
        self.left = 50
        self.top = 50
        self.width = 1500
        self.height = 1500
        self.setScreen()
        loadUi('Screen.ui', self)
        # if we select Load option under File menu from main window then it connects to the load_csv_file function
        self.actionLoad.triggered.connect(self.load_csv_file)
        # if we select Edit data option under File menu from main window then it connects to the edit_data function
        self.menuEdit.triggered.connect(self.edit_data)
        # if we select Plot option from main window then it connects to the plot function
        self.actionPlot_Data.triggered.connect(self.plot)
        # if we select Add data option under File menu from main window then it connects to the add_data function
        self.menuAdd_Data.triggered.connect(self.add_data)
        # if we select Save as PNG option under File menu from main window then it connects to the saveAsPNG function
        self.save_plot.triggered.connect(self.saveAsPNG)

    # setting the screen for the main window
    def setScreen(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height )


    # by clicking on Add Data option from the main window this function is executed
    #this function adds an empty row to the table
    def add_data(self):
        # checking for data is empty which indicates that csv file not loaded
        if(data.empty) :
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!") #raises message box
        else:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            QMessageBox.about(self, "Add Data", "Empty row is Added to The Table You can Add the data now!!!")


    #when we select Editdata option from the main window this function is executed and it calls the editTablefunction
    def edit_data(self):
        # checking for data is empty which indicates that csv file not loaded
        if (data.empty):
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!")
        else:
            other = MainFrame()
            MainFrame.FrameList.append(other)
            # calling editTable function
            other.editTable()
            other.layout = QVBoxLayout()
            other.layout.addWidget(other.tableWidget)
            other.setLayout(other.layout)
            other.show()
            self.destroy()


    # editTable function will give the permission to edit the  contents of the table which is displayed from the loaded csv file
    def editTable(self):
        # df contains number of rows and columns of dataFrame
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


    # if we click on scatter plot buuton then this function is called,selected column names from the comboboxes are retrieved
    #and the  ploting is takes between two selected columns and title, lables are added and the plot is displayed
    def on_click_scatter(self):
        self.flag=1
        self.imageTitle ='Scatter Plot'
        plt.title(self.imageTitle)
        # getting the current selected item from the combobox1
        text1 = str(self.comboBox1.currentText())
        # getting the current selected item from the combobox2
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
            # all values from selected column1 are stored as list in x_axis
            x_axis = data[text1].values
            # all values from selected column2 are stored as list in y_axis
            y_axis = data[text2].values
            # plotting scatterplot
            plt.scatter(x_axis,y_axis)
            plt.savefig("plottedImage")
            plt.show()


    # if we click on scatter plot with smoooth lines buuton then this function is called,selected column names from the comboboxes are retrieved
    #and the  ploting is takes between two selected columns and title, lables are added and the plot is displayed
    def on_click_scatter_smooth(self):
        self.flag=1
        self.imageTitle ='Scatter Plot With Smooth Lines'
        plt.title(self.imageTitle )#setting title for scatter plot with smooth line
        text1 = str(self.comboBox1.currentText()) #getting the current selected item from the combobox1
        text2 = str(self.comboBox2.currentText()) #getting the current selected item from the combobox2
        plt.xlabel(text1) #setting x lable to the plot
        plt.ylabel(text2) #setting y lable to the plot
        if (text1 == 'please select column1' and text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Columns first")
        elif (text1 == 'please select column1'):
            QMessageBox.about(self, "Plotting", "Select Column1")
        elif (text2 == 'please select column2'):
            QMessageBox.about(self, "Plotting", "Select Column2")
        elif (text1 == text2):
            QMessageBox.about(self, "Plotting", "x-axis and y-axis should not be same please select different!!!")
        else:
            # all values from selected column1 are stored as list in x_axis
            x_axis = data[text1]
            # all values from selected column2 are stored as list in y_axis
            y_axis = data[text2]
            x_smooth = np.linspace(x_axis.min(), x_axis.max(),len(x_axis)*500)
            p = interp1d(x_axis, y_axis, kind='quadratic')
            y_smooth = p(x_smooth)
            # plotting scatter plot
            plt.scatter(x_axis,y_axis)
            #plotting a smooth line
            plt.plot(x_smooth, y_smooth)
            plt.savefig("plottedImage")
            plt.show()


    # if we click on lines buuton this function is called,selected column names from the comboboxes are retrieved
    #and the line plot is takes between two selected columns and title, lables are added and the plot is displayed
    def on_click_lines(self):
        self.flag=1
        self.imageTitle='Line Plot'
        plt.title(self.imageTitle)
        global data
        # getting the current selected item from the combobox1
        text1 = str(self.comboBox1.currentText())
        # getting the current selected item from the combobox2
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
            # all values from selected column1 are stored as list in x_axis
            x_axis=data[text1].values
            # all values from selected column2 are stored as list in y_axis
            y_axis= data[text2].values
            # plotting line plot
            plt.plot(x_axis,y_axis)
            plt.savefig("plottedImage")
            plt.show()


    #from the main frame if we select Save As PNG then this  function is executed and it is used to save the plotted image
    def saveAsPNG(self,plt):
        # checking for data is not empty which indicates that csv file loaded
        if (not data.empty):
            if(self.flag==0):
                QMessageBox.about(self, 'Important', "please plot first!!")
            else:
               QMessageBox.about(self, 'Save As PNG', self.imageTitle+ " "+"is saved to your folder you can check over there")
        else:
            # if csv file is not loaded message box will be raised
            QMessageBox.about(self, 'Important', "Please Load Data First !!!")


    # plot displays two combo boxes each combo box contains the column names of the dataFrame we have to selct two columns
    # it also displays 3 buttons,choosing one of those buttons shows us a plot according to the selected button
    def plot(self):
        # checking for data is empty which indicates that cvs file not loaded
        if (data.empty):
            QMessageBox.about(self, "Empty CSV File", "Please Load CSV File First!!!")
        else:
            QMessageBox.about(self, "Plot", "NOTE : Please select the columns wich have numeric data only !!!")
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
                # adding an item to the combobox2 and the item is column name of the dataset
                other.comboBox2.addItem(columns[i])
            button1= QPushButton('scatter points',other)
            button1.move(100, 70) # setting button position in the frame
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


    # load csv_file () csv file is loaded.the path of the csv file is found out and it reads by using pandas
    # after loading it calls createTable function
    def load_csv_file(self):
        options = QFileDialog.Options()
        options= QFileDialog.DontUseNativeDialog
        self.fileName= QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                       "Python Files (*.csv)", options=options)

        global data
        # reading csv file from the path and storing it into data
        data=pd.read_csv(self.fileName[0])

        self.size=data.shape
        # calling  createTable function to create table like structure
        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.show()


    # createTable function creates a table and the number of rows,columns of the table depends on the rows & columns of the dataFrame(csv file)
    #in each cell of the table the corresponding data of the csv file is retrived and placed
    #editable option is disabled and finally loaded csv file data is displayed in the form of table
    def createTable(self):
        df=data.shape
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.tableWidget = QTableWidget(centralWidget)
        self.tableWidget.setRowCount(df[0])
        self.tableWidget.setColumnCount(df[1])
        # getting column names from dataset
        column_names = data.columns
        for i in range(0,1):
            for j in range(0,len(column_names)):
                item = QTableWidgetItem(column_names[j])
                # disabling the editable option for column name
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # adding column name to the table in the i'th row and j'th column
                self.tableWidget.setItem(i, j, item)
        # data values are stored into list as two dimensional array
        list=data.values
        for i in range(1, df[0]):
            for j in range(0, df[1]):
                value = str(list[i][j])
                item = QTableWidgetItem(value)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # adding data item to the table in the i'th row and j'th column
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setFixedHeight(TABLE_FIXED_HEIGHT)
        self.tableWidget.setFixedWidth(TABLE_FIXED_WIDTH)

#execution start from here
if __name__ == '__main__':
    application = QApplication(sys.argv)
    start= MainFrame()
    start.show()
    sys.exit(application.exec())
