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

            <p>do admin stuff here</p>

            <h2>Add an event</h1>
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


def return_purchase_html():
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet" href='../static/global.css'>
            <link rel="stylesheet" href='../static/membership.css'>
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

            <h1>Payment</h1>
            <p></p>

            <h2>Add an event</h1>


        </body>
    </html>
    """
    return html