
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, url_for,request,flash,make_response,make_response
import urllib.request, urllib.parse
from forms import *
import csv
from flask_migrate import Migrate


app=Flask(__name__)
app.config['SECRET_KEY']= 'ADKADKFJ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
migrate= Migrate(app, db)

# created a telegram bot for all the call in forms. 
def sendtelegram(params):
    url = "https://api.telegram.org/bot5738222395:AAEM5NwDAN1Zc052xI_i9-YlrVnvmSkN9p4/sendMessage?chat_id=-633441737&text=" + urllib.parse.quote(params)
    content = urllib.request.urlopen(url).read()
    print(content)
    return content

#TABLE CLASS DEFINITION FOR BOTH CENTRALMAL AND TRIPGHANA.
class Course(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String())
        comment = db.Column(db.String())
        def __repr__(self):
            return f"Course('{self.id}', {self.email}', {self.comment}')"

class Tripghana(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String())
    password = db.Column(db.String())
    username= db.Column(db.String())
    def __repr__(self):
        return f"Course('{self.id}', {self.email}', {self.comment}')"

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
  

class Src(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    srcname = db.Column(db.String())
    name = db.Column(db.String())
    srcnumb= db.Column(db.String())
    Hoodie =db.Column(db.String())
    sweat =db.Column(db.String())
    bag =db.Column(db.String())
    shirt =db.Column(db.String())
    
    def __repr__(self):
        return f"Src('{self.id}', {self.srcnumb}', {self.name}')"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    def __repr__(self):
        return f"Item('{self.id}', {self.name}')"

class Central(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String())
    def __repr__(self):
        return f"Central('{self.id}', {self.phone}')"
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewname= db.Column(db.String())
    review= db.Column(db.String())
    def __repr__(self):
        return f"Review('{self.id}', {self.reviewname},{self.review}')"
#END OF TBLE CLASS. 
   
   
#    src ussd
    
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
#another ussd
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

#end of ussd
#ROUTES AVAILABLE FOR ALL THE NEEDED HTML DOCUMENTS. 
@app.route('/ent',methods=['GET','POST'])
def homee():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('ent.html')
    return render_template('ent.html')

@app.route('/base',methods=['GET','POST'])
def base():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('base.html')
    return render_template('base.html')

@app.route('/',methods=['GET','POST'])
def centralmall():
    form = Add()
    if request.method=='POST':
        print(form.phone.data)
        src=Central(phone=form.phone.data)
        db.session.add(src)
        db.session.commit
        print(src.phone)
        sendtelegram("FREE AIRTIME" + '\n' + 
                      "Phone Number= " + src.phone
        )
        flash(src.phone +" " + "Congratulations, you just won airtime.","success")
        return redirect("/menu")
    return render_template('about.html')


class Length:
    """
    Validates the length of a string.

    :param min:
        The minimum required length of the string. If not provided, minimum
        length will not be checked.
    :param max:
        The maximum length of the string. If not provided, maximum length
        will not be checked.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated using `%(min)d` and `%(max)d` if desired. Useful defaults
        are provided depending on the existence of min and max.

    When supported, sets the `minlength` and `maxlength` attributes on widgets.
    """

    def __init__(self, min=-1, max=-1, message=None):
        assert (
            min != -1 or max != -1
        ), "At least one of `min` or `max` must be specified."
        assert max == -1 or min <= max, "`min` cannot be more than `max`."
        self.min = min
        self.max = max
        self.message = message
        self.field_flags = {}
        if self.min != -1:
            self.field_flags["minlength"] = self.min
        if self.max != -1:
            self.field_flags["maxlength"] = self.max

    def __call__(self, form, field):
        length = field.data and len(field.data) or 0
        if length >= self.min and (self.max == -1 or length <= self.max):
            return

        if self.message is not None:
            message = self.message

        elif self.max == -1:
            message = field.ngettext(
                "Field must be at least %(min)d character long.",
                "Field must be at least %(min)d characters long.",
                self.min,
            )
        elif self.min == -1:
            message = field.ngettext(
                "Field cannot be longer than %(max)d character.",
                "Field cannot be longer than %(max)d characters.",
                self.max,
            )
        elif self.min == self.max:
            message = field.ngettext(
                "Field must be exactly %(max)d character long.",
                "Field must be exactly %(max)d characters long.",
                self.max,
            )
        else:
            message = field.gettext(
                "Field must be between %(min)d and %(max)d characters long."
            )

        raise ValidationError(message % dict(min=self.min, max=self.max, length=length))





@app.route('/shop',methods=['GET','POST'])
def shop():
    form = SRCC()
    if request.method=='POST':
        print(form.sweat.data)
        print(form.shirt.data)
        print(form.name.data)
        print(form.srcname.data)
        print(form.Hoodie.data)
        print(form.srcnumb.data)
        print(form.bag.data)
        src=Src(srcname=form.srcname.data,
                shirt=form.shirt.data,
                srcnumb=form.srcnumb.data,
                name=form.name.data,
                Hoodie=form.Hoodie.data,
                sweat=form.sweat.data,
              bag=form.bag.data)
        db.session.add(src)
        db.session.commit
        print(src.sweat)
        print(src.shirt)
        print(src.srcnumb)
        print(src.srcname)
        print(src.Hoodie)
        print(src.sweat)
        print(src.name)
        sendtelegram("SRC POP-UP STORE ORDER:" + '\n' + 
                      "Name = " + src.srcname  + '\n' + 
                      "Number = " + src.srcnumb  + '\n' + 
                      "Hostel = " + src.name  + '\n' + 
                      "Qty Hoodie = " + src.Hoodie  + '\n' + 
                      "Qty Bag = " + src.bag  + '\n' + 
                    "Qty Shirt = " + src.shirt  + '\n' + 
                    "Qty Sweat Shirt = " + src.sweat)
        flash("Order Confirmed, Delivery is in the next 5 minutes","success")
        return redirect("/centralmal")
    persons=Src.query.order_by(Src.id.desc()).all()
    print(persons)
    return render_template('shop.html',persons=persons)

@app.route('/centralmal',methods=['GET','POST'])
def centralmal():
    form = SRCC()
    if request.method=='POST':
        print(form.name.data)
        print(form.srcname.data)
        print(form.srcnumb.data)
        src=Src(srcname=form.srcname.data,
                srcnumb=form.srcnumb.data,
                name=form.name.data,
              )
        db.session.add(src)
        db.session.commit()
        print(src.srcnumb)
        print(src.srcname)
        print(src.name)
        sendtelegram("REQUEST ITEM" + '\n' + 
                      "Name = " + src.srcname  + '\n' + 
                      "Number = " + src.srcnumb  + '\n' + 
                      "Item = " + src.name       
        )
        flash("We are currently restocking, Our team will call you in a minute.","success")
        return redirect("/centralmal")
    return render_template('centralmal.html')


@app.route('/kalitexcreatives',methods=['GET','POST'])
def kalitexcreatives():
    return render_template('kalitexcreativs.html')



@app.route('/trail')
def trial():
    return render_template('trail.html')

@app.route('/lydia',methods=['GET','POST'])
def lydia():
    form = SRCC()
    if request.method=='POST':
        print(form.sweat.data)
        print(form.name.data)
        print(form.srcname.data)
        print(form.srcnumb.data)
        src=Src(srcname=form.srcname.data,
                srcnumb=form.srcnumb.data,
                name=form.name.data,
                sweat=form.sweat.data,
              )
        db.session.add(src)
        db.session.commit()
        print(src.sweat)
        print(src.srcnumb)
        print(src.srcname)
        print(src.name)
        sendtelegram("LYNAF CENTRAL ORDER:" + '\n' + 
                      "Name = " + src.srcname  + '\n' + 
                      "Number = " + src.srcnumb  + '\n' + 
                      "Hostel = " + src.name  + '\n' + 
                    "Quantity Bodycon= " + src.sweat)
        flash("We will call you in a minute to confirm your order, Preoder ID:CM2840201#.","success")
        return redirect("/centralmal")
    return render_template('lydia.html')


@app.route('/vendor1',methods=['GET','POST'])
def vendor1():
    if request.method=='POST':
        return render_template('vendor1.html')
    return render_template('vendor1.html')


@app.route('/menu',methods=['GET','POST'])
def menu():
    return render_template('menu.html')
    
    
@app.route('/product',methods=['GET','POST'])
def product():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('product.html')
    return render_template('product.html')

@app.route('/contact1',methods=['GET','POST'])
def contact1():
    if request.method=='POST':
        return render_template('contact1.html')
    return render_template('contact1.html')

@app.route('/about')
def about():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('head.html')
    return render_template('head.html')

@app.route('/event')
def event():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('photo.html')
    return render_template('photo.html')

@app.route('/four')
def four():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('phone.html')
    return render_template('phone.html')

@app.route('/review',methods=['GET','POST'])
def review():
    form = Reviewcomment()
    if request.method=='POST':
        print(form.reviewname.data)
        print(form.review.data)
        src=Review(reviewname=form.reviewname.data,
                review=form.review.data)
        db.session.add(src)
        db.session.commit()        
        print(src.reviewname)
        print(src.review)
        sendtelegram("REVIEWS" + '\n' + 
                      "Name = " + src.reviewname  + '\n' + 
                      "Review = " + src.review)
        return redirect("/review")
    return render_template('happy.html')

@app.route('/search',methods=['GET','POST'])
def search():
    form = SRCC()
    if request.method=='POST':
        print(form.name.data)
        print(form.srcname.data)
        print(form.srcnumb.data)
        src=Src(srcname=form.srcname.data,  
                srcnumb=form.srcnumb.data,
                name=form.name.data,)
        db.session.add(src)
        db.session.commit()
        print(src.sweat)
        print(src.srcnumb)
        print(src.srcname)
        print(src.name)
        sendtelegram("REQUEST ITEM" + '\n' + 
                      "Name = " + src.srcname  + '\n' + 
                      "Number = " + src.srcnumb  + '\n' + 
                      "Item = " + src.name)
        flash("We will call you in a minute, search ID:CM0111#.","success")
        return redirect("/search")
    return render_template('search.html')

@app.route('/blog')
def blog():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('blog.html')
    return render_template('blog.html')

@app.route('/security')
def outteam():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('debit.html')
    return render_template('debit.html')


''''
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    name=Course.query.get_or_404(id)
    form = RegistrationForm()
    form.username.data=name.name
    if request.method=='POST':
        print(form.username.data)
        print(form.password.data)
        namelogin=  se(name=form.username.data)
        db.session.add(namelogin)
        db.session.commit()
        # Handle POST Request here
        return redirect(url_for('six'))
    return render_template('signup.html', form=form)
'''

@app.route('/heads')
def heads():
    return render_template("heads.html")

@app.route('/delivery')
def delivery():
    return render_template("delivery.html")



@app.route('/login', methods=["POST","GET"])
def login():
    form = Login()
    print ('try')
    print(form.email.data)
    print(form.password.data)
    if form.validate_on_submit():
        print("form Validated successfully")
        user = Tripghana.query.filter_by(email = form.email.data).first()
        print("user:" + user.email + "found")
        print(user.password)
        if user and form.password.data == user.password:
            print(user.email + "validored successfully")
            if user == None:
                flash(f"There was a problem")   
            #login_user(user)
            flash (f' ' + user.email + ',Welcome Admin ' ,'success')
            return redirect(url_for('/home'))
            # next = request.args.get('next')
        else:
            flash (f'Wrong Password ', 'success')
    return render_template("login.html")

@app.route('/sign', methods=["POST","GET"])
def sign():
    form = Account()
    print(form.password.data)
    print(form.email.data)
    print(form.username.data)
    if request.method=='POST':
        if form.validate_on_submit():
            namelogin=Tripghana(email=form.email.data,password=form.password.data,username=form.data)
            db.session.add(namelogin)
            db.session.commit()
            # login_user(user, remember=True)
            # print(current_user)
            flash("Welcome" + " " + namelogin.username)
            return redirect(url_for('/login'))
        else:
            print(form.errors)
    return render_template("sign.html",form=form)


@app.route('/signinn' , methods=["POST","GET"])
def signinn():
    return render_template("signinn.html")


@app.route('/budget', methods=['POST', 'GET'])
def index2():
    form = First()
    if request.method=='POST':
        print(form.name.data)
        newentry=Item(name=form.name.data)
        db.session.add(newentry)
        db.session.commit()
        print(newentry.name)
        flash("Welcome  to Mytripghana" + " " + newentry.name + " " + "Take a trip with us.","success")
        return redirect("/home")
    return render_template("index2.html", form=form)

@app.route('/additem')
def additem():
    return render_template("additem.html")


@app.route('/form')
def form():
    return render_template("form.html")
  
@app.route('/welcome' , methods=['POST', 'GET'])
def welcome():
    form = First()
    if request.method=='POST':
        print(form.name.data)
        newentry=Item(name=form.name.data)
        db.session.add(newentry)
        db.session.commit()
        print("successful")
        return redirect("/home")
    return render_template("welcome.html", form=form)
   

@app.route('/home', methods=['POST','GET'])
def home():
    form = RegistrationForm()
    if request.method=='POST':
        print(form.email.data)
        print(form.comment.data)
        newentry=Course(email=form.email.data, comment=form.comment.data)
        db.session.add(newentry)
        db.session.commit()
        print(newentry.email)
        print(newentry.comment)
        flash("We appreciate your feedback.")
        return redirect("/home")
    return render_template("venue.html", form=form)

@app.route("/delete/<int:id>")
def delete(id):
        delete=Course.query.get_or_404(id)
        try:
            db.session.delete(delete)
            db.session.commit()
            return redirect('/comment') 
        except: 
            return "errrrrorrr"
    
 
@app.route('/hotel')
def hotel():
    return render_template('hotel.html')


@app.route('/restaurant')
def restaurant():
    return render_template('rest.html')


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(host='0.0.0.0',port=3000,debug=True)
