from flask import Flask, jsonify, render_template_string
import mysql.connector
import os,sys
import boto3
import json
from botocore.exceptions import ClientError

app = Flask(__name__)

secret_name = "rds!cluster-51e800d1-3125-4ebd-be2f-1067688c35ba"
region_name = "us-east-1"
db_host = "ea-ppaul-aurora-svrls.cluster-ceqmtdpc4l3k.us-east-1.rds.amazonaws.com"
ImageVersion="Ver:2025-03-22-9:50am"
def get_secret():
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client( service_name='secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value( SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    secret = get_secret_value_response['SecretString']
    dict_result_json = json.loads(secret.replace("'", "\""))
    username = dict_result_json["username"]
    password = dict_result_json["password"]
    return username,password

db_user,db_pwd=get_secret()

def add_employee_login():
    try:
        conn = mysql.connector.connect( host=db_host, user=db_user, password=db_pwd, database="hr")
        cursor = conn.cursor()
        employee_id=61
        query = "INSERT INTO employee_logins (employee_id) VALUES(%s);"
        values = (employee_id,)
        cursor.execute(query, values)
        conn.commit() 
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return;

def get_employee_count():
    ecount=0
    try:
        conn = mysql.connector.connect( host=db_host, user=db_user, password=db_pwd, database="hr")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM employee_logins where employee_id = 61;")
        ecount = cursor.fetchone()[0]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return ecount;

@app.route('/')
def hello():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head> <title>My HTML</title> </head>
    <body>
        <h1>Hello from Flask!</h1>
        <br>{ImageVersion}<br><br><br>
        <a href="/add">Add a New Login Entry</a>
        <br><br><br>
        <a href="/get">Get Login Count</a>
    </body>
    </html>
"""
    return render_template_string(html_content)
#    return jsonify({'message': 'Hello, World!'})

@app.route('/add')
def add():
    add_employee_login()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head> <title>My HTML</title> </head>
    <body>
        <h1>Hello from Flask!</h1>
        <br>{ImageVersion}<br><br><br>
        <p>New Login Added</p>
        <a href="../">Back</a>
    </body>
    </html>
"""
    return render_template_string(html_content)
#    return jsonify({'message': 'Hello, World!'})
@app.route('/get')
def get():
    employee_count = get_employee_count()
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head> <title>My HTML</title> </head>
    <body>
        <h1>Hello from Flask!</h1>
        <br>{ImageVersion}<br><br><br>
        <p>Total Logins: <bold>{employee_count}</bold></p>
        <a href="../">Back</a>
    </body>
    </html>
"""
    return render_template_string(html_content)
#    return jsonify({'message': 'Hello, World!'})

@app.route('/<path:my_path>')
def catch_all(my_path):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head> <title>My HTML</title> </head>
    <body>
        <br>{ImageVersion}<br><br><br>
        <h1>ERROR!!!</h1>
        <h1>Path "{my_path}" Not Defined!!!</h1>
        <h1>ERROR!!!</h1>
        <a href="/add">Add a New Login Entry</a>
        <br><br><br>
        <a href="/get">Get Login Count</a>
    </body>
    </html>
"""
    return render_template_string(html_content)

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0')
    ##app.run(debug=True,host='0.0.0.0',port=8282)
