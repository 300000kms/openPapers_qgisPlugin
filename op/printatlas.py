'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

from qgis.core import QgsProject, QgsFeatureRequest, QgsExpression, QgsLayout, QgsLayoutItem, \
    QgsReadWriteContext,QgsLayoutExporter, \
    QgsVectorLayer, QgsFeature, QgsGeometryUtils, QgsGeometry, QgsRectangle, QgsField, \
    QgsMapThemeCollection

from qgis.PyQt.QtCore import QFileInfo, QPointF, QVariant
from qgis.gui import QgsMapCanvas
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtGui import QPainter, QImage, QCursor
from qgis.PyQt.QtCore import QSizeF, QSize, QRect, QRectF
import os
import math
import shutil
import barcode
try:
    import qrcode
    print('qrcode ready')
except Exception as e:
    print(e)



###############################################################################
###############################################################################
def debug(x):
    if True:
        print (x)
    return
def printRaster(composition, nameFile, root_out):
    global pag
    dpi = 150
    path = root_out +'/'+ str(pag).zfill(3)+'_'+nameFile+'.png'
    
    exporter = QgsLayoutExporter(composition)
    #exporter.exportToPdf(path, QgsLayoutExporter.PdfExportSettings())
    
    image_settings = exporter.ImageExportSettings()
    image_settings.dpi = 300 # or whatever you want    
    exporter.exportToImage( path, image_settings)
    pag += 1
    return


def saveProject(name):
    project = QgsProject.instance()
    project.write(QFileInfo(root+name+'.qgs'))
    return


def filter(layerName, criteria):
    #desc=layers[layerName]
    l=QgsProject.instance().mapLayer(mapL[layerName])
    l.setSubsetString(criteria)
    return


def mapLmake():
    global mapL
    mapL={}
    lyrsName = QgsProject.instance().mapLayers().values()
    for l in lyrsName:
        mapL[l.name()]=l.id()
    return


def makeQR(data,name):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
    qr.add_data(data)
    qr.make(fit=True)
    root_code = os.path.dirname(os.path.realpath(__file__))
    img = qr.make_image()
    path = root_code+'/temp/'+name+'.png'
    img.save(path)
    return path
    
def makeBarcode(data, name):
    debug (data)
    bc = barcode.get_barcode_class('code39')
    root_code = os.path.dirname(os.path.realpath(__file__))
    path = root_code+'/temp/'+name+'.svg'
    #bc('lalala').save(path)
    #bc(data).save(path)
    return path
    
def emptyTemp():
    root_code = os.path.dirname(os.path.realpath(__file__))
    #shutil.rmtree(root_code+'/temp')
    return
    
def featureFields(b):
    result =[a.name() for a in b.fields()]
    return result


