
import cv2
import numpy
import face_recognition

from local_db import local_db
from utils import encode_image
from server import socketio
from shortuuid import ShortUUID
from flask_socketio import join_room
from utils import encode_image


class TakeAttendance: 
    studentData = None
    attendance = False
    def __init__(self):
        self.camera = cv2.VideoCapture(0);
        self.frame = None;
        
    def stream(self):
        frame_count = 0;
        studentName = " Unknown"
        color = (0, 0, 255)
        
        while True:
            success, self.frame = self.camera.read()
            self.frame = cv2.flip(self.frame, 1)
            small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = numpy.ascontiguousarray(self.frame[:, :, ::-1])

            face_locations = face_recognition.face_locations(small_frame)
            if(len(face_locations) == 0):
                studentName = " Unknown"
                color = (0, 0, 255)
            if(self.studentData is not None and len(face_locations) > 0):
                id = ShortUUID().random(length=20)
                isAdded = local_db.addStudent(id, self.studentData["username"], self.studentData["roll_no"])
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                encode_image.dump(face_encodings[0], id)
                cv2.imwrite(f'static/faces/{id}.jpg', self.frame)
                if(isAdded is not False):
                    socketio.emit("clinet", {"type": "user", "user": id})
                self.studentData = None
            
            if(frame_count == 30): 
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                student_id = encode_image.search(face_encodings)
                if(student_id):                    
                    color =  (255, 0, 0)
                    studentData = local_db.getStudent(student_id)
                    studentName = studentData[1]
                    if( local_db.hasAttendance(student_id) is False):
                        if(self.attendance is True):
                            local_db.takeAttendance(student_id)
                            socketio.emit("clinet", {"type": "attendance"})
                            self.attendance =False;
                            color =  (0, 255, 0)
                    else: color =  (0, 255, 0)
                frame_count = 0;
            frame_count += 1
            
            for (top, right, bottom, left) in face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(self.frame , (left, top), (right, bottom), color, 2)
                cv2.rectangle(self.frame , (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(self.frame , studentName, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    
            if not success: break
            else:
                _, buffer = cv2.imencode('.jpg', self.frame )
                frameBuffer = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frameBuffer + b'\r\n')
                       
    def addNewStudent(self, student):
        self.studentData = student
    def takeAttendance(self):
        self.attendance = True
        
@socketio.on('clinet')
def handle_message(data):
    if("type" in data ):
        if(data["type"] == "add"):
            take_attendance.addNewStudent(data)
        elif(data["type"] == "take"):
            take_attendance.takeAttendance()

    
    
@socketio.on('join')
def on_join(connect):
    if(connect is True):
        join_room("clinet")

take_attendance = TakeAttendance();