import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from object_detection.utils import label_map_util

class PanelDetector:
    def __init__(self):
        # Load the TensorFlow model and label map
        self.detect_fn = tf.saved_model.load("D:\\tarek\\YoloPvDetect\\app\\model\\saved_model")
        self.category_index = label_map_util.create_category_index_from_labelmap(
            "D:\\tarek\\YoloPvDetect\\app\\model\\labelmap.pbtxt", use_display_name=True)

    def load_image_into_numpy_array(self, path):
        # Load image into numpy array
        image = Image.open(path).convert('RGB')
        return np.array(image)

    def run_detection_and_return_image(self, image_path):
        # Convert image to numpy array
        image_np = self.load_image_into_numpy_array(image_path)

        # Run TensorFlow detection
        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]
        detections = self.detect_fn(input_tensor)

        # Post-process detections
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        # Filter detections based on score and size
        valid_boxes = []
        valid_scores = []
        valid_classes = []
        for i, box in enumerate(detections['detection_boxes']):
            ymin, xmin, ymax, xmax = box
            width = (xmax - xmin) * image_np.shape[1]
            height = (ymax - ymin) * image_np.shape[0]
            if detections['detection_scores'][i] >= 0.95 and height > 51 and width > 31:
                valid_boxes.append(box)
                valid_scores.append(detections['detection_scores'][i])
                valid_classes.append(detections['detection_classes'][i])

        # Count the saved bounding boxes
        saved_count = len(valid_boxes)

        # Visualize only the valid detection results using OpenCV
        image_np_with_detections = image_np.copy()
        for i, box in enumerate(valid_boxes):
            class_id = valid_classes[i]
            score = valid_scores[i]
            display_str = f"{self.category_index[class_id]['name']}: {int(score * 100)}%"
            ymin, xmin, ymax, xmax = box
            (left, right, top, bottom) = (xmin * image_np.shape[1], xmax * image_np.shape[1],
                                          ymin * image_np.shape[0], ymax * image_np.shape[0])
            cv2.rectangle(image_np_with_detections, (int(left), int(top)), (int(right), int(bottom)), (64, 224, 208), 2)

        return image_np_with_detections, saved_count
