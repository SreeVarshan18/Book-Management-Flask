from flask import Flask, request, render_template, session
from flask_session import Session
import sqlite3 as s

from werkzeug.utils import redirect

connection = s.connect("BookManagement.db", check_same_thread=False)

listoftables = connection.execute("SELECT NAME FROM sqlite_master WHERE type='table' AND name= 'BOOKS'").fetchall()

if listoftables != []:
    print("Table Already Exist")
else:
    connection.execute('''CREATE TABLE BOOKS(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        AUTHOR TEXT,
                        CATEGORY TEXT,
                        PRICE TEXT,
                        PUBLISHER TEXT
                        
                       )''')

    print("Table Created Successfully")

listoftables2 = connection.execute("SELECT NAME FROM sqlite_master WHERE type='table' AND name= 'USER'").fetchall()

if listoftables2 != []:
    print("Table Already Exist")
else:
    connection.execute('''CREATE TABLE USER(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        ADDRESS TEXT,
                        EMAIL TEXT,
                        PHONE INTEGER,
                        PASS TEXT

                       )''')

    print("Table Created Successfully")
App = Flask(__name__)
App.config["SESSION_PERMANENT"] = False
App.config["SESSION_TYPE"] = "filesystem"
Session(App)

@App.route('/', methods=['GET','POST'])
def login():
    global result1, result2, a, b
    if request.method == "POST":
        getEmail = request.form["email"]
        getPass = request.form["pass"]
        cursor = connection.cursor()
        query = "SELECT * FROM USER WHERE EMAIL='"+getEmail+"' AND PASS='"+getPass+"'"
        print(query)
        result1 = cursor.execute(query).fetchall()
        if len(result1) > 0:
            for i in result1:
                getName = i[1]
                getId = i[0]
                session["name"] = getName
                session["id"] = getId

            return redirect('/userpage')
        else:
            return render_template("userlogin.html", status=True)


    else:

        return render_template("userlogin.html", status=False)



@App.route('/userreg', methods=['GET','POST'])
def userRegister():
    global a
    if request.method == "POST":
        getName = request.form["name"]
        getAdd = request.form["add"]
        getnEmail = request.form["email"]
        getPhone = request.form["pno"]
        getnPass = request.form["pass"]
        result1 = connection.execute("SELECT EMAIL FROM USER")
        for i in result1:
            print(i[0])
            a = i[0]
        if getnEmail != a:
            connection.execute("INSERT INTO USER(NAME, ADDRESS, EMAIL, PHONE, PASS) \
                            VALUES('" + getName + "', '" + getAdd + "', '" + getnEmail + "', " + getPhone + ", '" + getnPass + "')")
            connection.commit()
            print("Inserted Successfully")
            return redirect('/')
        else:
            return render_template("userregister.html", status=True)


    else:

        return render_template("userregister.html", status=False)



@App.route('/login', methods=['GET', 'POST'])
def adminLogin():
    if request.method == "POST":
        getUser = request.form["uname"]
        getPass = request.form["pass"]
        if getUser == "admin" and getPass == "9875":
            return redirect('/dash')
        else:
            return render_template("login.html", status=True)
    else:
        return render_template("login.html", status=False)


@App.route('/dash', methods=['GET', 'POST'])
def dashboard():
    if request.method == "POST":
        getName = request.form["name"]
        getAu = request.form["auth"]
        getCat = request.form["cat"]
        getPrice = request.form["price"]
        getPub = request.form["pub"]

        connection.execute("INSERT INTO BOOKS(NAME, AUTHOR, CATEGORY, PRICE, PUBLISHER) \
        VALUES('"+getName+"', '"+getAu+"', '"+getCat+"', '"+getPrice+"', '"+getPub+"')")
        connection.commit()
        print("Inserted Successfully")
        return redirect('/view')
    return render_template("dashboard.html")


@App.route('/view')
def viewall():
    cursor = connection.cursor()
    count = cursor.execute("SELECT * FROM BOOKS")

    result = cursor.fetchall()
    return render_template("view.html", books=result)


@App.route('/search', methods=['GET', 'POST'])
def search():
    cursor = connection.cursor()
    if request.method == "POST":
        getName = request.form["name"]
        count = cursor.execute("SELECT * FROM BOOKS WHERE NAME='" + getName + "'")
        result = cursor.fetchall()
        if result is None:
            print("Book Name Not Exist")
        else:
            return render_template("search.html", search=result, status=True)
    else:
        return render_template("search.html", search=[], status=False)


@App.route('/delete', methods=['GET', 'POST'])
def deletion():
    cursor = connection.cursor()
    if request.method == "POST":
        getName = request.form["name"]
        connection.execute(" DELETE FROM BOOKS WHERE NAME='" + getName + "'")
        connection.commit()

        return redirect('/view')
    return render_template("delete.html")


@App.route('/update', methods=['GET', 'POST'])
def updation():
    global getNName
    cursor = connection.cursor()
    if request.method == "POST":
        getNName = request.form["name"]
        count = cursor.execute("SELECT * FROM BOOKS WHERE NAME='" + getNName + "'")
        result = cursor.fetchall()
        if result is None:
            print("Book Name Not Exist")
        else:

            return render_template("update.html", search=result, status=True)


    else:

        return render_template("update.html", search=[], status=False)


@App.route('/up', methods=['GET', 'POST'])
def updatedata():
    if request.method == "POST":
        getName = request.form["name"]
        getAu = request.form["auth"]
        getCat = request.form["cat"]
        getPrice = request.form["price"]
        getPub = request.form["pub"]

        connection.execute("UPDATE BOOKS SET NAME='" + getName + "', AUTHOR='" + getAu + "'\
                            ,CATEGORY='" + getCat + "', PRICE='" + getPrice + "', PUBLISHER='" + getPub + "' \
                                  WHERE NAME='" + getNName + "'")
        connection.commit()
        print("Updated Successfully")
        return redirect('/view')
    return render_template("up.html")



@App.route('/userpage')
def userpage():
    if not session.get("name"):
        return redirect('/')
    else:
        return render_template("userpage.html")

@App.route('/logout')
def logout():
    session["name"] = None
    return redirect('/')


if __name__ == "__main__":
    App.run()