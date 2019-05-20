# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LabelConnectorDialog
                                 A QGIS plugin
 This plugin creates label connector (line from centroid to the label)
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-05-13
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Oslandia
        email                : infos@oslandia.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import ntpath

from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
from .label_connector_utils import populateComboBox

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'label_connector_dialog_base.ui'))


class LabelConnectorDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(LabelConnectorDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        populateComboBox(self.labelStyleCombo)
        self.rememberChoice.setChecked(
            not QtCore.QSettings().value("LabelConnector/showWindow", True))

        lastFile = QtCore.QSettings().value("LabelConnector/lastFile", "")

        populateComboBox(self.labelStyleCombo)
        self.labelStyleCombo.setCurrentText(ntpath.basename(lastFile))

        self.button_box.setEnabled(self.labelStyleCombo.count() > 0)