def mkChapter(b, qptChapter,project_name, root_out, zl_layer, zl_field, di_layer, di_field, di_name):
    """
    b es un bound
    """
    root_code = os.path.dirname(os.path.realpath(__file__))
    Lz = zl_layer #QgsProject.instance().mapLayer(mapL['zones'])
    
    file_qptChapter= open(qptChapter,'r')
    template_content_chapter=file_qptChapter.read()
    file_qptChapter.close()
    
    ###
    #filter('zones', '"name" = \''+b.attribute('name')+'\'' )#cuidado si el valor es integer o string
    #filter('zones2', '"name" = \''+b.attribute('name')+'\'' )#cuidado si el valor es integer o string
    #filter('divisions', '"name" = \''+b.attribute('name')+'\'' )
    #filter('divisions2', '"name" = \'' + b.attribute('name') + '\'')

    QgsProject.instance().mapLayer(ZVL).setSubsetString( '"name" = \''+b.attribute('name')+'\'' )
    QgsProject.instance().mapLayer(DVL).setSubsetString('"name" = \''+b.attribute('name')+'\'' )
    QgsProject.instance().mapLayer(DVL2).setSubsetString('"name" = \''+b.attribute('name')+'\'' )


    ### seleccionamos la zona
    zz = Lz.getFeatures(QgsFeatureRequest(QgsExpression('"name" = \''+b.attribute('name')+'\''))) #cuidado si el valor es integer o string
    zz = [x for x in zz]

    # escogemos el distrito correspondiente a la zona
    #filter('districtes', '"name" = \''+unicode(zz[0].attribute('d_name'))+'\'' )
    di_layer.setSubsetString('"'+di_field+'" = \''+unicode(zz[0].attribute(zl_field))+'\'')

    global currentDistrict
    #currentDistrict = unicode(zz[0].attribute('d_id'))
    currentDistrict = unicode(zz[0].attribute(zl_field))
    
    #coje la geometria del distriro
    #distri = QgsProject.instance().mapLayer(mapL['districtes'])
    gd = [d for d in di_layer.getFeatures()][0]

    #canvas = QgsMapCanvas()
    document = QDomDocument()
    document.setContent(template_content_chapter)
    
    p = QgsProject().instance()
    composition = QgsLayout (p)
    composition.loadFromTemplate(document,QgsReadWriteContext())

    ##
    bounds = (b.geometry()).boundingBox()
    
    map_item =  composition.itemById('mapa')
    map_item.zoomToExtent(bounds)
    map_item.setKeepLayerStyles(True)
    map_item.setKeepLayerSet (True)
    map_item.setFollowVisibilityPreset(True)
    map_item.setFollowVisibilityPresetName ('_zona_big')
    
    map_item_distri = composition.itemById('mapDistrito')
    map_item_distri.zoomToExtent(gd.geometry().boundingBox())
    map_item_distri.setKeepLayerStyles(True)
    map_item_distri.setKeepLayerSet (True)
    map_item_distri.setFollowVisibilityPreset(True)
    map_item_distri.setFollowVisibilityPresetName ('_zona_small')

    ##title
    ti = composition.itemById('project')
    ti.setText(project_name)

    ##zona
    zo = composition.itemById('zona')
    zo.setText(str(b.attribute('id')))
    
    corners = composition.itemById('corners')
    corners.setPicturePath(root_code+'/templates/corners_a4.svg')
    
    logo = composition.itemById('logo')
    logo.setPicturePath(root_code+'/templates/logo.svg')
    
    #norte = composition.itemById('norte')
    #norte.setPicturePath(root_code+'templates/norte.svg')
    #norte.setRotation(angle)
    
    ##barrio y distrito
    distrito = composition.itemById('distrito')
    distrito.setText('districte : '+ unicode(zz[0].attribute('d_name')))
    barrio = composition.itemById('barrio')
    fields = [e.name() for e in zz[0].fields().toList()]
    if 'b_name' in fields:
        barrio.setText('barri : '+zz[0].attribute('b_name')) #legacy
    else:
        barrio.setText('zona : '+zz[0].attribute('name').replace('_', '.'))
    
    
    composition.refresh()
    image_name = str(b.attribute('name').replace('_', '-'))+'_'+currentDistrict
    printRaster(composition, image_name, root_out)

    # filter('divisions', '' )
    # filter('divisions2', '' )
    # filter('districtes', '' )

    QgsProject.instance().mapLayer(DVL).setSubsetString('')
    QgsProject.instance().mapLayer(DVL2).setSubsetString('')
    
    return


