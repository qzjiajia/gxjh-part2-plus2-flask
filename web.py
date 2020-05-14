from flask import Flask, render_template, request, make_response, send_file, send_from_directory
import time
import os
import json
import base64
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'board'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)


def getDb():
    return mysql.get_db()


def getCursor():
    return mysql.get_db().cursor()


def getTime():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save("uploaddir/{}_{}".format(getTime(), f.filename))
        return '1'


@app.route('/uploaderlist', methods=['GET'])
def uploaderlist():
    list_dir = os.listdir("uploaddir")
    list_file = []
    for i in list_dir:
        s = i.split("_", maxsplit=1)
        time = s[0]
        filename = s[1]
        d = {"filename": filename, "time": time, "savename": i}
        list_file.append(d)
    return json.dumps(list_file)


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd() + "/uploaddir"  # 假设在当前目录
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


@app.route('/board')
def board():
    return render_template('board.html')


def b64en(s):
    ss = s.encode("utf-8")
    return base64.b64encode(ss).decode("utf-8")


def b64de(s):
    ss = s.encode("utf-8")
    return base64.b64decode(ss).decode("utf-8")


@app.route('/getBoard', methods=['GET'])
def getBoard():
    sql = "SELECT * FROM `board`"
    try:
        # 执行SQL语句
        cursor = getCursor()
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        l = []
        for row in results:
            id = row[0]
            try:
                string = b64de(row[1])
            except:
                string = row[1]
            time = row[2]
            # 打印结果
            print("id=%s,string=%s,time=%s" % \
                  (id, string, time))
            d = {"id": id, "string": string, "time": str(time)}
            l.append(d)
        return json.dumps(l)
    except Exception as e:
        print("Error: unable to fetch data, {}".format(e))
        return json.dumps([])


@app.route('/sendBoard', methods=['POST'])
def sendBoard():
    try:
        string = b64en(request.form['string'])
        cursor = getCursor()
        cursor.execute("INSERT INTO `board` (`id`, `str`) VALUES (NULL, '%s')" % (string))
        getDb().commit()
        return "success"
    except Exception as e:
        getDb().rollback()
        return "error: {}".format(e)


if __name__ == '__main__':
    app.run(debug=True)
