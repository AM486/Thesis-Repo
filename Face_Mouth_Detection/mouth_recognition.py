import cv2


# Get user supplied values
#imagePath = sys.argv[1]
#cascPath = sys.argv[2]

# Create the haar cascade
cap = cv2.VideoCapture(0)
cap.set( 4, 640)
cap.set( 3, 480)

faceCascade = cv2.CascadeClassifier("haarcascade_mouth_default.xml")
while(True):
    ret, frame = cap.read()
# Read the image
#image = cv2.imread("abba.png")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(20, 20),
        flags = cv2.CASCADE_SCALE_IMAGE 
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print "Found {0} faces!".format(len(faces))
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()