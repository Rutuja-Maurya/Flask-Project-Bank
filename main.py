from flask import Flask,render_template,redirect,request,session
import mysql.connector
import os
app = Flask(__name__)
app.secret_key = "Firstbit"

@app.route("/login",methods=["GET","POST"])
def login():
    if(request.method == "GET"):
        return render_template("login.html")
    else:
        uname = request.form["uname"]
        pwd = request.form["pwd"]
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",   
                database = 'BankDemo'                        
                )
        cursor = mydb.cursor()
        sql = "select count(*) from UserInfo where username=%s and password=%s"
        val = (uname,pwd)
        cursor.execute(sql,val)
        count = cursor.fetchone() #This is fetch all records
        count = int(count[0])
        if(count==1):
            #User is valid
            session["uname"] = uname
            return redirect("/showAllAccounts")
        else:
            return redirect("/login")
        '''cursor.execute(sql,val)
        record = cursor.fetchone()
        if(int(record[0]) == 1):
            session["uname"] = uname
            return redirect("/showAllAccounts")
        else:
            return redirect("/login")'''



@app.route("/addAccount",methods=["GET","POST"])
def addAccount():
    if(request.method == "GET"):
        return render_template("addAccount.html")
    else:
        name = request.form["name"]
        balance = request.form["balance"]
        password = request.form["password"]
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",   
                database = 'BankDemo'                        
                )
        cursor = mydb.cursor()
        sql = "insert into bank_accounts (name,balance,password) values (%s,%s,%s)"
        val = (name,balance,password)
        cursor.execute(sql,val)
        mydb.commit()
        mydb.close()
        return redirect("/showAllAccounts")

@app.route("/showAllAccounts")
def showAllAccounts():
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",   
                database = 'BankDemo'                        
                )
    cursor = mydb.cursor()
    sql = "select * from bank_accounts"
    cursor.execute(sql)
    records = cursor.fetchall() #This is fetch all records
    return render_template("showAllAccounts.html",bank_accountss=records)

@app.route("/deleteAccount/<acc_no>",methods=["GET","POST"])
def deleteAccount(acc_no):
    if(request.method == "GET"):
        return render_template("deleteConfirm.html")
    else:
        action = request.form["action"]
        if(action == "Yes"):
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",   
                database = 'BankDemo'                        
                )
            cursor = mydb.cursor()
            sql = "delete from bank_accounts where acc_no=%s"
            val = (acc_no,)
            cursor.execute(sql,val)
            mydb.commit()
            mydb.close()
        return redirect("/showAllAccounts")

@app.route("/editAccount/<acc_no>",methods=["GET","POST"])
def editAccount(acc_no):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",   
                database = 'BankDemo'                        
                )
    cursor = mydb.cursor()
    if(request.method == "GET"):
        sql = "select * from bank_accounts where acc_no=%s"
        val = (acc_no,)
        cursor.execute(sql,val)
        bank_accounts = cursor.fetchone() #This is fetch one record
        return render_template("editAccount.html",bank_accounts=bank_accounts)
    else:
        name = request.form["name"]
        sql = "update bank_accounts set name=%s where acc_no=%s"
        val = (name,acc_no)
        cursor.execute(sql,val)
        mydb.commit()
        mydb.close()
        return redirect("/showAllAccounts")
    

def NavBar():
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",   
                database = 'BankDemo'                        
                )
    cursor = mydb.cursor()
    sql = "select * from images"
    cursor.execute(sql)
    records = cursor.fetchall()    
    return render_template("NavBar.html",images=records)

@app.route("/about")
def about():
    return render_template("about.html")



app.add_url_rule('/','',NavBar)
#app.add_url_rule("/login",'login',login,methods=["GET","POST"])


if(__name__ == "__main__"):
    app.run(debug=True)