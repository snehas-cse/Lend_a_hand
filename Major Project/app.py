import base64
from flask import *
from flask_mysqldb import MySQL
from datetime import datetime
# from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vetrivel@14'
app.config['MYSQL_DB'] = 'lendahand'
app.secret_key = "kenshin"  

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hrithikdas2nd@gmail.com'
app.config['MAIL_PASSWORD'] = 'xnkermlbeodmkwcz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)
# mail.init_app(app)


mysql=MySQL(app)
 

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/userhome")
def userhome():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from event where status=(%s)",['ongoing'])

        # Commit to DB
    ongoingevents = cur.fetchall()
    cur.execute("select * from event where status=(%s)",['upcoming'])
    upcomingevents = cur.fetchall()
    mysql.connection.commit()
    print(ongoingevents,upcomingevents)
        # Close 
    cur.close()
    return render_template("userhome.html",ongoingevents=ongoingevents,upcomingevents=upcomingevents)

@app.route("/activeeventpage")
def activeEventPage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from rough")

        # Commit to DB
    result = cur.fetchall()

    mysql.connection.commit()

        # Close connection
    cur.close()
    print(result)
    return render_template("activeEventpage.html",nums=result)

@app.route("/organisereventpage")
def organiserEventPage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from rough")

        # Commit to DB
    result = cur.fetchall()

    mysql.connection.commit()

        # Close connection
    cur.close()
    print(result)
    return render_template("organisereventpage.html",nums=result)


@app.route("/rough")
def rough():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from rough")

        # Commit to DB
    result = cur.fetchall()

    mysql.connection.commit()

        # Close connection
    cur.close()
    return render_template("rough.html",nums=result)

@app.route("/volunteersignup", methods = ["GET","POST"])
def volunteersignup():
    print(request.data)
    # name = request.form['name']
    # email = request.form['email']
    # password = request.form['password']
    # phonenumber = request.form['phonenumber']
    # role = 'volunteer'
    # cur = mysql.connection.cursor()

    #     # Execute query
    # cur.execute("INSERT INTO users(name,email,password,phonenumber,role) VALUES(%s,%s,%s,%s,%s)",[name],[email],[password],[phonenumber],[role])

    # mysql.connection.commit()

    #     # Close connection
    # cur.close()

    return render_template("volunteersignup.html")


@app.route("/organisersignup")
def organisersignup():
    return render_template("organisersignup.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/organiserhomepage")
def organiserhomepage():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from completed_event_table")
    events = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template("organiserhomepage.html",events=events)

@app.route("/addevent")
def addevent():
    return render_template("add_event.html")

@app.route("/organiserprofile")
def organiserProfile():
    print(session)
    if 'email' in session:
        email = session['email']
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("select * from users where email=(%s)",[email])
        user = cur.fetchall()
        cur.execute("select count(*) from event where email=(%s) and status='completed'",[email])
        count = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    
        return render_template("organiserprofile.html",user=user,count=count)
    return render_template("organiserprofile.html")

@app.route("/savevolunteer",methods = ["POST"])
def savevolunteer():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    phonenumber = request.form['phonenumber']
    latitude=request.form['latitude']
    longitude=request.form['longitude']

    cur = mysql.connection.cursor()

       
    cur.execute("INSERT INTO volunteers(name,email,password,phone_number,latitude,longitude) VALUES(%s,%s,%s,%s,%s,%s)",[name,email,password,phonenumber,latitude,longitude])

    mysql.connection.commit()

        # Close connection
    cur.close()
    return render_template("signin.html")
@app.route("/saveorganiser",methods = ["POST"])
def saveorganiser():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    phonenumber = request.form['phonenumber']
    role = 'organiser'
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("INSERT INTO users(name,email,password,phone_number,role) VALUES(%s,%s,%s,%s,%s)",[name,email,password,phonenumber,role])
    
    mysql.connection.commit()

        # Close connection
    cur.close()
    return render_template("signin.html")

@app.route("/validate",methods = ["GET","POST"])
def validate():
    
    email = request.form['email']
    password = request.form['password']
   
  
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select email,password from volunteers")
    volunteers = cur.fetchall()
    cur.execute("select email,password from organisers")
    organisers = cur.fetchall()
    mysql.connection.commit()

        # Close connection
    cur.close()
    for i in volunteers:
        if(i[0] == email and i[1] == password):
            if request.method == "POST":  
                session['email']=request.form['email']
                session['role']='volunteer'
            return render_template("volunteerhomepage.html")
    for i in organisers: 
        if(i[0] == email and i[1] == password):
            if request.method == "POST":  
                session['email']=request.form['email']
                session['role']='organiser'

            return organiserhomepage()
    
        
    return render_template("signin.html")

