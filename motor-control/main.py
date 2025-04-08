import time
import camera
import motor_controller
import tape_detection
import numpy as np
import cv2

def process_frame():
    # Capture a frame
    frame = camera.get_camera_frame()
    if frame is None:
        return None

    # Detect blue and yellow tape
    blue_contours, yellow_contours = tape_detection.detect_tapes(frame)

    # Calculate centroids of the contours
    blue_centroid = None
    yellow_centroid = None

    # Process blue tape contours
    if len(blue_contours) > 0:
        blue_c = max(blue_contours, key=cv2.contourArea)
        M = cv2.moments(blue_c)
        if M["m00"] != 0:
            blue_centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # Process yellow tape contours
    if len(yellow_contours) > 0:
        yellow_c = max(yellow_contours, key=cv2.contourArea)
        M = cv2.moments(yellow_c)
        if M["m00"] != 0:
            yellow_centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    return blue_centroid, yellow_centroid

def adjust_movement(blue_centroid, yellow_centroid):
    if blue_centroid and yellow_centroid:
        # Calculate the horizontal position of the tape center
        mid_point = (blue_centroid[0] + yellow_centroid[0]) // 2

        # Get the image width (assuming the frame is of constant size)
        frame_width = 640  # Assuming a 640x480 resolution

        # Set speed levels
        stop_threshold = frame_width // 3
        move_threshold = 2 * (frame_width // 3)

        if mid_point < stop_threshold:
            # Move left (forward with some correction speed)
            motor_controller.move_forward(70)
        elif mid_point > move_threshold:
            # Move right (forward with some correction speed)
            motor_controller.move_forward(70)
        else:
            # Stay centered
            motor_controller.stop_motors()

def main():
    try:
        while True:
            blue_centroid, yellow_centroid = process_frame()
            if blue_centroid and yellow_centroid:
                adjust_movement(blue_centroid, yellow_centroid)
            else:
                motor_controller.stop_motors()  # Stop if no tape is detected

            time.sleep(0.1)

    except KeyboardInterrupt:
        motor_controller.cleanup()

if __name__ == "__main__":
    main()
