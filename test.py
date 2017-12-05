__author__ = "Eddie Hurtado"

import cv2
import numpy as np
import pypylon.pylon as PYLON

cameras = []

try:
    # get the devices connected
    devices = PYLON.TlFactory.GetInstance().EnumerateDevices()
    print("Detected devices: " + str(len(devices)))

    if len(devices) > 0:
        for deviceInfo in devices:
            # create an instant camera object with the camera devices founded
            device = PYLON.TlFactory.GetInstance().CreateDevice(deviceInfo)
            camera = PYLON.InstantCamera(device)

            # print the model name of the camera
            print("Using device: "+camera.GetDeviceInfo().GetModelName())

            # open the camera before accessing any parameters
            camera.Open()

            # if you're using more than one camera (with a switch or router to one port ethenet card) 
            # you have to set the acquisition frame rate of the cameras that bandwidth can support
            camera.AcquisitionFrameRateEnable.SetValue(True)
            camera.AcquisitionFrameRateAbs.SetValue(25.0)

            #start grabbing
            camera.StartGrabbing(PYLON.GrabStrategy_LatestImageOnly)

            cameras.append(camera)

        # create a pylon ImageFormatConverter object
        formatConverter = PYLON.ImageFormatConverter()
        # specify the output pixel format
        formatConverter.OutputPixelFormat.SetValue(PYLON.PixelType_BGR8packed)
        
        while True: # you can use camera.IsGrabbing() for validation
            i = 1
            for camera in cameras:
                # wait for an image and then retrieve it. 5000ms timeout used.
                grabResult = camera.RetrieveResult(5000, PYLON.TimeoutHandling_ThrowException)
                # image grabbed successfully?
                if grabResult.GrabSucceeded():
                    # get dimentions of grabbed buffer
                    rows = grabResult.GetHeight()
                    cols = grabResult.GetWidth()

                    # convert grabbed buffer to pylon image
                    pylonImage = formatConverter.Convert(grabResult)
                    
                    # create OpenCV image from pylon image
                    cvImage = np.frombuffer(pylonImage.GetBuffer(), np.uint8).reshape(rows, cols, 3)
                    # resize frame (optional)
                    resized = cv2.resize(cvImage, (700, 500))

                    # show frame
                    cv2.imshow('frame {}'.format(i), resized)
                    i = i + 1
            
            # wait for 'q' key to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # closing cameras
        for camera in cameras:
            camera.Close()

        # close windows
        cv2.destroyAllWindows()
    
    print("Exit.")

except Exception as e:
    print(e)
    for camera in cameras:
        if camera.IsOpen():
            camera.Close()
    
    print("Exit.")

