
import Tkinter as tk
from ttk import Style
import cv2
import thread

recording=True
face= False
mouth=False

class Application(tk.Frame):    
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.initUI()

    def initUI(self):
        self.master.title("Face Recognition")
        self.style = Style()
        self.style.theme_use("default")     
        self.pack(fill=tk.BOTH, expand=True)   

        rightFrame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        rightFrame.pack(fill=tk.BOTH, expand=True)
        rightFrame["width"]=150
        rightFrame["height"]=100
        rightFrame["bg"]="green"
        
        def toggleFace():            
            global face
            if face==True:
                face=False
                faceButton.config(fg="red")    
                
            else:
                face=True
                faceButton.config(fg="green")   
            print "Face Recognition ",face 
        
        
        def toggleMouth():
            global mouth
            if mouth==True:
                mouth=False
                mouthButton.config(fg="red")    
                
            else:
                mouth=True
                mouthButton.config(fg="green")   
            print "Mouth Recognition ",mouth             
            
            
        faceButton = tk.Button(rightFrame, text="Face", fg="red", command=toggleFace)
        faceButton.grid(row=0, column=0,   padx=5, pady=15 ,ipadx=50, sticky='' )
        mouthButton = tk.Button(rightFrame, text="Mouth", fg="red", command=toggleMouth)
        mouthButton.grid(row=1, column=0,   padx=5, pady=5, ipadx=45 , sticky='' )  
        
        stopButton = tk.Button(self, text="Stop",command=self.stopCapture)
        stopButton.pack(side=tk.RIGHT,  padx=5,)
        startButton = tk.Button(self, text="Capture", command=self.initCapture)
        startButton.pack(side=tk.RIGHT,   pady=5)
   
 
    def initCapture(self):
#        print "Yo!"
        def runCapture (  ):        
            cap = cv2.VideoCapture(0)
            cap.set( 4, 640)
            cap.set( 3, 480) 
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            mouthCascade = cv2.CascadeClassifier("haarcascade_mouth_default.xml")

            global recording
#            print recording
            recording=True
            while(recording):
                ret, frame = cap.read()
                if face==True                :
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags = cv2.CASCADE_SCALE_IMAGE 
                    )
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+h, y+w), (0, 255, 0), 2)
                
                if mouth==True                :
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    mouths = mouthCascade.detectMultiScale(
                        gray,
                        scaleFactor=1.5,
                        minNeighbors=10,
                        minSize=(20, 20),
                        flags = cv2.CASCADE_SCALE_IMAGE
                    )
                    for (x, y, w, h) in mouths:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
         
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        try:
            thread.start_new_thread(runCapture, ( ) )
        except:
            print "Error: unable to start thread"  
            
    def stopCapture(self):
        print "Stop!" 
        global recording
        recording=False
    
    
        
root = tk.Tk()
root.geometry("150x150+300+250")
app = Application(master=root)
app.mainloop()