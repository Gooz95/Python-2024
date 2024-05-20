# useful website for sql queries in a postgreSQL db:
# https://www.tutorialspoint.com/postgresql/postgresql_where_clause.htm

# this script is only for initializing the database on user computer
from psycopg2 import OperationalError, connect, errors

# establish connnection with database
def create_connection(settings):
    connection = None
    try:
        connection = connect(
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
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            password TEXT,
            user_type TEXT
            );"""
    CUR.execute(sql)

    fake_users = [["Lewis","Rumsby","lewisrum","9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c","admin"], 
                  ["Axel","Seston","axelses","65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5","user"],
                  ["Dawood","Madarshahian","dawoodmad","a075d17f3d453073853f813838c15b8023b8c487038436354fe599c3942e1f95","trainer"], 
                  ["Luis", "Henrique","luishen","c0e21a8ff85153deac82fe7f09c0da1b3bd90ac0ae204e78d7148753b4363c03", "trainer"]]
    # passwords: pass123, qwerty, p@ssw0rd, wordpass
    for i in fake_users:
        CUR.execute(f"INSERT INTO users (first_name, last_name, username, password, user_type) VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}');")



# create events/classes table
def events_table_creation():
    sql = """CREATE TABLE events (
            id SERIAL PRIMARY KEY,
            class_name TEXT,
            date TEXT,
            start_time TEXT,
            end_time TEXT,
            trainer_id INT
            );"""
    CUR.execute(sql)

    fake_events = [["Cardio","03-04-2024","09:30","10:30", 1], 
                   ["Gym","05-04-2024","14:45","16:15", 2], 
                   ["Calesthenics","05-04-2024","10:00","12:30", 1]]
    for i in fake_events:
        CUR.execute(f"INSERT INTO events (class_name, date, start_time, end_time, trainer_id) VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}', '{i[4]}');")



# trainers table
# create trainers table
def trainers_table_creation():
    sql = """CREATE TABLE trainers (
            id SERIAL PRIMARY KEY,
            trainer_fn TEXT,
            trainer_ln TEXT,
            hours REAL
            );"""
    CUR.execute(sql)

    fake_trainers = [["Dawood","Madarshahian",0.0], 
                     ["Luis", "Henrique",0.0]]
    for i in fake_trainers:
        CUR.execute(f"INSERT INTO trainers (trainer_fn, trainer_ln, hours) VALUES ('{i[0]}', '{i[1]}', '{i[2]}');")




# these are various connection settings depending on which db you are trying to connnect to - Lewis
# set up the postgreSQL database and choose the other option if your params are not in the array below
# you will also need to change the connection params in siwel.py to yours
settings = [
    #[db_name,  username,  password, hostname,   port  ]
    ["gym_db", "postgres", "lewis", "localhost", "5432"], # pgAdmin 4 on Lewis computer
    ["rum21133032", "rum21133032", "", "rum21133032.webdev.ucb.ac.uk", "5432"], # VirtualMin db on University LAN
    ["gym_db", "postgres", "dawood", "localhost", "5432"], # pgAdmin 4 on Dawood computer
    ["gym_db", "postgres", "lewis", "localhost", "5432"], # docker container on Lewis laptop
    ["gym_db", "postgres", "axel", "localhost", "5432"], # pgadmin4 on axel's computer
    ["tre21143355", "tre21143355", "", "tre21143355.webdev.ucb.ac.uk", "5432"],
    ["ses21139317", "ses21139317", "", "ses21139317.webdev.ucb.ac.uk", "5432"] #VirtualMin db on University LAN
    # add the params you have set for your database here
]
for id, i in enumerate(settings):
    print(f"{id+1}. {i}")
print(f"{id+2}. Other")
choice = int(input("Which settings to use?\n> "))-1

# if choice was to use other database params
if choice == len(settings):
    new = []
    new.append(input("Database name: "))
    new.append(input("Database user: "))
    new.append(input("Database password: "))
    new.append(input("Database hostname: "))
    new.append(input("Database port: "))
    settings.append(new)

CONN = create_connection(settings[choice])
if  CONN == None:
    print("Connection to PostgreSQL DB unsuccessful")
else:
    CONN.autocommit = True
    CUR = CONN.cursor()
    for i in ["users", "events", "trainers"]:
        try:
            CUR.execute(f"DROP TABLE {i};")
        except errors.UndefinedTable:
            pass
    users_table_creation()
    events_table_creation()
    trainers_table_creation()

    # show a test query
    CUR.execute("SELECT first_name FROM users WHERE user_type = 'trainer';")
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