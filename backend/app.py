import cv2
import numpy as np
from flask import Flask, request, jsonify , send_file , send_from_directory
import os
from flask_cors import CORS , cross_origin

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def detect_cars(image_path):
    # Load YOLO
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]  

    # Load image
    img = cv2.imread(image_path)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 2:  # Car class ID in YOLO
                # Object detected as a car
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-maximum suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes
    colors = np.random.uniform(0, 255, size=(len(class_ids), 3))
    total_cars = 0
    for i in range(len(boxes)):
        if i in indexes:
            total_cars += 1
            x, y, w, h = boxes[i]
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    
    # Draw total count
    cv2.putText(img, f'Total Cars: {total_cars}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Save the image with bounding boxes and total count
    result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + os.path.basename(image_path))
    cv2.imwrite(result_image_path, img)

    return result_image_path










@app.route('/upload', methods=['POST'])
@cross_origin(supports_credentials=True)
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Detect cars and draw bounding boxes
        result_image_path = detect_cars(file_path)
 
        return send_file(result_image_path, as_attachment=True)

    



if __name__ == '__main__':
    app.run(host='0.0.0.0')

