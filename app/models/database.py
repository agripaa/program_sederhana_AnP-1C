import json
from app import mysql, app


def execute_query(query, data=None, fetchall=True):
    with app.app_context():
        cur = mysql.connection.cursor()

        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)

        mysql.connection.commit()

        if fetchall:
            res = cur.fetchall()
        else:
            res = cur.fetchone()

        cur.close()

    return res


def create_tables():
    create_products_query = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            price INT NOT NULL,
            image_path VARCHAR(255) NOT NULL
        )
    """

    create_users_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(25) NOT NULL,
            password VARCHAR(15) NOT NULL
        )
    """

    create_cart_query = """
        CREATE TABLE IF NOT EXISTS cart (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            product_id INT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            name VARCHAR(50) NOT NULL,
            price INT NOT NULL,
            image_path VARCHAR(255) NOT NULL,
            list VARCHAR(25) NOT NULL
        )
    """

    execute_query(create_products_query)
    execute_query(create_users_query)
    execute_query(create_cart_query)


create_tables()
