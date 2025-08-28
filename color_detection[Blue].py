import cv2
import numpy as np

# A function to find the largest contour in a mask.
def find_largest_contour(mask):
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # If no contours are found, return None
    if not contours:
        return None, None
        
    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Calculate the center of the bounding box
    center_x = x + w // 2
    center_y = y + h // 2
    
    return largest_contour, (center_x, center_y)

# Set the HSV color range for blue.
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

# Initialize the camera. Use the correct device index if it's not 0.
# The `ls /dev/video*` command can help confirm this.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

while True:
    # Read a frame from the video stream.
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame from BGR to HSV color space.
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # In your main loop, change the mask creation to use the blue ranges.
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # Find the largest contour and its center in the green mask.
    largest_contour, center = find_largest_contour(blue_mask)

    if largest_contour is not None and cv2.contourArea(largest_contour) > 500: # Filter out small noise
        # Draw a bounding box around the detected object
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Draw a circle at the center of the object
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
        # Display the coordinates of the center point
        cv2.putText(frame, f'({center[0]}, {center[1]})', (center[0] + 10, center[1] + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # Print coordinates to the terminal (useful for further automation)
        print(f"Blue object detected at: ({center[0]}, {center[1]})")

    # Display the original frame with detection overlays.
    cv2.imshow('Color Detection', frame)
    
    # Display the mask for debugging purposes (optional)
    cv2.imshow('Mask', blue_mask)

    # Break the loop if the 'q' key is pressed.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all windows.
cap.release()
cv2.destroyAllWindows()
