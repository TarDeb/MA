from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from panel_detector import PanelDetector
from utils import nparray_to_qpixmap
from PyQt5 import QtCore
import os

class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.detector = PanelDetector()
        self.setup_ui()

    def setup_ui(self):
        # Set up the user interface for the object detection window
        self.setWindowTitle('Panel Detection')
        self.setGeometry(100, 100, 800, 600)

        # Button to run the detection
        self.button = QPushButton('Detect Panel', self)
        self.button.setFixedSize(120, 30)
        self.button.clicked.connect(self.run_detection)

        # Label to display the image
        self.label = QLabel(self)

        # Label to display the number of bounding boxes
        self.info_label = QLabel('No detection Panel', self)

        # Layout to arrange widgets
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.button, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.info_label)
        self.setLayout(self.layout)

    def run_detection(self):
        # If no image path is provided, get it from a file dialog
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpg *.jpeg *.png)")
        if self.image_path:
            # Run object detection and display results
            image_np_with_detections, saved_count = self.detector.run_detection_and_return_image(self.image_path)
            pixmap = nparray_to_qpixmap(image_np_with_detections)
            self.label.setPixmap(pixmap)
            # Update the label with the number of bounding boxes saved
            self.info_label.setText(
                f'<span style="font-size:11pt; font-weight:300;"> Name Image: {os.path.basename(self.image_path)} Number of Panel: {saved_count}</span>')
