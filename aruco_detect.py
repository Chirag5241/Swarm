import numpy as np
import cv2
import cv2.aruco as aruco
#import math
 
 
cap = cv2.VideoCapture(1)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))

id_cent = np.zeros((20,3))
 
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cap.set(3,620)
    cap.set(4,480)
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
 
    #print(parameters)
 
    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    #print(ids)
    
    if len(corners)!=0:

        for i in range(len(ids)):

            for j in range(4):
                #print(ids[i][0])
                x = corners[i][0][j][0]
                y = corners[i][0][j][1]
                #print(x,y) 
                cx = (int)(abs(corners[i][0][0][0] + corners[i][0][2][0]) / 2.0)
                cy = (int)(abs(corners[i][0][0][1] + corners[i][0][2][1]) / 2.0)

                id_cent[i][0] = ids[i][0]
                id_cent[i][1] = cx
                id_cent[i][2] = cy

                cx1 = (int)(abs(corners[i][0][2][0] + corners[i][0][3][0]) / 2.0)
                cy1 = (int)(abs(corners[i][0][2][1] + corners[i][0][3][1]) / 2.0)

                cx2 = (int)(abs(corners[i][0][0][0] + corners[i][0][3][0]) / 2.0)
                cy2 = (int)(abs(corners[i][0][0][1] + corners[i][0][3][1]) / 2.0)

                cv2.line(frame, (cx, cy), (cx1, cy1), (0, 0, 255), 2)
                cv2.line(frame, (cx, cy), (cx2, cy2), (0, 255, 0), 2)

                #cv2.drawMarker(frame, (x,y), (0, 255, 0), cv2.MARKER_STAR, markerSize=4, thickness=4, line_type=cv2.LINE_AA)
                #cv2.drawMarker(frame, (cx,cy), (200, 0, 255), cv2.MARKER_STAR, markerSize=4, thickness=4, line_type=cv2.LINE_AA)

            
 
    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs

    aruco.drawDetectedMarkers(frame, corners, ids)

    for i in range(20):
        if id_cent[i][0] != 0:
            print(id_cent[i])
 
    #print(rejectedImgPoints)
    # Display the resulting frame
    #cv2.imshow('frame',gray)
    cv2.imshow('frame1',frame)

    for i in range(20):
        id_cent[i][0] = 0

    #out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()