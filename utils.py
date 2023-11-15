import os
import glob
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif


def correct_distortion(img, k1, k2, p1, p2, k3, rotation_angle):
    h, w = img.shape[:2]
    camera_matrix = np.array([[766.14, 0, w / 2.0], [0, 766.14, h / 2.0], [0, 0, 1]])
    dist_coeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float64)
    img_undistorted = cv2.undistort(img, camera_matrix, dist_coeffs)
    M = cv2.getRotationMatrix2D((w / 2.0, h / 2.0), rotation_angle, 1)
    img_rotated = cv2.warpAffine(img_undistorted, M, (w, h))
    return img_rotated


def process_images(input_folder, output_folder, progress_callback):
    image_files = glob.glob(os.path.join(input_folder, "*.JPG"))
    total_images = len(image_files)
    progress_callback(0, total_images)  # Initialize progress bar

    k1, k2, p1, p2, k3, rotation_angle = -0.35245767, 0.13652994, 0.00065283, 0.00075075, 0.1339468, -2
    for index, file in enumerate(image_files):
        # Open the original image using PIL and extract metadata
        original_image = Image.open(file)
        exif_data = piexif.load(original_image.info['exif']) if 'exif' in original_image.info else None

        # Convert PIL image to OpenCV format
        img = np.array(original_image)
        img_corrected = correct_distortion(img, k1, k2, p1, p2, k3, rotation_angle)

        # Convert corrected image back to PIL format
        corrected_image = Image.fromarray(img_corrected)

        # Save the corrected image with original metadata
        filename = os.path.basename(file)
        output_file_path = os.path.join(output_folder, filename)
        if exif_data:
            exif_bytes = piexif.dump(exif_data)
            corrected_image.save(output_file_path, "JPEG", quality=100, exif=exif_bytes)
        else:
            corrected_image.save(output_file_path, "JPEG", quality=100)

        print(f"Successfully wrote {output_file_path}")
        progress_callback(index + 1, total_images)  # Update progress bar


def get_gps_coordinates(image_path):
    img = Image.open(image_path)
    exif_data = img._getexif()
    if not exif_data:
        return None
    geo_data = {}
    for tag, value in TAGS.items():
        if tag in exif_data:
            if TAGS[tag] == "GPSInfo":
                for tag_value in exif_data[tag]:
                    if tag_value in GPSTAGS:
                        geo_data[GPSTAGS[tag_value]] = exif_data[tag][tag_value]

    lat_data = geo_data.get("GPSLatitude", None)
    lon_data = geo_data.get("GPSLongitude", None)

    if not lat_data or not lon_data:
        return None

    lat = sum(float(x) / float(y) for x, y in zip(lat_data, (1, 60.0, 3600.0)))
    lon = sum(float(x) / float(y) for x, y in zip(lon_data, (1, 60.0, 3600.0)))

    lat = lat if geo_data["GPSLatitudeRef"] == "N" else -lat
    lon = lon if geo_data["GPSLongitudeRef"] == "E" else -lon

    return lat, lon


# NumPy array-> QImage-> QPixmap.
def nparray_to_qpixmap(image):
    # Convert numpy array to QPixmap
    height, width, channel = image.shape
    bytes_per_line = 3 * width
    q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(q_img)
