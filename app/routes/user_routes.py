from flask import render_template, request, redirect, url_for, flash
from app import app, mysql
from app.models.product_model import Product

USER_ID = 1


@app.route("/user/dashboard/")
def user_dashboard():
    return render_template("user/dashboard.html")


@app.route("/user/cart", methods=["GET", "POST"])
def view_cart():
    user_id = USER_ID
    cart = Product.get_user_cart(user_id)
    total_amount = Product.calculate_total_price(cart)

    if request.method == "POST":
        payment = float(request.form["payment"])
        if payment < total_amount:
            return render_template(
                "user/view_cart.html",
                products_in_cart=cart,
                total_amount=total_amount,
                err="duit anda kurang!",
            )
        else:
            Product.delete_cart_product()
            return redirect(url_for("order_success"))

    return render_template(
        "user/view_cart.html",
        products_in_cart=cart,
        total_amount=total_amount,
    )


@app.route("/user/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    user_id = USER_ID
    Product.add_to_cart(user_id, product_id)
    return redirect(url_for("order"))


@app.route("/user/delete_cart/<string:cart_list>")
def delete_product_cart_id(cart_list):
    Product.delete_product_cart_by_id(cart_list)
    return redirect(url_for("view_cart"))


@app.route("/user/order", methods=["GET", "POST"])
def order():
    products = Product.get_all_products()

    if request.method == "POST":
        return render_template("user/product_card.html", products=products)

    return render_template("user/product_card.html", products=products)


@app.route("/user/order_success", methods=["GET", "POST"])
def order_success():
    queue = Product.generate_order_number()
    return render_template("user/order_success.html", queue=queue)
