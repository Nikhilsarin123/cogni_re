from flask import Flask
from flask import jsonify
from flask import send_file
from flask import request
from flask_mail import Mail
from flask_mail import Message
import json
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from io import BytesIO
import base64
from sqlalchemy import func













##### DATABASE CONFIGURATION ###########

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)

##### CONFIG.JSON FILE CONFIGURATION ########

with open('config.json', 'r') as c:
    params = json.load(c)["params"]



###### CONFIGURING MAIL FUNCTIONALITY #######
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)









####### INDEX ROUTE ########

@app.route('/', methods=['GET','POST'])
def index():
   if request.method == "POST":
        name=request.form.get('name')
        company_name=request.form.get('cname')
        email=request.form.get('email')
        contact=request.form.get('contactno')
        entry = Request_Demo_Form(name=name, company_name=company_name, email=email,contact=contact)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('Request From  ' + name + " " + company_name,
                      sender=email,
                      recipients=[params['gmail-user']],
                      body="Name   :  " + name+ "\n" + "Company Name   :  " + company_name+ "\n" + "Email   :  " + email + "\n" + "Contact No  :  " + contact)
        print("POST METHOD CHAL GYA")
        return render_template('index.html')
   else:
       return render_template('index.html')






######### ABOUTUS ROUTE ########

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('aboutus.html')




########## DEEPOPTICS ROUTE ##########

@app.route('/deepoptics', methods=['GET','POST'])
def deepoptics():
    return render_template('deepoptics.html')






############ PRODUCTS ROUTE ###########

@app.route('/products', methods=['GET','POST'])
def products():
    return render_template('product.html')





############ BLOGS ROUTE ###########

@app.route('/blogs', methods=['GET','POST'])
def blogs():
    return render_template('blogs.html')





########### HIRING ROUTE ##########

@app.route('/hiring', methods=['GET','POST'])
def hiring():
    return render_template('hiring.html')


########  ROUTE FORM IN HIRING #############

@app.route('/hireopening' , methods=['GET','POST'])

def hireform():
    if request.method == "POST":
        name=request.form.get('fullname')
        email=request.form.get('email')
        phone_no=request.form.get('tel')
        location=request.form.get('location')
        experience=request.form.get('experience')
        expected_ctc=request.form.get('number')
        #request for uploading file
        pic=request.files['inputfile']
        
        # filename = secure_filename(pic.filename)
        
        # data=HiringForm(name=filedata.filename,data=filedata.read())
        filename = secure_filename(pic.filename)
        # filename = secure_filename(file.filename)
        

        entry = HiringForm(name=name, email=email, phone_no=phone_no,location=location,experience=experience,expected_ctc=expected_ctc,filename=filename,data=pic.read())
        db.session.add(entry)
        db.session.commit()
        
        # file_datareturn=HiringForm.query.filter_by(sno=1).first()
        max_sno=db.session.query(func.max(HiringForm.sno))
        file_datareturn=db.session.query(HiringForm).filter_by(sno=max_sno).first()
        
        # binary_data=base64.b64decode(file_datareturn)
        # ffff=BytesIO(file_datareturn.data)
        
        # return send_file(BytesIO(file_datareturn.data),attachment_filename=filename)
        
        # SELECT * FROM site2 WHERE ID = (SELECT MAX(ID) FROM site2)"
        # tt=json.dumps(convert)
        
        mail.send_message('Request From  ' + name ,
                      sender=email,
                      recipients=[params['gmail-user']],
                      body=("Name   :  " + name + "\n" +  "Email   :  " + email + "\n" + "Phone Number  :  " + phone_no + "\n" + " Location  :  "  + location + "\n" + " Experience  :  "  + experience + "\n" + " Expected_CTC  :  "  + expected_ctc ))
        print("POST METHOD CHAL GYA")
        return ("file saved succesfully")
        return render_template('hiring.html')
    else:
        return render_template('form.html')





########## CONTACT US ROUTE ###############

@app.route('/contactus', methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name=request.form.get('Name')
        company_name=request.form.get('Company_Name')
        email=request.form.get('email')
        contact_no=request.form.get('contact')
        message=request.form.get('subject')
        entry = Contact_Us_Form(name=name, company_name=company_name, email=email,contact_no=contact_no,message=message)
        db.session.add(entry)
        db.session.commit()
        print("chal gya")
        mail.send_message('Message From  ' + name + " " + company_name,
                      sender=email,
                      recipients=[params['gmail-user']],
                      body="Name   :  " + name+ "\n" + "Company Name   :  " + company_name+ "\n" + "Email   :  " + email + "\n" + "Contact No  :  " + contact_no+ "\n" + "Message  :  " + message)
        print("post method")
        return render_template('contactus.html')
    else:
        print("GET METHOD RUNNING")
        return render_template('contactus.html')














################################### DATABASE MODEL #############################







#### FOR "/contact" ROUTE ####
#### CONTACTUS BACKEND DATABASE MODEL ######

class Contact_Us_Form(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    company_name=db.Column(db.String, nullable=False)
    email=db.Column(db.String,nullable=False)
    contact_no=db.Column(db.Integer,nullable=False)
    message=db.Column(db.String,nullable=False)

def __repr__(self):
    return 'QUERY'+ self.name














##### FOR "/" ROUTE  #######
##### REQUEST DEMO FORM BACKEND DATABASE MODEL ####

class Request_Demo_Form(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    company_name=db.Column(db.String, nullable=False)
    email=db.Column(db.String,nullable=False)
    contact=db.Column(db.Integer,nullable=False)















##### FOR '/hiring' ROUTE ########
###### VIEW OPENING FORM BACKEND DATABASE MODEL #####

class HiringForm(db.Model):

    sno= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.Integer,nullable=False)
    location=db.Column(db.String,nullable=False)
    experience=db.Column(db.Integer, nullable=False)
    expected_ctc=db.Column(db.Integer,nullable=False)
    # Use flask-file-upload's `file_upload.Column()` to associate a file with a SQLAlchemy Model:
    # data= file_upload.Column()
    data=db.Column(db.LargeBinary)
    filename=db.Column(db.Text)





















if __name__=="__main__":
    app.run(debug=True)