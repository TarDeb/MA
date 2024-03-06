from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFileDialog, QProgressBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5 import QtCore, QtGui
from new_window import NewWindow
from utils import *

class IntegratedApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.detection_window = None
        self.image_list = []
        self.current_index = 0
        self.input_folder_path = ""
        self.output_folder_path = ""

        self.setWindowTitle('ThermoPV')
        self.setStyleSheet("""
                    QMainWindow {
                        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                          stop:0 #FFFFFF, stop:1 #B6FBFF); 
                    }
                    QPushButton {
                        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                                          stop:0 #4B79A1, stop:1 #283E51);
                        color: white;
                        border: none;
                        font-family: 'Segoe UI', Helvetica, sans-serif;
                        font-size: 12px;
                        font-weight: 600;
                        padding: 10px 15px;
                        border-radius: 5px;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                    }
                    QPushButton:hover {
                        background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #283E51, stop:1 #4B79A1);
                    }
                    QProgressBar {
                        border: 2px solid grey; border-radius: 15px; color: black; text-align: center;
                        height: 20px; font-family: 'Arial', sans-serif; font-size: 14px; font-weight: bold;
                    }
                    QProgressBar::chunk {
                        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0598CC, stop:1 #0CD3E2);
                        border-radius: 13px;}}""")

        # Main layout
        main_layout = QHBoxLayout()

        # Image section layout
        img_layout = QVBoxLayout()

        # Open separate window button
        self.new_window_button = QPushButton('Panel Detect', self)



        #################
        # self.new_button = QPushButton('CSV', self)
        #
        # self.new_button.clicked.connect(self.create_CSV)
        #  # Assuming you have a method to handle the button click
        # self.new_button.setFixedSize(120, 30)
        ###################
        self.new_window_button.clicked.connect(self.open_new_window)
        self.new_window_button.setFixedSize(120, 30)
        img_layout.addWidget(self.new_window_button, alignment=QtCore.Qt.AlignCenter)

        # Image name label
        self.image_name_label = QLabel(self)
        img_layout.addWidget(self.image_name_label, alignment=QtCore.Qt.AlignCenter)

        # Image coordinates label
        self.image_coords_label = QLabel(self)
        img_layout.addWidget(self.image_coords_label, alignment=QtCore.Qt.AlignCenter)

        # Image label with default pixmap
        pixmap = QPixmap(800, 600)
        pixmap.fill(QtCore.Qt.black)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont('Arial', 35))
        painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, "No Image Loaded")
        painter.end()

        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)
        img_layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignCenter)

        # Navigation buttons
        self.prev_button = QPushButton('Previous', self)
        self.prev_button.setFixedSize(120, 30)
        self.prev_button.clicked.connect(self.prev_image)
        self.next_button = QPushButton('Next', self)
        self.next_button.setFixedSize(120, 30)
        self.next_button.clicked.connect(self.next_image)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.prev_button)
        btn_layout.addWidget(self.next_button)
        img_layout.addLayout(btn_layout)

        # Input, output, (process buttons)
        btn_select_input = QPushButton('Select Input Folder', self)
        btn_select_input.setFixedSize(250, 30)
        btn_select_input.clicked.connect(self.set_input_folder)
        btn_select_output = QPushButton('Select Output Folder', self)
        btn_select_output.setFixedSize(250, 30)
        btn_select_output.clicked.connect(self.set_output_folder)

        btn_process = QPushButton('Process Images', self)
        btn_process.setFixedSize(250, 30)
        btn_process.clicked.connect(self.process_and_load)

        btn_load_images = QPushButton('Load Image', self)
        btn_load_images.setFixedSize(250, 30)
        btn_load_images.clicked.connect(self.load_images_from_folder)

        img_layout.addWidget(btn_load_images, alignment=QtCore.Qt.AlignCenter)
        img_layout.addWidget(btn_select_input, alignment=QtCore.Qt.AlignCenter)
        img_layout.addWidget(btn_select_output, alignment=QtCore.Qt.AlignCenter)
        img_layout.addWidget(btn_process, alignment=QtCore.Qt.AlignCenter)

        main_layout.addLayout(img_layout)

        map_layout = QVBoxLayout()
        self.web_view = QWebEngineView(self)
        map_layout.addWidget(self.web_view)

        self.web_view.setMinimumSize(QtCore.QSize(500, 500))
        self.web_view.setMaximumSize(QtCore.QSize(550, 550))
        main_layout.addLayout(map_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.load_original_images()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedSize(350, 30)
        img_layout.addWidget(self.progress_bar, alignment=QtCore.Qt.AlignCenter)

    def load_google_maps(self, lat, lon):
        base_url = f"https://www.google.com/maps/@{lat},{lon},25z/data=!3m1!1e3"
        self.web_view.load(QUrl(base_url))

    def set_input_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if path:
            self.input_folder_path = path

    def set_output_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_folder_path = path

    def load_images_from_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if path:
            self.image_list = glob.glob(os.path.join(path, "*.JPG"))
            if self.image_list:
                self.show_image_without_processing(self.image_list[0])

    def process_and_load(self):
        process_images(self.input_folder_path, self.output_folder_path, self.update_progress_bar)
        self.load_original_images()
        self.progress_bar.reset()

    def load_original_images(self):
        self.image_list = glob.glob(os.path.join(self.input_folder_path, "*.JPG"))
        if self.image_list:
            self.show_image(self.image_list[0])

    def update_progress_bar(self, current, total):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)

    def show_image_without_processing(self, image_path):
        filename = os.path.basename(image_path)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixmap = nparray_to_qpixmap(image)

        self.image_name_label.setText(f"<b><u>Image Name:</u></b> {filename}")
        self.image_label.setPixmap(pixmap.scaled(800, 600, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

        coords = get_gps_coordinates(image_path)
        if coords:
            lat, lon = coords
            ajust_lat = lat +  0.00011
            self.image_coords_label.setText(
                f"<b><font color='blue'>Coordinates: Lat: {lat:.5f}, Lon: {lon:.5f}</font></b>")
            self.load_google_maps(ajust_lat, lon)
        else:
            self.image_coords_label.setText(f"<font color='red'>Coordinates: Not Available</font></b>")

    def load_images_from_dialog(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "JPEG Files (*.JPG);;All Files (*)",
                                                options=options)
        if files:
            self.image_list = files
            self.show_image_without_processing(self.image_list[0])

    def show_image(self, image_path):
        filename = os.path.basename(image_path)

        # Load from the processed folder
        processed_image_path = os.path.join(self.output_folder_path, filename)

        # Check if the processed image exists, else load the original
        if os.path.exists(processed_image_path):
            image = cv2.imread(processed_image_path)
        else:
            image = cv2.imread(image_path)

        # Convert the color from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixmap = nparray_to_qpixmap(image)

        # Update the UI elements with the image information
        self.image_name_label.setText(f"Image Name: {filename}")
        self.image_label.setPixmap(pixmap.scaled(800, 600, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

        # Get GPS coordinates from the image metadata
        coords = get_gps_coordinates(image_path)
        if coords:
            lat, lon = coords
            # Adjust latitude and longitude slightly
            ajust_lat = lat + 0.00011# Slightly larger adjustment for latitude
            # Load the adjusted coordinates into Google Maps
            self.load_google_maps(ajust_lat, lon)

    def prev_image(self):
        self.current_index -= 1
        self.show_image_without_processing(self.image_list[self.current_index])

    def next_image(self):
        self.current_index += 1
        self.show_image_without_processing(self.image_list[self.current_index])

    def open_new_window(self):
        self.detection_window = NewWindow()  # Create the detection window
        self.detection_window.setGeometry(250, 100, 800, 600)  # Set geometry for the new window
        self.detection_window.show()


###

