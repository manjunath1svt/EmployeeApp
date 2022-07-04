from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime
import pymysql
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key = '325698'


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login',methods =['POST', 'GET'])
def login():
   if request.method == 'POST':
      email = request.form.get("email")
      password = request.form.get("password")
      print(email, password)

      con = pymysql.connect(
          host='127.0.0.1',
          user='root',
          password="Manjunath96@",
          port=3306,
          db='svt'
      )

      cur = con.cursor()
      query = """SELECT * FROM login_table WHERE email_id = '"""+email+"""' and password = '"""+password+"""'"""

      cur.execute(query)
      output = cur.fetchone()
      print(output)

      if output:
          current_time = datetime.datetime.now()
          session['loggedin'] = True
          session['id'] = output[0]
          session['loggedintime'] = current_time.strftime("%d/%m/%Y %H:%M:%S")

         

          return redirect(url_for('employeesearch'))

      else:
          return render_template('index.html')



@app.route('/logout',methods =['POST', 'GET'])
def logout():
    session.pop("id")
    session['loggedin'] = False

    print(session)
    return redirect(url_for('home'))






@app.route('/employeesearch')
def employeesearch():
    if session["loggedin"] == False:
        return redirect(url_for('home'))

    else:
        return render_template('employeesearch.html')



@app.route('/search', methods=['POST', 'GET'])
def search():

       if request.method == 'POST':
          value = request.form.get("value")
          employee = request.form.get("employee")

          con = pymysql.connect(
             host='127.0.0.1',
             user='root',
             password="Manjunath96@",
             port=3306,
             db='svt'
          )

          cur = con.cursor()
          query = """Select * from employee_table where """+value+""" = '"""+employee+"""'"""

          cur.execute(query)

          output = cur.fetchall()
          print(output)

          if output:

              empdetails = output[0]
              print(type(empdetails[1]))
              con.close()
              result = {'employee_id': empdetails[0],
                        'employee_name': empdetails[1],
                        'designation': empdetails[2],
                        'joining_id': empdetails[3],
                        'dept_id': empdetails[4],
                        'client_id': empdetails[5],
                        'client_name': empdetails[6],
                        'contact': empdetails[7],
                        'email_id': empdetails[8],
                        'dob': empdetails[9],
                        'location': empdetails[10],
                        'blood': empdetails[11],
                        'gender': empdetails[12],
                        'employeeimages': empdetails[13]
                        }




              print(result)

              return render_template('emp.html', data = result)

          else:
              return render_template('employeesearch.html')



if __name__ == '__main__':
   app.run(port=8000)

   #select * from employees where ID = ES02005

