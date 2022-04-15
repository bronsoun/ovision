import cv2
import time
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.7

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FPS, 10)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self,prev_frame_time):

        success, image = self.video.read()
        #x = self.video.get(cv2.CAP_PROP_FPS)

        fps, prev_frame_time = self.get_fps(prev_frame_time)

        cv2.putText(image, fps, (70, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3, cv2.LINE_AA)
        #print(x)
        image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(),prev_frame_time

    def get_fps(self, prev_frame_time):
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)
        fps = 'fps:' + str(fps)

        return fps, prev_frame_time



