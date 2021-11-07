from flask import Flask, request, render_template, redirect
import psycopg2
from config import config

app = Flask(__name__)

def connect(command):
    conn = None
    try:
        params = config()
        result = None
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        cur.execute(command)
        try:
            result = cur.fetchall()
        except:
            result = "Mutated!"

        # Print entire DB
        # cur.execute('SELECT * from katten')
        # db_all = cur.fetchall()
        # print(db_all)

        # Close and save
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return result

@app.route('/', methods =["GET"])
def view():
    command = """SELECT * FROM katten;"""
    poepout = connect(command)
    return render_template("index.html", poepout=poepout)

@app.route('/delete', methods =["GET", "POST"])
def delete():
    if request.method == "POST":
        name2del = request.form.get("naam")
        command = f"""DELETE FROM katten WHERE naam='{name2del}';"""
        select_all = """SELECT * FROM katten;"""
        antwoord = connect(command)
        if "Mutated" in antwoord:
            poepout = connect(select_all)
        return render_template("index.html", poepout = poepout)
    return render_template("delete.html")

@app.route('/add', methods =["GET", "POST"])
def add():
    if request.method == "POST":
        name2add = request.form.get("naam")
        color2add = request.form.get("kleur") 
        age2add = request.form.get("leeftijd")
        command = f"""INSERT INTO katten VALUES ('{name2add}', '{color2add}', {age2add});"""
        select_all = """SELECT * FROM katten;"""
        antwoord = connect(command)
        if "Mutated" in antwoord:
            poepout = connect(select_all)
        return render_template("index.html", poepout = poepout)
    return render_template("add.html")

@app.route('/edit', methods =["GET", "POST"])
def edit():
    if request.method == "POST":
        name2change = request.form.get("naam")
        age2change = request.form.get("leeftijd")
        command = f"""UPDATE katten SET leeftijd = {age2change} WHERE naam = '{name2change}';"""
        select_all = """SELECT * FROM katten;"""
        antwoord = connect(command)
        if "Mutated" in antwoord:
            poepout = connect(select_all)
        return render_template("index.html", poepout = poepout)
    return render_template("edit.html")

@app.route('/check', methods =["GET", "POST"])
def check():
    if request.method == "POST":
        name2check = request.form.get("naam")
        command = f"""SELECT * FROM katten WHERE naam = '{name2check}';"""
        poepout = connect(command)
        return render_template("index.html", poepout = poepout)
    return render_template("check.html")


if __name__=='__main__':
   app.run()