import cv2
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the cascade
face_cascade_path = os.path.join(current_dir, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Define the colors
yellow = (0, 255, 255)
green = (0, 255, 0)

# Capture video from the default camera
cap = cv2.VideoCapture(1)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If the frame was not retrieved properly, break the loop
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Get the dimensions of the frame
    height, width = frame.shape[:2]
    
    # Calculate the positions of the lines
    center_x = width // 2
    left_x = width // 4
    right_x = 3 * width // 4
    center_y = height //2 
    top_y = height // 5
    bottom_y = 4 * height // 5

    # Draw the lines on the frame
    cv2.line(frame, (center_x, 0), (center_x, height), (0, 255, 0), 2)
    cv2.line(frame, (left_x, 0), (left_x, height), (0, 255, 255), 2)
    cv2.line(frame, (right_x, 0), (right_x, height), (0, 255, 255), 2)
    cv2.line(frame, (0, center_y), (width, center_y), (0, 255, 0), 2)
    cv2.line(frame, (0, top_y), (width, top_y), (0, 255, 255), 2)
    cv2.line(frame, (0, bottom_y), (width, bottom_y), (0, 255, 255), 2)
    
    # Detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Check if the face is touching the lines
        if y + h >= bottom_y:
            print("Bottom")
        elif y <= top_y:
            print("Top")
        elif x + w >= right_x:
            print("Right")
        elif x <= left_x:
            print("Left")
        else:
            print("OK")
    
    # Display the resulting frame
    cv2.imshow('Face Detection with Lines', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()