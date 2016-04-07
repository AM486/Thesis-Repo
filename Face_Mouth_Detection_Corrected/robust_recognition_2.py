import cv2
import numpy as np




# Create the haar cascade
cap = cv2.VideoCapture("news.mp4")
#cap = cv2.VideoCapture(0)
#
#cap.set( 4, 640)
#cap.set( 3, 480)

#  throw "Error when reading image file";
if not cap.isOpened():  
    print "File not opened"

mouthCascade = cv2.CascadeClassifier("haarcascade_mouth_default.xml")
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

mouth_detect=False
face_detect=True

(xx,yy,ww,hh)=(None,None,None,None)
print xx,yy,ww,hh

while(True):
    ret, frame = cap.read()

    if frame is None:
        print 'EOF'
        break;
 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 # Detect face in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE 
    )  
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+h, y+w), (0, 255, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w] 
        
 #mouth detection  
        mouths = mouthCascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=2,
            minSize=(2, 2),
            flags = cv2.CASCADE_SCALE_IMAGE )
        if len(mouths)>0:
            print mouths
            print np.max(mouths, axis=1)
            ym_max=np.max(mouths, axis=1)         
            print 'ym_max',ym_max, np.max(ym_max)
            
   
        if len(mouths)>0:
            for (xm, ym, wm, hm) in mouths:   
                
#                print np.mean(mouths, axis=0)
                if ym>h/2:            
                    cv2.rectangle(roi_color, (xm, ym), (xm+wm, ym+hm), (0, 255, 255), 2) 
                    (xx,yy,ww,hh)=(xm,ym,xm+wm,ym+hm)
                else:
                   if(xx,yy,ww,hh) != (None,None,None,None):
                        cv2.rectangle(roi_color, (xx, yy), (ww, hh), (0, 255, 255), 2)    


    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print "Found {0} faces!".format(len(faces))
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()