#app

from flask import Flask, request, render_template, redirect, url_for, flash, session
import os, mysql.connector

connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Iwrtt6wmw!",
                    database="ED_Automated_Schedule",
                    )

my_cursor = connection.cursor()

#Creating a databse
#try:
    #my_cursor.execute("CREATE DATABASE ED_Automated_Schedule")
    #print("Database created successfully")
#except mysql.connector.Error as err:
   #print(f"Failed to create database: {err}")

#Creating a table 
#try:
    #my_cursor.execute("CREATE TABLE Providers (id int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), role VARCHAR(50), employment_status VARCHAR(50))")
    #print("Table created successfully")
#except mysql.connector.Error as err:
    #print(f"Failed to create table: {err}")

#my_cursor.execute("SELECT * FROM PROVIDERS")

#myresult = my_cursor.fetchall()
#print(myresult)

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/home', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        pass

    return render_template('index.html')

@app.route('/schedule', methods = ['GET', 'POST'])
def schedule():
    if request.method == 'GET':
        my_cursor.execute("SELECT * FROM providers")
        provider_list = my_cursor.fetchall()

    return render_template("schedule.html", providers = provider_list)

@app.route('/manage_providers')
def manage_providers():
    if request.method == 'GET':
        my_cursor.execute("SELECT * FROM providers")
        provider_list = my_cursor.fetchall()

    return render_template("providers.html", providers = provider_list)

@app.route('/insert_providers', methods = ['POST'])
def insert_providers():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        employment_status = request.form['employment_status']

        sql = "INSERT INTO providers (name, role, employment_status) VALUES (%s, %s, %s)"
        val = (name, role, employment_status)
        my_cursor.execute(sql, val)
        connection.commit()

    return redirect(url_for('manage_providers'))

@app.route('/update', methods = ['GET', 'POST'])
def update_providers():
    if request.method == 'POST':
        provider_id = request.form['id']
        name = request.form['name']
        role = request.form['role']
        employment_status = request.form['employment_status']
        
        sql = "UPDATE providers SET name = %s, role = %s, employment_status = %s WHERE id = %s"
        val = (name, role, employment_status, provider_id)
        
        my_cursor.execute(sql, val)
        connection.commit()

        return redirect(url_for('manage_providers'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete_providers(id):

    sql = "DELETE FROM providers WHERE id=%s"
    val = [(id)]
    my_cursor.execute(sql, val)
    connection.commit()

    return redirect(url_for('manage_providers'))

@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if request.method == 'GET':
        pass

    return render_template('settings.html')

if __name__ == "__main__":
    app.run(host="localhost", port=int("4000"), debug=True)