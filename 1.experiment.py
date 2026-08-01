import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)  # Gives the webcam a second to adjust exposure

first_frame = None

while True:
    check, frame = video.read()

    # If the camera fails to read the frame, break the loop
    if not check:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Capture the background frame and skip the rest of the loop
    if first_frame is None:
        first_frame = gray_frame_gau
        continue  # THIS IS THE FIX

    # Now this will only run from the 2nd frame onwards
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # Optional: Print max difference to prove motion is being detected
    # print("Highest pixel difference:", delta_frame.max())

    cv2.imshow("My video", delta_frame)

    print(delta_frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()  # Good practice to close the window properly