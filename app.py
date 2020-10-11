from flask import Flask, render_template, request, url_for, jsonify
from flask_mysqldb import MySQL
import yaml
from pprint import pprint

app = Flask(__name__)

#configure DB
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nrp = request.form['nrp']
        nama = request.form['nama']
        jenisKelamin = request.form['jenisKelamin']
        jurusan = request.form['jurusan']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO mahasiswa(nrp, nama, jenis_kelamin, jurusan) VALUES(%s, %s, %s, %s)", (nrp, nama, jenisKelamin, jurusan))
        mysql.connection.commit()
        cursor.close()
        # return 'success'
        return readData()
    else:
        return render_template('index.html')

@app.route('/read', methods=['GET'])
def readData():
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM mahasiswa")
    if result > 0:
        data = cursor.fetchall()
        return jsonify(data)
    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def updateData(id):
    if request.method == 'POST':
        nrp = request.form['nrp']
        nama = request.form['nama']
        jenisKelamin = request.form['jenisKelamin']
        jurusan = request.form['jurusan']
        cursor = mysql.connection.cursor()
        sql = "UPDATE mahasiswa SET nrp='{}', nama='{}', jenis_kelamin='{}', jurusan='{}' WHERE id={}".format(nrp, nama, jenisKelamin, jurusan, id)
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        return readData()
    else:
        return "Error Update"

@app.route('/delete/<int:id>', methods=['POST'])
def deleteData(id):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM mahasiswa WHERE id ={}".format(id)
        cursor.execute(sql)
        mysql.connection.commit()
        cursor.close()
        return readData()
    else:
        return "error delete"

@app.route('/detail/<int:id>', methods=['GET'])
def detailData(id):
    print(11111111111111)
    print(type(id))
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM mahasiswa WHERE id={}".format(id)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)