from app import app
from flask import redirect, render_template, request
from services.user_service import user_service
from services.image_service import img_service
from services.fragrance_service import fragrance_service

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

@app.route("/login", methods=["GET", "POST"])
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

@app.route('/add', methods=['GET', 'POST'])
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

        out = fragrance_service.post_new_fragrance(user_id, name, designer, nose, description, notes, year)
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
    all = fragrance_service.get_all("perfumers")
    return render_template("all_perfumers.html", perfumers=all)

@app.route("/browse/groups")
def list_groups():
    all = fragrance_service.get_all("groups")
    return render_template("all_groups.html", groups=all)

@app.route("/browse/designers")
def list_designers():
    all = fragrance_service.get_all("designers")
    return render_template("all_designers.html", designers=all)

@app.route("/browse/fragrances")
def list_fragrances():
    all = fragrance_service.get_all("fragrances")
    return render_template("all_fragrances.html", fragrances=all)

@app.route("/fragrances/<int:fragrance_id>")
def show_fragrance(fragrance_id):
    one = fragrance_service.get_one("fragrance", fragrance_id)
    reviews = fragrance_service.get_all("reviews", fragrance_id)
    print(fragrance_id, reviews)
    return render_template("fragrance.html", fragrance=one, reviews=reviews)

@app.route("/designers/<int:designer_id>")
def show_designer(designer_id):
    one = fragrance_service.get_one("designer", designer_id)
    fragrances_by_designer = fragrance_service.get_all_by_name("designer", one[1])
    return render_template("designer.html", designer=one, fragrances_by_designer=fragrances_by_designer)

@app.route("/perfumers/<int:perfumer_id>")
def show_perfumer(perfumer_id):
    one = fragrance_service.get_one("perfumer", perfumer_id)
    fragrances_by_perfumer = fragrance_service.get_all_by_name("perfumer", one[1])
    return render_template("perfumer.html", perfumer=one, fragrances_by_perfumer=fragrances_by_perfumer)

@app.route("/user_profile/<int:user_id>>")
def show_user_profile(user_id):
    one = user_service.get_username(user_id)
    query = fragrance_service.get_one("collection", user_id)
    favourite = query[0]
    collection =
    return render_template("user_profile.html", user=one, favourite=favourite, collection=collection)

@app.route("/statistics")
def show_statistics():
    return render_template("statistics.html")

@app.route("/recent_reviews")
def list_reviews():
    all = fragrance_service.get_all("reviews")
    return render_template("recent_reviews.html", reviews=all)

@app.route("/fragrances/<int:fragrance_id>/new_review")
def add_review(fragrance_id):
    one = fragrance_service.get_one("fragrance", fragrance_id)
    return render_template("review.html", fragrance=one)

@app.route("/send/<int:fragrance_id>", methods=["POST"])
def send_review(fragrance_id):
    rating = request.form["rating"]
    comment = request.form["comment"]
    u_id = user_service.get_user_id()
    if u_id != 0:
        fragrance_service.post_new_review(comment, rating, fragrance_id, int(u_id))
        url = f"/fragrances/{fragrance_id}"
        return redirect(url)
    else:
        return render_template("error.html", message="Failed to add a new review")


