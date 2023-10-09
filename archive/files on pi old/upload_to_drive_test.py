import os
import time
#import picamera2
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys


def save_to_drive(source_folder_path, destination_folder_name, destination_folder_id):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    try:
        files_to_upload = source_folder_path + 'I LOVE YOU.jpg'
        # List files in the local folder
        #files_to_upload = os.listdir(source_folder_path)
        
        # Create a new subfolder within the destination folder
        print('creating subfolder')
        subfolder_metadata = {
            'title': destination_folder_name,
            'parents': [{'id': destination_folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        print(f'creating subfolder step 2: {subfolder_metadata}')
        subfolder = drive.CreateFile(subfolder_metadata)
        print('uploading subfolder')
        subfolder.Upload()
        print('finish uploading subfolder')
        
        #for file_name in files_to_upload:
        #    file_path = os.path.join(source_folder_path, file_name)
            
            # Upload each file to the created subfolder on Google Drive
        #    print(f'upload file {file_name} to drive')
        print(f'upload file {files_to_upload} to drive')
        
        file_metadata = {
            'title': 'test.jpg',
            'parents': [{'id': subfolder['id']}]
        }
        print(f'creating file 2: {file_metadata}')
        file = drive.CreateFile(file_metadata)
        print('setting content file')
        file.SetContentFile(files_to_upload)
        print('uploading file')
        file.Upload()
        
        print(f"Uploaded {files_to_upload} to Google Drive")
            
    except Exception as e:
        print(f"An error occurred:  {e}")

if __name__ == "__main__":
    user_name = 'matthew'
    path_to_desktop = '/home/' + user_name + '/Desktop/'
    output_folder = time.strftime('%Y-%m-%d_%H-%M')
    num_images = 4
    interval_seconds = 1
    destination_folder_id='1vJgmXrr0CaPnVdkE1_mYz-zPS6OIY7ii'
    pause_interval = 10
    source_folder_path= path_to_desktop
    output_log = output_folder + '_output_log.txt'

    # Store the original stdout stream
    #original_stdout = sys.stdout
    
    # Call the function to redirect output to a file
    #redirect_output_to_file(output_log)

    #print(f'pause for {pause_interval} seconds to allow wifi connection')
    #wait_for_seconds(pause_interval)

    #print(f'Capturing {num_images} images at {interval_seconds}-second intervals...')
    #capture_images(user_name, output_folder, num_images, interval_seconds)
    #print('Image capture complete.')

    print("uploading files to drive...")
    save_to_drive(source_folder_path,output_folder, destination_folder_id)
    print('Finished')

    # Call the function to restore the original stdout
    #restore_original_stdout()