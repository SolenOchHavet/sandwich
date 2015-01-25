#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Signals for "Main"

"""

try:
    from PyQt4.QtCore import Qt

except:
    from PySide.QtCore import Qt


class Signals(object):
    def __init__(self):
        # The Toolbar
        self.toolbar.newlayerButton.released.connect(self.sgnNewLayer)
        self.toolbar.renameLayerButton.released.connect(self.sgnRenameLayer)
        self.toolbar.savelayerButton.released.connect(self.sgnSaveLayer)
        self.toolbar.renderButton.released.connect(self.sgnLaunchRender)
        self.toolbar.exportButton.released.connect(self.sgnLaunchExport)
        self.toolbar.globalsButton.released.connect(self.sgnLaunchGlobals)

        # The Render Layer List
        self.dataTree.itemSelectionChanged.connect(self.sgnSelectLayer)
        self.dataTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dataTree.customContextMenuRequested.connect(self.sgnContextMenuForRenderLayersList)

    def sgnContextMenuForRenderLayersList(self, position):
        """
        When user right clicks the list "Render Layers" to get the context
        menu. The context menu contains the items:
         * Delete Layer... (code 0). Will remove the layer after the user
           confirms the action.
        """

        iCode = self.uiShowContextMenu(0, position)

        if iCode == 0:
            # Abort if no render layer is selected!
            if not self.uiIsRenderLayerSelected():
                return

            sTitle = "Remove Render Layer?"
            sMessage = "Are you sure you wish to remove render layer " \
                "\"%s\"?" % \
                (self.sSelectedLayerName)

            if self.uiAsk(sTitle, sMessage):
                self.uiRemoveSelectedRenderLayer()

                self.sgnSelectLayer()

    def sgnLaunchExport(self):
        """
        When user clicks the button "Export..." to launch the Export dialog
        where user can export selected render layers into ready made render
        scenes
        """

        self.parent.showExport()

    def sgnLaunchGlobals(self):
        """
        When user clicks the button "Globals..." to launch the Globals dialog
        to access Sandwich's settings
        """

        self.parent.showGlobals()

    def sgnLaunchRender(self):
        """
        When user clicks the button "Render..." to launch the Render dialog
        which is Sandwich's render manager for rendering the render layers
        locally on user's machine. Simple but handy
        """

        self.parent.showRender()

    def sgnNewLayer(self):
        """
        When user clicks the button "New Layer..." to add a new render layer
        """

        sNewLayer = self.uiGetNewRenderLayer()

        if sNewLayer:
            self.core.newLayer(sNewLayer)
            self.core.layer().save()

            self.uiLoadRenderLayers()

            self.sgnSelectLayer()

    def sgnRenameLayer(self):
        """
        When user clicks the button "Rename Layer..." from the main toolbar to
        rename the selected render layer into a new name
        """

        sRenamedLayer = self.uiGetRenamedRenderLayer()

        if sRenamedLayer:
            self.core.layer().rename(self.sSelectedLayerName, sRenamedLayer)

            self.uiLoadRenderLayers(sRenamedLayer)
            self.uiSaveSelectedRenderLayer()

    def sgnSaveLayer(self):
        """
        When user clicks the button "Save Layer" to save any changes made in
        the current render layer and execute them.
        """

        # Use the UI-class to save each tab to the core
        self.uiSaveSelectedRenderLayerContent()

        # Now that the core has all the data, save it to the node in the scene
        self.core.saveSelection()
        self.core.revertLayerAttributes()
        self.core.layer().save()
        self.core.layer().execute()
        self.core.revertSelection()

        # Reload the "Render Globals" section
        self.renderglobalsFrame.uiLoadRenderGlobals()

    def sgnSelectLayer(self, sLayerName = None):
        """
        When user selects a render layer in the Render Layers list. Loads all
        the tabs in Sandwich with all settings related to the layer
        """
        
        if sLayerName:
            self.uiSetRenderLayer(sLayerName)

        self.uiSaveSelectedRenderLayer()

        self.core.layer().execute()
        self.uiLoadSelectedRenderLayer()

        self.shadersFrame.uiSaveSelectedShader()
        self.attributesFrame.uiSaveSelectedAttribute()

        self.uiUpdateWindowTitle()

        # Validates
        self.uiValidate()
        self.shadersFrame.uiValidate()
        self.attributesFrame.uiValidate()
        self.overrideglobalsFrame.uiValidate()

    def sgnSwitchRenderLayersForToolbar(self):
        """
        When user clicks the check box for menu item View > Render Layers to
        switch the visibility state for the render layers list
        """

        # Get the inverted state for the render layers list visibility
        # state
        bIsVisible = not self.core.ui.isRenderLayersVisible()

        # Change the render layers list visibility state
        self.uiSetRenderLayersVisible(bIsVisible)

        # Save the new state
        self.core.ui.setRenderLayersVisible(bIsVisible)

    def sgnSwitchVisibilityForToolbar(self):
        """
        When user clicks the check box for menu item View > Toolbar to switch
        the visibility state for the toolbar
        """

        # Get the inverted state for the toolbar visibility state
        bIsVisible = not self.core.ui.isToolbarVisible()

        # Change the toolbar visibility state
        self.uiSetToolbarVisible(bIsVisible)

        # Save the new state
        self.core.ui.setToolbarVisible(bIsVisible)