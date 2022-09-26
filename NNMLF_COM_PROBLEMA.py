# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NNMLF
                                 A QGIS plugin
 Esse plugin estima o padrão de distribuição espacial de feições lineares.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-10-04
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Marconi Martins Cunha
        email                : marconi.cunha@ufv.br
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant, QSortFilterProxyModel, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.gui import (QgsFieldComboBox, QgsMapLayerComboBox, QgsFileWidget, QgsFieldComboBox, QgsProcessingMapLayerComboBox)
from qgis.PyQt.QtWidgets import QAction
from qgis.core.additions.edit import edit
from qgis.core import (QgsProject, QgsField, QgsExpression, QgsFeature, QgsExpressionContext, QgsExpressionContextScope, QgsExpressionContextUtils,
                       QgsProcessing,
                       QgsFeatureSink,
                       QgsField,
                       QgsFields,
                       QgsProcessingException, QgsField, QgsExpression,
                       QgsProcessingAlgorithm,
                       QgsMapLayerProxyModel,
                       QgsFieldProxyModel,
                       QgsFeatureRequest,
                       QgsProcessingOutputNumber,
                       QgsVectorDataProvider,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterField,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFileDestination,
                       QgsProcessingParameterFeatureSink,
                       QgsApplication,
                       QgsProcessingParameterVectorLayer,
                       QgsGeometry,
                       QgsProcessing,
                       QgsProcessingParameterField,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterBoolean,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QWidget
import processing
import os
from qgis.PyQt import QtWidgets
import time
from PyQt5 import uic
from nnmlf.JanelaAjuda import Ui_MainWindow

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .NNMLF_dialog import NNMLFDialog
import os.path

class NewDialog:
    def __init__(self, parent):
        super(NewDialog, self).__(parent)


class NNMLF:
    """QGIS Plugin Implementation."""
    def open_new_dialog(self):
        self.nd = NewDialog(self)
        self.nd.show()

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
            'NNMLF_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Nearest Neighbor Method for Linear Features (NNMLF)')

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
        return QCoreApplication.translate('NNMLF', message)


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

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/NNMLF/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Nearest Neighbor Method for Linear Features (NNMLF)'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Nearest Neighbor Method for Linear Features (NNMLF)'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = NNMLFDialog()
############################ Marconi M. #########################################
        # Busca as camadas carregadas atualmente
        layers1 = QgsProject.instance().layerTreeRoot().children()
        layers = []
        for layer in layers1:
            if layer.layer().geometryType() == 1: # Permite que somente feições do tipo linha sejam selecionadas 
                layers.append(layer)

        # Limpa o conteúdo do comboBox de execuções anteriores
        self.dlg.comboBox.clear()
        
        # Preenche o comboBox com os nomes de todas as camadas carregadas
        self.dlg.comboBox.addItems([layer.name() for layer in layers])
        
        # Nivel confianca
        porcent = ["95%", "90%", "99%"]
        self.dlg.comboBox_3.clear()
        self.dlg.comboBox_3.addItems(porcent)

        # Unidade da area
        unit_area = ["km²", "m²", "ha"]
        self.dlg.comboBox_2.clear()
        self.dlg.comboBox_2.addItems(unit_area)

        # Opções de entrada Área
        opcoes_area = ["Enter area as layer", "Enter the area value"]
        self.dlg.comboBox_4.clear()
        self.dlg.comboBox_4.addItems(opcoes_area)

        ## Entrada do polígono da área
        # Busca as camadas carregadas atualmente
        layers2 = QgsProject.instance().layerTreeRoot().children()
        layers3 = []
        for layer in layers2:
            if layer.layer().geometryType() == 2: # Permite que somente feições do tipo polígono sejam selecionadas 
                layers3.append(layer)

        # Limpa o conteúdo do comboBox de execuções anteriores
        self.dlg.comboBox_5.clear()
        
        # Preenche o comboBox com os nomes de todas as camadas carregadas
        self.dlg.comboBox_5.addItems([layer.name() for layer in layers3])

       ## Ligar/Desligar as opções de entrada de acordo com a seleção do usuário

        # Desligar o valor da área e as unidades por padrão, deixando a seleção da camada
        self.dlg.comboBox_2.setEnabled(False)
        self.dlg.spinBox.setEnabled(False)
        self.dlg.comboBox_2.update()
        
        def liga_desliga_area():
            if self.dlg.comboBox_4.currentText() == 'Enter the area value': 
                self.dlg.comboBox_2.setEnabled(True)
                self.dlg.spinBox.setEnabled(True)
                self.dlg.comboBox_5.setEnabled(False)
                self.dlg.comboBox_2.update()
                self.dlg.comboBox_5.update()
            else:
                self.dlg.comboBox_2.setEnabled(False)
                self.dlg.spinBox.setEnabled(False)
                self.dlg.comboBox_5.setEnabled(True)
                self.dlg.comboBox_2.update()
                self.dlg.comboBox_5.update()
            
       # Conecta a função desliga_area comboBox da camada quando alterada
        self.dlg.comboBox_4.currentIndexChanged.connect(liga_desliga_area)

