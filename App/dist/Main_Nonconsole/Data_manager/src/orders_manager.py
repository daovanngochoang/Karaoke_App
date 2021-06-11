from Data_manager.src.Storage_data import Storage


class Order_manager:
    def __init__(self):
        self.storage = Storage()

    def insert(self, Order_name, debtor, Order_day, Order_starting_time, Order_ending_time, total_time,
               total_price, bill_file,table="orders"):
        # gererate id
        id = self.storage.ID_generating(table, 'Order_ID')

        command = "INSERT INTO {} (Order_ID, Order_name, debtor, Order_day, Order_starting_time, Order_ending_time," \
                  "total_time, total_price, bill_file) VALUE ('%s','%s','%s','%s','%s','%s','%s','%s','%s')".format(table)%(id,
                                                                                                            Order_name, debtor, Order_day, Order_starting_time, Order_ending_time, total_time, total_price, bill_file)

        self.storage.execute_query(command)
        print("Successfully insert order %s at %s" % (Order_name, Order_starting_time))

        return id

    def search_all_order_info(self, order_id, table="orders"):
        result = self.storage.Storage_search("Order_ID", order_id, table)
        return result

    def select_all(self):
        cur = self.storage.Select_all("orders")
        result = []
        count = 0
        for order in cur:
            result.append(order)
            count += 1
        return count, result

    def get_debtor(self, order_id, table="orders"):
        """
        get the debtor from bill
        :param order_id:
        :param table:
        :return:
        """
        result = self.search_all_order_info(order_id, table)
        return result[0][2]

    def show_bill_infor_and_calculate_total(self):
        quantity, bills = self.select_all()
        total = 0
        info = []
        for bill in bills:
            total += self.storage.remove_dot_to_number(bill[7])
            info.append((bill[0],bill[1],bill[2],bill[3],bill[7]))
        return quantity, info, self.storage.add_dot(total)



    def get_name(self, order_id, table="orders"):
        """
        get the bill's name
        :param order_id:
        :param table:
        :return:
        """
        result = self.search_all_order_info(order_id, table)
        return result[0][1]

    def get_time(self, order_id, table="orders"):
        """
        return start, end, total

        """
        result = self.search_all_order_info(order_id, table)
        return result[0][4], result[0][5], result[0][6]

    def get_price(self, order_id, table="orders"):
        result = self.search_all_order_info(order_id, table)
        return result[0][7]

    def get_location(self, order_id, table="orders"):
        result = self.search_all_order_info(order_id, table)
        return result[0][8]


    def update_start(self, start_time, Order_ID, table="orders"):
        """
        this update starting time
        :param start_time:
        :param Order_ID:
        :param table:
        :return:
        """
        self.storage.Storage_update("Order_ID", Order_ID,"Order_starting_time", start_time, table)

    def update_end(self, end_time, Order_ID, table="orders"):
        """
        this update ending time
        :param end_time:
        :param Order_ID:
        :param table:
        :return:
        """
        self.storage.Storage_update( "Order_ID", Order_ID,"Order_ending_time", end_time, table)

    def update_total_time(self, new_total, Order_ID, table="orders"):
        """
        update total time
        :param new_total:
        :param Order_ID:
        :param table:
        :return:
        """
        self.storage.Storage_update("Order_ID", Order_ID, "total_time", new_total, table)

    def update_price(self, new_price, Order_ID, table="orders"):
        self.storage.Storage_update("Order_ID", Order_ID, "total_price", new_price, table)

    def update_debtor(self, new_debtor, Order_ID, table="orders"):
        self.storage.Storage_update("Order_ID", Order_ID,"debtor", new_debtor,table)

    def update_file(self, new_file, Order_ID, table="orders"):
        self.storage.Storage_update("Order_ID", Order_ID,"bill_file", new_file,table)

    def delete(self, Order_ID, table="orders"):
        self.storage.Storage_delete("Order_ID", Order_ID, table)

    def get_debtor_bills(self):
        result = self.select_all()[1]
        debtor_bills = []
        quantity = 0
        total = 0
        for bill in result:

            if bill[2] != 'None' :
                debtor_bills.append((bill[0],bill[1],bill[2],bill[3],bill[7]))
                quantity+=1
                total += self.storage.remove_dot_to_number(bill[7])

        total = self.storage.add_dot(total)
        return quantity, total, debtor_bills




    def delete_empty_bills(self):
        command = "DELETE FROM orders WHERE total_price = 'None' OR total_price = '0'"
        self.storage.execute_query(command)
        print("delete all empty bills")

    def create_table(self):
        self.storage.Create_table("order", "orders")

    def clear_table(self):
        self.storage.delete_all("orders")

    def drop(self):
        self.storage.drop_table("orders")
