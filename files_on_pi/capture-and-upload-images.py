import os
import time
import picamera
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys

def capture_images(user_name, output_folder, num_images, interval_seconds):
    # Create the output folder on the desktop if it doesn't exist
    desktop_path = f'/home/{user_name}/Desktop/{output_folder}'
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)
    
    # Initialize the camera
    with picamera.PiCamera() as camera:
        for i in range(num_images):
            # Get the current time for naming the image
            current_time = time.strftime('%Y-%m-%d_%H-%M')
            
            # Capture an image
            image_path = os.path.join(desktop_path, f'image_{current_time}_{i + 1:03d}.jpg')
            camera.capture(image_path)
            
            print(f'Captured image: {image_path}')
            
            # Wait for the specified interval
            time.sleep(interval_seconds)

def save_to_drive(source_folder_path, destination_folder_name, destination_folder_id):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    try:
        # List files in the local folder
        files_to_upload = os.listdir(source_folder_path)
        
        # Create a new subfolder within the destination folder
        print('creating subfolder')
        subfolder_metadata = {
            'title': destination_folder_name,
            'parents': [{'id': destination_folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        print(f'creating subfolder 2: {subfolder_metadata}')
        subfolder = drive.CreateFile(subfolder_metadata)
        print('uploading subfolder')
        subfolder.Upload()
        print('finish uploading subfolder')
        
        for file_name in files_to_upload:
            file_path = os.path.join(source_folder_path, file_name)
            
            # Upload each file to the created subfolder on Google Drive
            print(f'upload file {file_name} to drive')
            file_metadata = {
                'title': file_name,
                'parents': [{'id': subfolder['id']}]
            }
            print(f'creating file 2: {file_metadata}')
            file = drive.CreateFile(file_metadata)
            print('setting content file')
            file.SetContentFile(file_path)
            print('uploading file')
            file.Upload()
            
            print(f"Uploaded {file_name} to Google Drive")
            
    except Exception as e:
        print(f"An error occurred:  {e}")

def wait_for_seconds(seconds):
    time.sleep(seconds)

def redirect_output_to_file(file_path):
    global original_stdout
    sys.stdout = open(file_path, 'w')  # Redirect stdout to the file

def restore_original_stdout():
    global original_stdout
    sys.stdout.close() #close the file
    sys.stdout = original_stdout  # Restore the original stdout

if __name__ == "__main__":
    user_name = 'mattvdb'
    path_to_desktop = '/home/' + user_name + '/Desktop/'
    output_folder = time.strftime('%Y-%m-%d_%H-%M')
    num_images = 4
    interval_seconds = 1
    destination_folder_id='1G-z207hJR-SXPbNAC3MDIW3THT-F-STa'
    pause_interval = 10
    source_folder_path= path_to_desktop+output_folder
    output_log = output_folder + '_output_log.txt'

    # Store the original stdout stream
    original_stdout = sys.stdout
    
    # Call the function to redirect output to a file
    redirect_output_to_file(output_log)

    print(f'pause for {pause_interval} seconds to allow wifi connection')
    wait_for_seconds(pause_interval)

    print(f'Capturing {num_images} images at {interval_seconds}-second intervals...')
    capture_images(output_folder, num_images, interval_seconds)
    print('Image capture complete.')

    print("uploading files to drive...")
    save_to_drive(source_folder_path,output_folder, destination_folder_id)
    print('Finished')

    # Call the function to restore the original stdout
    restore_original_stdout()