############################ Marconi M. #########################################
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
        #  Pega os parâmetros de entrada do usuário
            layer_selec_Index = self.dlg.comboBox.currentIndex()
            layer_selec = layers[layer_selec_Index].layer()
            nome_layer_selec = layer_selec.name()
            nivel_confianca = self.dlg.comboBox_3.currentText()
            area = self.dlg.spinBox.value()
            unidade_area = self.dlg.comboBox_2.currentText()
            indicador_area = self.dlg.comboBox_4.currentText()
            layer_area_Index = self.dlg.comboBox_5.currentIndex()
           # Encerra o código se usuário optar por entrar um shape da área e nenhuma camada for selecionada
##            if layer_area_Index >= 0 and indicador_area == "Enter area as layer": # Tem que testar TAMBÉM se a opção foi realmente para entrar como polígono
##                pass
##            else:
##                QMessageBox.information(None, "NNMLF Result", "Area layer not found!! \n"
##                                                              "When selecting the input area option as layer, \n"
##                                                              "the user must input a polygon layer.\n")
##                return
            if indicador_area == "Enter area as layer": # Tem que testar TAMBÉM se a opção foi realmente para entrar como polígono
                if layer_area_Index >= 0:
                    pass
                else:
                    QMessageBox.information(None, "NNMLF Result", "Area layer not found!! \n"
                                                              "When selecting the input area option as layer, \n"
                                                              "the user must input a polygon layer.\n")
                    return
            layer_area_selec = layers3[layer_area_Index].layer()

        #  0. Criar coluna com ID único
         ##  Passo 1. Criar um data provider (provedor de dados)
            layer_selec_dp = layer_selec.dataProvider()

         ##  Passo 2. Definir os campos de atributos e o seu tipo
            layer_selec_dp.addAttributes([QgsField("ID_Unico",  QVariant.Int)])
         
         ##  Passo 3. Atualizar os campos da tabela de atributos para o campo criado aparecer
            layer_selec.updateFields()      # ATENÇÃO: Atualiza o layer_selec
         
         ##  Passo 4. Criar um ID único para cada feição e preenche o campo criado
            expr = QgsExpression('$id + 1') # Expressão para popular o campo criado
            context = QgsExpressionContext() # Cria o contexto
            context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer_selec)) # Cria o contexto
            with edit(layer_selec): # Edita o campo criado e preenche com a expressão
              for f in layer_selec.getFeatures():
                context.setFeature(f)
                f['ID_Unico'] = expr.evaluate(context) # Usa a expressão criada "expr"
                layer_selec.updateFeature(f)
                      
        #  1. Extrair vertices das linhas
            ## Passo 1. Extrair os vértices
            vertices_test = processing.runAndLoadResults("native:extractvertices", {'INPUT': layer_selec, # entrada layer selecionada pelo usuário
                              'OUTPUT': 'memory:'}) # saida como arquivo temporário -> não precisa de permissão nem de caminho para salvar o resultado
         
            ## Passo 2. Passar a saída para QgsVectorLayer
            vertices = QgsProject.instance().mapLayer(vertices_test['OUTPUT'])
             
            ## Passo 3. Mudar o nome para facilitar a chamada da camada no código
            vertices.setName('vertices')

        #  2. Cálculo da distância entre pontos e linhas
            # Preparação para calcular a distância. Seleciona a fonte (source - S) e o alvo (target - T)
            sLayerName = "vertices"
            tLayerName = layer_selec.name()
            
            sLayers = QgsProject.instance().mapLayersByName(sLayerName)
            sLayer = sLayers[0]
            
            # Distância entre todas os feições de duas camadas diferentes
            tLayers = QgsProject.instance().mapLayersByName(tLayerName)
            tLayer = tLayers[0]
            sFeats = sLayer.getFeatures()
            tFeats = tLayer.getFeatures()
            
            teste_lista = []
            dist_pts_linhas = []
            teste_ID2 = [] # Para pegar 'ID_Unico' dos vertices
            teste_ID3 = [] # Para pegar 'ID_Unico' das linhas
            
            for sfeat in sFeats:
                sgeom = sfeat.geometry()
                tFeats = tLayer.getFeatures()
                for tfeat in tFeats:
                    tgeom = tfeat.geometry()
                    dist_pl = sgeom.distance(tgeom)
                    teste_lista.append(sfeat.id())
                    teste_lista.append(tfeat.id())
                    teste_lista.append(dist_pl)
                    dist_pts_linhas.append(dist_pl)
                    teste_ID2.append(sfeat["ID_Unico"])
                    teste_ID3.append(tfeat["ID_Unico"])
            
            soma_DE = []
            soma_PARA = []
            media_DE = []
            media_PARA = []
            
            soma = 0
            soma1 = 0
            contador = 0
            contador1 = 0
            
            ID_Unico_DE2 = []
            
            for j in range(1, max(teste_ID3) + 1):      # Iteração para os pontos (DE) teste_ID2
             for k in range(1, max(teste_ID3) + 1):     # Iteração para as linhas (PARA) teste_ID3
              for i in range(0, len(dist_pts_linhas)):  # Iteração para todos os pontos
                if teste_ID2[i] == j and teste_ID3[i] == k: # DE -> PARA
                    soma += dist_pts_linhas[i]
                    contador += 1
                if teste_ID2[i] == k and teste_ID3[i] == j: # PARA -> DE
                    soma1 += dist_pts_linhas[i]
                    contador1 += 1
              soma_DE.append(soma)
              media_DE.append(soma/contador)
              soma_PARA.append(soma1)
              media_PARA.append(soma1/contador1)
              soma = 0
              soma1 = 0
              contador = 0
              contador1 = 0
              ID_Unico_DE2.append(j)

        #  3. Calcular a Distância de Hausdorff
            dh = []
            for i in range(0, max(teste_ID3)*max(teste_ID3)):
                if media_DE[i] >= media_PARA[i]:
                    dh.append(media_DE[i])
                else:
                    dh.append(media_PARA[i])
            
            sub_dh_ordem = []
            dh_ordem = []

         #  4. Obter os Vizinhos mais Próximos de Primeira, Segunda e Terceira Ordens   

            for k in range(1, max(teste_ID3) + 1):
              for i in range(0, len(ID_Unico_DE2)):
                if ID_Unico_DE2[i] == k:
                   sub_dh_ordem.append(dh[i])
              sub_dh_ordem.sort()
              dh_ordem.append(sub_dh_ordem)
              sub_dh_ordem = []
            
            # Arrumar a lista dh_ordem (lista dentro de lista -> lista comum)
            dh_ordem_2 = []
            dh_ordem_2 = [item for sub_lista in dh_ordem for item in sub_lista]
            
            # Seleção
            VMPFL_Primeira_Ordem = []
            VMPFL_Segunda_Ordem = []
            VMPFL_Terceira_Ordem = []
            for i in range(0, len(ID_Unico_DE2), max(teste_ID3)):
                VMPFL_Primeira_Ordem.append(dh_ordem_2[i + 1]) # Menor Distância de Hausdorff observada (Vizinho Mais Próximo de Primeira Ordem)
                VMPFL_Segunda_Ordem.append(dh_ordem_2[i + 2])  # Segunda menor Distância de Hausdorff observada (Vizinho Mais Próximo de Segunda Ordem)
                VMPFL_Terceira_Ordem.append(dh_ordem_2[i + 3]) # Terceira menor Distância de Hausdorff observada (Vizinho Mais Próximo de Terceira Ordem)
            
         #  5. R Observado
            import sys
           # Analisar qual a opção de área do usuário
           # Passar a área de entrada do usuário para m2. "Area" necessariamente em m2
            if indicador_area == "Enter area as layer":
                features = layer_area_selec.getFeatures() 
                for f in features:
                    geom = f.geometry()
                    Area = geom.area() # "Area" já em m2
                    area = Area
                    unidade_area = "m²"
            else: # indicador_area == "Enter the area value"
                # Encerra o código se usuário optar por entrar com o valor da área e esse valor for Zero
                if area == 0:
                    QMessageBox.information(None, "NNMLF Result", "Area value cannot be Zero! \n"
                                                                  "Please enter a valid value.\n")
                    return
                # Passar a área de entrada do usuário para m2
                if unidade_area == "km²":
                    Area = area*1000*1000
                elif unidade_area == "m²":
                    Area = area
                else: # ha
                    Area = area*100*100
            
            ## R Observado
            R_OBS = sum(VMPFL_Primeira_Ordem)/max(teste_ID3)
            R_OBS_2 = sum(VMPFL_Segunda_Ordem)/max(teste_ID3)
            R_OBS_3 = sum(VMPFL_Terceira_Ordem)/max(teste_ID3)
            
         #  6. R Esperado
            Gamma_1 = [0.5000, 0.7500, 0.9375, 1.0937, 1.2305, 1.3535]
            Gamma_2 = [0.2613, 0.2722, 0.2757, 0.2775, 0.2784, 0.2789]

           ## R Esperado 
            R_ESP = Gamma_1[0]*((Area/max(teste_ID3))**0.5)
            R_ESP_2 = Gamma_1[1]*((Area/max(teste_ID3))**0.5)
            R_ESP_3 = Gamma_1[2]*((Area/max(teste_ID3))**0.5)
            
         #  7. Calcular a estatística R
            R = R_OBS/R_ESP
            R_2 = R_OBS_2/R_ESP_2
            R_3 = R_OBS_3/R_ESP_3
            
         #  8. Aplicar o teste Z
            SE = Gamma_2[0]*((Area/(max(teste_ID3)**2))**0.5)
            SE_2 = Gamma_2[1]*((Area/(max(teste_ID3)**2))**0.5)
            SE_3 = Gamma_2[2]*((Area/(max(teste_ID3)**2))**0.5)
            
            Z = (R_OBS - R_ESP)/SE
            Z_2 = (R_OBS_2 - R_ESP_2)/SE_2
            Z_3 = (R_OBS_3 - R_ESP_3)/SE_3
            
            # Selecionar o z tabelado baseado na escolha do nível de confiança requerido pelo usuário
            if nivel_confianca == "95%":
                Z_tab = 1.9599639845400536 # Nível de Confiança de 95%
            elif nivel_confianca == "90%":
                Z_tab = 1.6448536269514715 # Nível de Confiança de 90%
            else: # 99%
                Z_tab = 2.5758293035488999 # Nível de Confiança de 99%

         #  9. Inferir sobre o padrão de distribuição espacial das linhas
            ## Primeira Ordem
            if abs(Z) < Z_tab: # Não rejeita H0 -> Padrão ALEATÓRIO
                Padrao_Pri_Ord = "Random"
            elif R < 1:                     # Padrão AGRUPADO
                Padrao_Pri_Ord = "Clustered"
            else:                           # Padrão DISPERSO
                Padrao_Pri_Ord = "Dispersed"
 
            ## Segunda Ordem
            if abs(Z_2) < Z_tab: # Não rejeita H0 -> Padrão ALEATÓRIO
                Padrao_Seg_Ord = "Random"
            elif R_2 < 1:                     # Padrão AGRUPADO
                Padrao_Seg_Ord = "Clustered"
            else:                             # Padrão DISPERSO
                Padrao_Seg_Ord = "Dispersed"
            
            ## Terceira Ordem
            if abs(Z_3) < Z_tab: # Não rejeita H0 -> Padrão ALEATÓRIO
                Padrao_Ter_Ord = "Random"
            elif R_3 < 1:                     # Padrão AGRUPADO
                Padrao_Ter_Ord = "Clustered"
            else:                             # Padrão DISPERSO
                Padrao_Ter_Ord = "Dispersed"

         #  10. Apresentar os resultados ao usuário
         ## 10.1. Gravar os resultados na tabela de atributos
           ### Preencher campos do tipo Double
           ##  Passo 1. Criar um data provider (provedor de dados)
            layer_selec_dp = layer_selec.dataProvider()

           ##  Passo 2. Definir os campos de atributos e o seu tipo
            layer_selec_dp.addAttributes([QgsField("NNMLF_1_Or",  QVariant.String),
                                          QgsField("NNMLF_2_Or",  QVariant.String),
                                          QgsField("NNMLF_3_Or",  QVariant.String),
                                          QgsField("Confid_Lev",  QVariant.String),
                                          QgsField("Area_m2",  QVariant.Double)])
         
           ##  Passo 3. Atualizar os campos da tabela de atributos para o campo criado aparecer
            layer_selec.updateFields()      # ATENÇÃO: Atualiza o layer_selec
         
           ##  Passo 4. Preenche os campos criados
            expr_Area = QgsExpression('{}'.format(round(Area, 3)))
            context = QgsExpressionContext() # Cria o contexto
            context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer_selec)) # Cria o contexto
            string_Pri_Ord = str(Padrao_Pri_Ord)
            string_Seg_Ord = str(Padrao_Seg_Ord)
            string_Ter_Ord = str(Padrao_Ter_Ord)
            string_Confid_Lev = str(nivel_confianca)
            with edit(layer_selec): # Edita o campo criado e preenche com a expressão
              for f in layer_selec.getFeatures():
                context.setFeature(f)
                f['NNMLF_1_Or'] = string_Pri_Ord
                f['NNMLF_2_Or'] = string_Seg_Ord
                f['NNMLF_3_Or'] = string_Ter_Ord
                f['Confid_Lev'] = string_Confid_Lev
                f['Area_m2'] = expr_Area.evaluate(context)
                layer_selec.updateFeature(f)

            QMessageBox.information(None, "NNMLF Result", f"Input Data: \n"
                                    f"   Layer: {str(nome_layer_selec)}           Area: {area:0.3f} {str(unidade_area)}           \n" # Area
                                    f"   Confidence Level: {str(nivel_confianca)}           \n" # nivel_confianca
                                    f"           \n"
                                    f"Statistics and Results: \n"
                                    f"   NNMLF First Order           \n"
                                    f"     R Observed = {R_OBS:0.3f}           R Expected = {R_ESP:0.3f}            Index R = {R:0.3f}            \n"
                                    f"     Z Calculated = {Z:0.3f}            Z-Score Table = {Z_tab:0.3f}            \n"
                                    f"     Result: {str(Padrao_Pri_Ord)}            \n"
                                    f"           \n"
                                    f"   NNMLF Second Order           \n"
                                    f"     R Observed = {R_OBS_2:0.3f}            R Expected = {R_ESP_2:0.3f}            Index R = {R_2:0.3f}            \n"
                                    f"     Z Calculated = {Z_2:0.3f}            Z-Score Table = {Z_tab:0.3f}            \n"
                                    f"     Result: {str(Padrao_Seg_Ord)}            \n"
                                    f"           \n"
                                    f"   NNMLF Third Order           \n"
                                    f"     R Observed = {R_OBS_3:0.3f}            R Expected = {R_ESP_3:0.3f}            Index R = {R_3:0.3f}            \n"
                                    f"     Z Calculated = {Z_3:0.3f}            Z-Score Table = {Z_tab:0.3f}            \n"
                                    f"     Result: {str(Padrao_Ter_Ord)}            \n" 
                                    f"           \n"
                                    f"           \n"
                                    f"PS.: The results were recorded in the attribute table.           \n")
