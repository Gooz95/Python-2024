# this script is only for initializing the database on user computer
import psycopg2
from psycopg2 import OperationalError
# useful website for sql queries in a postgreSQL db:
# https://www.tutorialspoint.com/postgresql/postgresql_where_clause.htm

# establish connnection with database
def create_connection(settings):
    connection = None
    try:
        connection = psycopg2.connect(
            database=settings[0],
            user=settings[1],
            password=settings[2],
            host=settings[3],
            port=settings[4],
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection



# create users table
def users_table_creation():
    sql = """CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            firstname TEXT,
            lastname TEXT,
            username TEXT,
            password TEXT,
            usertype TEXT
            );"""
    CUR.execute(sql)

    fake_users = [["Lewis","Rumsby","lewisrum","pass123","admin"], ["Axel","Seston","axelses","qwerty","user"],["Dawood","Madarshahian","dawoodmad","p@ssw0rd","trainer"], ["Luis", "Henrique","luishen","wordpass", "trainer"]]
    for i in fake_users:
        CUR.execute(f"INSERT INTO users (firstname, lastname, username, password, usertype) VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}');")



# create events/classes table
def events_table_creation():
    sql = """CREATE TABLE events (
            id SERIAL PRIMARY KEY,
            classname TEXT,
            date TEXT,
            starttime TEXT,
            endtime TEXT,
            trainer_id INT
            );"""
    CUR.execute(sql)

    fake_events = [["Cardio","03-04-2024","09:30","10:30", 3], ["Gym","05-04-2024","14:45","16:15", 4], ["Calesthenics","05-04-2024","10:00","12:30", 3]]
    for i in fake_events:
        CUR.execute(f"INSERT INTO events (classname, date, starttime, endtime, trainer_id) VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}');")




# these are various connection settings depending on which db you are trying to connnect to - Lewis
# set up the postgreSQL database and add your params below then run the script
# you will also need to change the connection params in siwel.py to yours
settings = [
    #[db_name,  username,  password, hostname,   port  ]
    ["gym_db", "postgres", "lewis", "localhost", "5432"], # pgAdmin 4 on Lewis computer
    ["rum21133032", "rum21133032", "", "rum21133032.webdev.ucb.ac.uk", "5432"], # VirtualMin db on University LAN
    ["gym_db", "postgres", "dawood", "localhost", "5432"], # pgAdmin 4 on Dawood computer
    ["gym_db", "postgres", "lewis", "localhost", "5432"], # docker container on Lewis laptop
    # add the params you have set for your database here
]
for id, i in enumerate(settings):
    print(f"{id+1}. {i}")
choice = int(input("Which settings to use?\n> "))-1

CONN = create_connection(settings[choice])
if  CONN == None:
    print("Connection to PostgreSQL DB unsuccessful")
else:
    CONN.autocommit = True
    CUR = CONN.cursor()
    for i in ["users", "events"]:
        try:
            CUR.execute(f"DROP TABLE {i};")
        except psycopg2.errors.UndefinedTable:
            pass
    users_table_creation()
    events_table_creation()

    # show a test query
    CUR.execute("SELECT firstname FROM users WHERE usertype = 'trainer';")
    result = CUR.fetchall()
    for row in result:
        print(row[0])

    CUR.close()
    CONN.close()










# ignore
# ################################### IMPORTANT ################################### #
# DATABASE_URL="postgresql://rum21133032@rum21133032.webdev.ucb.ac.uk:5432/rum21133032"
# rum21133032
# jowqZoTBPEd1EsE
# ################################################################################# #