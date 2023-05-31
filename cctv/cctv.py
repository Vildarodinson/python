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
    choice = input("Choose an option:\n1. Use an existing folder\n2. Create a new folder\n")
    if choice == '1':
        folder = choose_folder()
    else:
        folder = os.path.join(os.path.expanduser("~"), "Videos", "recordings")
        os.makedirs(folder, exist_ok=True)

    video_capture = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    while True:
        video_writer = None

        while video_capture.isOpened():
            ret, frame = video_capture.read()

            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            timestamp = f"Date: {date_str} Time: {time_str}"

            if video_writer is None:
                filename = os.path.join(folder, f'{timestamp}.avi')
                video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

            text = timestamp
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            text_pos = (frame.shape[1] - text_size[0] - 10, frame.shape[0] - 10)

            cv2.putText(frame, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

            video_writer.write(frame)

            cv2.imshow('CCTV', frame)
            cv2.namedWindow('CCTV', cv2.WINDOW_NORMAL)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('1'):
                break

            now = datetime.now()  # Update the current time

        if video_writer is not None:
            video_writer.release()

        if key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

save_video()
