import cv2
import numpy as np
import time

print("""
     Your cloak is loading....
     hide from your webcam for the first 5 seconds, as it needs to capture the background (without you in it) 
""")

# Initialize webcam
video = cv2.VideoCapture(0)
time.sleep(3)

# Capture static background frame
bg_frame = 0
for _ in range(30):
    success, bg_frame = video.read()

# Flip background for mirror view
bg_frame = np.flip(bg_frame, axis=1)

while video.isOpened():
    success, frame = video.read()
    if not success:
        break

    # Flip the frame horizontally (mirror effect)
    frame = np.flip(frame, axis=1)

    # Convert BGR image to HSV color space
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Slightly smoothen the image
    blurred_hsv = cv2.GaussianBlur(hsv_img, (35, 35), 0)

    # Lower red hue range, you can swap out the colour, this is set to red
    red_lower_1 = np.array([0, 120, 70])
    red_upper_1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv_img, red_lower_1, red_upper_1)

    # Upper red hue range
    red_lower_2 = np.array([170, 120, 70])
    red_upper_2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv_img, red_lower_2, red_upper_2)

    # Combine both red masks
    full_mask = mask_red1 + mask_red2

    # Clean up noise from the mask
    full_mask = cv2.morphologyEx(
        full_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Replace detected red areas with background
    frame[np.where(full_mask == 255)] = bg_frame[np.where(full_mask == 255)]

    # Show the final output
    cv2.imshow('Magic Window', frame)

    # Break loop if ESC key is pressed
    if cv2.waitKey(10) == 27:
        break
