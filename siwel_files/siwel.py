from psycopg2 import OperationalError, connect
from hashlib import sha256
from datetime import datetime



# these parameters need to be changed based on who is testing the website, refer to db_init.py for params
# if testing at University use the VirtualMin database it has postgreSQL db already there
# if testing at home download pgAdmin from https://www.postgresql.org
# run db_init.py before trying to run the website as the tables will not exist
def create_connection():
    con = None
    try:
        con = connect(
            database="gym_db",
            user="postgres",
            password="lewis",
            host="localhost",
            port="5432",
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return con


# create global connection and cursor variables
# possibly a better way to do this as this runs twice on server startup and the connection and cursor never get closed
# however as the goal for the project was not about best practices this will do
CONN = create_connection()
if CONN == None:
    print("Connection to PostgreSQL DB unsuccessful")
else:
    CONN.autocommit = True
    CUR = CONN.cursor()

# ==========================================================












# =========================================================
# view event html
def return_event_html(day, month, year):
    date = f"{str(day).zfill(2)}-{month}-{year}" # reformat the date
    CUR.execute(f"SELECT * FROM events WHERE date = '{date}';")
    result = CUR.fetchall()

    results = "<table><tr><th>Class name</th><th>Hours</th></tr>"
    if len(result) == 0: # if no results then set the output to inform user of this
        results=f"<p>No events</p>"
    else: # if results exist then create a table to display to user
        for row in result:
            results += f"<tr><td>{row[1]}</td><td>{row[3]} -> {row[4]}</td></tr>"
        results+="</table>"

            
    # returning html as a string works the same way as 'render_template' does with a html file however
    # this allows for python variables to be used on the html page using f-strings
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Classes</title>
            <link rel="stylesheet" href='../../static/global.css'>
            <link rel="stylesheet" href='../../static/classes.css'>
        </head>
        <body>

            <nav class="navbar">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/profile">Profile</a></li>
                    <li><a href="/classes" class="active">Classes</a></li>
                    <li><a href="/membership">Membership</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>

            <h2>Classes scheduled for {str(day).zfill(2)}-{month}-{year}:</h1>
            <div class="container">
                {results}
            </div>

        </body>
    </html>
    """
    return html



# admin event add - html page
def return_admin_html():
    month_select = "" # select input for months
    for count, i in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]):
        month_select += f"<option value='{str(count+1).zfill(2)}'>{i}</option>"

    trainer_select = ""

    CUR.execute("SELECT id, trainer_fn, trainer_ln FROM trainers;") # query for trainers
    trainers = CUR.fetchall()
    for i in trainers:
        trainer_select += f"<option value='{i[0]}'>{i[1]} {i[2]}</option>" # select input with all known trainers in

    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Admin</title>
            <link rel="stylesheet" href='../static/global.css'>
            <link rel="stylesheet" href='../static/classes.css'>
        </head>
        <body>

            <nav class="navbar">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/profile">Profile</a></li>
                    <li><a href="/classes">Classes</a></li>
                    <li><a href="/membership">Membership</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>

            <div class="admin-section">
                <h1>Admin Guide</h1>
                <p>Greetings and welcome to the gym class schedule admin guide. We'll go over what you need to know in this guide to efficiently plan, maintain, and let staff and members know when classes are being held at the gym.</p>
                <p>Establish Class Schedule Structure -</p> 
                <p>In the table below on the "class name" bar, determine the type of class you are scheduling (for example, Yoga, Boxing and Weight ligting).</p>
                <p>Decide upon the year month and date of the class and input the information into the table.
                <p>The duration of the class needs to be arranged, use the dropdown options to choose how long the class will last for on the date you have decided.</p>
                <p>Finally use the dropdown option to select the name of the gym instructor that will host the class.</p>
            </div>

            <div class="container">
                <form class="event_add" action="/event-add/" method="post">
                    <input type="text" placeholder="Class name" name="class-name">
                    <input type="number" min=1 max=31 value=1 name="day">
                    <select name="month">
                        {month_select}
                    </select>
                    <input type="number" min=2020 max=2034 value=2024 name="year">
                    <input type="time" name="start-time">
                    <input type="time" name="end-time">
                    <select name="trainers">
                        {trainer_select}
                    </select>
                    <input type="submit" value="Submit">
                </form>
            </div>

            <div class="container">
                <h2>Manage user</h2>
                <form class="event_add" action="/manage-user/" method="post">
                    <input type="text" placeholder="Username" name="usern">
                    <select name="user-type">
                        <option value='user'>User</option>
                        <option value='trainer'>Trainer</option>
                        <option value='admin'>Admin</option>
                    </select>
                    <input type="submit" value="Submit">
                </form>
            </div>

        </body>
    </html>
    """
    return html

# purchase a specific membership page
def return_purchase_html(type):
    # dicts with the relevant data associated with plan selected, this is accessed and displayed based off which option user selected
    values = {
        "standard": {
            "name" : "Standard Plan",
            "price" : "£11.99",
            "desc" : "The Standard Plan offers access to our full range of gym facilities, including cardio equipment, weightlifting machines, and group fitness classes. With this plan, you can work out at any time during our regular opening hours. Additionally, you'll receive personalized support from our experienced trainers to help you achieve your fitness goals. Join the Standard Plan today to start your journey towards a healthier lifestyle!"
        },
        "premium": {
            "name" : "Premium Plan",
            "price" : "£17.99",
            "desc" : "Upgrade to our Premium Plan for an enhanced gym experience. With the Premium Plan, you'll enjoy all the benefits of our Standard Plan, plus exclusive perks such as access to our premium fitness equipment, sauna, and steam room facilities. You'll also receive priority booking for our most popular group fitness classes and personalized training sessions with our top-tier trainers. Join the Premium Plan today to take your fitness journey to the next level!"
        },
        "family": {
            "name" : "Family Plan",
            "price" : "£19.99",
            "desc" : "Our Family Plan is perfect for families who want to prioritize health and fitness together. With the Family Plan, you and your loved ones can enjoy unlimited access to our gym facilities, group fitness classes, and exclusive amenities at a discounted rate. Stay motivated and support each other on your fitness journey while saving money with our Family Plan. Join today and make health and wellness a family affair!"
        }
    }
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Membership</title>
            <link rel="stylesheet" href='../../static/global.css'>
            <link rel="stylesheet" href='../../static/membership.css'>
        </head>
        <body>

            <nav class="navbar">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/profile">Profile</a></li>
                    <li><a href="/classes">Classes</a></li>
                    <li><a href="/membership" class="active">Membership</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>

            
            <div class="plan-description">
                <h1>{values[type]["name"]}</h1>
                <p>{values[type]["desc"]}</p>
                <p>Price = {values[type]["price"]}</p>
                <button class="buy-button">Buy Now</button>
            </div>

        </body>
    </html>
    """
    return html

# show profile/account information based on if they are logged in or not
def return_profile_html(usern):
    # if user logged in cookie is None then no one is logged in, if not None then it is a username
    if usern != None:
        CUR.execute(f"SELECT first_name, last_name, user_type FROM users WHERE username = '{usern}';")
        result = CUR.fetchall()

        if_admin = ""
        if result[0][2] == "admin": # add button linking to admin page if they are an admin
            if_admin = """
                    <div class="container">
                        <a class="button" href='/admin/'>Admin</a>
                    </div>
                    """

        # create the content to display if user was logged in
        content = f"""
                    <div class="container">
                        <h1>Member Profile</h1>
                        <h2>Welcome, {result[0][0]} {result[0][1]}!</h2>
                        <p>Your username is: {usern}</p>
                        <p>Here, you can view and manage your membership information.</p>
                        <h3>Your Classes</h3>
                        <p>Show classes for the user that they are signed up for.</p>
                        <h3>Membership Plans</h3>
                        <p>View and manage your membership plans here.</p>
                        <h3>Billing and Invoice</h3>
                        <p>Access your billing information and view invoices.</p>

                        <a class="button" href="/logout/">Log out</a>
                    </div>
                    {if_admin}
                    """
        
    else: # if no one logged in then display option for login/create an account
        content = f"""
                    <div class="container">
                        <h1>Login Page</h1>
                        <p>If you already have an account, please select the 'Log in' button and fill out the username and password section. </p>
                        <p>From there you can view all account details including your arranged classes, plans billing and more!</p>
                        <p>If you would like to create an account, you can do that on this page too! Please select the 'create an account' option below and follow the instructions on the next page.</p>
                    </div>
                    
                    <div class="container">
                        <a class="button" href="/profile/login/">Log in</a>
                        <a class="button" href="/profile/create-account">Create an account</a>
                    </div>
                    """

    # pass content into the base layout for page
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Profile</title>
            <link rel="stylesheet" href='../../static/global.css'>
            <link rel="stylesheet" href='../../static/profile.css'>
        </head>
        <body>
            <nav class="navbar">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/profile" class="active">Profile</a></li>
                    <li><a href="/classes">Classes</a></li>
                    <li><a href="/membership">Membership</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>
            
            {content}

            <footer class="footer">
                <nav class="bottom-navbar">
                    <!-- Your bottom navigation bar content -->
                </nav>
                <p class="copyright">© 2024 Your Company Name. All rights reserved.</p>
            </footer>

        </body>
    </html>
    """
    return html


# log in a user and return their name and if they are admin
def log_in_user(usern, passw):
    h_passw = sha256(passw.encode('utf-8')).hexdigest() # hash password
    CUR.execute(f"SELECT user_type FROM users WHERE username = '{usern}' AND password = '{h_passw}';") # find if user exists in table
    result = CUR.fetchall()

    if len(result) == 1: # if there is a result then the user exists
        if result[0][0] == "admin": # if user is an admin then send back admin=True as well
            return {"login":True, "data":[usern, True]} # logged in is True as well as username and admin = True
        else:
            return {"login":True, "data":[usern, False]} # logged in is True as well as username and admin = False
    else:
        return {"login":False} # logged in is False




# create a user account
def create_user(firstn, lastn, passw):
    usern = firstn.lower() + lastn.lower()[:3]


    for i in range(0, 100):
        usern2 = usern
        CUR.execute(f"SELECT * FROM users WHERE username = '{usern2}';") # check if the username exists
        result = CUR.fetchall()

        if len(result) == 0: # if it is unique then break from the loop
            break
        else:
            usern += str(i) # however if it is not unique then add i to the end of the username and recheck, i increments with each non unique pass so if there are mutliple 'lewisrum' it will
            # then generate 'lewisrum0', 'lewisrum1', 'lewisrum2', ... etc. with enough generation (100+) this will begin creating duplicate usernames however this can be avoided with an arbitrarily 
            # high number however the loop will take longer and longer to complete and also still does not fix the problem however, alternative solutions can be making the user decide their username 
            # for themselves or adding something more complex to the end of the initial username that doesnt scale with the for loop like a randomly generated 4 length string 

    h_passw = sha256(passw.encode('utf-8')).hexdigest() # hash the password
    CUR.execute(f"INSERT INTO users (first_name, last_name, username, password, user_type) VALUES ('{firstn}', '{lastn}', '{usern}', '{h_passw}', 'user');") # add new user to table
    return usern2




# admin function for adding an event
def db_event_add(class_name, day, month, year, start_time, end_time, trainer):
    def convert(x):
        X = x.split(":") # split time in hours and minutes
        date = datetime(2024, 1, 1, int(X[0]), int(X[1]), 0) # convert time to a datetime object
        time = date.timestamp() # get timestamp of the object
        return time # return the timestamp

    date = f"{str(day).zfill(2)}-{month}-{year}" # reformat date

    no_empty_values = True
    for i in [class_name, start_time, end_time]: # quick loop to ensure values are not empty
        if i == "":
            no_empty_values = False # no empty value check

    if no_empty_values: # add the event to the database if the check is passed
        hours = (convert(end_time) - convert(start_time)) / 3600 # convert time into timestamps and compare then divide by 3600 to get difference in hours
        if hours <= 0:
            print("Invalid time") # time cannot be negative
        else:
            CUR.execute(f"SELECT hours FROM trainers WHERE id = '{trainer}';") # get hours of trainer from db
            result = CUR.fetchall()
            hours += result[0][0] # existing hours + new hours

            CUR.execute(f"UPDATE trainers SET hours = {hours} WHERE id = '{trainer}';") # updates trainer hours
            CUR.execute(f"INSERT INTO events (class_name, date, start_time, end_time, trainer_id) VALUES ('{class_name}', '{date}', '{start_time}', '{end_time}', '{int(trainer)}');") # add new event to table
            CONN.commit()
    else:
        print("Values cannot be empty") # pointless commiting to console as admin will likely not have access to console
        # it could be display to admin, however it can be argued that the admin should just be told not to add empty values or it will not add it to the db
        # printing this or not the event is not added regardless



# manage a user's type in the database
def db_user_update(usern, usert):
    CUR.execute(f"SELECT first_name, last_name, user_type FROM users WHERE username = '{usern}';") # get relevant information on the user
    result = CUR.fetchall()

    if usert == result[0][2]: # if changing a trainer to trainer then pass to avoid issues
        print("trainer to trainer")
    else: # other same usertype to usertype cases dont matter
        CUR.execute(f"UPDATE users SET user_type = '{usert}' WHERE username = '{usern}';") # change the user type
        if usert == "trainer": # if they are changing to trainer then add a new trainer to the trainer table
            CUR.execute(f"INSERT INTO trainers (trainer_fn, trainer_ln, hours) VALUES ('{result[0][0]}', '{result[0][1]}', '0');")
        elif result[0][2] == "trainer": # if they were a trainer before then delete their trainer row in the trainer table
            CUR.execute(f"DELETE FROM trainers WHERE trainer_fn ='{result[0][0]}';")
        CONN.commit() # commit changes
        
    print("User does not exist")