def mkDiv(b, z, qptDivision, project_name, root_out,zl_layer,zl_field, di_layer, di_field, di_name):

    root_code = os.path.dirname(os.path.realpath(__file__))
    Lz = zl_layer #QgsProject.instance().mapLayer(mapL['zones'])
    debug(b.attributes())
    #angle = b.attribute('ang')
    angle = b.attribute(2)
    #esto visulamente es correcto
    ##pero me fastidia la lectira posterior porque no dejo rastro de esta manipulacion
    ##para el escaneo posterio deberia de modificar el orden de los bounds en el qr y en el pie de pagina
    
    if angle > 45:
        angle = angle-90
    elif angle < -45:
        angle = angle+90

    # sql = '"name" = \''+b.attribute('name')+'\''
    # sql += ' AND "x" = '+str(b.attribute('x'))
    # sql += ' AND "y" = '+str(b.attribute('y'))
    #filter('divisions', sql)

    sql = '"name" = \''+b.attribute(1)+'\''
    sql += ' AND "x" = '+str(b.attribute(3))
    sql += ' AND "y" = '+str(b.attribute(4))

    QgsProject.instance().mapLayer(DVL).setSubsetString(sql)
    
    sql2 = '"name" = \''+b.attribute(1)+'\''
    #sql2 = '"name" = \'' + b.attribute('name') + '\''
    #filter('divisions2', sql2)
    QgsProject.instance().mapLayer(DVL2).setSubsetString(sql)

    template_file = open(qptDivision, 'r')
    template_content = template_file.read()
    template_file.close()
    document = QDomDocument()
    document.setContent(template_content)
    
    p = QgsProject().instance()
    composition = QgsLayout (p)
    composition.loadFromTemplate(document,QgsReadWriteContext())

    ##mapa principal
    map_item = composition.itemById('mapa')
    map_item.setKeepLayerStyles(True)
    map_item.setKeepLayerSet(True)
    map_item.setFollowVisibilityPreset(True)
    map_item.setFollowVisibilityPresetName ('_szona_big')
    
    map_item.setMapRotation(-angle)########
    cc = b.geometry().centroid().asPoint()
    coordsDesc = str(b.geometry().asWkt())[10:][:-2].split(', ')
    
    b.geometry().rotate(-angle, cc)
    rBound = b.geometry().boundingBox()
    map_item.zoomToExtent(rBound)

    ##mapa 2
    map_item2 = composition.itemById('minimapa')
    map_item2.setKeepLayerStyles(True)
    map_item2.setKeepLayerSet(True)
    map_item2.setFollowVisibilityPreset(True)
    map_item2.setFollowVisibilityPresetName ('_szona_small')

    #cuidado que aqu´i se lia con valor integer o string
    zz = zl_layer.getFeatures(QgsFeatureRequest(QgsExpression('"name" = \''+b.attribute(1)+'\'')))
    zz = [x for x in zz]
    z =  zz[0].geometry()
    map_item2.zoomToExtent(z.boundingBox())

    ##barrio y distrito
    distrito = composition.itemById('distrito')
    distrito.setText('districte : '+unicode(zz[0].attribute('d_name')))

    barrio = composition.itemById('barrio')

    fields = [e.name() for e in zz[0].fields().toList()]
    if 'b_name' in fields:
        barrio.setText('barri : '+zz[0].attribute('b_name'))
    else:
        barrio.setText('zona : '+zz[0].attribute('name').replace('_', '.'))

    ##anotacion coordenadas
    coordsDesc = [c.split(' ') for c in coordsDesc]

    coords = composition.itemById('coordenadas')
    coords.setText(' aX: '+str(round(float(coordsDesc[0][0]),0))+ \
                   ' ay: '+str(round(float(coordsDesc[0][1]),0))+ \
                   ' bX: '+str(round(float(coordsDesc[1][0]),0))+ \
                   ' by: '+str(round(float(coordsDesc[1][1]),0))+ \
                   ' cX: '+str(round(float(coordsDesc[2][0]),0))+ \
                   ' cy: '+str(round(float(coordsDesc[2][1]),0))+ \
                   ' dX: '+str(round(float(coordsDesc[3][0]),0))+ \
                   ' dy: '+str(round(float(coordsDesc[3][1]),0))
                   )

    ##zona
    zo = composition.itemById('zona')
    zo.setText(str(b.attribute(1).replace('_', '.')))
    
    ##title
    ti = composition.itemById('project')
    ti.setText(project_name)
    
    ##cbarres
    #cb_name = 'cb_'+str(b.attribute('name').replace('_', '.'))+'_'+str(b.attribute('x'))+'_'+str(b.attribute('y'))
    cb_text = '*'+str(b.attribute(1).replace('_', '.'))+','+str(b.attribute(3))+','+str(b.attribute(4))+'*'
    #makeBarcode(cb_text, cb_name)
    
    cbarres = composition.itemById('cbarres')
    cbarres.setText(cb_text)

    #qrcode
    name = str(b.attribute(1).replace('_', '.'))+'_'+str(b.attribute(3))+'_'+str(b.attribute(4))
    qr = composition.itemById('qrcode')
    data =  name+' '+ \
            str(round(float(coordsDesc[0][0]),3))+' '+ \
            str(round(float(coordsDesc[0][1]),3))+', '+ \
            str(round(float(coordsDesc[1][0]),3))+' '+ \
            str(round(float(coordsDesc[1][1]),3))+', '+ \
            str(round(float(coordsDesc[2][0]),3))+' '+ \
            str(round(float(coordsDesc[2][1]),3))+', '+ \
            str(round(float(coordsDesc[3][0]),3))+' '+ \
            str(round(float(coordsDesc[3][1]),3))

    qrpath = makeQR(data,name)
    qr.setPicturePath(qrpath)

    #pagina
    pagina = composition.itemById('pagina')
    pagina.setText(name)
    
    #norte
    corners = composition.itemById('corners')
    corners.setPicturePath(root_code+'/templates/corners_a4.svg')
    
    logo = composition.itemById('logo')
    logo.setPicturePath(root_code+'/templates/logo.svg')
    
    norte = composition.itemById('norte')
    norte.setPicturePath(root_code+'/templates/norte.svg')
    norte.setRotation(angle)

    composition.refresh()
    currentDistrict = unicode(zz[0].attribute(zl_field))
    image_name = str(b.attribute(1).replace('_', '-'))+'_'+str(b.id())+'_'+currentDistrict
    printRaster(composition, image_name, root_out)
    return


