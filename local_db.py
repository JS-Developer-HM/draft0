import glob
import datetime
from connection import db;
from shortuuid import ShortUUID

class LocalDB:
    def __init__(self):
        try: 
            print("Starting")
            db.create(f"""
                CREATE TABLE IF NOT EXISTS Students (
                ID VARCHAR(30) NOT NULL,
                name VARCHAR(30),
                roll_no INT,
                date DATETIME,
                PRIMARY KEY (ID)
            )""")
            db.create(f"""
                CREATE TABLE IF NOT EXISTS Attendance (
                ID VARCHAR(30) NOT NULL,
                studentID VARCHAR(30),
                date DATETIME,
                PRIMARY KEY (ID)
            )""") 
            db.create(f"""
                CREATE TABLE IF NOT EXISTS Signs ( 
                ID VARCHAR(30) NOT NULL,
                studentID VARCHAR(30),
                type INT, 
                date DATETIME, 
                PRIMARY KEY (ID)
            )""")
            self.students = db.read(f"SELECT * FROM Students")
            self.attendance = db.read(f"""
                SELECT Attendance.StudentID, Students.Name, Students.Roll_NO, Students.Date FROM attendance
                INNER JOIN Students ON Attendance.StudentID=Students.ID
                WHERE DATE(Attendance.Date) = current_date();
            """)
            self.totalDections = glob.glob('./static/*.pkl');
        except Exception as e:
            print(e)
        finally: print("SQL Table Created Successfully") 
        
    def addStudent(self, id, name, roll):
        try:
            db.insert(f"INSERT INTO Students values (%s, %s, %s, CURRENT_TIMESTAMP())", (id, name, roll))
            self.students.append((id, name, roll, datetime.datetime.now()))
        except Exception as e:
            print(e)
            return False
    
    def getStudent(self, studentId):
        for student in self.students:
            if student[0] == studentId:
                return student
        return False
        
    def takeAttendance(self, studentId):
        student = self.getStudent(studentId);
        if student:
            id = ShortUUID().random(length=20)
            db.insert(f"INSERT INTO Attendance values (%s, %s, CURRENT_TIMESTAMP())", (id, studentId))
            self.attendance.append((student[0], student[1], student[2], datetime.datetime.now()))
            
    def hasAttendance(self, studentId):
        for student in self.attendance:
            if student[0] == studentId:
                return True
        return False

    def getAttendance(self):
        return self.attendance
        
            
local_db = LocalDB();