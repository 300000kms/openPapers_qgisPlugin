
<img style = "height:50px" src="https://raw.githubusercontent.com/300000kms/arrels/master/logo.png">

# openPapers Qsis3 Plugin

## Make an atlas, print it, draw, scan and analize.

#### The power of the paper for the collaborative surveys!

<img src ="https://raw.githubusercontent.com/300000kms/openPapers_qgisPlugin/master/img/resume_lite.gif">

### what is it ?

This tool has been developed by [30000Km/s](http://www.300000kms.net) to help [Arrels foundation] (https://www.arrelsfundacio.org) to make the annual survey to count homeless people in Barcelona.

The purpose of this tools is generate a cartography to organize and be used by citizens in crowd surveys where GPS, phones and modern technologies are not precise enought or they need skilled people.

<img src ="https://raw.githubusercontent.com/300000kms/arrels/master/img/photo.jpg">


### How it works?

Once you have defined in Qgis the areas of the city you want to explore then the plugin generates an atlas that optimize the subdivision of the regions in paper sheets and coordinates the final documents.

The plugin will generate an atlas divided in ZONES and AREAS, where a zone contains different areas, and each area is printed in different papers according their size.

Once the data is on the paper, it can be scanned and digitized with othe tools that we are developing and testing, even you can create a new map with the small parts collected. 

Also we provide qr code and bar code description for process the survei after it collection.


### how is it?

#### What do you need?

- a base map of your city, territory or piece of land that you want to explore

- divide it in different AREAS according the lead teams that are going to help you with this big task (assign them an id and a name)

- divide (in other file) the AREAS in ZONES, and to each ZONE assign a name and the id of the belonging AREA 

#### Prepare your qgis file

- set a beautiful style to your map, when it's ready launch the plugin

#### The panel
<img src ="https://raw.githubusercontent.com/300000kms/openPapers_qgisPlugin/master/img/panel.png">

General:
 - project name: this will be printed in the template 
 - folder: where you want to store a copy of the files
 
 Areas
 - areas layer: the layer with the description of the polygons of the areas
 - area id attribute: the field that identifies each polygon of the areas
 - area name attribute: the name associated to each of these polygons
 
 Zones
 - zones layer: the layer with the description of the subdivision of the areas in zones  
 - area id attribute: the field where is indicated the name og¡f the belonging area
 - aprox. scale: the aproximate scale to be used in the subdivisions of the zones
 
 Select templates (advanced users only)
 - zone template: the template of the zone
 - subzone template: the template of the subzone
 - form: the template of the form
 - form file: a png with the image of the form to insert
 
 Others: 
 - print form: check this box if you want to print the form (is optional!)
 - print test: check this box if you want to print a test to verify that all works as expected
 
### and now explore your streets!

 <img style ="width:600px" width="600px" src ="https://github.com/300000kms/arrels/blob/master/img/recompte-2016-600x400.jpg?raw=true">
<br>
 <img style ="width:600px" width="600px" src ="https://github.com/300000kms/arrels/blob/master/img/CixFSxBXIAI499s.jpg?raw=true">
<br>
 <img style ="width:600px" width="600px" src ="https://github.com/300000kms/arrels/blob/master/img/arrels_viewer.png?raw=true">
<br>

### and then?
- we have a repository with examples of data to use [here](https://github.com/300000kms/openPapers_exampleData)
- another repo with experiments to rescan the maps and build a mega super big one as a result of all them (works!!) [here](https://github.com/300000kms/arrels/tree/master/_formReader)
