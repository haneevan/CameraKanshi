import cv2
import numpy as np

# A function to find the largest contour in a mask.
def find_largest_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None
    
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    center_x = x + w // 2
    center_y = y + h // 2
    
    return largest_contour, (center_x, center_y)

# Define the HSV ranges and properties for each color.
# The 'red' color needs two ranges and a single mask.
colors_to_detect = [
    {
        'name': 'red',
        'lower_ranges': [np.array([0, 50, 50]), np.array([160, 50, 50])],
        'upper_ranges': [np.array([10, 255, 255]), np.array([179, 255, 255])],
        'color_bgr': (0, 0, 255)  # BGR for drawing the rectangle and text
    },
    {
        'name': 'green',
        'lower_ranges': [np.array([40, 50, 50])],
        'upper_ranges': [np.array([80, 255, 255])],
        'color_bgr': (0, 255, 0)
    },
    {
        'name': 'blue',
        'lower_ranges': [np.array([90, 50, 50])],
        'upper_ranges': [np.array([130, 255, 255])],
        'color_bgr': (255, 0, 0)
    }
]

# Initialize the camera.
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Process each color in the list
    for color in colors_to_detect:
        masks = []
        for i in range(len(color['lower_ranges'])):
            mask = cv2.inRange(hsv_frame, color['lower_ranges'][i], color['upper_ranges'][i])
            masks.append(mask)
        
        # Combine masks if there are more than one (for red)
        final_mask = masks[0]
        if len(masks) > 1:
            for i in range(1, len(masks)):
                final_mask = cv2.add(final_mask, masks[i])

        # Find the largest contour in the final mask
        largest_contour, center = find_largest_contour(final_mask)

        # Draw on the original frame if a significant contour is found
        if largest_contour is not None and cv2.contourArea(largest_contour) > 500:
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color['color_bgr'], 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1) # Black dot for visibility

            # Add text label above the rectangle
            cv2.putText(frame, color['name'], (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color['color_bgr'], 2)

    # Display the final frame
    cv2.imshow('Multi-Color Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