def mkForm(b,qptForm,form_file,project_name, root_out, zl_layer,zl_field, di_layer, di_field, di_name):
    root_code = os.path.dirname(os.path.realpath(__file__))
    name = str(b.attribute(1).replace('_', '.'))+'_'+str(b.attribute(3))+'_'+str(b.attribute(4))

    template_file = open(qptForm,'r')
    template_content = template_file.read()
    template_file.close()
    document = QDomDocument()
    document.setContent(template_content)
    
    composition = QgsLayout (QgsProject().instance())
    composition.loadFromTemplate(document,QgsReadWriteContext())
    
    corners = composition.itemById('corners')
    corners.setPicturePath(root_code+'/templates/corners_a4.svg')
    
    logo = composition.itemById('logo')
    logo.setPicturePath(root_code+'/templates/logo.svg')
    
    ##title
    ti = composition.itemById('project')
    ti.setText(project_name)

    ##zona
    zo = composition.itemById('zona')
    zo.setText(str(b.attribute(1).replace('_', '.')))

    ##pagina
    zo = composition.itemById('pagina')
    zo.setText(name)
    
    #form
    qr = composition.itemById('form')
    qr.setPicturePath(form_file)

    #qrcode
    qr = composition.itemById('qrcode')
    data =  name
    qrpath = makeQR(data,name)
    qr.setPicturePath(qrpath)

    ##cbarres
    cbarres = composition.itemById('cbarres')
    cbarres.setText('*'+str(b.attribute(1).replace('_', '.'))+','+str(b.attribute(3))+','+str(b.attribute(4))+'*')

    composition.refresh()

    zz = zl_layer.getFeatures(QgsFeatureRequest(QgsExpression('"name" = \'' + b.attribute(1) + '\'')))
    zz = [x for x in zz]
    z = zz[0].geometry()
    currentDistrict = unicode(zz[0].attribute(zl_field))

    image_name = str(b.attribute(1).replace('_', '-'))+'_'+str(b.id())+'_form'+'_'+currentDistrict
    printRaster(composition, image_name, root_out)
    return


