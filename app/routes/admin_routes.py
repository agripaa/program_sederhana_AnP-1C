import os
from flask import render_template, request, redirect, url_for, flash
from app import app, mysql
from app.models.product_model import Product


@app.route("/admin/upload_product", methods=["GET", "POST"])
def upload_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        image = request.files["image"]

        if all([name, price, image]):
            image_path = f"static/image/{image.filename}"
            image.save(os.path.join("app", image_path))

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO products (name, price, image_path) VALUES (%s, %s, %s)",
                (name, price, image.filename),
            )
            mysql.connection.commit()
            cur.close()

            flash("Product uploaded successfully!", "success")
            return redirect(url_for("upload_product"))

    return render_template("admin/upload_product.html")


@app.route("/admin/dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if all([username, password]):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user WHERE username = %s", (username,))
            user = cur.fetchone()

            if user is None:
                flash("User not found!", "warning")
                return redirect(url_for("admin_dashboard"))

            mysql.connection.commit()
            cur.close()

            flash("You're logged in successfully", "success")
            return redirect(url_for("admin_dashboard"))

    products = Product.get_all_products()
    return render_template("admin/dashboard.html", products=products)