@app.route("/addorganisedevent",methods = ["POST"])
def addorganisedevent():
    title = request.form['title']
    description = request.form['description']
    #eventdate = request.form['date']
    eventdate = request.form['datepicker']
    #status = request.form.get('status')
    print(request.form.keys())
    #print(status)
    time = request.form['timer']
    time = time + ":00"
    scheduled_datetime = eventdate + " " + time
    date = datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    email = session['email']
    print(scheduled_datetime, date)
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("INSERT INTO event(email,activity_title,activity_description,creating_datetime,scheduled_datetime,status) VALUES(%s,%s,%s,%s,%s,%s)",[email,title,description,date,scheduled_datetime,'upcoming'])
    
    mysql.connection.commit()

        # Close connection
    cur.close()
    return organiserhomepage


# @app.route("/upload",methods=["POST"])
# def upload():
#     file = request.files['image']
    
#     file.save(file.filename)
#     newfile = file.read()

#     cur = mysql.connection.cursor()
#     cur.execute("insert  completed_event_table(images) values(%s)",[newfile])
   
#     mysql.connection.commit()

#         # Close connection
#     cur.close()
#     return "Success "

# @app.route("/download")
# def download():
#     cur = mysql.connection.cursor()
#     cur.execute("select images from  completed_event_table")
#     images = cur.fetchall()
   
#     mysql.connection.commit()

#         # Close connection
#     cur.close()
#     return render_template("images.html",images=images)
@app.route('/success',methods = ["POST"])  
def success():  
    if request.method == "POST":  
        session['email']=request.form['email']  
    return render_template('success.html')  
 
@app.route("/ongoingevents",methods=["POST","GET"])
def ongoingevents():
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from event where status='ongoing'")
    events = cur.fetchall()
    print(events)
    mysql.connection.commit()
    cur.close()
    return render_template("ongoingevents.html",events=events)

@app.route('/logout')  
def logout():  
    if 'email' in session:  
        session.pop('email',None)  
        return render_template('logout.html');  
    else:  
        return '<p>user already logged out</p>'  

@app.route("/upcomingeventpage")
def upcomingevent():
    return render_template("upcomingeventpage.html")

@app.route("/registered")
def registered():
    return "success"

# @app.route("/email", methods=['GET', 'POST'])
# def email():
#     if request.method == "POST":
#         cursor = mysql.connection.cursor()
#         conn = mysql.connection
#         #city = request.form['city']
#         cursor.execute("SELECT email from activity_registering_table WHERE status=%s", [1])
#         conn.commit()
#         data = cursor.fetchall()
#         l = []
#         for i in data:
#             l.append(i[0])
#         for i in l:
#             msg = Message('Hello from the other side!', sender='hrithikdas2nd@gmail.com',
#                           recipients=[i])
#             msg.body = "Hey Hrithik, checking if the this msg is going to users registered for activity, lmk if it works"
#             mail.send(msg)

#         return "Message sent!"
#     return render_template('mail.html')

@app.route("/organisereventpage/<string:title>")
def generateEventpage(title):
    cur = mysql.connection.cursor()

        # Execute query
    cur.execute("select * from event where activity_title=(%s)",[title])
    events = cur.fetchone()
    print(events)
    cur.execute("select * from rough")
    nums = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return render_template('eventpage.html',event=events,nums=nums)

@app.route("/volunteerprofilewithevent")
def myprofile():
    if 'email' in session:
        email = session['email']
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("select * from volunteers where email=(%s)",[email])
        user = cur.fetchall()
        cur.execute("select count(*) from event where status='completed' and title in (select event_title from event_volunteer_table  where volunteer_email=(%s)) ",[email])
        
        count = cur.fetchall()
        cur.execute("select title,description,scheduled_datetime from event where status='completed' and title in (select event_title from event_volunteer_table  where volunteer_email=(%s)) ",[email])

        info=cur.fetchall()
        mysql.connection.commit()
        cur.close()
    
        return render_template("volunteerprofilewithevent.html",user=user,count=count,info=info)


    return render_template("volunteerprofilewithevent.html")

app.run(debug=True)



