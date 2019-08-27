'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

from qgis.core import QgsProject
from qgis.PyQt.QtCore import QFileInfo, QPointF
from qgis.gui import QgsMapCanvas
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtGui import QPainter, QImage
from qgis.PyQt.QtCore import QSizeF, QSize, QRect, QRectF
import os
import shutil
import barcode
try:
    import qrcode
    print('qrcode ready')
except Exception as e:
    print (e)



###############################################################################
###############################################################################

def printRaster(composition, nameFile, root_out):
    global pag
    dpi = 150
    path = root_out + str(pag).zfill(3)+'_'+nameFile+'.png'
    
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
    desc=layers[layerName]
    l=QgsProject.instance().mapLayer(mapL[layerName])
    l.setSubsetString(criteria)
    return


def mapL():
    mapL={}
    #reg = QgsMapLayerRegistry.instance()
    #lyrsName = reg.mapLayers().values()
    lyrsName = QgsProject.instance().mapLayers().values()
    for l in lyrsName:
        mapL[l.name()]=l.id()
    return mapL


def makeQR(data,name):
    qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    path = PATH+'/temp/'+name+'.png'
    img.save(path)
    return path
    
def makeBarcode(data, name):
    print (data)
    bc = barcode.get_barcode_class('code39')
    path = PATH+'/temp/'+name+'.svg'
    #bc('lalala').save(path)
    #bc(data).save(path)
    return path
    
def emptyTemp():
    shutil.rmtree(PATH+'/temp')
    return
    
def featureFields(b):
    result =[a.name() for a in b.fields()]
    return result


def mkChapter(b, qptChapter,project_name, root_out, root_code):
    """
    b es un bound
    """
    Lz = QgsProject.instance().mapLayer(mapL['zones'])
    
    file_qptChapter= open(qptChapter,'r')
    template_content_chapter=file_qptChapter.read()
    file_qptChapter.close()
    
    ###
    filter('zones', '"name" = \''+b.attribute('name')+'\'' )#cuidado si el valor es integer o string
    filter('zones2', '"name" = \''+b.attribute('name')+'\'' )#cuidado si el valor es integer o string
    filter('divisions', '"name" = \''+b.attribute('name')+'\'' )
    filter('divisions2', '"name" = \''+b.attribute('name')+'\'' )

    ### seleccionamos la zona
    zz = Lz.getFeatures(QgsFeatureRequest(QgsExpression('"name" = \''+b.attribute('name')+'\''))) #cuidado si el valor es integer o string
    zz = [x for x in zz]

    # escogemos el distrito correspondiente a la zona
    filter('districtes', '"name" = \''+unicode(zz[0].attribute('d_name'))+'\'' )
    global currentDistrict
    currentDistrict = unicode(zz[0].attribute('d_id'))
    
    #coje la geometria del distriro
    distri = QgsProject.instance().mapLayer(mapL['districtes'])
    gd= [d for d in distri.getFeatures()][0]

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
    map_item.setKeepLayerStyles(False)
    map_item.setKeepLayerSet (False)
    
    #map_item.setLayers(QgsProject.instance().mapThemeCollection().mapThemeVisibleLayers('chapter_big'))
    map_item.setFollowVisibilityPresetName ('chapter_big')
    
    map_item_distri = composition.itemById('mapDistrito')
    map_item_distri.zoomToExtent(gd.geometry().boundingBox())
    map_item_distri.setKeepLayerStyles(False)
    map_item_distri.setKeepLayerSet (False)

    #qgis2 #layerSet = QgsProject.instance().visibilityPresetCollection().presetVisibleLayers('chapter_small')
    #map_item_distri.setLayerSet(layerSet)
    map_item.setFollowVisibilityPresetName ('chapter_small')

    ##title
    ti = composition.itemById('project')
    ti.setText(project_name)

    ##zona
    zo = composition.itemById('zona')
    zo.setText(str(b.attribute('id')))
    
    corners = composition.itemById('corners')
    corners.setPicturePath(root_code+'templates/corners_a4.svg')
    
    logo = composition.itemById('logo')
    logo.setPicturePath(root_code+'templates/logo.svg')
    
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

    filter('divisions', '' )
    filter('divisions2', '' )
    filter('districtes', '' )
    
    return


