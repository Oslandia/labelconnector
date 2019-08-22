# EN: LabelConnector plugin documentation

LabelConnector allows the creation of label connectors by automatically configuring a new style using the power of the QGIS geometry generator. It is designed for QGIS 3.4 and QGIS 3.8 waiting for native label callout support landing in QGIS 3.10

It aimed to be the successor of [EasyCustomLabeling plugin](https://github.com/haubourg/EasyCustomLabeling). 

To apply a label connector, you must click on the button located in the label toolbar.

If your layer does not have auxiliary storage in the project, the plugin will create it and you will be asked for a primary key (see QGIS Documentation).

The plugin will propose you to apply a connector style, these are available in the plugin's labelStyles folder. 

If a label connector is already present, a check is made and you are not allowed to add another one. You can exceed this limit by deleting the comment.

Known issues:

 - Label Connectors can't be used with renderers not allowing geometry generators. This can be the case for Heatmap, Point displacement, cluster, inverted polygon and 2.5D renderer 
  
 - Feature symbols are modified by those connector lines, since they belong to feature symbology, so you will actually see thos lines into the map legend.   ![Lines in Symbology](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/symbols_with_line.png). A simple workaround is to convert the symbology to ruled based symbology, which separates line callouts in a separate legend element. ![Lines in Symbology workaround](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/symbols_with_line_workaround.png)
   
 - [#11](https://github.com/Oslandia/labelconnector/issues/11) Callouts can be sometimes drawn "under" some features.  ![Lines underneath features](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/callout_underneath_feature.png). It is possible to circumvent this by activating symbol levels and give a higher score to callout lines. ![Lines underneath features](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/callout_underneath_feature_workaround.png)

 - [#28](https://github.com/Oslandia/labelconnector/issues/28) When the layer already has ruled based labels before using label connector action, the rules are lost and we get back to simple labeling. To prevent any lost, the plugin saves your old before doing anything so that yo can restore those settings.  ![Style saved](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/style_saved.png)




# FR: Documentation du plugin LabelConnector

LabelConnector permets la création de connecteur d'étiquette en configurant automatiquement un nouveau style utilisant la puissance du générateur de géométrie de QGIS. 

Il vise à remplacer [l'extension EasyCustomLabeling](https://github.com/haubourg/EasyCustomLabeling), et dans l'attente de l'arrivée du support natif des connecteurs d'étiquettes dans QGIS 3.10. 

Pour appliquer un connecteur d'étiquette, vous devez cliquer sur le bouton situé dans la barre d'outils des étiquettes.

Si votre couche ne possède pas de stockage auxiliaire dans le projet, le plugin va le créer et une clef primaire vous sera demandé (cf QGIS Documentation).

Le plugin vous proposera d'appliquer un style de connecteur, ceux-ci sont disponibles dans le dossier labelStyles du plugin. 

Dans le cas où un connecteur d'étiquettes serait déjà présent, une vérification est effectuée et vous interdit l'ajout d'un autre. Vous pouvez outrepasser cette limite en supprimant le commentaire.

Problèmes connus / limitations:

- Les connecteurs d'étiquettes ne fonctionnent que pour les moteurs de rendu supportant les générateurs de géométries, et donc pas pour les cartes de chaleurs, déplacement de points, regroupements (clusters), polygones inversés et rendu 2,5D. 

 - Les symboles de légende sont modifiés par les lignes des connecteurs, puisqu'elles font partie de la symbologie.  ![Lines in Symbology](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/symbols_with_line.png). Il est possible de rendre la légende plus lisible en la convertissant en règles, ce qui va déplacer la ligne de connecteur dans une règle séparée. ![Lines in Symbology workaround](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/symbols_with_line_workaround.png)
   
 - [#11](https://github.com/Oslandia/labelconnector/issues/11) L'ordre d'affichage des connecteurs et des objets géographique peut aboutir à des lignes dessinées en dessous de certains objets.  ![Lines underneath features](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/callout_underneath_feature.png). Il est possible de forcer l'ordre d'affichage en utilisant les niveaux de symbole. ![Lines underneath features](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/callout_underneath_feature_workaround.png)

 - [#28](https://github.com/Oslandia/labelconnector/issues/28) Si la couche cible contient des règles d'étiquetage, le plugin va les écraser en basculer en règle simple ! Le style précédent est sauvegardé pour éviter de perdre votre travail dans ce cas [Style saved](https://raw.githubusercontent.com/Oslandia/labelconnector/master/help/source/style_saved.png)

