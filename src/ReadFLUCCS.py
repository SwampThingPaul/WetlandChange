## Title: Lee and Collier County Land Use-Cover change analysis
## Created by: Paul Julian (pjulian@sccf.org)
## Date: 2022-07-06

# Libraries
import os 
import qgis.core

## Importing data into QGIS via python script
## https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/loadlayer.html
data_path=str('C:/Julian_LaCie/_GISData')

### Read Data into Project
FL_Cnty=data_path+'/FloridaCounties/Florida_Counties.shp'
FL_Cnty_vlayer= QgsVectorLayer(FL_Cnty,"county", "ogr")
# QgsProject.instance().addMapLayer(FL_Cnty_vlayer)

FLUCCS2014=data_path+'/SFWMD_FLUCCS/FLUCCS_2014_2016/SFWMD_Land_Cover_Land_Use_2014-2016.shp'
FLUCCS2014_vlayer = QgsVectorLayer(FLUCCS2014, "FLUCCS2014", "ogr")
# QgsProject.instance().addMapLayer(FLUCCS2014_vlayer)

FLUCCS2017=data_path+'/SFWMD_FLUCCS/FLUCCS_2017_2019/SFWMD_LCLU_2017_2019.shp'
FLUCCS2017_vlayer = QgsVectorLayer(FLUCCS2017, "FLUCCS2017", "ogr")
# QgsProject.instance().addMapLayer(FLUCCS2017_vlayer)

## reproject data to common projection
## EPSG:34326 = WGS84
## EPSG:32617 = WGS84 UTM17
param={'INPUT':FL_Cnty_vlayer,'TARGET_CRS':'EPSG:32617','OUTPUT':'memory:CountyUTM'}
FL_Cnty_pro=processing.run('native:reprojectlayer',param)['OUTPUT']
# QgsProject.instance().addMapLayer(FL_Cnty_pro);

param={'INPUT':FLUCCS2014_vlayer,'TARGET_CRS':'EPSG:32617','OUTPUT':'memory:FLUCCS2014'}
FLUCCS2014_pro=processing.run('native:reprojectlayer',param)['OUTPUT']
# QgsProject.instance().addMapLayer(FLUCCS2014_pro)

param={'INPUT':FLUCCS2017_vlayer,'TARGET_CRS':'EPSG:32617','OUTPUT':'memory:FLUCCS2017'}
FLUCCS2017_pro=processing.run('native:reprojectlayer',param)['OUTPUT']
# QgsProject.instance().addMapLayer(FLUCCS2017_pro)
## FLUCCS 2014 has invalid geometry
## see https://www.qgistutorials.com/en/docs/3/handling_invalid_geometries.html

#param={ 'ERROR_OUTPUT' : 'memory:error_out',\
#'IGNORE_RING_SELF_INTERSECTION' : False, \
#'INPUT_LAYER' :FLUCCS2014_pro,\
#'INVALID_OUTPUT' : 'memory:invalid_out',\
#'METHOD' : 2,\
#'VALID_OUTPUT' : 'memory:valid_out' }
#checkFLUCCS2014=processing.run('qgis:checkvalidity',param)
#QgsProject.instance().addMapLayer(checkFLUCCS2014['ERROR_OUTPUT'])
#QgsProject.instance().addMapLayer(checkFLUCCS2014['INVALID_OUTPUT'])
#QgsProject.instance().addMapLayer(checkFLUCCS2014['VALID_OUTPUT'])

param={\
'INPUT' :FLUCCS2014_pro,\
'OUTPUT':'memory:FLUCCS2014_pro_fix'}
FLUCCS2014_pro2=processing.run('native:fixgeometries',param)['OUTPUT']
# QgsProject.instance().addMapLayer(FLUCCS2014_pro2)

param={\
'INPUT' :FLUCCS2017_pro,\
'OUTPUT':'memory:FLUCCS2017_pro_fix'}
FLUCCS2017_pro2=processing.run('native:fixgeometries',param)['OUTPUT']
# QgsProject.instance().addMapLayer(FLUCCS2017_pro2)

# subset County for Lee and Collier
express_val='COUNTYNAME=\'LEE\' OR COUNTYNAME=\'COLLIER\''
param={'INPUT':FL_Cnty_pro,'EXPRESSION':express_val,'OUTPUT': 'memory:LeeCollier'}
FL_Cnty_pro2=processing.run("qgis:extractbyexpression",param)['OUTPUT']
# QgsProject.instance().addMapLayer(FL_Cnty_pro2)

param={'INPUT':FL_Cnty_pro2,\
'DISSOLVE' : True, 'DISTANCE' : 5000, 'END_CAP_STYLE' : 0,\
'JOIN_STYLE' : 0, 'MITER_LIMIT' : 2,\
'OUTPUT' :'memory:LeeCollier_buff'}
FL_Cnty_buff=processing.run("native:buffer",param)['OUTPUT']
QgsProject.instance().addMapLayer(FL_Cnty_buff)

# Clip FLUCCS to Lee and Collier County
param={'INPUT':FLUCCS2014_pro2,'OVERLAY':FL_Cnty_buff,'OUTPUT': 'memory:FLUCCS2014_LeeCollier'}
FLUCCS2014_clip=processing.run("native:clip",param)['OUTPUT']
QgsProject.instance().addMapLayer(FLUCCS2014_clip)

param={'INPUT':FLUCCS2017_pro2,'OVERLAY':FL_Cnty_buff,'OUTPUT': 'memory:FLUCCS2017_LeeCollier'}
FLUCCS2017_clip=processing.run("native:clip",param)['OUTPUT']
QgsProject.instance().addMapLayer(FLUCCS2017_clip)

## Dissolve

## Union

## export union shapefiles

