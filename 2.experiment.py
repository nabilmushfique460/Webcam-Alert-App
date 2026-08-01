import cv2
import time
import numpy as np

video = cv2.VideoCapture(0)
# Increased sleep time to let the webcam auto-focus/auto-exposure adjust
time.sleep(2)

first_frame = None

while True:
    check, frame = video.read()

    if not check:
        print("Error: Could not read from webcam.")
        break

    # Failsafe: Check if the camera is physically blocked or returning pitch black
    if frame.max() == 0:
        print("Warning: The camera frame is completely black!")

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau
        print("Captured background frame. Now looking for motion...")
        continue

    # Calculate difference
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Thresholding: Any difference > 30 becomes stark white (255), everything else black (0)
    # This makes motion incredibly obvious on screen.
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Print the amount of motion instead of the raw pixel array
    motion_pixels = cv2.countNonZero(thresh_frame)
    if motion_pixels > 0:
        print(f"Motion detected! {motion_pixels} pixels changed.")

    # Show three windows so you can debug visually
    cv2.imshow("1. Normal Camera", frame)
    cv2.imshow("2. Raw Difference (Delta)", delta_frame)
    cv2.imshow("3. Amplified Motion (Threshold)", thresh_frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()