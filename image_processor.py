import cv2
import numpy as np
from PIL import Image
import piexif

def correct_distortion(img, k1, k2, p1, p2, k3, rotation_angle):
  h, w = img.shape[:2]
    camera_matrix = np.array([[766.14, 0, w / 2.0], [0, 766.14, h / 2.0], [0, 0, 1]])
    dist_coeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float64)
    img_undistorted = cv2.undistort(img, camera_matrix, dist_coeffs)
    M = cv2.getRotationMatrix2D((w / 2.0, h / 2.0), rotation_angle, 1)
    img_rotated = cv2.warpAffine(img_undistorted, M, (w, h))
    return img_rotated

def process_images(input_folder, output_folder):
    image_files = glob.glob(os.path.join(input_folder, "*.JPG"))
    k1, k2, p1, p2, k3, rotation_angle = -0.35245767, 0.13652994, 0.00065283, 0.00075075, 0.1339468, -2
    for file in image_files:
        img = cv2.imread(file)
        img_corrected = correct_distortion(img, k1, k2, p1, p2, k3, rotation_angle)
        filename = os.path.basename(file)
        output_file_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_file_path, img_corrected, [cv2.IMWRITE_JPEG_QUALITY, 100])
        print(f"Successfully wrote {output_file_path}")


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

    lat = sum(float(x)/float(y) for x, y in zip(lat_data, (1, 60.0, 3600.0)))
    lon = sum(float(x)/float(y) for x, y in zip(lon_data, (1, 60.0, 3600.0)))

    lat = lat if geo_data["GPSLatitudeRef"] == "N" else -lat
    lon = lon if geo_data["GPSLongitudeRef"] == "E" else -lon

    return lat, lon
