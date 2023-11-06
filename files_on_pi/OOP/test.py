'''
from owntime import Timer
import time

inte = 25

output = 1/inte

time_ = Timer()

print (output)
print(time.time())
time_.sleep(output)
print(time.tiem())
'''
import drive
from owntime import Timer
access_token_timer = Timer()

drive_auth = drive.DriveAuth('matthew', access_token_timer)

drive_upload = drive.DriveUpload('matthew', drive_auth, access_token_timer)
#print(drive_auth.retrieve_refresh_token)
#drive_upload.collect_folder_paths_to_upload()
#drive_upload.delete_folders()
#drive_upload.upload_folders_to_drive()
#drive.request_device_authorization()
print(drive_upload.check_for_low_memory())