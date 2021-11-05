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

        cur.execute('SELECT * from katten')

        db_all = cur.fetchall()
        print(db_all)

        for command in commands:
            cur.execute(command)
            probeersel = cur.fetchall()
            print(probeersel)

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


@app.route('/', methods =["GET"])
def view():
    commands = (
    """
    SELECT * FROM katten;
    """,
    )
    connect(commands)


if __name__=='__main__':
   app.run()