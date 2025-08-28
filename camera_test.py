import cv2

# Replace '0' with the number from your 'ls /dev/video*' output, if it's different.
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Error: Could not open video device.")
else:
    print("Camera is available! A live preview window should appear.")
    while True:
        ret, frame = video_capture.read()
        if ret:
            cv2.imshow('Camera Test', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_capture.release()
cv2.destroyAllWindows()