def showLayers():
    reg = QgsMapLayerRegistry.instance()
    for l in reg.mapLayers().values():
        debug ( l.id() )
    return


def getSubzones(z, paper, scale):
    '''
    '''
    divisiones = []
    for f in  QgsProject.instance().mapLayer(DVL).getFeatures():
        QgsProject.instance().mapLayer(DVL).dataProvider().deleteFeatures([f.id()])
    for f in  QgsProject.instance().mapLayer(DVL2).getFeatures():
        QgsProject.instance().mapLayer(DVL2).dataProvider().deleteFeatures([f.id()])

    pr = QgsProject.instance().mapLayer(DVL).dataProvider()
    pr2 = QgsProject.instance().mapLayer(DVL2).dataProvider()

    geom, area, angle, width, height = z.geometry().orientedMinimumBoundingBox()
    centroid = geom.centroid()

    ##
    l1 = (z.geometry().orientedMinimumBoundingBox()[0].vertexAt(0).distance(
        z.geometry().orientedMinimumBoundingBox()[0].vertexAt(1)
    ))

    l2 = (z.geometry().orientedMinimumBoundingBox()[0].vertexAt(1).distance(
        z.geometry().orientedMinimumBoundingBox()[0].vertexAt(2)
    ))

    ##calcular angulo
    a1 = math.degrees(QgsGeometryUtils.angleBetweenThreePoints(
        geom.vertexAt(0).x(), geom.vertexAt(0).y(),
        geom.vertexAt(1).x(), geom.vertexAt(1).y(),
        geom.vertexAt(1).x(), geom.vertexAt(1).y() + 1000000,
    ))

    a2 = math.degrees(QgsGeometryUtils.angleBetweenThreePoints(
        geom.vertexAt(2).x(), geom.vertexAt(2).y(),
        geom.vertexAt(1).x(), geom.vertexAt(1).y(),
        geom.vertexAt(1).x(), geom.vertexAt(1).y() + 1000000,
    ))

    a = a1 if l1 < l2 else a2

    geom.rotate(a, centroid.asPoint())

    ##numero de divisiones
    # nx = int(l1 / paper[0] * 0.001 / scale + 1)
    # ny = int(l2 / paper[1] * 0.001 / scale + 1)
    nx = int(l1 / paper[0] * 1000 * scale + 1)
    ny = int(l2 / paper[1] * 1000 * scale + 1)

    debug (('matrix: ',nx, ny))
    ##si son enteras cual es el tamaño final
    # flx = nx * paper[0] / 0.001 * scale
    # fly = ny * paper[1] / 0.001 * scale
    flx = nx * paper[0] / scale / 1000
    fly = ny * paper[1] / scale / 1000

    # longitudes de los nuevos cuadrados
    l_x = flx / nx
    l_y = fly / ny

    # desplazamiento del resultado respecto a una matriz
    # o centro del nuevo bbox
    cx = flx / 2
    cy = fly / 2

    #generar las divisiones
    matrix = [nx, ny]
    for fex in range(matrix[0]):
        for fey in range(matrix[1]):
            feat = QgsFeature()

            ng = QgsGeometry().fromRect(QgsRectangle(
                fex * l_x,
                fey * l_y,
                (fex + 1) * l_x,
                (fey + 1) * l_y
            ))
            ng.translate(centroid.asPoint().x() - cx, centroid.asPoint().y() - cy)
            ng.rotate(-a, centroid.asPoint())
            feat.setGeometry(ng)
            feat.setAttributes([
                z.attribute('id'),
                z.attribute('name'),
                a,
                fex,
                fey
            ])

            pr.addFeatures([feat])
            pr2.addFeatures([feat])
            divisiones.append(feat)

    QgsProject.instance().mapLayer(DVL).commitChanges()
    QgsProject.instance().mapLayer(DVL2).commitChanges()

    return divisiones


###########################################################################
###########################################################################

