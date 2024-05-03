import psycopg2
from psycopg2 import OperationalError
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
            password TEXT,
            usertype TEXT
            );"""
    CUR.execute(sql)
    CONN.commit()

    fake_users = [["Lewis","Rumsby","pass123","admin"], ["Axel","Seston","qwerty","user"],["Dawood","Madarshahian","p@ssw0rd","trainer"]]
    for i in fake_users:
        CUR.execute(f"INSERT INTO Users (firstname, lastname, password, usertype) VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}');")
        CONN.commit()



# create events/classes table
def events_table_creation():
    sql = """CREATE TABLE events (
            id SERIAL PRIMARY KEY,
            classname TEXT,
            date TEXT,
            starttime TEXT,
            endtime TEXT
            trainer TEXT
            );"""
    CUR.execute(sql)
    CONN.commit()

    fake_users = [["Lewis","Rumsby","pass123","admin"], ["Axel","Seston","qwerty","user"],["Dawood","Madarshahian","p@ssw0rd","trainer"]]
    for i in fake_users:
        CUR.execute(f"INSERT INTO Users (firstname, lastname, password, usertype) VALUES ('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}');")
        CONN.commit()


# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
# rows = CUR.execute("SELECT * FROM your_table WHERE user = 'lewis';")
# conn.commit()

# ################################### IMPORTANT ################################### #
# DATABASE_URL="postgresql://rum21133032@rum21133032.webdev.ucb.ac.uk:5432/rum21133032"
# rum21133032
# jowqZoTBPEd1EsE
# ################################################################################# #


# these are various connection settings depending on which db you are trying to connnect to - Lewis
settings = [
    ["gym_db", "postgres", "lewis", "localhost", "5432"], # pgAdmin 4 on Lewis computer
    ["rum21133032", "rum21133032", "", "rum21133032.webdev.ucb.ac.uk", "5432"] # VirtualMin db on University LAN
]
for id, i in enumerate(settings):
    print(f"{id+1}. {i}")
choice = int(input("Which settings to use?\n> "))-1

CONN = create_connection(settings[choice])
if  CONN == None:
    print("Connection to PostgreSQL DB unsuccessful")
else:
    CUR = CONN.cursor()
    CUR.execute("DROP TABLE users;")
    users_table_creation()

    CUR.execute("SELECT * FROM users WHERE usertype = 'admin';")
    result = CUR.fetchall()
    for row in result:
        print(row)

    CUR.close()
    CONN.close()
