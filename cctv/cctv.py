import cv2
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def choose_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path

def save_video():
    # Prompt user to choose folder
    choice = input("Choose an option:\n1. Use an existing folder\n2. Create a new folder\n")
    if choice == '1':
        folder = choose_folder()
    else:
        folder = os.path.join(os.path.expanduser("~"), "Videos", "recordings")
        os.makedirs(folder, exist_ok=True)

    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Set up video capture
    video_capture = cv2.VideoCapture(0)  # Change the index to use a different webcam

    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filename = os.path.join(folder, f'{timestamp}.avi')
    video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    # Start recording
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        # Write the frame to the video file
        video_writer.write(frame)
        # Display the frame
        cv2.imshow('CCTV', frame)
        cv2.namedWindow('CCTV', cv2.WINDOW_NORMAL)
        # Stop recording when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the video capture and writer
    video_capture.release()
    video_writer.release()

    # Close all windows
    cv2.destroyAllWindows()

# Run the program
save_video()
