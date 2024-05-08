import psycopg2
from psycopg2 import OperationalError

def create_connection(): # these parameters need to be changed based on who is testing the website, check db_init.py for known params
    con = None
    try:
        con = psycopg2.connect(
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
CONN = create_connection()
if CONN == None:
    print("Connection to PostgreSQL DB unsuccessful")
else:
    CONN.autocommit = True
    CUR = CONN.cursor()



# view event html
def return_event_html(day, month, year):
    date = f"{str(day).zfill(2)}-{month}-{year}"
    CUR.execute(f"SELECT * FROM events WHERE date = '{date}';")
    result = CUR.fetchall()

    results = "<table><tr><th>Class name</th><th>Hours</th></tr>"
    if len(result) == 0:
        results=f"<p>No events</p>"
    else:
        for row in result:
            results += f"<tr><td>{row[1]}</td><td>{row[3]} -> {row[4]}</td></tr>"
        results+="</table>"

            

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

            <h2>Classes scheduled for {str(day).zfill(2)}-{month}-{year}</h1>
            <div class="container">
                {results}
            </div>

        </body>
    </html>
    """

    return html


# admin event add html
def return_admin_html():
    month_select = ""
    for count, i in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]):
        month_select += f"<option value='{str(count+1).zfill(2)}'>{i}</option>"

    trainer_select = ""

    CUR.execute("SELECT id, firstname FROM users WHERE usertype = 'trainer';")
    trainers = CUR.fetchall()
    for i in trainers:
        trainer_select += f"<option value='{i[0]}'>{i[1]}</option>"

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

            <h2>Add an event</h2>

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

        </body>
    </html>
    """
    return html

# purchase a specific membership page
def return_purchase_html(type):
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
                    <li><a href="/membership">Membership</a></li>
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
    if usern != None:
        CUR.execute(f"SELECT firstname, lastname, usertype FROM users WHERE username = '{usern}';")
        result = CUR.fetchall()

        if_admin = ""
        if result[0][2] == "admin":
            if_admin = """
                    <div class="container">
                        <a href='/admin/'>Admin</a>
                    </div>
                    """

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

                        <a href="/logout/">Log out</a>
                    </div>
                    {if_admin}
                    """
    else:
        content = f"""
                    <div class="container">
                        <a href="/profile/login/">Log in</a>
                        <a href="/profile/create-account">Create an account</a>
                    </div>
                    """

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
    CUR.execute(f"SELECT usertype FROM users WHERE username = '{usern}' AND password = '{passw}';")
    result = CUR.fetchall()

    if len(result) == 1:
        if result[0][0] == "admin":
            return {"login":True, "data":[usern, True]}
        else:
            return {"login":True, "data":[usern, False]}
    else:
        return {"login":False}

# create a user account
def create_user(firstn, lastn, passw):
    usern = firstn.lower() + lastn.lower()[:3]


    for i in range(0, 100):
        usern2 = usern
        CUR.execute(f"SELECT * FROM users WHERE username = '{usern2}';")
        result = CUR.fetchall()

        if len(result) == 0:
            break
        else:
            usern += str(i)
    
    CUR.execute(f"INSERT INTO users (firstname, lastname, username, password, usertype) VALUES ('{firstn}', '{lastn}', '{usern}', '{passw}', 'user');")
    return usern2

# admin function for adding an event
def db_event_add(class_name, day, month, year, start_time, end_time, trainer):
    date = f"{str(day).zfill(2)}-{month}-{year}"
    no_empty_values = True
    for i in [class_name, start_time, end_time]:
        if i == "":
            no_empty_values = False
    if no_empty_values:
        CUR.execute(f"INSERT INTO events (classname, date, starttime, endtime, trainer_id) VALUES ('{class_name}', '{date}', '{start_time}', '{end_time}', '{int(trainer)}');")
        CONN.commit()
    else:
        print("Values cannot be empty")
    