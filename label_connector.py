# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LabelConnector
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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QAction, QMessageBox, QToolBar
from PyQt5 import QtXml
from qgis.core import (QgsMapLayer, QgsGeometryGeneratorSymbolLayer, QgsSymbol, QgsPalLayerSettings,
                       QgsPropertyCollection, QgsProperty, QgsPropertyDefinition, QgsVectorLayerSimpleLabeling)
from qgis.gui import QgsNewAuxiliaryLayerDialog

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .label_connector_dialog import LabelConnectorDialog
from .label_connector_settings import LabelConnectorSettings
import os.path


class LabelConnector:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            '{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # define toolBar by default find the label toolbar
        # else it will be the plugin toolbar
        self.toolBar = self.iface.mainWindow().findChild(QToolBar, "mLabelToolBar")
        if not self.toolBar:
            print("Label toolbar not found\n")
            self.toolBar = pluginToolBar()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Label Connector')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('LabelConnector', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip='Adds a symbol showing connectors when labels are manually moved',
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.toolBar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        # label connector
        icon_path = ':/plugins/label_connector/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Create label connector'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # settings
        icon_path = ':/plugins/label_connector/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Label connector settings'),
            callback=self.runSettings,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False)

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Label Connector'),
                action)
            self.toolBar.removeAction(action)

    def runSettings(self):
        dlgSettings = LabelConnectorSettings()
        # show the dialog
        dlgSettings.show()
        # Run the dialog event loop
        result = dlgSettings.exec_()
        if result:
            QSettings().setValue("LabelConnector/showWindow",
                                 not dlgSettings.checkBox.isChecked())

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = LabelConnectorDialog()

        self.layer = self.iface.activeLayer()

        if not self.layer or (self.layer.type() != QgsMapLayer.VectorLayer):
            QMessageBox.warning(self.iface.mainWindow(), self.tr("No active vector layer"),
                                self.tr("Label connector requires a vector layer"))
            return

        ret = False
        expressionFile = ""
        if QSettings().value("LabelConnector/showWindow", True):
            # show the dialog
            self.dlg.show()
            # Run the dialog event loop
            result = self.dlg.exec_()
            if result:
                expressionFile = self.dlg.labelStyleCombo.currentData()
                ret = self.applyStyle(expressionFile)
                QSettings().setValue("LabelConnector/showWindow",
                                     not self.dlg.dontShowBox.isChecked())
        else:
            expressionFile = QSettings().value("LabelConnector/lastFile", "")
            if expressionFile:
                ret = self.applyStyle(expressionFile)
            else:
                QMessageBox.critical(self.iface.mainWindow(), self.tr("No expression file"),
                                     self.tr("Cannot find a previous expression file applied."))

        QSettings().setValue("LabelConnector/lastFile", expressionFile)

    def checkAuxiliaryStorage(self):
        if not self.layer.auxiliaryLayer():
            dlg = QgsNewAuxiliaryLayerDialog(self.layer)
            dlg.exec_()

        if not self.layer.auxiliaryLayer():
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Auxiliary Layer Error"),
                                 "{}".format("Cannot create auxiliary storage for {}".format(self.layer.name())))
            return False

        return True

    def createAuxiliaryFields(self):
        props = (('PositionX', QgsPropertyDefinition.DataTypeNumeric, 'labeling'),
                 ('PositionY', QgsPropertyDefinition.DataTypeNumeric, 'labeling'),
                 ('Hali', QgsPropertyDefinition.DataTypeString, 'labeling'),
                 ('Vali', QgsPropertyDefinition.DataTypeString, 'labeling'))

        for prop in props:
            p = QgsPropertyDefinition(prop[0], prop[1], '', '', prop[2])
            if not self.layer.auxiliaryLayer().exists(p):
                self.layer.auxiliaryLayer().addAuxiliaryField(p)

        self.layer.auxiliaryLayer().save()

    def createDefinedProperties(self):
        props = (('"auxiliary_storage_labeling_positionx"', QgsPalLayerSettings.PositionX),
                 ('"auxiliary_storage_labeling_positiony"',
                  QgsPalLayerSettings.PositionY),
                 ('case when  "auxiliary_storage_labeling_positionx" < x(point_on_surface($geometry)) then \'Right\' else \'Left\' end', QgsPalLayerSettings.Hali),
                 ('case when  "auxiliary_storage_labeling_positiony" < y(point_on_surface($geometry)) then \'Top\' else \'Bottom\' end', QgsPalLayerSettings.Vali))

        pc = QgsPropertyCollection('labelConnector')
        for prop in props:
            p = QgsProperty()
            p.setExpressionString(prop[0])
            pc.setProperty(prop[1], p)

        pal_layer = QgsPalLayerSettings()
        pal_layer.setDataDefinedProperties(pc)
        pal_layer.fieldName = self.layer.fields()[0].name()
        pal_layer.enabled = True

        labeler = QgsVectorLayerSimpleLabeling(pal_layer)

        self.layer.setLabeling(labeler)
        self.layer.setLabelsEnabled(True)

    def applyStyle(self, expressionFile):
        try:
            with open(expressionFile, 'r') as f:
                expr = ''.join(f.readlines())
                styleManager = self.layer.styleManager()
                if styleManager.addStyleFromLayer("label_style"):
                    if styleManager.setCurrentStyle("label_style"):
                        if self.checkAuxiliaryStorage():
                            self.createAuxiliaryFields()
                            self.createDefinedProperties()

                        sym = self.layer.renderer().symbol()
                        sym_layer = QgsGeometryGeneratorSymbolLayer.create(
                            {'geometryModifier': expr})
                        sym_layer.setSymbolType(QgsSymbol.Line)
                        sym_layer.subSymbol().symbolLayer(0).setStrokeColor(QColor(0, 0, 0))
                        sym.appendSymbolLayer(sym_layer)
                    else:
                        QMessageBox.warning(self.iface.mainWindow(), self.tr("Current style"),
                                            self.tr("Cannot change current style to 'label_style'"))
                        return False
                else:
                    QMessageBox.warning(self.iface.mainWindow(), self.tr("Add style"),
                                        self.tr("Cannot add new style 'label_style'"))
                    return False
            if self.iface.mapCanvas().isCachingEnabled():
                self.layer.triggerRepaint()
            else:
                self.iface.mapCanvas().refresh()
        except Exception as e:
            QMessageBox.critical(self.iface.mainWindow(), self.tr("Error"),
                                 "{}".format(str(e)))
            return False

        return True
