import psycopg2
from psycopg2 import OperationalError

from random import choice as r_choice

db_name = "rum21133032"
db_user = "rum21133032"
db_password = ""
db_host = "rum21133032.webdev.ucb.ac.uk"
db_port = "5432"

def db_create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

# CONN = db_create_connection(db_name, db_user, db_password, db_host, db_port)
# CUR = CONN.cursor()

# CUR.close()
# CONN.close()


def return_test_html():
    # rows = CUR.execute("SELECT * FROM your_table WHERE user = 'lewis';")

    # replacement for creating a fake database pull request
    test_data1 = ["luis", "lewis", "axel", "dawood", "richard", "victor", "fahmida"]
    test_data2 = ["apple", "banana", "orange"]
    req=[]
    for count, i in enumerate(test_data1):
        req.append(
            {"id":count, "name":i, "likes":r_choice(test_data2)}
        )

    rows = ""
    for row in req:
        rows += f"<p>{row['name']} likes {row['likes']}s</p>"

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet" href='../static/global.css'>
        </head>
        <body>

            <nav class="navbar">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/classes">Classes</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>

            <h2>Test showing a database query</h1>
            <div class="container">
                <p>{rows}</p>
            </div>

        </body>
    </html>
    """

    return html




def return_event_html(day, month, year):

    # do database query for events with this date
    # if none return "no events"

    # create admin page where they can add events for a date

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet" href='../static/global.css'>
            <link rel="stylesheet" href='../static/classes.css'>
        </head>
        <body>

            <nav class="navbar">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/classes">Classes</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>

            <h2>test</h1>
            <div class="container">
            
                <p>{day}</p>

                <p>{month}</p>

                <p>{year}</p>
                
            </div>

        </body>
    </html>
    """

    return html


# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
# conn.commit()

# ################################### IMPORTANT ################################### #
# DATABASE_URL="postgresql://rum21133032@rum21133032.webdev.ucb.ac.uk:5432/rum21133032"
# rum21133032
# jowqZoTBPEd1EsE
# ################################################################################# #