
from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2, socket

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    prev_frame_time = 0
    new_frame_time = 0
    while True:
        frame, prev_frame_time = camera.get_frame(prev_frame_time)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6767, debug=True)
