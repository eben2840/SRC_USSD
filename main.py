from flask import Flask,redirect,url_for,render_template,request,make_response
import csv
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


db = SQLAlchemy(app)

class Studenthalls(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    studentName= db.Column(db.String() )
    regno= db.Column(db.String() )
    gender= db.Column(db.String() )
    program= db.Column(db.String() )
    level= db.Column(db.String()  )
    email= db.Column(db.String()  )
    hallname= db.Column(db.String()  )
    def __repr__(self):
        return f"Studenthalls('{self.id}', {self.studentName}', {self.regno})"
  
    
    
@app.route("/readcsv",)
def readcsv():
    with open('Studenthalls.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        studentbody=[]
        for line in csv_reader:
            studentName=line["StudentName"]
            regno=line["regno"]
            gender=line["gender"]
            program=line["program"]
            level=line["LEVEL"]
            email=line["email"]
            hallname=line['hallname']
            newStudent = Studenthalls(studentName=studentName, regno=regno, gender=gender,
                                      program=program, level=level, email=email,hallname=hallname)
            
            try:
                db.session.add(newStudent)
                db.session.commit()
            except Exception as e:
                print(e)
            
            print(newStudent.id)
            print(newStudent.studentName)
            
            student={
                "studentname":studentName,
                "regno":regno,
                "gender":gender,
                "program":program,
                "level":level,
                "email":email,
                "hallname":hallname
            }
            studentbody.append(student)
            
            # write to db
            
    return studentbody

@app.route("/findbyid")
def findbyid():
    print("input")
    input=request.args.get('id')
    print(input)
    student=Studenthalls.query.filter_by(regno=input).first()   
    print(student) 
    
    if student == None:
        return make_response("no results found", 404)
    student={
        "studentname":student.studentName,
        "regno":student.regno,
        "gender":student.gender,
        "program":student.program,
        "level":student.level,
        "email":student.email,
        "hallname":student.hallname
    }
    
    return student



if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(host='0.0.0.0', port=5000,debug=True)