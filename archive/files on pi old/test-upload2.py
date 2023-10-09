from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth('/home/matthew/Desktop/Master_Dev/raspberry-pi/settings.yaml')
drive = GoogleDrive(gauth)


file1 = drive.CreateFile({'title': 'Hello2.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Hello World!') # Set content of the file from given string.
file1.Upload()