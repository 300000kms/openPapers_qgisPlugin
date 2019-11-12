# how to

pb_tool config
pb_tool clean
pb_tool compile
pb_tool deploy


--------

Plugin Builder Results
Congratulations! You just built a plugin for QGIS!


Your plugin openPapers was created in:
  /home/hp2018/Documents/repos/qgis-plugins/open_papers 
Your QGIS plugin directory is located at:
  /home/hp2018/.local/share/QGIS/QGIS3/profiles/default/python/plugins 

What's Next
If resources.py is not present in your plugin directory, compile the resources file using pyrcc5 (simply use pb_tool or make if you have automake) 

Optionally, test the generated sources using make test (or run tests from your IDE) 

Copy the entire directory containing your new plugin to the QGIS plugin directory (see Notes below) 

Test the plugin by enabling it in the QGIS plugin manager 

Customize it by editing the implementation file open_papers.py 

Create your own custom icon, replacing the default icon.png 

Modify your user interface by opening open_papers_dialog_base.ui in Qt Designer 

Notes: 
You can use pb_tool to compile, deploy, and manage your plugin. Tweak the pb_tool.cfg file included with your plugin as you add files. Install pb_tool using pip or easy_install. See http://loc8.cc/pb_tool for more information. 
You can also use the Makefile to compile and deploy when you make changes. This requires GNU make (gmake). The Makefile is ready to use, however you will have to edit it to add addional Python source files, dialogs, and translations. 
For information on writing PyQGIS code, see http://loc8.cc/pyqgis_resources for a list of resources. 
©2011-2019 GeoApt LLC - geoapt.com 
