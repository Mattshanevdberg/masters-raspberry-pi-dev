from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def save_to_drive(credentials_file, source_folder_path, destination_folder_name, destination_folder_id):
    # Authenticate using the provided credentials file
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_file)
    if gauth.credentials is None:
        # Authenticate and save credentials to file
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(credentials_file)

    # Create a GoogleDrive instance
    drive = GoogleDrive(gauth)

    try:
        # List files in the local folder
        files_to_upload = os.listdir(source_folder_path)
        
        # Create a new subfolder within the destination folder
        subfolder_metadata = {
            'title': destination_folder_name,
            'parents': [{'id': destination_folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        subfolder = drive.CreateFile(subfolder_metadata)
        subfolder.Upload()

        for file_name in files_to_upload:
            file_path = os.path.join(source_folder_path, file_name)
            
            # Upload each file to the created subfolder on Google Drive
            file_metadata = {
                'title': file_name,
                'parents': [{'id': subfolder['id']}]
            }
            file = drive.CreateFile(file_metadata)
            file.SetContentFile(file_path)
            file.Upload()
            
            print(f"Uploaded {file_name} to Google Drive")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function with the appropriate inputs
save_to_drive(
    credentials_file='/home/matthew/Desktop/Master_Dev/raspberry-pi/client_secrets.json',
    source_folder_path='/home/matthew/Desktop/Masters-data/test-folder-upload',
    destination_folder_name='Replace-this-name',
    destination_folder_id='1G-z207hJR-SXPbNAC3MDIW3THT-F-STa'
)

