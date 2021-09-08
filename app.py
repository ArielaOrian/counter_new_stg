import mysql.connector
import json
#from flask import Flask
from flask import Flask, request, request_started

app = Flask(__name__)

# orig flask app
counter = 0
@app.route('/', methods=["POST", "GET"])
# @app.route('/')
def index():
    global counter
    if request.method == "POST":
       counter+=1
       return "Hmm, Plus 1 please "
    else:
       return str(f"Our COUNTER is: {counter} ")

# flask with db
@app.route('/widgets')
def get_widgets() :
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="inventory"
  )
  cursor = mydb.cursor()


  cursor.execute("SELECT * FROM widgets")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()
  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)

@app.route('/initdb')
def db_init():
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1"
  )
  cursor = mydb.cursor()

  cursor.execute("DROP DATABASE IF EXISTS inventory")
  cursor.execute("CREATE DATABASE inventory")
  cursor.close()

  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="p@ssw0rd1",
    database="inventory"
  )
  cursor = mydb.cursor()

  cursor.execute("DROP TABLE IF EXISTS widgets")
  cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
  cursor.close()

  return 'init database'

#orig flask app
if __name__ == '__main__':
   app.run(debug=True,port=5000,host='0.0.0.0')
[ec2-user@ip-172-31-39-92 py_docker]$







