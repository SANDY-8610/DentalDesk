from flask import Flask, render_template, flash, request, session, send_file
import pickle
import mysql.connector
import sys

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/NewDoctor")
def NewDoctor():
    return render_template('NewDoctor.html')


@app.route("/DoctorLogin")
def DoctorLogin():
    return render_template('DoctorLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/DoctorInfo")
def DoctorInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb  ")
    data = cur.fetchall()
    return render_template('DoctorInfo.html', data=data)


@app.route("/ADRemove")
def ADRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from doctortb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Doctor  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb  ")
    data = cur.fetchall()
    return render_template('DoctorInfo.html', data=data)


@app.route("/AURemove")
def AURemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from regtb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('User  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/ADrugInfo")
def ADrugInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  apptb   ")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb   ")
    data1 = cur.fetchall()
    return render_template('ADrugInfo.html', data=data, data1=data1)


@app.route("/newdoct", methods=['GET', 'POST'])
def newdoct():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']
        specialist = request.form['Specialist']

        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctortb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + specialist + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('Doctor  Register Successfully')
        return render_template('DoctorLogin.html')


@app.route("/doctlogin", methods=['GET', 'POST'])
def doctlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['ename'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from doctortb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('DoctorLogin.html', data=data)
        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('DoctorHome.html', data=data)


@app.route("/DoctorHome")
def DoctorHome():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb where username='" + username + "' ")
    data = cur.fetchall()
    return render_template('DoctorHome.html', data=data)


@app.route("/DAppoitmentInfo")
def DAppoitmentInfo():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
    data1 = cur.fetchall()

    return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/Accept")
def Accept():
    id = request.args.get('id')
    session['aid'] = id

    return render_template('Amount.html')


@app.route("/aamt", methods=['GET', 'POST'])
def aamt():
    if request.method == 'POST':

        amt = request.form['amt']
        id = session['aid']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute(
            "update   apptb set status='Approved',Amount='" + amt + "' where id='" + id + "'")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM apptb where  id='" + id + "'")
        data1 = cursor.fetchone()

        if data1:
            mobile = data1[2]

            sendmsg(mobile, "Appointment Request Accept..!")

        flash('Appointment Status  Update  Successfully!')

        username = session['ename']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
        data1 = cur.fetchall()

        return render_template('DrugsInfo.html', data=data)


@app.route("/Reject")
def Reject():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cursor = conn.cursor()
    cursor.execute(
        "update apptb set status='Reject' where id='" + id + "'")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM apptb where  id='" + id + "'")
    data1 = cursor.fetchone()

    if data1:
        mobile = data1[2]

        sendmsg(mobile, "Appointment Request Reject..!")

    flash('Appointment Status  Update  Successfully!')

    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
    data1 = cur.fetchall()

    return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/AssignDrug")
def AssignDrug():
    id = request.args.get('id')
    st = request.args.get('st')
    session['apid'] = id
    if st == "Accept":
        flash("Waiting for User Payment..!")

        return DAppoitmentInfo()
    elif st == "paid":
        return render_template('DAssignDrug.html')


    else:
        flash("Appointment Reject")
        username = session['ename']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
        data1 = cur.fetchall()

        return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/drugs", methods=['GET', 'POST'])
def drugs():
    if request.method == 'POST':

        date = request.form['date']
        minfo = request.form['minfo']
        oinfo = request.form['oinfo']
        file = request.files['file']
        file.save("static/upload/" + file.filename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM apptb where  id='" + session['apid'] + "'")
        data = cursor.fetchone()

        if data:
            uname = data[1]
            mobile = data[2]
            email = data[3]
            dname = data[4]

        else:

            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  drugtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + dname + "','" +
            minfo + "','" + oinfo + "','" + file.filename + "','" + date + "')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM drugtb where DoctorName='" + dname + "' ")
        data = cur.fetchall()

        mailmsg = "MedicineInfo :" + minfo + " \nOther Info :" + oinfo

        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        fromaddr = "projectmailm@gmail.com"
        toaddr = email

        # instance of MIMEMultipart
        msg = MIMEMultipart()

        # storing the senders email address
        msg['From'] = fromaddr

        # storing the receivers email address
        msg['To'] = toaddr

        # storing the subject
        msg['Subject'] = "Dental Doctor"

        # string to store the body of the mail
        body = mailmsg

        # attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # open the file to be sent
        filename = file.filename
        attachment = open("./static/upload/" + file.filename, "rb")

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

        # creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)

        # start TLS for security
        s.starttls()

        # Authentication
        s.login(fromaddr, "qmgn xecl bkqv musr")

        # Converts the Multipart msg into a string
        text = msg.as_string()

        # sending the mail
        s.sendmail(fromaddr, toaddr, text)

        # terminating the session
        s.quit()

        return render_template('DrugsInfo.html', data=data)


@app.route("/DrugsInfo")
def DrugsInfo():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb where DoctorName='" + username + "' ")
    data = cur.fetchall()
    return render_template('DrugsInfo.html', data=data)


@app.route('/download')
def download():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM drugtb where  id = '" + str(id) + "'")
    data = cursor.fetchone()
    if data:
        filename = "static\\upload\\" + data[7]

        return send_file(filename, as_attachment=True)

    else:
        return 'Incorrect username / password !'


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']

        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb where username='" + uname + "'  ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route("/Search")
def Search():
    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                   database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb  ")
    data = cur.fetchall()
    return render_template('ViewDoctor.html', data=data)


@app.route("/ViewDoctor", methods=['GET', 'POST'])
def ViewDoctor():
    if request.method == 'POST':

        ans = session['Ans']

        if ans == 'Yes':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb  ")
            data = cur.fetchone()
            if data is None:
                uname = session['uname']

                flash('No Doctor Found!')
                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='1Dentaldoctornewdb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM regtb where username='" + uname + "' ")
                data = cur.fetchall()

                return render_template('UserHome.html', data=data)



            else:
                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='1Dentaldoctornewdb')
                cur = conn.cursor()
                cur.execute("SELECT * FROM doctortb  ")
                data = cur.fetchall()
                return render_template('ViewDoctor.html', data=data)




        else:
            uname = session['uname']
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + uname + "' ")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/Appointment")
def Appointment():
    dname = request.args.get('id')
    session['dname'] = dname
    return render_template('Appointment.html')


