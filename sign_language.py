import cv2
import numpy
import face_recognition

from local_db import local_db
from utils import encode_image
from server import socketio
from shortuuid import ShortUUID
from utils import encode_image
import mediapipe as mp


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
tipIds = [4, 8, 12, 16, 20]

class SignLanguage: 
    feedback = None
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
            results = hands.process(self.frame)
            lmList = []


            face_locations = face_recognition.face_locations(small_frame)
            if(len(face_locations) == 0):
                studentName = " Unknown"
                color = (0, 0, 255)
            else:
                if results.multi_hand_landmarks:
                    for handLms in results.multi_hand_landmarks:
                        for id, lm in enumerate(handLms.landmark):
                            h, w, _ = self.frame.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            lmList.append([id, cx, cy])
                        mpDraw.draw_landmarks(self.frame, handLms, mpHands.HAND_CONNECTIONS)
        
                        if len(lmList) == 21:
                            fingers = []
                            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
        
                            for tip in range(1, 5):
                                if lmList[tipIds[tip]][2] < lmList[tipIds[tip] - 2][2]:
                                    fingers.append(1)
                                else:
                                    fingers.append(0)
                            totalFingers = fingers.count(1)
                            feedback = ["Bad", "Not bad", "Okay", "Good", "Perfect"][totalFingers - 1]
        

            
            if(frame_count == 30): 
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                student_id = encode_image.search(face_encodings)
                if(student_id):                    
                    color =  (255, 0, 0)
                    studentData = local_db.getStudent(student_id)
                    studentName = studentData[1]

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
                    
                    
sign_language = SignLanguage()