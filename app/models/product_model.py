from app.models.database import execute_query
import string
import random


class Product:
    @staticmethod
    def get_all_products():
        query = "SELECT * FROM products"
        return execute_query(query)

    @classmethod
    def get_product_by_id(cls, product_id):
        query = "SELECT * FROM products WHERE id = %s"
        return execute_query(query, [product_id])

    @classmethod
    def get_user_cart(cls, user_id):
        query = "SELECT * FROM cart WHERE user_id = %s"
        result = execute_query(query, (user_id,))
        return result

    @classmethod
    def add_to_cart(cls, user_id, product_id):
        product = cls.get_product_by_id(product_id)
        rand_str = cls.generate_order_number()
        query = "INSERT INTO cart (user_id, product_id, name, price, image_path, list) VALUES (%s, %s, %s, %s, %s, %s)"
        return execute_query(
            query,
            (
                user_id,
                product_id,
                product[0][1],
                product[0][2],
                product[0][3],
                rand_str,
            ),
        )

    @classmethod
    def delete_cart_product(cls):
        query = "DELETE FROM cart"
        return execute_query(query)

    @staticmethod
    def calculate_total_price(cart):
        total_price = 0
        for product_id in cart:
            total_price += Product.get_product_price_by_id(product_id[1])
        return total_price

    @classmethod
    def get_product_price_by_id(cls, product_id):
        product = cls.get_product_by_id(product_id)
        return product[0][2] if product else 0

    @staticmethod
    def generate_order_number():
        return f"ORD{random.randint(100000, 999999)}"

    @staticmethod
    def get_cart_data(user_id):
        query = "SELECT id FROM cart WHERE user_id = %s"
        return execute_query(query, (user_id,))

    @staticmethod
    def delete_product_cart_by_id(cart_list):
        query = "DELETE FROM cart WHERE list = %s"
        return execute_query(query, (cart_list,))
