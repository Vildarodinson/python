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

def create_recordings_folder():
    videos_folder = os.path.join(os.path.expanduser("~"), "Videos")
    recordings_folder = os.path.join(videos_folder, "recordings")
    os.makedirs(recordings_folder, exist_ok=True)
    return recordings_folder

def open_folder_in_explorer(folder):
    if os.name == 'nt':  # if windows
        os.system(f'explorer "{folder}"')
    else:
        print("Opening the folder in file explorer is not supported on this platform.")

def save_video():
    choice = input("Choose an option:\n1. Choose an existing folder\n2. Create a new folder\n")
    
    if choice == '1':
        folder = choose_folder()
    elif choice == '2':
        folder = create_recordings_folder()
    else:
        print("Invalid choice. Exiting.")
        return

    video_capture = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    recording = False
    video_writer = None
    frames = []

    print("Press 'P' to not save the recording.")

    while True:
        ret, frame = video_capture.read()

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        timestamp = f"Date: {date_str} Time: {time_str}"

        if not recording:
            filename = os.path.join(folder, f'{timestamp}.avi')
            video_writer = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
            recording = True
            print("Recording started")

        # displaying date and time
        text = timestamp
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        text_pos = (frame.shape[1] - text_size[0] - 10, 30)

        cv2.putText(frame, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        video_writer.write(frame)
        frames.append(frame.copy())

        cv2.imshow('CCTV', frame)
        cv2.namedWindow('CCTV', cv2.WINDOW_NORMAL)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') and recording:
            print("Recording stopped")
            video_writer.release()
            recording = False

            if frames:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                video_filename = os.path.join(folder, f'{timestamp}_full.avi')
                full_video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))
                for saved_frame in frames:
                    full_video_writer.write(saved_frame)
                full_video_writer.release()
                print(f"Individual recording saved as {filename}")
                print(f"Full recording saved as {video_filename}")
                frames = []

            break 

        if key == ord('p'):
            print("Recording not saved. Exiting.")
            break

    video_capture.release()
    cv2.destroyAllWindows()

save_video()
