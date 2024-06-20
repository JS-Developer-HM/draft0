from local_db import local_db
from take_attendance import take_attendance
from sign_language import sign_language
from flask import render_template, Response
from server import socketio, app
try: 
    
    
    @app.route('/')
    def dashboard():
        return render_template('Dashboard.html')
    
    @app.route('/take_attendance')
    def TakeAttendance():
        return render_template(
            'TakeAttendance.html',
            total_students = len(local_db.students),
            today_students_attendance = local_db.attendance
        )
        
    @app.route('/sign_language') 
    def SignLanguage():
        return render_template(
            'SignLanguage.html',
        )
        
    @app.route('/video_feed')
    def video_feed():
        return Response(take_attendance.stream() , mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/video_feed_2')
    def video_feed_2():
        return Response(sign_language.stream() , mimetype='multipart/x-mixed-replace; boundary=frame')

    
    if __name__ == '__main__': 
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
        
        
except Exception as e:
    print("An Error Occured", e)
    
    
