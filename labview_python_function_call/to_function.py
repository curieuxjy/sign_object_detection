import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import time
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

# function 1 call 1 result
# everytime call the camera
def start():
    
    PATH_TO_CKPT = "D:/GitHub/traffic_sign_object_detection/fine_tuned_model/ssd_1st/frozen_inference_graph.pb"
    PATH_TO_LABELS = "D:/GitHub/traffic_sign_object_detection/data/annotations/label_map.pbtxt"

    NUM_CLASSES = 5

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    detection_graph = tf.Graph()
    
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    video = cv2.VideoCapture(0) # 0:web_cam 1:logitech
    ret = video.set(3,720)
    ret = video.set(4,720)

    a_dict = {"bicycle": 1, "child":2, "const":3, "bump":2, "cross":4, "":0}

    result_list = []

    for i in range(5):

        ret, frame = video.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)

        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})
        disp_name = vis_util.visualize_boxes_and_labels_on_image_array(
            frame,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.6
            )
       
        disp_name = disp_name.split(":")[0]
       
        result = a_dict[disp_name]
        result_list.append(result)

    num_1 = result_list.count(1)
    num_2 = result_list.count(2)
    num_3 = result_list.count(3)
    num_4 = result_list.count(4)

    return_last = 0
    if num_1 >= 3:
        return_last = 1
    elif num_2 >= 3:
        return_last = 2
    elif num_3 >= 3:
        return_last = 3
    elif num_4 >= 3:
        return_last = 4

    # if you want to change to string
    # activate this code
    # return_last = str(return_last)

    return return_last

if __name__=="__main__":
    start()