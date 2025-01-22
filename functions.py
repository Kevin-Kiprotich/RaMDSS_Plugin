from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QFileDialog
from qgis.core import QgsProject, QgsVectorLayer

def addVectorLayer(path):
    # Get the QGIS project instance
    project = QgsProject.instance()

    # Extract the layer name from the file path
    file = path.split('/')[-1]
    parts = file.split('.')  # Remove the file extension
    fileName = '.'.join(parts[:-1])
    # Create a vector layer
    layer = QgsVectorLayer(path, fileName, 'ogr')  # 'ogr' is the provider for vector data

    # Check if the layer is valid
    if layer.isValid():
        # Add the layer to the project
        project.addMapLayer(layer)
        print(f"Layer '{fileName}' added successfully!")
    else:
        show_error_message("Could not add layer because the layer is invalid.")

def show_error_message(message):
    """
        Shows an error message if an error occurs.
        Args:
            message (str): Error message to be displayed.
    """
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Error")
    msg_box.setText(message)
    msg_box.exec_()

def show_info_message(message):
    """
    Shows an information message.
    Args:
        message (str): Information message to be displayed.
    """
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)  # Change to Information icon
    msg_box.setWindowTitle("Information")  # Update window title
    msg_box.setText(message)
    msg_box.exec_()

def getOutputDestination(parent=None):
    """
    Open a file dialog to allow the user to select where to save the output GeoTIFF file.

    Returns:
        str: The file path selected by the user to save the GeoTIFF file, or an empty string if canceled.
    """
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getSaveFileName(parent, "Select Output Destination", "", "GeoJSON File (*.geojson *.json);;All Files (*)", options=options)
    
    if file_name:
        return file_name
    else:
        return ""