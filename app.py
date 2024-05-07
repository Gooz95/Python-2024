# https://code.tutsplus.com/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972t

from flask import Flask, render_template, request, redirect, make_response
from siwel_files import siwel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/membership/')
def membership():
    return render_template('membership.html')

@app.route('/classes/')
def classes():
    return render_template('classes.html')

@app.route('/services/')
def services():
    return render_template('services.html')

@app.route('/about/')
def about():
    return render_template('about.html')



# lewis custom library stuff:
# purchase a specific membership type
@app.route('/membership/purchases/')
def purchase():
    type = request.args.get("type")
    if type not in ["standard", "premium", "family"]:
        return redirect("/membership/", code=302)
    else:
        return siwel.return_purchase_html(type)
    

# allow user to view events/classes
@app.route('/classes/event-view/', methods=['POST'])
def event_view():
    day = request.form.get("day")
    month = request.form.get("month")
    year = request.form.get("year")
    return siwel.return_event_html(day, month, year)



# admin stuff
# add event/class page
@app.route('/admin/')
def admin():
    try:
        admin = request.cookies.get("admin")
        if bool(int(admin)):
            return siwel.return_admin_html()
    except:
        pass
    return redirect("/", code=302)

# handle event add form
@app.route('/event-add/', methods=['POST'])
def event_add():
    class_name = request.form.get("class-name")
    day = request.form.get("day")
    month = request.form.get("month")
    year = request.form.get("year")
    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")
    trainer = request.form.get("trainers")


    siwel.db_event_add(class_name, day, month, year, start_time, end_time, trainer)
    return redirect("/admin/", code=302)



# handling user stuff
# profile page
@app.route('/profile/')
def profile():
    user = request.cookies.get("user")
    print(user)
    return siwel.return_profile_html(user)

# login page
@app.route('/profile/login/')
def login():
    return render_template('login.html')

# handle the login form
@app.route('/login-event/', methods=['POST'])
def login_event():
    usern = request.form.get("username")
    passw = request.form.get("password")
    login = siwel.log_in_user(usern, passw)

    if login["login"]:
        res = make_response(redirect("/profile/", code=302))
        if login["data"][1]:
            res.set_cookie("admin", "1")
        res.set_cookie("user", login["data"][0])
        return res

    return redirect("/login/", code=302)

# create a user account
@app.route('/profile/create-account/')
def create_account():
    return render_template('create-account.html')

# handle the create account form
@app.route('/create-user/', methods=['POST'])
def create_event():
    firstn = request.form.get("firstname")
    lastn = request.form.get("lastname")
    passw = request.form.get("password")
    create = siwel.create_user(firstn, lastn, passw)

    res = make_response(redirect("/profile/", code=302))
    res.set_cookie("user", create)
    return res

# logout and delete cookies
@app.route('/logout/')
def logout_event():
    res = make_response(redirect("/profile/", code=302))
    res.set_cookie("user", max_age=0)
    res.set_cookie("admin", max_age=0)
    return res



# host the website
if __name__ == "__main__":
    app.run(debug=True)