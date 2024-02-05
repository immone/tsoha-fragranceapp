from app import app
from flask import redirect, render_template, request
from services.user_service import user_service
from services.image_service import img_service
from services.fragrance_service import fragrance_repository

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Your username should consists of 1-20 characters")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="The password verification failed")
        if password1 == "":
            return render_template("error.html", message="Empty password")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Unknown user role")

        if not user_service.register_user(username, password1, role):
            return render_template("error.html", message="Failed to register")
        return redirect("/")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not user_service.login_user(username, password):
            return render_template("error.html", message="Wrong username or password")
        return redirect("/")

@app.route("/logout")
def logout():
    user_service.logout_user()
    return redirect("/")

@app.route('/add', methods=['get', 'post'])
def add():
    user_service.check_role(2)

    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        user_service.check_csrf()
        user_id = user_service.get_user_id()

        designer = request.form["designer"]
        name = request.form["name"]
        year = request.form["year"]
        nose = request.form["perfumer"]
        description = request.form["description"]
        notes = request.form["headnotes"] + ";" + request.form["middlenotes"] + ";" + request.form["bottomnotes"]

        out = fragrance_repository.post_new_fragrance(user_id, name, designer, nose, description, notes, year)
        #img_service.post(out)
        return redirect("/")

@app.route('/info')
def about():
    return render_template("info.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route("/browse/perfumers")
def list_perfumers():
    all = fragrance_repository.get_all("perfumers")
    return render_template("all_perfumers.html", perfumers=all)

@app.route("/browse/groups")
def list_groups():
    all = fragrance_repository.get_all("groups")
    return render_template("all_groups.html", groups=all)

@app.route("/browse/designers")
def list_designers():
    all = fragrance_repository.get_all("designers")
    return render_template("all_designers.html", designers=all)

@app.route("/browse/fragrances")
def list_fragrances():
    all = fragrance_repository.get_all("fragrances")
    return render_template("all_fragrances.html", fragrances=all)

@app.route("/fragrances/<int:fragrance_id>")
def show_fragrance(fragrance_id):
    one = fragrance_repository.get_one(fragrance_id)
    return render_template("fragrance.html", fragrance=one)

@app.route("/user_profile")
def show_user_profile():
    #one = user_service.get_user_id()
    return render_template("user_profile.html")

@app.route("/statistics")
def show_statistics():
    return render_template("statistics.html")

@app.route("/recent_reviews")
def list_reviews():
    all = fragrance_repository.get_all("reviews")
    if all:
        all = all[8]
    return render_template("recent_reviews.html", reviews=all)
