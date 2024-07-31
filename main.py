"""
Watchdog Script for Monitoring Directory Changes

This script uses the watchdog library to monitor a specified directory for file creation events.
When a file is created in the monitored directory, it logs the event to the console.

Classes:
    MyFileHandler -- Handles file system events.
    
Functions:
    main -- Sets up the observer and starts monitoring the directory.
"""

import time
import pydicom
import numpy as np
import cv2  # OpenCV library for image processing
import os

from pydicom.uid import generate_uid
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler


MY_INPUT_PATH = os.path.join(os.getcwd(), "INPUT")  # Your INPUT folder path
MY_OUTPUT_PATH = os.path.join(os.getcwd(), "INPUT") # Your OUTPUT folder path

def check_dicom(file_path):
    """Check if the file is a valid DICOM file."""
    try:
        ds = pydicom.dcmread(file_path)
        return True, ds
    except:
        return False, None


def modify_descriptions(ds):
    """Append 'AI' to study description and series description."""
    if 'StudyDescription' in ds:
        ds.StudyDescription += " SeenByAI"
    else:
         ds.StudyDescription = "StudySeenByAI"

    if 'SeriesDescription' in ds:
        ds.SeriesDescription += "SeenByAI"
    else:
        ds.StudyDescription = "SeriesSeenByAI"

    if 'StudyInstanceUID' in ds:
        ds.StudyInstanceUID += ".1"
    if 'SeriesInstanceUID' in ds:
        ds.SeriesInstanceUID += ".1"
    return ds

def add_text_to_image(ds, text="seen by AI"):
    """Add text to the DICOM image."""
    # Extract pixel data
    pixel_array = ds.pixel_array
    # Convert to an OpenCV image
    image = np.copy(pixel_array)
    
    if len(image.shape) == 3 and image.shape[0] == 1:  # For grayscale images with shape (1, H, W)
        image = image[0]

    # Define the position and font for the text
    MAX_LENGTH = np.max(image.shape)
    position = (MAX_LENGTH//2-40, MAX_LENGTH//2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # White color
    thickness = 2

    # Add text to the image
    image_with_text = cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

    # Update the pixel data in the DICOM dataset
    ds.PixelData = image_with_text.tobytes()
    return ds

def process_dicom(input_file, output_file):
    check, ds = check_dicom(input_file)

    if check:
        try:
            ds = modify_descriptions(ds)
            ds = add_text_to_image(ds)

            basename = os.path.basename(output_file)
            os.makedirs(output_file.replace(basename,""), exist_ok=True)

            ds.save_as(output_file)
            print(f"File saved to {output_file}")
        except:
             print("The provided file is not a valid DICOM file to modify.")

    else:
        print("The provided file is not a valid DICOM file.")

class MyFileHandler(FileSystemEventHandler):
    """
    Custom event handler for handling file system events.
    
    Methods:
        on_created(event) -- Logs file creation events.
    """
    
    # Comment the following method to log modified file events.
    def on_modified(self, event):
        """
        Called when a file or directory is modified.
        Logs the modified file path to the console.
        
        Parameters:
            event (FileSystemEvent) -- The event object containing event information.
        """
        if not event.is_directory:
            print(f'Modified file: {event.src_path}')
            process_dicom(event.src_path, event.src_path.replace("INPUT", "OUTPUT"))
    
    def on_created(self, event):
        """
        Called when a file or directory is created.
        Logs the created file path to the console.
        
        Parameters:
            event (FileSystemEvent) -- The event object containing event information.
        """
        if not event.is_directory:
            print(f'Created file: {event.src_path}')
            process_dicom(event.src_path, event.src_path.replace("INPUT", "OUTPUT"))

    
    # Uncomment the following method to log deleted file events.
    # def on_deleted(self, event):
    #     """
    #     Called when a file or directory is deleted.
    #     Logs the deleted file path to the console.
    #     
    #     Parameters:
    #         event (FileSystemEvent) -- The event object containing event information.
    #     """
    #     if not event.is_directory:
    #         print(f'Deleted file: {event.src_path}')



def main():
    """
    Main function to set up the observer and start monitoring the directory.
    
    This function sets up the event handler, observer, and starts the observer to monitor the specified directory
    for file creation events. It keeps the observer running until interrupted.
    """
    event_handler = MyFileHandler()
    observer = PollingObserver(timeout=1)
    observer.schedule(event_handler, MY_INPUT_PATH, recursive=True)
    observer.start()
    
    print("SERVICE IS RUNNING ...")
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
