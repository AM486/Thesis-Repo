##### Face - Mouth Detection
==============
I am using Python and OpenCV 3.1.0. I added some code in order to export the detected face and mouth coordinates per frame in a text file. The exported file notation is acoording to the following pattern:

<span>#{frame_index}</span><span><face{face_index}=x:{xface1}-{xface2},y:{yface1}-{yface2}></span><mouth=x:{xmouth1}-{xmouth2},y:{ymouth1}-{ymouth2}>

ex:
#1212<face(0)=x:117-220,y:79-182><mouth=x:153-183,y:158-177>
#1212<face(1)=x:391-521,y:86-216><mouth=x:429-487,y:167-207> 

