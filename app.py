from flask import Flask, json, Response, request
import logging
import sys
import psycopg2
import os

# Logging
whatsLogger = logging.getLogger(__name__)
whatsLogger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
whatsLogger.addHandler(ch)


# Set up DB
conn_String = "dbname='whatsTwilio'"
try:
    global cursor
    conn = psycopg2.connect(conn_String)
    cursor = conn.cursor()
except Exception as e:
    whatsLogger.error("DB Error")
    whatsLogger.error(str(e))

app = Flask(__name__)

# Pass a dictionary and it gets sent as json
# @params dictionary[data], int[statusCode]
# @returns object[Response]

def JsonResponse(data, statusCode):
    serverResponse = Response(
        response = json.dumps(data),
        status=statusCode,
        mimetype='application/json'
        )
    
    return serverResponse

@app.route("/whatsapp", methods=["GET", "POST"])
def returnMessage():
    global cursor
    message = request.form['Body']
    sender = request.form['From'][10:]
    whatsLogger.debug(sender)
    whatsLogger.debug(message)
    cursor.execute(""" SELECT * FROM contacts WHERE number ='%s' """ % sender)
    username = cursor.fetchall()
    whatsLogger.debug(username)
    return Response("Karanja has received your message, " + username[0][1], mimetype='text/plain', status=200)

@app.route("/Admin")
def Admin():
    return "<h1>Admin Page</h1>"

if __name__ == "__main__":
    app.run()