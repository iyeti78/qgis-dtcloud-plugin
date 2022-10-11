# -*- coding: utf-8 -*-
"""
/***************************************************************************
 dtcloudDialog
                                 A QGIS plugin
 dtcloud
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-07-12
        git sha              : $Format:%H$
        copyright            : (C) 2022 by egis
        email                : iyeti@egiskorea.com
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
import json
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from PyQt5.QtGui import ( QStandardItem, QStandardItemModel)
from PyQt5.Qt import QDesktopServices, QUrl, QMessageBox
from qgis.core import (
  QgsApplication,
  QgsDataSourceUri,
  QgsCategorizedSymbolRenderer,
  QgsClassificationRange,
  QgsPointXY,
  QgsProject,
  QgsExpression,
  QgsField,
  QgsFields,
  QgsFeature,
  QgsFeatureRequest,
  QgsFeatureRenderer,
  QgsGeometry,
  QgsGraduatedSymbolRenderer,
  QgsMarkerSymbol,
  QgsMessageLog,
  QgsRectangle,
  QgsRendererCategory,
  QgsRendererRange,
  QgsSettings,
  QgsSymbol,
  QgsRasterLayer,
  QgsWkbTypes,
  QgsSpatialIndex,
  QgsVectorLayerUtils,
  QgsCoordinateReferenceSystem
)
import json,urllib.request
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dtcloud_dialog_base.ui'))

    
class dtcloudDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(dtcloudDialog, self).__init__(parent)
        self.setupUi(self)

        str1 = '''
{
  "layers": [
    {
      "DATAID": 8182,
      "SHP_TABLE_NAME": "user_shp_newlayer3165_1660700908865",
      "SHP_DATA_STORE_NAME": "dtw_user_geo_newlayer3165",
      "SHP_LAYER_FULLNAME": "newlayer3165:user_shp_newlayer3165_1660700908865",
      "SHAPE_TYPE": "multipolygon",
      "WORKSPACE": "newlayer3165",
      "COORD_EPSG": "EPSG:4326",
      "DATA_NAME": "a"
    },
    {
      "DATAID": 8189,
      "SHP_TABLE_NAME": "user_shp_newlayer3165_1660709985865",
      "SHP_DATA_STORE_NAME": "dtw_user_geo_newlayer3165",
      "SHP_LAYER_FULLNAME": "newlayer3165:user_shp_newlayer3165_1660709985865",
      "SHAPE_TYPE": "multipolygon",
      "WORKSPACE": "newlayer3165",
      "COORD_EPSG": "EPSG:4326",
      "DATA_NAME": "b"
    },
    {
      "DATAID": 8190,
      "SHP_TABLE_NAME": "user_shp_newlayer3165_1660710063821",
      "SHP_DATA_STORE_NAME": "dtw_user_geo_newlayer3165",
      "SHP_LAYER_FULLNAME": "newlayer3165:user_shp_newlayer3165_1660710063821",
      "SHAPE_TYPE": "multipolygon",
      "WORKSPACE": "newlayer3165",
      "COORD_EPSG": "EPSG:4326",
      "DATA_NAME": "c"
    }   
  ],
  "url": "https://geo.dtwincloud.com/newlayer3165/wms?",
  "status": "200"
}
'''
#        self.comboBox.clear()   
        

        
        

#        for layer in self.jsonObject:
#            self.comboBox.addItem(layer['name'])
        self.model = QStandardItemModel()
        self.model.clear()

        self.pushButton.clicked.connect(self.button1Click)
        self.pushButton_2.clicked.connect(self.button2Click)
        self.pushButton_3.clicked.connect(self.button3Click)
        self.pushButton_4.clicked.connect(self.button4Click)
        self.pushButton_5.clicked.connect(self.button5Click)
        key = QgsSettings().value("dtcloud/key", "test")
        data = urllib.request.urlopen("http://218.235.89.19:8787/plugin/getLayerInfo.do?apiKey="+key).read()
        self.jsonObject = json.loads(data);
        self.url = self.jsonObject['url']
        if self.jsonObject['status'] == "200":
            self.jsonObject = self.jsonObject['layers']
            self.lineEdit.setText(key)
            self.showList()
        else:
            QtWidgets.QMessageBox.information(self, "error", "invalid key")

    def showList(self):
        self.model.clear()        
        for layer in self.jsonObject:
            item = QStandardItem(layer['DATA_NAME'])
            item.setCheckable(True)
            self.model.appendRow(item)
        self.listView.setModel(self.model)

    def button1Click(self):
        url1 = QUrl('https://dtwincloud.com')
        QDesktopServices.openUrl(url1)

    def button2Click(self):
        i = 0
        layerlist = []
        while self.model.item(i):
            if self.model.item(i).checkState():
                shpname = self.model.item(i).text()
                layername = self.model.item(i).text()
                for layer in reversed(self.jsonObject):
                    if layer['DATA_NAME'] == shpname:
                        shpname = layer['SHP_TABLE_NAME']
                urlWithParams = 'url='+self.url+'version=1.1.0&format=image/png&layers='+shpname+'&styles=&crs=EPSG:4326'
                rlayer = QgsRasterLayer(urlWithParams, layername, 'wms')
                if not rlayer.isValid():
                    print("Layer failed to load!")
                else:
                    layerlist.append(rlayer)
            i += 1
        QgsProject.instance().addMapLayers(layerlist)
        self.close()

    def button3Click(self):
        key = self.lineEdit.text()
        data = urllib.request.urlopen("http://218.235.89.19:8787/plugin/getLayerInfo.do?apiKey="+key).read()
        self.jsonObject = json.loads(data);
        self.url = self.jsonObject['url']
        if self.jsonObject['status'] == "200":
            self.jsonObject = self.jsonObject['layers']
            self.lineEdit.setText(key)
            self.showList()
            QgsSettings().setValue("dtcloud/key", key)
        else:
            self.model.clear()
            QtWidgets.QMessageBox.information(self, "error", "invalid key")

    def button4Click(self):
        key = self.lineEdit.text()
        data = urllib.request.urlopen("http://218.235.89.19:8787/plugin/getLayerInfo.do?apiKey="+key).read()
        self.jsonObject = json.loads(data);
        self.url = self.jsonObject['url']
        if self.jsonObject['status'] == "200":
            self.jsonObject = self.jsonObject['layers']
            self.lineEdit.setText(key)
            self.model.clear()
            for layer in self.jsonObject:
                item = QStandardItem(layer['DATA_NAME'])
                item.setCheckable(True)
                item.setCheckState(2)
                self.model.appendRow(item)
            self.listView.setModel(self.model)
            QgsSettings().setValue("dtcloud/key", key)

    def button5Click(self):
        key = self.lineEdit.text()
        data = urllib.request.urlopen("http://218.235.89.19:8787/plugin/getLayerInfo.do?apiKey="+key).read()
        self.jsonObject = json.loads(data);
        self.url = self.jsonObject['url']
        if self.jsonObject['status'] == "200":
            self.jsonObject = self.jsonObject['layers']
            self.lineEdit.setText(key)
            self.model.clear()
            for layer in self.jsonObject:
                item = QStandardItem(layer['DATA_NAME'])
                item.setCheckable(True)
                item.setCheckState(0)
                self.model.appendRow(item)
            self.listView.setModel(self.model)
            QgsSettings().setValue("dtcloud/key", key)