def makeAtlas(
        qptChapter,
        qptDivision,
        qptForm,
        zl_layer,
        zl_field,
        di_layer,
        di_field,
        di_name,
        scale,
        form_file=None,
        form=False,
        project_name='',
        root_out = '',
        pbar=False,
        isTest =True
    ):

    root_code = os.path.dirname(os.path.realpath(__file__))

    ## getpapersize
    template_file = open(qptDivision, 'r')
    template_content = template_file.read()
    template_file.close()
    document = QDomDocument()
    document.setContent(template_content)
    p = QgsProject().instance()
    composition = QgsLayout(p)
    composition.loadFromTemplate(document, QgsReadWriteContext())
    map_item = composition.itemById('mapa')
    paper = [map_item.sizeWithUnits().width(), map_item.sizeWithUnits().height()]


    ##get visible layers
    visibleLayers = p.mapThemeCollection().masterVisibleLayers()

    ## get project srid...
    crs = zl_layer.dataProvider().sourceCrs ().authid()

    ## zones 1 layer
    zvl = zl_layer.clone()
    global ZVL
    ZVL = zvl.id()
    QgsProject.instance().addMapLayer(zvl)
    #pr = zvl.dataProvider()
    QgsProject.instance().mapLayer(ZVL).loadNamedStyle(root_code + '/templates/layerstyles/zones.qml')

    ## divisions 1 layer
    dvl = QgsVectorLayer("Polygon?crs="+crs, "divisions_layer", "memory")
    global DVL
    DVL = dvl.id()
    QgsProject.instance().addMapLayer(dvl)
    #pr = dvl.dataProvider()
    QgsProject.instance().mapLayer(DVL).startEditing()
    QgsProject.instance().mapLayer(DVL).loadNamedStyle(root_code + '/templates/layerstyles/div1.qml')

    pr_dvl = QgsProject.instance().mapLayer(DVL).dataProvider()
    pr_dvl.addAttributes([
        QgsField('id', QVariant.String),
        QgsField('name', QVariant.String),
        QgsField('ang', QVariant.String),
        QgsField('x', QVariant.String),
        QgsField('y', QVariant.String),
    ])

    QgsProject.instance().mapLayer(DVL).commitChanges()

    ## divisions 2 layer
    dvl2 = QgsVectorLayer("Polygon?crs=" + crs, "divisions_layer", "memory")
    global DVL2
    DVL2 = dvl2.id()
    QgsProject.instance().addMapLayer(dvl2)
    #pr = dvl2.dataProvider()
    QgsProject.instance().mapLayer(DVL2).startEditing()
    QgsProject.instance().mapLayer(DVL2).loadNamedStyle(root_code + '/templates/layerstyles/div2.qml')
    pr_dvl2 = QgsProject.instance().mapLayer(DVL2).dataProvider()
    pr_dvl2.addAttributes([
        QgsField('id', QVariant.String),
        QgsField('name', QVariant.String),
        QgsField('ang', QVariant.String),
        QgsField('x', QVariant.String),
        QgsField('y', QVariant.String),
    ])
    QgsProject.instance().mapLayer(DVL2).commitChanges()



    debug('>> layers setted')

    ##makestyles::
    p = QgsProject.instance()

    #_zona_big
    p.mapThemeCollection().removeMapTheme('_zona_big')
    rec = QgsMapThemeCollection().MapThemeRecord()
    recList=[]
    vl = visibleLayers
    for v in vl:
        recList.append(QgsMapThemeCollection().MapThemeLayerRecord(v))
    recList.append(QgsMapThemeCollection().MapThemeLayerRecord (zvl))
    recList.append(QgsMapThemeCollection().MapThemeLayerRecord(dvl))
    recList.append(QgsMapThemeCollection().MapThemeLayerRecord(dvl2))
    rec.setLayerRecords (recList)
    p.mapThemeCollection().insert('_zona_big', rec)

    #_zona_small
    p.mapThemeCollection().removeMapTheme('_zona_small')
    rec = QgsMapThemeCollection().MapThemeRecord()
    recList = []
    vl = visibleLayers
    for v in vl:
        recList.append(QgsMapThemeCollection().MapThemeLayerRecord(v))
    if di_layer not in vl:
        recList.append(QgsMapThemeCollection().MapThemeLayerRecord(di_layer))
    recList.append(QgsMapThemeCollection().MapThemeLayerRecord(zvl))
    rec.setLayerRecords(recList)
    p.mapThemeCollection().insert('_zona_small', rec)

    #_szona_big
    p.mapThemeCollection().removeMapTheme('_szona_big')
    rec = QgsMapThemeCollection().MapThemeRecord()
    recList = []
    vl = visibleLayers
    for v in vl:
        recList.append(QgsMapThemeCollection().MapThemeLayerRecord(v))
    if di_layer not in vl:
        recList.append(QgsMapThemeCollection().MapThemeLayerRecord(di_layer))
    recList.append(QgsMapThemeCollection().MapThemeLayerRecord(zvl))
    rec.setLayerRecords(recList)
    p.mapThemeCollection().insert('_szona_big', rec)

    #_szona_small
    p.mapThemeCollection().removeMapTheme('_szona_small')
    rec = QgsMapThemeCollection().MapThemeRecord()
    recList=[]
    vl = visibleLayers
    for v in vl:
        recList.append(QgsMapThemeCollection().MapThemeLayerRecord(v))
    if di_layer not in vl:
        recList.append(QgsMapThemeCollection().MapThemeLayerRecord(di_layer))
    recList.append(QgsMapThemeCollection().MapThemeLayerRecord(zvl))
    recList.append(QgsMapThemeCollection().MapThemeLayerRecord(dvl))
    recList.append(QgsMapThemeCollection().MapThemeLayerRecord(dvl2))
    rec.setLayerRecords(recList)
    p.mapThemeCollection().insert('_szona_small', rec)

    global mapL
    mapLmake()

    ##se puede agilizar
    #Lz = zl_layer #QgsProject.instance().mapLayer(mapL['zones'])

    #Lb = QgsProject.instance().mapLayer(mapL['bounds'])
    #Ld = QgsProject.instance().mapLayer(mapL['divisions'])

    ###########################################################################


    x=0
    global pag
    pag=1
    #for b in Lb.getFeatures():
    fr = 0
    zones_f = [zzz for zzz in zl_layer.getFeatures()]
    if pbar:
        pbar.setValue(1)
    for b in zones_f:
        if pbar:
            pbar.setValue(100/len(zones_f)*fr)
        fr+=1
        debug ('>>>> chapter: ')
        debug (b.attributes())

        #isTest
        #self.dlg.progressBar.setValue(int(10))
        szs = getSubzones(b, paper, scale)
        mkChapter(b, qptChapter,project_name, root_out, zl_layer, zl_field, di_layer, di_field, di_name)
        szfr=0
        for sz in szs:
            szfr+=1
            if pbar:
                pbar.setValue(100 / len(zones_f) * fr + 100 / len(zones_f)/len(szs)*szfr)
            debug ('>>>> division: ')
            mkDiv(sz, b.geometry(), qptDivision,project_name, root_out, zl_layer, zl_field, di_layer, di_field, di_name)
            if form:
                mkForm(sz, qptForm, form_file,project_name, root_out, zl_layer, zl_field, di_layer, di_field, di_name)
            if isTest:
                break
        if isTest:
            break
        x+=1
    
    #emptyTemp()

    # #remove styles
    p.mapThemeCollection().removeMapTheme('_zona_big')
    p.mapThemeCollection().removeMapTheme('_zona_small')
    p.mapThemeCollection().removeMapTheme('_szona_big')
    p.mapThemeCollection().removeMapTheme('_szona_small')

    #remove layers
    QgsProject.instance().removeMapLayer(ZVL)
    QgsProject.instance().removeMapLayer(DVL)
    QgsProject.instance().removeMapLayer(DVL2)

    debug('end')

    return

'''
meter capa en estilo
crear las capas te,porales de zonas
eliminar las capas temporales
'''
