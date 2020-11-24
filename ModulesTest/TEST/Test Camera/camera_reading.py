#Be careful!!!! Start preview only works if the raspberry pi is attached to a monitor
#It doesn't work over VNC
from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.start_preview()
sleep(20)
camera.stop_preview()