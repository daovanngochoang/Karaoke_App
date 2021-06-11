from Data_manager.src.Storage_data import Storage
from Data_manager.src.product_manager import product_manager


class Order_detail_manager:
    def __init__(self):
        self.Storage = Storage()
        self.manage_product = product_manager()

    def insert(self, Order_ID, Product_ID, quantity):
        """
        insert the product of the order by the order id
        :param Order_ID:
        :param Product_ID:
        :param quantity:
        :return:
        """

        if quantity > 0:  # no one gonna add a product which has no quantity =))
            # check if that product is exist
            count, result = self.select_product_from_order("quantity", Order_ID, Product_ID, "order_products")
            new_quantity = 0

            if count > 0: # if its exist

                for ori_quantity in result: # update the quantity
                    new_quantity = quantity + ori_quantity[0]

                # cal culate the total price of that product
                total_price = self.calculate_total_product_price(Product_ID, new_quantity)
                total_price = self.Storage.add_dot(total_price) # add dot to the price

                # update the quantity and the total price to database
                self.update_table_order_product("total_price", total_price, Order_ID, Product_ID, "order_products")
                self.update_table_order_product('quantity', new_quantity, Order_ID, Product_ID, "order_products")

            else:
                # if that product is exist => insert to data base
                total_price = self.calculate_total_product_price(Product_ID, quantity)
                total_price = self.Storage.add_dot(total_price)
                command = "INSERT INTO order_products (Order_ID, Product_ID, quantity, total_price) VALUE ('%s','%s','%s','%s')" % (
                Order_ID, Product_ID, quantity, total_price)
                self.Storage.execute_query(command)
                print("Successfully insert !")

    def calculate_total_product_price(self, product_ID, quantity):
        """
        # product price = price x quantity
        :param product_ID:
        :param quantity:
        :return:
        """

        origin_price = self.manage_product.get_price(product_ID)
        origin_price = self.Storage.remove_dot_to_number(origin_price)
        result = quantity * origin_price

        return result

    def select_product_from_order(self, option, Order_ID, Product_ID, table):

        """
        select the product in order by the order id and product id
        return count, result from order_products table
        """
        command = "select %s from %s where Order_ID = '%s' and Product_ID = '%s'" % (
            option, table, Order_ID, Product_ID)
        result = self.Storage.select_by_query(command)

        final_result = []
        count = 0
        try:
            for i in result:
                count += 1
                final_result.append(i)
        except:
            pass
        return count, final_result

    def update_table_order_product(self, option, new_val, Order_ID, Product_ID, table):
        """
        :param option:         option is the category that we gonna make an update on
        :param new_val:        the new val that we want to update
        :param Order_ID: find by order id and product id
        :param Product_ID:
        :param table: in the table
        :return:
        """
        update_command = "UPDATE %s SET %s = '%s' WHERE Order_ID= '%s' and Product_ID = '%s'" % (
            table, option, new_val, Order_ID, Product_ID)
        self.Storage.execute_query(update_command)

    def get_individual_total_price(self, Order_ID, Product_ID, table="order_products"):
        result = self.select_product_from_order("total_price", Order_ID, Product_ID, table)
        return result[1][0]

    def get_all_price_of_order(self, Order_ID, table="order_products"):
        command = "select total_price from %s where Order_id = '%s'" % (table, Order_ID)
        result = self.Storage.select_by_query(command)
        all_price = []
        for price in result:
            all_price.append(price[0])
        return all_price

    def get_quantity(self, Order_ID, Product_ID, table="order_products"):
        result = self.select_product_from_order("quantity", Order_ID, Product_ID, table)
        return result[1][0]

    def update_quantity(self, new_quantity, Order_ID, Product_ID, table="order_products"):
        self.update_table_order_product("quantity", new_quantity, Order_ID, Product_ID, table)

    def update_price(self, new_price, Order_ID, Product_ID, table="order_products"):
        self.update_table_order_product("total_price", new_price, Order_ID, Product_ID, table)

    def delete_product(self, product_id, order_id):
        command = "delete from order_products where Order_ID = '%s' AND Product_ID = '%s'" % (order_id, product_id)
        self.Storage.execute_query(command)
        print("successfully remove %s" % (product_id))

    def delete_product_from_order(self, order_id):
        command = "delete from order_products where Order_ID = '%s'" % (order_id)
        self.Storage.execute_query(command)

    def select_detail_order(self, Order_id):
        command = "SELECT product_id, product_name, product_price, quantity, order_products.total_price FROM " \
                  "order_products INNER JOIN orders USING (Order_ID ) INNER JOIN product_data USING (product_id) " \
                  "where order_products.Order_ID = '%s'" % Order_id

        cur = self.Storage.select_by_query(command)
        result = []
        for item in cur:
            result.append((item[0], item[1], item[2], item[3], item[4]))
        return result

    def select_detail_product_from_order(self, order_id, product_id):
        """
        get specific product info from the bill id, name, price, quantity, total_price
        """
        command = "SELECT product_id, product_name, product_price, quantity, order_products.total_price FROM " \
                  "order_products INNER JOIN orders USING (Order_ID ) INNER JOIN product_data USING (product_id) " \
                  "where order_products.Order_ID = '%s' and order_products.Product_ID = '%s'" % (order_id, product_id)
        result = []
        cur = self.Storage.select_by_query(command)
        for item in cur:
            result.append(item)
        return result

    def drop(self):
        self.Storage.drop_table("order_products")

    def create(self):
        self.Storage.Create_table("order_product", "order_products")

    def select_all(self):
        return self.Storage.Select_all("order_products")
