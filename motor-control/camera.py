import cv2

def get_camera_frame():
    # Initialize camera (default camera 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    ret, frame = cap.read()
    if ret:
        return frame
    else:
        print("Error: Could not read frame.")
        return None

    cap.release()
