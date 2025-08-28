1. Checking the camera availability from raspberry pi with code
    >lsusb
2. doing it first before connecting the camera, then run the code again when connecting camera
3. check if any device connected 
4. after getting the device list, next are checking the device index with code
    >ls /dev/video*
5. will get a /dev/video list, and that's means it worked
6. next were installing the opencv camera
   >-running on virtual environment so we can install it
   >-move the directiory terminal to the targeted folder
   >-using cd /home/*target folder*
   >-run pip install opencv-python
    
