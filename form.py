#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Program        shape_classifier
Authors        Dustin Delmer, Kyle Maysey, David Robison.
Date            05/11/2013
Description    Takes an image of a shape from file and attempts to identify the shape.
"""

import sys
from PyQt4 import QtGui, QtCore
import TestFeature

from scipy.sparse.csgraph import _validation

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):         
              
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        # Label for the first row
        lbl_filePath = QtGui.QLabel('<b>Filepath:</b>')
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
        grid.addWidget(self.img_shape,1,1) 
        grid.setRowStretch(1,1)
        grid.setColumnStretch(1,1)     
        
        
        # Adds the classify button
        btn = QtGui.QPushButton('Identify Shape')
        btn.clicked.connect(self.determineShape)
        btn.setToolTip('Classify shape of image specified by system path')
        grid.addWidget(btn,2,1)
        
        
        # Output
        
        # Shape feature labels
        fontOutput1 = QtGui.QFont('Calibri', 12, QtGui.QFont.Light)
        fontOutput2 = QtGui.QFont('Calibri', 14, QtGui.QFont.Light)
        
        self.lbl_features = QtGui.QLabel('<u><b>Image Features</b></u>')
        grid.addWidget(self.lbl_features,3,1)
        self.lbl_features.setFont(fontOutput2)
        self.lbl_features.show()        
        
        self.lbl_corners = QtGui.QLabel('')
        grid.addWidget(self.lbl_corners,4,1)       
        self.lbl_corners.setFont(fontOutput1)
       
        self.lbl_angles = QtGui.QLabel('')
        grid.addWidget(self.lbl_angles,5,1)
        self.lbl_angles.setFont(fontOutput1)
        
        self.lbl_sides = QtGui.QLabel('')
        grid.addWidget(self.lbl_sides,6,1)   
        self.lbl_sides.setFont(fontOutput1)          
        
        # Shape result label
        self.lbl_features = QtGui.QLabel('<u><b>Result</b></u>')
        grid.addWidget(self.lbl_features,7,1)
        self.lbl_features.setFont(fontOutput2)
        self.lbl_features.show()        
        
        self.lbl_classifiedAs = QtGui.QLabel('')
        grid.addWidget(self.lbl_classifiedAs,8,1)
        
        self.lbl_classifiedAs.setFont(fontOutput1)   
        
    
        # Main window properties
        self.resize(500, 500)
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
            
            # Sets the image
            myPixmap = QtGui.QPixmap(fileName).scaled(self.img_shape.size(), QtCore.Qt.KeepAspectRatio)
            self.img_shape.setPixmap(QtGui.QPixmap(myPixmap))
            
            self.img_shape.show()
            
            # Sets the file path to image on text box.
            self.filePath.setText(fileName)
            
            # Clear shape text
            self.lbl_classifiedAs.setText('')
            self.lbl_corners.setText('') 
            self.lbl_sides.setText('') 
            self.lbl_angles.setText('')             
            
    def determineShape(self):  
        
        # Check to see if image has been selected.
        fileName = self.filePath.text()
        
        if (fileName == ""):
            return
        try:
            fvec, shape = TestFeature.main(str(fileName), int(4))
            self.lbl_classifiedAs.setText('<b>Classified as:</b>     %s!' % shape)
            self.lbl_corners.setText('<b>Number of corners:</b>     %s' % fvec[0])
            self.lbl_angles.setText('<b>Average angle deviation:</b>     %s' % fvec[1])
            self.lbl_sides.setText('<b>Maximum side ratio:</b>     %s' % fvec[2])
            
        except(ZeroDivisionError):
            self.lbl_classifiedAs.setText('Unable to detect!')
        
    
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