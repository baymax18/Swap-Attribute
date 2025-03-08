

from qgis.PyQt.QtWidgets import QMessageBox, QAction
from qgis.core import QgsProject, edit

class SwapAttribute:
    """QGIS Plugin Implementation to swap attributes of two selected features."""

    def __init__(self, iface):
        """Initialize the plugin."""
        self.iface = iface
        self.actions = []  # Initialize the list of actions
        self.toolbar = self.iface.addToolBar("Swap Attribute")

    def initGui(self):
        """Creates menu item and toolbar button."""
        self.action = QAction("Swap Attributes", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("&Swap Attribute", self.action)
        self.toolbar.addAction(self.action)
        self.actions.append(self.action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu("&Swap Attribute", action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar  # Remove toolbar if needed

    def run(self):
        """Main function to swap attributes of two selected features."""
        layer = self.iface.activeLayer()

        if not layer:
            QMessageBox.critical(None, "Error", "No active layer selected!")
            return

        # Get selected features
        selected_features = layer.selectedFeatures()

        if len(selected_features) != 2:
            QMessageBox.warning(None, "Warning", "Please select exactly two features!")
            return

        feature1, feature2 = selected_features

        with edit(layer):  # Start editing
            for field in layer.fields():  # Loop through all fields
                field_name = field.name()

                # Swap attribute values
                temp = feature1[field_name]
                feature1[field_name] = feature2[field_name]
                feature2[field_name] = temp

                layer.updateFeature(feature1)
                layer.updateFeature(feature2)

        QMessageBox.information(None, "Success", "Attributes swapped successfully!")
