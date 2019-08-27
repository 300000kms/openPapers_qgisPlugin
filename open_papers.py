# -*- coding: utf-8 -*-
"""
/***************************************************************************
 openPapers
                                 A QGIS plugin
 Open Papers: Make an atlas, print it, draw, scan and analize.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-08-15
        git sha              : $Format:%H$
        copyright            : (C) 2019 by 300.000kms.net
        email                : info@300000kms.net
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
from qgis.PyQt.QtCore import Qt, QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon, QCursor
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QApplication
from qgis.gui import  QgsScaleWidget
from qgis.PyQt.QtWidgets import QToolBar

from qgis.core import QgsMapLayerProxyModel

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .open_papers_dialog import openPapersDialog
import os.path


from .op import printatlas



class openPapers:
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
            'openPapers_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&openPapers')
        self.toolbar = self.iface.addToolBar(u'openPapers')
        self.toolbar.setObjectName(u'openPapers')

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
        return QCoreApplication.translate('openPapers', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
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

        self.dlg = openPapersDialog()

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            #self.iface.addToolBarIcon(action)
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/open_papers/icon.png'
        #icon_path = ':/plugins/Spanish_Inspire_Catastral_Downloader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'open papers'),
            callback=self.run,
            parent= self.iface.mainWindow()
        )

        # will be set False in run()
        self.first_start = True

        # icon_path = ':/plugins/open_papers/icon.png'
        # self.add_action(
        #     icon_path,
        #     text=self.tr(u'oppen papers2'),
        #     callback=self.run,
        #     parent=self.iface.mainWindow())
        #
        # # will be set False in run()
        # self.first_start = True

        self.dlg.pushButton_select_path.clicked.connect(self.select_output_folder)
        self.dlg.pushButton_run.clicked.connect(self.doit)
        return


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&openPapers'),
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar


    def doit(self):
        #QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.dlg.progressBar.setValue(0)

        qptChapter = self.dlg.mQgsFileWidget_1.filePath()
        qptDivision = self.dlg.mQgsFileWidget_2.filePath()
        qptForm = self.dlg.mQgsFileWidget_3.filePath()

        printForm = True if self.dlg.checkBox.isChecked() else False
        isTest = True if self.dlg.checkBox_2.isChecked() else False

        zl_layer = self.dlg.mMapLayerComboBox.currentLayer()
        zl_field = self.dlg.mFieldComboBox.currentText()
        di_layer = self.dlg.mMapLayerComboBox_2.currentLayer()
        di_field = self.dlg.mFieldComboBox_2.currentText()
        di_name  = self.dlg.mFieldComboBox_3.currentText()
        scale = 1.0 / self.dlg.mScaleWidget.scale()

        printatlas.makeAtlas(
            qptChapter,
            qptDivision,
            qptForm,
            zl_layer,
            zl_field,
            di_layer,
            di_field,
            di_name,
            scale,
            form_file=self.dlg.mQgsFileWidget_4.filePath(),
            form=printForm,
            project_name=self.dlg.f_project_name.text(),  # 'Cens Barcelona 2019',
            root_out=self.dlg.lineEdit_path.text(),
            pbar = self.dlg.progressBar,
            isTest = isTest
            # '/home/hp2018/Documents/_projects/_impulsem/project_badalona/out/',
        )
        self.dlg.progressBar.setValue(100)  # No llega al 100% aunque lo descargue,es random

        #QApplication.restoreOverrideCursor()
        self.dlg.close()
        return

    #############################################3
    ##ui

    def getLayerFields(self):
        layer = self.dlg.mMapLayerComboBox.currentLayer()
        self.dlg.mFieldComboBox.setLayer(layer)
        return

    def getLayerFieldsArea(self):
        layer = self.dlg.mMapLayerComboBox_2.currentLayer()
        self.dlg.mFieldComboBox_3.setLayer(layer)
        self.dlg.mFieldComboBox_2.setLayer(layer)
        return

    def select_output_folder(self):
        """Select output folder"""

        self.dlg.lineEdit_path.clear()
        folder = QFileDialog.getExistingDirectory(self.dlg, "Select folder")
        self.dlg.lineEdit_path.setText(folder)

    ##
    def run(self):
        """Run method that performs all the real work"""
        #root_code = '/home/hp2018/Documents/_projects/_impulsem/code/'
        root_code = os.path.dirname(os.path.realpath(__file__))
        print(root_code)
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            #self.dlg = openPapersDialog()

        self.dlg.progressBar.setValue(0)

        self.dlg.mQgsFileWidget_1.setFilePath(root_code + 'templates/arrelsAtlas_chapter.qpt')
        self.dlg.mQgsFileWidget_2.setFilePath(root_code + 'templates/arrelsAtlas_division.qpt')
        self.dlg.mQgsFileWidget_3.setFilePath(root_code + 'templates/arrelsAtlas_form.qpt')
        self.dlg.checkBox.setChecked(1)
        self.dlg.mQgsFileWidget_4.setFilePath(root_code + '/assets/formArrels_03.svg')

        self.dlg.mMapLayerComboBox.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.dlg.mMapLayerComboBox.layerChanged.connect(self.getLayerFields)

        self.dlg.mMapLayerComboBox_2.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.dlg.mMapLayerComboBox_2.layerChanged.connect(self.getLayerFieldsArea)

        self.dlg.setWindowIcon(QIcon(':/plugins/open_papers/icon.png'));
        self.dlg.mScaleWidget.setScale(2000)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result: pass

