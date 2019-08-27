<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" simplifyAlgorithm="0" version="3.4.10-Madeira" maxScale="0" simplifyLocal="1" simplifyDrawingHints="1" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" simplifyDrawingTol="1" styleCategories="AllStyleCategories" minScale="1e+8" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol alpha="1" type="fill" clip_to_extent="1" name="0" force_rhr="0">
        <layer enabled="1" locked="0" class="SimpleFill" pass="0">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="162,12,203,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="no"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <LinearlyInterpolatedDiagramRenderer lowerValue="0" upperHeight="50" diagramType="Histogram" upperValue="0" attributeLegend="1" lowerHeight="0" classificationAttributeExpression="" lowerWidth="0" upperWidth="50">
    <DiagramCategory diagramOrientation="Up" minScaleDenominator="100000" enabled="0" minimumSize="0" backgroundColor="#ffffff" penWidth="0" height="15" maxScaleDenominator="1e+8" scaleBasedVisibility="0" sizeType="MM" lineSizeType="MM" rotationOffset="270" penColor="#000000" scaleDependency="Area" opacity="1" sizeScale="3x:0,0,0,0,0,0" barWidth="5" penAlpha="255" backgroundAlpha="255" width="15" labelPlacementMethod="XHeight" lineSizeScale="3x:0,0,0,0,0,0">
      <fontProperties description="Ubuntu,11,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
    </DiagramCategory>
  </LinearlyInterpolatedDiagramRenderer>
  <DiagramLayerSettings showAll="1" zIndex="0" placement="0" obstacle="0" dist="0" linePlacementFlags="2" priority="0">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option type="Map" name="properties">
          <Option type="Map" name="show">
            <Option value="true" type="bool" name="active"/>
            <Option value="rowid" type="QString" name="field"/>
            <Option value="2" type="int" name="type"/>
          </Option>
        </Option>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="rowid">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" type="QString" name="IsMultiline"/>
            <Option value="0" type="QString" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" type="QString" name="IsMultiline"/>
            <Option value="0" type="QString" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" type="QString" name="IsMultiline"/>
            <Option value="0" type="QString" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="ang">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" type="QString" name="IsMultiline"/>
            <Option value="0" type="QString" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="x">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" type="QString" name="IsMultiline"/>
            <Option value="0" type="QString" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="y">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="0" type="QString" name="IsMultiline"/>
            <Option value="0" type="QString" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="rowid" index="0" name=""/>
    <alias field="id" index="1" name=""/>
    <alias field="name" index="2" name=""/>
    <alias field="ang" index="3" name=""/>
    <alias field="x" index="4" name=""/>
    <alias field="y" index="5" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="rowid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="" applyOnUpdate="0"/>
    <default field="name" expression="" applyOnUpdate="0"/>
    <default field="ang" expression="" applyOnUpdate="0"/>
    <default field="x" expression="" applyOnUpdate="0"/>
    <default field="y" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="rowid" constraints="3" notnull_strength="1" exp_strength="0" unique_strength="1"/>
    <constraint field="id" constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint field="name" constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint field="ang" constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint field="x" constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0"/>
    <constraint field="y" constraints="0" notnull_strength="0" exp_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="rowid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="name" desc="" exp=""/>
    <constraint field="ang" desc="" exp=""/>
    <constraint field="x" desc="" exp=""/>
    <constraint field="y" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column hidden="0" type="field" width="-1" name="id"/>
      <column hidden="0" type="field" width="-1" name="name"/>
      <column hidden="0" type="field" width="-1" name="ang"/>
      <column hidden="0" type="field" width="-1" name="x"/>
      <column hidden="0" type="field" width="-1" name="y"/>
      <column hidden="1" type="actions" width="-1"/>
      <column hidden="0" type="field" width="-1" name="rowid"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- codificación: utf-8 -*-
"""
Los formularios de QGIS pueden tener una función de Python que
es llamada cuando se abre el formulario.

Use esta función para añadir lógica extra a sus formularios.

Introduzca el nombre de la función en el campo
"Python Init function".
Sigue un ejemplo:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="ang"/>
    <field editable="1" name="id"/>
    <field editable="1" name="name"/>
    <field editable="1" name="rowid"/>
    <field editable="1" name="x"/>
    <field editable="1" name="y"/>
  </editable>
  <labelOnTop>
    <field name="ang" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="name" labelOnTop="0"/>
    <field name="rowid" labelOnTop="0"/>
    <field name="x" labelOnTop="0"/>
    <field name="y" labelOnTop="0"/>
  </labelOnTop>
  <widgets>
    <widget name="rowid">
      <config/>
    </widget>
  </widgets>
  <previewExpression>"name" = 'zona 1'</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
