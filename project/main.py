import os
import PySide2
import sys

#import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib import animation
#from Imcompressible.Imcompress import Imcompress

#def main():
#Im1 = Imcompress()
    #psi = Im1.cal_stream(0.1,0.1)
    
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide2.QtWidgets import QApplication
from PySide2 import QtCore
from run_ui import MainWindow


if __name__ =="__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication([])
    mainw = MainWindow()
    mainw.show()
    app.exec_()
    #sys.exit(app.exec_())
    
#if __name__=="__main__":
    #main()