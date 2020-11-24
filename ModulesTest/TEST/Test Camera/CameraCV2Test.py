'''
#################################################
                    IMPORTS
#################################################
'''
import numpy as np
import cv2
import signal
import sys
import time

'''
#################################################
            VARIABLES & FUNCTIONS
#################################################
'''
# Flag to notify if the VideoCapture was secured
# Will help in freeing camera if key exeptions are sent
global capSecuredFlag 
capSecuredFlag = False
# Will store frame read from camera
global dslrFrame

def cleanCloseout():
    if capSecuredFlag:
        cap.release()                                       # Release capture
    cv2.destroyAllWindows()                                 # Destroy all of the windows created by OpenCV
    print("Program has been properly terminated")           # Notify
    sys.exit(0)                                             # Exit program

'''
#################################################
            SIGNALS HANDLERS
#################################################
'''
# Custom Exception Class for Alarm Handle
class TimeOutException(Exception):
    pass

# Ctrl+C Signal handler function
def SIGINT_handler(sig,frame):
    print('You pressed Ctrl+C!')
    print('Releasing Camera')
    # Do a clean closeout
    cleanCloseout()
    
# Alarm Handle to raise Exception for timeout purposes
def alarm_handler(sig,frame):
    print("Alarm signal received")
    print("Action is taking too long")
    raise TimeOutException()

# Register signal handlers
signal.signal(signal.SIGINT, SIGINT_handler)        # Signal Handler for (Ctrl + C)
signal.signal(signal.SIGTERM, SIGINT_handler)       # Signal Handler for Software termination signal (sent by kill by default)
signal.signal(signal.SIGALRM, alarm_handler)        # Signal Handler for alarms
print('Ctrl+C or STOP will exit code properly')

'''
#################################################
        INITIALIZE VIDEO CAPTURE
#################################################
'''
print("Initializing Video Capture Device")

# Only try action for 5s if it takes longer then we must be stuck 
# Thus timeout and exit code
signal.alarm(5)
try:
    cap = cv2.VideoCapture(0)
except TimeOutException as ex:
    print(ex)
    print("Unable to get Video Capture, it is recomended that you reboot the device due to potential CSI2 resource being locked!")
    print("Exiting Code")
    cleanCloseout()
# If all went well and code executed within 15s, turn off alarm
signal.alarm(0)

# If video device was captured, check if camera is opened
if cap.isOpened():
    # If opened, print and set the capSecuredFlag flag to true
    print("Video Capture Opened")
    capSecuredFlag = True
else:
    # If not exit the program
    print('Failed to open Video Capture')
    # Release capture device
    cap.release()
    cleanCloseout()

# If video device was captured and opened, reduce the frame size.
# Reducing frame size has helped some people with the select timeout issue(CHECK ERROR_SOLUTION DOCUMENT): 
#   select timeout
#   VIDIOC_DQBUF: Resource temporarily unavailable
# I will reduce it to the lowest frame width
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Then set the format into MJPG in the FourCC format 
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
# Also reduce the buffer to 3, might help, I don't know
cap.set(cv2.CAP_PROP_BUFFERSIZE,1)

'''
#################################################
            READ AND PROCESS FRAMES
#################################################
'''
# Create a window named 'frame' for displaying the video feed
# Allow resizing with cv2.WINDOW_NORMAL or autosizing with cv2.WINDOW_AUTOSIZE
cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)

# While the video capture device is open, capture frame-by-frame
while(cap.isOpened()):
    # Sleep for a little between each loop, might help with errors not sure
    #time.sleep(0.1)
    print("Reading Frame")
    try:
        # Set timeout of 5s
        signal.alarm(15)
        try:
            ret,dslrFrame = cap.read()
        except TimeOutException as ex:
            print("cap.read() took too long")
            print("Releasing Cap device")
            cap.release()
            capSecuredFlag = False
            print("Trying to recapture it(CODE WILL BE EXITED IF IT DOESN'T WORK)")

            # Set timeout of 5s
            signal.alarm(15)
            try:
                cap = cv2.VideoCapture(0)
            except TimeOutException as ex:
                print(ex)
                print("Unable to get Video Capture, it is recomended that you reboot the device due to potential CSI2 resource being locked!")
                print("Exiting Code")
                cleanCloseout()
            # If all went well and code executed within 15s, turn off alarm
            signal.alarm(0)

            # If we got here, Video was captured, so let's check if it's opened
            print("Device Recaptured!!!")
            if cap.isOpened():
                # If opened, print and set the capSecuredFlag flag to true
                print("Video Re-Capture Opened")
                capSecuredFlag = True
            else:
                # If not exit the program
                print('Failed to open Video Re-Capture')
                # Release capture device
                cap.release()
                capSecuredFlag = False
                cleanCloseout()
            
            # If device is opened, try to grab a frame with timeout
            print("Trying to GRAB FRAME")
            signal.alarm(15)
            try:
                ret = cap.grab()
            except TimeOutException as ex:
                print(ex)
                print("Unable to grab frame, weird")
                print("Exiting Code")
                cleanCloseout()
            signal.alarm(0)

            # If frame was grab, check if it was successful
            if ret:
                print("Frame grabbed succesfully, will retrieve it and display")
                ret1, dslrFrame = cap.retrieve()
                if not ret1:
                    print("Unable to retrieve frame, altough it was grabbed! Check what is going on")
                    continue
            else:
                print("Frame grabbed not valid, must be underlying issue somewhere, EXITING CODE")
                cleanCloseout()
                continue

            # If recapture, grabing and retriving was successful
            # Show frame then continue loop
            cv2.imshow('frame',dslrFrame) 
            if cv2.waitKey(1) & 0xFF == ord('q'):           # Press q for quiting
                break
            continue
        
        # If cap.read() was successful in the first place just set the alarm to zero and go on with life
        signal.alarm(0)

        
        # If cap.read() frame is not valid
        if not ret:
            print('DSLR Frame not valid')                   # Print a notification
            if cv2.waitKey(1) & 0xFF == ord('q'):           # Press q for quiting
                break
            continue                                        # Otherwise, just skip this loop and skip to the next one

        # However, if frame is valid
        print("Frame Valid")
        cv2.imshow('frame',dslrFrame)                       # Display the captured image
        if cv2.waitKey(1) & 0xFF == ord('q'):               # Press q for quiting
            break
    
    # If any exceptions were raised whn trying the above, print it
    except Exception as ex:
        print("Exception raised:",ex)

'''
#################################################
            CLOSEOUT PROCEDURE
#################################################
'''
# When everything is done, do a clean closeout
cleanCloseout()
'''
#################################################
#################################################
'''