@app.route("/appointment", methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        dname = session['dname']
        uname = session['uname']
        date = request.form['date']
        info = request.form['info']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM regtb where  UserNAme='" + uname + "'")
        data = cursor.fetchone()

        if data:
            mobile = data[3]
            email = data[2]


        else:

            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM doctortb where  UserNAme='" + dname + "'")
        data1 = cursor.fetchone()

        if data1:
            mobile1 = data1[3]

            sendmsg(mobile1, "Appointment Request Received..!")

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  apptb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + dname + "','" + date + "','" + info + "','waiting','')")
        conn.commit()
        conn.close()

        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
        data1 = cur.fetchall()
        return render_template('UDrugsInfo.html', data=data, data1=data1)


@app.route("/pay")
def pay():
    id = request.args.get('id')
    st = request.args.get('st')
    session['aid'] = id
    amt = request.args.get('amt')
    if st=="Approved":
        return render_template('Payment.html', amt=amt)
    elif  st=="paid":
        flash("Already Amount Paid")
        return UDrugsInfo()
    else:
        flash("Request Reject..!")
        return UDrugsInfo()





@app.route("/payaa", methods=['GET', 'POST'])
def payaa():
    if request.method == 'POST':
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
        cursor = conn.cursor()
        cursor.execute(
            "update apptb set status='paid' where id='" + session['aid'] + "'")
        conn.commit()
        conn.close()

        return UDrugsInfo()


@app.route("/UDrugsInfo")
def UDrugsInfo():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1Dentaldoctornewdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
    data1 = cur.fetchall()
    return render_template('UDrugsInfo.html', data=data, data1=data1)


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
