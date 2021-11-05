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
        cur.execute('SELECT * from katten')
        db_all = cur.fetchall()
        print(db_all)

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
    return f"""
    <h2>Visual DB representation</h2>
    <p>{str(poepout)}</p>
    <br>
    <h3>API calls</h3>
    <br>
    <h5>/</h5>
    <p>This page, shows the full Database.</p>
    <h5>/delete?naam=...</h5>
    <p>Takes the name and deletes it from the DB if present.</p>
    <h5>/add?naam=...&kleur=...&leeftijd=...</h5>
    <p>Adds the name, color and age of the cat. Age must be an integer.</p>
    <h5>/edit?naam=...&leeftijd=...</h5>
    <p>Mutates the age of the mentioned cat (if present) into the input. Age must be an integer.</p>
    """

@app.route('/delete', methods =["GET", "POST"])
def delete():
    name2del = request.args['naam']

    command = f"""DELETE FROM katten WHERE naam='{name2del}';"""

    poepout = connect(command)
    return str(poepout)

@app.route('/add', methods =["GET", "POST"])
def add():
    name2add = request.args['naam']
    color2add = request.args['kleur'] 
    age2add = request.args['leeftijd']

    command = f"""INSERT INTO katten VALUES ('{name2add}', '{color2add}', {age2add});"""

    poepout = connect(command)
    return str(poepout)

@app.route('/edit', methods =["GET", "POST"])
def edit():
    name2change = request.args['naam']
    age2change = request.args['leeftijd']

    command = f"""UPDATE katten SET leeftijd = {age2change} WHERE naam = '{name2change}';"""

    poepout = connect(command)
    return str(poepout)

if __name__=='__main__':
   app.run()