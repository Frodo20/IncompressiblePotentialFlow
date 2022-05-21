# -*- coding: utf-8 -*-

import os
from re import S
from turtle import up
import PySide2
import sys

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


from PySide2.QtUiTools import QUiLoader
import matplotlib
matplotlib.use("Qt5Agg")

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from PySide2.QtGui import QDoubleValidator, QIntValidator

import numpy as np
from Imcompressible.Imcompress import Imcompress
import matplotlib.animation as ani
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel,QWidget
from ui_main import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        #self.ui=Ui_GUI()
        self.ui.setupUi(self)
        self.setWindowTitle('绘制流函数')
        #self.resize(640, 780)
        # self.ui.resize(1200,1200)
        self.fig = plt.figure(figsize=(10,6),dpi=80)
        axis = self.fig.add_subplot(1,1,1)  # Prep empty plot
        self.initialize_figure(self.fig, axis)
        self.init_event()
        self.init_para()
        #self.change_plot()
    
    def init_event(self):
        self.doubleOnly=QDoubleValidator() # 限制输入为浮点数
        self.intOnly=QIntValidator() # 限制输入为整型数
        
        self.ui.pushButton.clicked.connect(self.plot)
        self.ui.pushButton_2.clicked.connect(self.clear_1)
        self.ui.pushButton_3.clicked.connect(self.exit_1)

        #self.ui.auto_y.toggled.connect(lambda: self.sety(self.ui.auto_y))
        #self.ui.fix_y.toggled.connect(lambda: self.sety(self.ui.fix_y))

        #self.IsFixY =False
        #self.up_y=0
        #self.down_y=0

        self.ui.lineEdit.textChanged.connect(self.set_length)
        self.ui.lineEdit.setValidator(self.doubleOnly)

        self.ui.lineEdit_2.textChanged.connect(self.set_width)
        self.ui.lineEdit_2.setValidator(self.doubleOnly)

        self.ui.lineEdit_3.textChanged.connect(self.change_r)
        self.ui.lineEdit_3.setValidator(self.doubleOnly)

        self.ui.lineEdit_4.textChanged.connect(self.change_v)
        self.ui.lineEdit_4.setValidator(self.doubleOnly)

        self.ui.lineEdit_5.textChanged.connect(self.change_step_x)
        self.ui.lineEdit_5.setValidator(self.doubleOnly)

        self.ui.lineEdit_6.textChanged.connect(self.change_step_y)
        self.ui.lineEdit_6.setValidator(self.doubleOnly)

        self.ui.lineEdit_7.textChanged.connect(self.change_eps)
        self.ui.lineEdit_7.setValidator(self.doubleOnly)

        self.ui.lineEdit_8.textChanged.connect(self.change_incre)
        self.ui.lineEdit_8.setValidator(self.doubleOnly)

        self.ui.lineEdit_9.textChanged.connect(self.change_num)
        self.ui.lineEdit_9.setValidator(self.intOnly)

        self.ui.radioButton.toggled.connect(lambda:self.change_save(self.ui.radioButton))
        #self.ui.task2.toggled.connect(lambda: self.change_type(self.ui.task2))
        #self.ui.task3.toggled.connect(lambda: self.change_type(self.ui.task3))

        #self.ui.FTBS.toggled.connect(lambda: self.change_method(self.ui.FTBS))
        #self.ui.FTFS.toggled.connect(lambda: self.change_method(self.ui.FTFS))
        #self.ui.FTCS.toggled.connect(lambda: self.change_method(self.ui.FTCS))

    def set_length(self):
        self.length=float(self.ui.lineEdit.text()) if self.ui.lineEdit.text()!="" and self.ui.lineEdit.text()!="-" else 0

    def set_width(self):
        self.width=float(self.ui.lineEdit_2.text()) if self.ui.lineEdit_2.text()!="" and self.ui.lineEdit_2.text()!="-" else 0

    #def sety(self,button):
        #if button.text() == '固定模式':
            #if button.isChecked()== True:
                #self.IsFixY =True

        #elif button.text() == '自动调整':
            #if button.isChecked()== True:
                #self.IsFixY =False


    def change_r(self):
        self.r=float(self.ui.lineEdit_3.text()) if self.ui.lineEdit_3.text()!="" and self.ui.lineEdit.text()!="-" else 0

    def change_v(self):
        self.v=float(self.ui.lineEdit_4.text()) if self.ui.lineEdit_4.text()!="" else 0

    def change_step_x(self):
        self.step_x=float(self.ui.lineEdit_5.text())  if self.ui.lineEdit_5.text() !="" else 0

    def change_step_y(self):
        self.step_y=float(self.ui.lineEdit_6.text()) if self.ui.lineEdit_6.text() !="" else 0

    def change_eps(self):
        self.eps=float(self.ui.lineEdit_7.text()) if self.ui.lineEdit_7.text()!="" else 0

    def change_incre(self):
        self.incre=float(self.ui.lineEdit_8.text()) if self.ui.lineEdit_8.text()!="" else 0

    def change_num(self):
        self.num=int(self.ui.lineEdit_9.text()) if self.ui.lineEdit_9.text()!="" else 0

    def change_save(self,button):
        if button.text() =='保存数据':
            if button.isChecked()==True:
                self.sav=1

    #def change_type(self,button):
        #if button.text() == '题目1':
            #if button.isChecked()== True:
                #self.type=1

        #elif button.text() == '题目2':
           #if button.isChecked()== True:
               #self.type=2

        #elif button.text() == '题目3':
            #if button.isChecked()== True:
                #self.type=3

    #def change_method(self,button):
        #if button.text() == 'FTBS':
            #if button.isChecked()== True:
                #self.method="FTBS"

        #elif button.text() == 'FTFS':
            #if button.isChecked()== True:
                #self.method="FTFS"

        #elif button.text() == 'FTCS':
            #if button.isChecked()== True:
                #self.method="FTCS"

    def init_para(self):
        self.length=3.5
        self.width=2
        self.v=1
        self.r=1
        self.step_x=0.1
        self.step_y=0.1
        self.eps=1e-7
        self.incre=0.1
        self.sav=0
        self.num=8

    def plot(self):
        sender = self.sender()
        #self.showcal()
        self.change_plot()

    def change_plot(self):
        self.clear()

        Im1 = Imcompress(_length=self.length,_width=self.width,_r=self.r,_v=self.v)

        psi = Im1.cal_stream(dx=self.step_x,dy=self.step_y,eps=self.eps,save_flag=self.sav)

        x = np.arange(0,self.length+self.step_x,self.step_x)
        y = np.arange(0,self.width+self.step_y,self.step_y)

        incre = np.arange(self.incre,self.num*self.incre,self.incre)
            
            
        #plot
        #plt.figure(figsize=(8,6),dpi=80)
        C=plt.contour(x,y,psi,incre)
        plt.clabel(C,inline=True,fontsize=10)
        plt.ylabel("y")
        plt.title("Stream Function Line",weight="bold")
        #self.colorbar=plt.colorbar()
        #plt.show()

        self.canvas.draw()


    def showcal(self):
        #self.ui.statusBar().show()
        self.ui.statusBar.showMessage("正在计算...",0)
    
    def clearshow(self):
        self.ui.statusBar.clearMessage()

    def clear_1(self):
        sender = self.sender()
        self.clear()

    def clear(self):
        #self.colorbar.remove()
        self.ax.clear()
        self.canvas.draw()

    def exit_1(self):
        sender = self.sender()
        self.exit()

    def exit(self): #退出应用程序
        app = QApplication.instance()
        app.quit()
        #sys.exit(self.exec_())

    def initialize_figure(self, fig, ax):
        ''' 
        Initializes a matplotlib figure inside a GUI container.
        Only call this once when initializing.
        '''
        # Figure creation (self.fig and self.ax)
        self.fig = fig
        self.ax = ax

        # Canvas creation
        self.canvas = FigureCanvas(self.fig)
        self.ui.verticalLayout_3.addWidget(self.canvas)
        # self.fig.tight_layout()
        self.canvas.draw()

        # Toolbar creation
        self.toolbar = NavigationToolbar(self.canvas, self,coordinates=True)
        self.ui.verticalLayout_4.addWidget(self.toolbar)
