from screeninfo import get_monitors  # Added for getting screen size
from utils import read_license_plate
from sort.sort import *
import cv2
from ultralytics import YOLO
import time  # Added for controlling frame rate

# Dictionary containing all information
results = {}

# Object tracker
mot_tracker = Sort()

# Load models
license_plate_detector = YOLO('model/best.pt')

# Load video
# camera = cv2.VideoCapture(0)
# video = './videos/teste.mp4'
url = 'http://192.168.1.9:8080/video'
cap = cv2.VideoCapture(url)

# start_time = 254
# start_time_ms = start_time * 1000
# cap.set(cv2.CAP_PROP_POS_MSEC, start_time_ms)

# Get screen size and calculate 30% dimensions
monitor = get_monitors()[0]  # Assumes primary monitor
screen_width = monitor.width
screen_height = monitor.height
window_width = int(screen_width * 0.3)
window_height = int(screen_height * 0.3)

# Vehicles that should be included in detection
# auto, bike, bus, car, lcv, minivan, pickup, tractor, truck, multi-axle truck
vehicles = [1, 2, 3, 4, 6, 7, 8, 10, 12, 13]

# Create resizable window
cv2.namedWindow('Vehicle and License Plate Detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Vehicle and License Plate Detection',
                 window_width, window_height)


# Configure framerate
one_second = 1
framerate = 20
fps = one_second / framerate

# Read frames until video is over
frame_nmr = -1
ret = True
validcounter = 0
while ret:
    frame_nmr += 1
    ret, frame = cap.read()

    if ret:
        # Initialize for every frame to process the entire video
        results[frame_nmr] = {}

        # Detect license plates
        license_plates = license_plate_detector(frame, verbose=False)[0]

        # List of [x1, y1, x2, y2, score, class_id]
        detections = license_plates.boxes.data.tolist()

        if detections:
            # Select plate with highest score
            best_plate = max(detections, key=lambda x: x[4])
            x1, y1, x2, y2, score, class_id = best_plate

            # Draw bounding box for license plate (red for license plates)
            cv2.rectangle(frame, (int(x1), int(y1)),
                          (int(x2), int(y2)), (0, 0, 255), 2)
            cv2.putText(frame, f'License Plate', (int(x1), int(
                y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Crop license plate
            license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2), :]

            # Try to remove Irish county text by cutting off top part of plate
            h, w, _ = license_plate_crop.shape
            top_cut_ratio = 0.25
            cut_y = int(h * top_cut_ratio)
            license_plate_crop = license_plate_crop[cut_y:h, 0:w]
            # cv2.imshow("Cropped", license_plate_crop)
            # cv2.waitKey(1)

            # Process license plate
            license_plate_crop_thresh = cv2.cvtColor(
                license_plate_crop, cv2.COLOR_BGR2GRAY)

            # Apply bilateral filter to reduce noise while preserving edges (helps distinguish shapes)
            # license_plate_crop_filtered = cv2.bilateralFilter(
            #     license_plate_crop_gray, 9, 75, 75)

            # Sharpen the image to enhance character edges (useful for distinguishing O from D)
            # kernel_sharpen = np.array(
            #     [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            # license_plate_crop_sharp = cv2.filter2D(
            #     license_plate_crop_gray, -1, kernel_sharpen)
            #
            # license_plate_crop_thresh = cv2.adaptiveThreshold(
            #     # 11 - 2 balanceado 13 - 2 bastante no começo pouco d
            #     license_plate_crop_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 13, 1)

            cv2.imshow('final', license_plate_crop_thresh)
            cv2.waitKey(1)
            # Read license plate number
            license_plate_text, license_plate_text_score = read_license_plate(
                license_plate_crop_thresh)

            # Calculate text size for centering
            text_size = cv2.getTextSize(
                license_plate_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            # Center horizontally
            text_x = int((x1 + x2) / 2 - text_size[0] / 2)
            # Place below the box (10px offset + text height)
            text_y = int(y2) + 10 + text_size[1]
            cv2.putText(frame, license_plate_text, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            validplates = ['08-D-27995', '181-D-49808',
                           '192-D-4208', '142-D-24686', '202-D-20242', '96-D-37901', '05-WX-4145', '00-KK-442']

            if license_plate_text in validplates:
                validcounter += 1
                print("------------------------------------------------------------")
                print("| Found a valid license plate: ",
                      license_plate_text, " |")
                print("|                                                          |")
                print("|                                                          |")
                print("|                                                          |")
                print("|                                                          |")
                print("|                                                          |")
                print("|                                                          |")
                print("|                                                          |")
                print("|                                                          |")
                print("|                                                          |")
                print("-----------------------------------")
                print("Valid counter: ", validcounter)

            if license_plate_text:
                print('Detected plate: ', license_plate_text)

        # Display the frame with bounding boxes (moved outside if detections to show regardless)
        cv2.imshow('Vehicle and License Plate Detection', frame)
        cv2.waitKey(1)

        # Sleep for 1 second to achieve 1 frame per second processing
        time.sleep(fps)

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()

# Write results
# write_csv(results, "./test.csv")
