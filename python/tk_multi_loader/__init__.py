# Copyright (c) 2015 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

from .open_publish_form import open_publish_browser

import sgtk
from sgtk.platform.qt import QtCore, QtGui

from .ui import resources_rc

help_screen = sgtk.platform.import_framework("tk-framework-qtwidgets", "help_screen") 

def show_dialog(app):
    """
    Show the main loader dialog
    
    :param app:    The parent App
    """
    # defer imports so that the app works gracefully in batch modes
    from .dialog import AppDialog
    
    # Create and display the splash screen
    app.log_debug("Displaying splash dialog")
    splash_pix = QtGui.QPixmap(":/res/splash.png") 
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    QtCore.QCoreApplication.processEvents()

    app.log_debug("Trying to load LoaderActionManager")
    # create the action manager for the Loader UI:
    from .loader_action_manager import LoaderActionManager
    action_manager = LoaderActionManager()
        
    # start ui
    ui_title = app.get_setting("title_name")
    app.log_debug("Starting Dialog: %s" % ui_title)
    w = app.engine.show_dialog(ui_title, app, AppDialog, action_manager)

    # Keep pointer to dialog so as to be able to hide/show it in actions
    engine_name = app.engine.instance_name
    app.log_debug("Detected Engine: %s" % engine_name)
    
    # attach splash screen to the main window to help GC
    w.__splash_screen = splash
    
    # hide splash screen after loader UI show
    splash.finish(w.window())
        
    # pop up help screen
    if w.is_first_launch() and not (engine_name == "tk-fusion"):
        # wait a bit before show window
        QtCore.QTimer.singleShot(1400, w.show_help_popup)
        

        
    