def mkDiv(b, z, qptDivision,project_name, root_out, root_code):
    Lz = QgsProject.instance().mapLayer(mapL['zones'])
    angle = b.attribute('ang')
    #esto visulamente es correcto
    ##pero me fastidia la lectira posterior porque no dejo rastro de esta manipulacion
    ##para el escaneo posterio deberia de modificar el orden de los bounds en el qr y en el pie de pagina
    
    if angle > 45:
        angle = angle-90
    elif angle < -45:
        angle = angle+90

    sql = '"name" = \''+b.attribute('name')+'\''
    sql += ' AND "x" = '+str(b.attribute('x'))
    sql += ' AND "y" = '+str(b.attribute('y'))
    filter('divisions', sql)
    
    sql2='"name" = \''+b.attribute('name')+'\''
    filter('divisions2', sql2)

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
    map_item.setKeepLayerStyles(False)
    map_item.setFollowVisibilityPresetName ('division_big')
    
    map_item.setMapRotation(-angle)########
    cc = b.geometry().centroid().asPoint()
    coordsDesc = str(b.geometry().asWkt())[10:][:-2].split(', ')
    
    b.geometry().rotate(-angle, cc)
    rBound = b.geometry().boundingBox()
    map_item.zoomToExtent(rBound)

    ##mapa 2
    map_item2 = composition.itemById('minimapa')
    map_item2.setKeepLayerStyles(False)
    map_item2.setFollowVisibilityPresetName ('division_small')

    #cuidado que aqu´i se lia con valor integer o string
    zz = Lz.getFeatures(QgsFeatureRequest(QgsExpression('"name" = \''+b.attribute('name')+'\'')))
    zz = [x for x in zz]
    z = zz[0].geometry()
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
    zo.setText(str(b.attribute('name').replace('_', '.')))
    
    ##title
    ti = composition.itemById('project')
    ti.setText(project_name)
    
    ##cbarres
    #cb_name = 'cb_'+str(b.attribute('name').replace('_', '.'))+'_'+str(b.attribute('x'))+'_'+str(b.attribute('y'))
    cb_text = '*'+str(b.attribute('name').replace('_', '.'))+','+str(b.attribute('x'))+','+str(b.attribute('y'))+'*'
    #makeBarcode(cb_text, cb_name)
    
    cbarres = composition.itemById('cbarres')
    cbarres.setText(cb_text)

    #qrcode
    name = str(b.attribute('name').replace('_', '.'))+'_'+str(b.attribute('x'))+'_'+str(b.attribute('y'))
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
    corners.setPicturePath(root_code+'templates/corners_a4.svg')
    
    logo = composition.itemById('logo')
    logo.setPicturePath(root_code+'templates/logo.svg')
    
    norte = composition.itemById('norte')
    norte.setPicturePath(root_code+'templates/norte.svg')
    norte.setRotation(angle)

    composition.refresh()
    image_name = str(b.attribute('name').replace('_', '-'))+'_'+str(b.id())+'_'+currentDistrict
    printRaster(composition, image_name, root_out)
    return

def mkForm(b,qptForm,form_file,project_name, root_out, root_code):
    
    name = str(b.attribute('name').replace('_', '.'))+'_'+str(b.attribute('x'))+'_'+str(b.attribute('y'))

    template_file = open(qptForm,'r')
    template_content = template_file.read()
    template_file.close()
    document = QDomDocument()
    document.setContent(template_content)
    
    composition = QgsLayout (QgsProject().instance())
    composition.loadFromTemplate(document,QgsReadWriteContext())
    
    corners = composition.itemById('corners')
    corners.setPicturePath(root_code+'templates/corners_a4.svg')
    
    logo = composition.itemById('logo')
    logo.setPicturePath(root_code+'templates/logo.svg')
    
    ##title
    ti = composition.itemById('project')
    ti.setText(project_name)

    ##zona
    zo = composition.itemById('zona')
    zo.setText(str(b.attribute('name').replace('_', '.')))

    ##pagina
    zo = composition.itemById('pagina')
    zo.setText(name)
    
    #form
    qr = composition.itemById('form')
    qr.setPicturePath(form_file)
    
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
    cbarres.setText('*'+str(b.attribute('name').replace('_', '.'))+','+str(b.attribute('x'))+','+str(b.attribute('y'))+'*')

    composition.refresh()
    
    image_name = str(b.attribute('name').replace('_', '-'))+'_'+str(b.id())+'_form'+'_'+currentDistrict
    printRaster(composition, image_name, root_out)
    return


