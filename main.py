from flask import Flask, request, render_template
import psycopg2
from config import config

app = Flask(__name__)

def connect(command):
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        cur.execute(command)
        result = cur.fetchall()
        print(result)

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
    return str(poepout)

@app.route('/delete', methods =["GET", "POST"])
def delete():
    name2del = request.args['naam']

    command = f"""SELECT * FROM katten WHERE naam='{name2del}';"""

    poepout = connect(command)
    return str(poepout)



if __name__=='__main__':
   app.run()