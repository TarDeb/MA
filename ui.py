from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QProgressBar
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import glob
import os
import cv2
from image_processor import correct_distortion, get_gps_coordinates, process_images