def showLayers():
    reg = QgsMapLayerRegistry.instance()
    for l in reg.mapLayers().values():
        print ( l.id() )
    return


###########################################################################
###########################################################################
def makeAtlas(qptChapter,qptDivision,qptForm, form_file=None,form=False,project_name='',  root_out = '', root_code = ''):
    
    ##setstyles divisions2 divisions
    layer = QgsProject.instance().mapLayersByName("divisions")[0]
    layer.loadNamedStyle(root_code + 'templates/layerstyles/divisions.qml')
    
    layer2 = QgsProject.instance().mapLayersByName("divisions2")[0]
    layer2.loadNamedStyle(root_code + 'templates/layerstyles/divisions2.qml')
    
    zones = QgsProject.instance().mapLayersByName("zones")[0]
    zones.loadNamedStyle(root_code + 'templates/layerstyles/zones.qml')
    
    zones2 = QgsProject.instance().mapLayersByName("zones2")[0]
    zones2.loadNamedStyle(root_code + 'templates/layerstyles/zones.qml')
    
    global PATH
    #print(os.path.dirname(os.path.realpath('__file__')))
    #PATH = '/'.join(os.getcwd().split('/')[0:-1])
    PATH = root_code
    
    global mapL
    mapL = mapL()

    ##se puede agilizar
    Lz = QgsProject.instance().mapLayer(mapL['zones'])
    Lb = QgsProject.instance().mapLayer(mapL['bounds'])
    Ld = QgsProject.instance().mapLayer(mapL['divisions'])

    #Lzf = [a.name() for a in Lz.fields()]
    #Lbf = [a.name() for a in Lb.fields()]
    #Ldf = [a.name() for a in Ld.fields()]
    ###########################################################################

    currentDistrict = ''
    x=0
    
    global pag
    pag=1
    for b in Lb.getFeatures():
        print ('>>>> chapter: '),
        print (b.attributes())
        if x>=0 and x < 1:  #and b.attributes()[0] > 324: #para provocar una salida rapida , dejar 2000
            mkChapter(b, qptChapter,project_name, root_out, root_code)
            exp = QgsExpression('name = \''+b.attribute('name')+'\'')
            z = b.geometry()
            request = QgsFeatureRequest(exp)
            for d in Ld.getFeatures(request):
                print ('>>>> division: '),
                mkDiv(d, z, qptDivision,project_name, root_out, root_code)
                if form:
                    mkForm(d, qptForm, form_file,project_name, root_out, root_code)
        x+=1
    
    #emptyTemp()
    return


##############################

#root = '/home/hp2018/Documents/_projects/_impulsem/project_badalona/'
#root_out = 
#root_code = 
root_code = '/home/hp2018/Documents/_projects/_impulsem/code/'
qptChapter  = root_code + 'templates/arrelsAtlas_chapter.qpt'
qptDivision = root_code + 'templates/arrelsAtlas_division.qpt'
qptForm     = root_code + 'templates/arrelsAtlas_form.qpt'

'''
makeAtlas(
    qptChapter,
    qptDivision,
    qptForm,
    #z1,
    #z2,
    #d1,
    #d2
    form_file = '/home/hp2018/Documents/_projects/_impulsem/code/assets/formArrels_03.svg',
    form = True,
    project_name = 'Cens Barcelona 2019',
    root_out  = '/home/hp2018/Documents/_projects/_impulsem/project_badalona/out/',
    root_code = '/home/hp2018/Documents/_projects/_impulsem/code/',
    )
'''
