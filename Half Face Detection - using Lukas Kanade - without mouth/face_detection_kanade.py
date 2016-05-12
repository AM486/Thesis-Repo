import numpy as np
import cv2

#######################
#Half face detection and tracking using Lukas-Kanade 
#algorithm. The cascade tracking is ignored when the
#good points movements are under a threshold value (10pxl).
#Cascade detection is forced when roi box gets distorted
#and when the number of good points are under a threshold (15 points)
#######################


cap = cv2.VideoCapture('060627NETED2100.avi')
#cap = cv2.VideoCapture('news.mp4')

#cap = cv2.VideoCapture(0)
#cap.set( 4, 640)
#cap.set( 3, 480)

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.01,
                       minDistance = 5,
                       blockSize = 5 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (10,10),
                  maxLevel = 20,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors

def detect(old_frame,faces):
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        old_gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20),
        flags = cv2.CASCADE_SCALE_IMAGE 
    )
    if len(faces)==0:
        return [],[],[],[]
    f_temp=faces
    points=[]
    r_gray=[]
    r_color=[]
    coords=[]
    if len(faces)>0:
        ##reduces overlaping faces
        for i in range (len(faces)):
            (x0, y0, w0, h0) = faces[i] 
            for k in range (len(faces)):
                (x1, y1, w1, h1) = faces[k] 
                if x1>x0 and y1>y0 and x1+w1<x0+w0 and h1+h1<y0+h0:                    
                    f_temp = np.delete(f_temp, (k), axis=0)
        faces=f_temp
        
        (x, y, w, h) = faces[0]        
        roi_gray = old_gray[y:y+h, x:x+w]
        roi_color=old_frame[y:y+h, x:x+w]
        points.append( cv2.goodFeaturesToTrack(roi_gray, mask = None, **feature_params))
        r_gray=[roi_gray]
        r_color=[roi_color]
        coords=[ (x, y, w, h) ]

    for (x, y, w, h) in faces:
        cv2.rectangle(old_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  
        roi_gray=old_gray[y:y+h, x:x+w]
        roi_color=old_frame[y:y+h, x:x+w]

        p=cv2.goodFeaturesToTrack(roi_gray, mask = None, **feature_params)
        if not np.in1d(p,points).all():            
            points.append(p)
            r_gray.append( roi_gray )
            r_color.append( roi_color)
            coords.append( (x, y, w, h) )
        # Create a mask image for drawing purposes
             
    cv2.imshow('old_frame',old_frame)

    return r_gray,points,faces,coords
    
    
frameNo=0    
faces=()
while len(faces) ==0:          
    ret, old_frame = cap.read() 
    frameNo+=1
    print frameNo,'retrack-init'          
    r_oldgray,points,faces,coords=detect(old_frame,faces)
#    print len(faces)

mask = np.zeros_like(old_frame)  
p0=np.asarray(points)
x_=0
y_=0 
w_=0            
h_=0
while(1):
    ret,frame = cap.read()
    
    if frame is None:
        print 'EOF'
        break;    
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameNo+=1

    if len(points)==0:
        print frameNo,'retrack-points'    
        faces=()      
        r_oldgray,points,faces,coords=detect(frame,faces)
        mask = np.zeros_like(frame)  
        p0=np.asarray(points) 
#        print '-',len(faces)
    else:
        for i in range(len(points)):        
            if i>=len(coords):
                print frameNo,'retrack-coords'    
                faces=()      
                r_oldgray,points,faces,coords=detect(frame,faces)
                mask = np.zeros_like(frame)  
                p0=np.asarray(points) 
                break        
                                            

            (x, y, w, h)=coords[i]   
#            cv2.rectangle(frame, (x, y), (w+x, h+y), (0, 0, 255), 2)  

            roi_gray=frame_gray[y:y+h, x:x+w]
            p0 =   points[i]
            # calculate optical flow
            p1, st, err = cv2.calcOpticalFlowPyrLK(r_oldgray[i], roi_gray,p0 , None, **lk_params)               
            
    
            # Select good points
            good_new = p1[st==1]
            good_old = p0[st==1]
            
            if good_new.size>0 and good_old.size>0:
                x_new=int(min(good_new[:,0]))
                y_new=int(min(good_new[:,1])) 
                
                x_old=int(min(good_old[:,0]))
                y_old=int(min(good_old[:,1]))    
    
                thresh=10
                  
                if abs(x_new-x_old)<thresh and abs(y_new-y_old)<thresh:#ignore changes for less than <thresh> pixels          
                    x_=int(min(good_old[:,0])+x-10)
                    y_=int(min(good_old[:,1])+y-10)    
                    w_=int(max(good_old[:,0])+x+10)            
                    h_=int(max(good_old[:,1])+y+10)  
                else:
                    x_=int(min(good_new[:,0])+x-10)
                    y_=int(min(good_new[:,1])+y-10)    
                    w_=int(max(good_new[:,0])+x+10)            
                    h_=int(max(good_new[:,1])+y+10)
                    
     
    
                if  good_new.size<15:
                    print frameNo,'retrack-improve'
                    faces=()      
                    r_oldgray,points,faces,coords=detect(frame,faces)
                    mask = np.zeros_like(frame)  
                    p0=np.asarray(points) 
    #                print '-',len(faces)
                    if len(faces)==0:
                        break
                    
        
                else:       
                    
                   
                    if w_<x+w or h_<y+h:
                        print frameNo,'retrack-improve2'
                        faces=()      
                        r_oldgray,points,faces,coords=detect(frame,faces)
                        mask = np.zeros_like(old_frame)  
                        p0=np.asarray(points) 
                        if len(faces)==0:
                            break                        
    
                    cv2.rectangle(frame, (x_, y_), (w_, h_), (0, 255, 0), 2)  
                    cv2.rectangle(frame, (x_, y_-(y_-h_)/2), (w_, h_), (255, 255, 0), 2)  
                    font = cv2.FONT_HERSHEY_PLAIN
    
                    cv2.putText(frame,str((x_, y_-(y_-h_)/2)), (x_-2, y_-(y_-h_)/2-4), font, .8,  (255, 255, 255),1)
            else:
                print 'else!!!!'
                faces=()      
                r_oldgray,points,faces,coords=detect(frame,faces)
                mask = np.zeros_like(frame)  
                p0=np.asarray(points) 
                 
                break


#                if w_>x+w:
#                    if h_>y+h:                
#                        cv2.rectangle(frame, (x_, y_), (w_, h_), (0, 255, 0), 2)  
#                    else:
#                        cv2.rectangle(frame, (x_, y_), (w_, y+h), (0, 255, 0), 2) 
#                else:
#                    if h_>y+h:                
#                        cv2.rectangle(frame, (x_, y_), (w+x, h_), (0, 255, 0), 2)  
#                    else:
#                        cv2.rectangle(frame, (x_, y_), (w+x, h+y), (0, 255, 0), 2) 
#    
            
            # draw the tracks
            for i,(new,old) in enumerate(zip(good_new,good_old)):
                a,b = new.ravel()+(x,y)
                a,b=(int(a),int(b))     
                frame = cv2.circle(frame,(a,b),2,(0,0,255),-1)
    
    img = cv2.add(frame,mask)

    cv2.imshow('frame',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

#     Now update the previous frame and previous points
#    old_gray = frame_gray.copy()
#    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()