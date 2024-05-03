import psycopg2
from psycopg2 import OperationalError

def create_connection():
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

# CONN = create_connection()
# if CONN == None:
#     print("Connection to PostgreSQL DB unsuccessful")
# else:
#     CUR = CONN.cursor()
    

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
                    <li><a href="/profile">Profile</a></li>
                    <li><a href="/classes">Classes</a></li>
                    <li><a href="/membership">Membership</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/about">About</a></li>
                </ul>
            </nav>

            <h2>test</h1>
            <div class="container">
            
                <p>{str(day).zfill(2)}-{month}-{year}</p>
                
            </div>

        </body>
    </html>
    """

    return html


def return_admin_html():
    month_select = ""
    for count, i in enumerate(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]):
        month_select += f"<option value='{str(count+1).zfill(2)}'>{i}</option>"

    trainer_select = ""
    for i in ["Adam", "Barry", "Axel", "Lewis"]: # would actually be an sql query for trainers
        trainer_select += f"<option value='{i.lower()}'>{i}</option>" # value would be trainer id with id+name as option

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