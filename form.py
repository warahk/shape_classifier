#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

This program shows a confirmation 
message box when we click on the close
button of the application window. 

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):
                       
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        # Label for the first row
        lbl_filePath = QtGui.QLabel('Filepath:')
        grid.addWidget(lbl_filePath,0,0)

        # Display the file path in a label
        self.filePath = QtGui.QLineEdit()
        grid.addWidget(self.filePath,0,1)
        
        # Adds the image select button
        btn_imgSelect = QtGui.QPushButton('Select Image')
        btn_imgSelect.clicked.connect(self.open)
        btn_imgSelect.setToolTip('Identify the image you would like to detect from.')
        grid.addWidget(btn_imgSelect,0,2)
        
        
        # Display image
        self.img_shape = QtGui.QLabel(self)
        self.img_shape.setGeometry(10, 10, 400, 100)
        grid.addWidget(self.img_shape,1,1)        
        
        
        # Adds the classify button
        btn = QtGui.QPushButton('Identify Shape')
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.setToolTip('Classify shape of image specified by system path')
        grid.addWidget(btn,2,1)
        
        
        # This is where image will display
        label = QtGui.QLabel()
        grid.addWidget(label,5,0) 
    
        self.resize(500, 400)
        self.setLayout(grid)   
        self.setWindowTitle('Shape Identifier')   
        self.setWindowIcon(QtGui.QIcon('small_icon.png')) 
        self.show()
        self.center()
        
    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath())
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s.  Make sure you have the right path and you have selected an image." % fileName)
                return
            
            self.img_shape.setPixmap(QtGui.QPixmap(fileName))
            self.img_shape.show()
            
            self.filePath.setText(fileName)
        
    
    def center(self):
       
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())      
        
    def closeEvent(self, event):
        
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()