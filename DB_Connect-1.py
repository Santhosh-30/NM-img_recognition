from flask import Flask, render_template
import ibm_db

app = Flask(__name__)

# Connect to DB2
conn = ibm_db.connect("DATABASE=mydb;HOSTNAME=myhostname;PORT=myport;UID=myusername;PWD=mypassword;", "", "")

@app.route('/')
def index():
    stmt = ibm_db.exec_immediate(conn, "SELECT * FROM mytable")
    result = ibm_db.fetch_both(stmt)
    return render_template('index.html', data=result)

if __name__ == '__main__':
    app.run(debug=True)