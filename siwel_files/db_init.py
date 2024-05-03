import psycopg2
from psycopg2 import OperationalError

# db_name = "rum21133032"
# db_user = "rum21133032"
# db_password = ""
# db_host = "rum21133032.webdev.ucb.ac.uk"
# db_port = "5432"

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

def table_creation():
    sql = """CREATE TABLE Users (
            ID int NOT NULL AUTO_INCREMENT,
            FirstName varchar(255),
            LastName varchar(255),
            Password varchar(255),
            PRIMARY KEY (ID)
            );"""
    
    CUR.execute(sql)
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

    table_creation()

    test = "INSERT INTO Users (FirstName, LastName, Password) VALUES ('Lewis', 'Rumsby', 'pass123');"
    CUR.execute(test)
    CONN.commit()

    CUR.close()
    CONN.close()
