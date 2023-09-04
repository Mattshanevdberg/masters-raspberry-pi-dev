import os
import time
import picamera

def capture_images(output_folder, num_images, interval_seconds):
    # Create the output folder on the desktop if it doesn't exist
    desktop_path = f'/home/mattvdb/Desktop/{output_folder}'
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

if __name__ == "__main__":
    output_folder = time.strftime('%Y-%m-%d_%H-%M')
    num_images = 20
    interval_seconds = 1
    
    print(f'Capturing {num_images} images at {interval_seconds}-second intervals...')
    capture_images(output_folder, num_images, interval_seconds)
    print('Image capture complete.')

