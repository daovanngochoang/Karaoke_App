from Data_manager.src.Storage_data import Storage
from Data_manager.src.Order_detail_manager import Order_detail_manager
from Data_manager.src.orders_manager import Order_manager
from Data_manager.src.product_manager import product_manager
from Data_manager.src.time_control import time_control
from Data_manager.src.bill_manager import bill_manager
import numpy as np


# from GUI.tab import tab


class Controler:
    def __init__(self, room):

        self.order_control = Order_manager()
        self.product_control = product_manager()
        self.order_detail_control = Order_detail_manager()
        self.Storage = Storage()
        self.time_control = time_control()
        self.bill_control = bill_manager()

        # self.ui_control = ui_controller()

        self.bill_created = False
        self.order_id = None
        self.time_price = 0
        self.bill_name = ""
        self.product_id = None
        self.date = ""
        self.total_price = 0
        self.total_time = 0
        self.Order_name = ""
        self.path_file = ""
        self.origin_time_price = 0
        self.room_name = room


    def get_product_id(self, product_id, window, name):
        # get product id from button that display product
        window.config(text=name, font=('Helvetica 18 bold'))
        self.product_id = product_id
        return product_id

    def reset_text(self, window):
        window.config(text=" ")

    # get and set product quantity
    def get_quantity(self, spin_text):
        return int(spin_text.get())
    def set_quantity(self, spin_text, number):
        return spin_text.set(number)

    def get_debt(self, window):
        """
        get debtor
        :param window:
        :return:
        """
        debtor = window.get()
        debt_bill_name = self.bill_name + ".docx"
        new_path = self.bill_control.manage_debtor(self.order_id, debtor, self.path_file, debt_bill_name)
        if new_path != None:
            self.path_file = new_path

    def set_debt(self, window):
        window.delete(0, 'end')

    def insert_treview(self, trv, info):
        for dt in info:
            trv.insert("", 'end', iid=dt[0], values=(dt[0], dt[1], dt[2], dt[3], dt[4]))

    def tree_view_control(self, trv, product_id=None):
        if product_id == None:
            trv.delete(self.product_id)
        else:
            trv.delete(product_id)

    def delete_trv(self, trv):
        item = trv.selection()
        for i in item:
            trv.delete(i)
            self.order_detail_control.delete_product(i, self.order_id)

    def convert_date_format(self, date):
        final = ""
        for i in date:
            if i == "/":
                final += "_"
            else:
                final += i
        return final

    def add_product(self, spin_box_text, treeview):
        """
        if bill is not created => create bill
        and change bill_created to True
        + set order name = room + date + time (hours, minutes)
        + create + insert the order to database and get the order id
        + add product follow the order id
        + order quantity +1

        + insert to treeview
            - clear that item in treeview and re update if its exist in the treeview
        """
        quantity = self.get_quantity(spin_box_text)

        if not self.bill_created:
            self.date = self.time_control.get_current_time('date')  # get day
            date = self.convert_date_format(self.date)
            h, m = self.time_control.get_current_time().split(":")
            self.Order_name = self.bill_name = self.room_name + "_" + date + "-%s_%s" % (h, m)  # name = the room name
            self.order_id = self.order_control.insert(self.Order_name, None, self.date, None, None, None, None, None,
                                                      "orders")

            self.order_detail_control.insert(self.order_id, self.product_id, quantity)
            self.bill_created = True

        else:
            self.order_detail_control.insert(self.order_id, self.product_id, quantity)


        # insert to treeview
        infor = self.order_detail_control.select_detail_product_from_order(self.order_id, self.product_id)
        try:
            self.tree_view_control(treeview)
        except:
            pass
        self.insert_treview(treeview, infor)

    def delete_empty_bills(self):
        self.order_control.delete_empty_bills()



    def order_closing(self, window, treeview):
        """
        + get ending time
        + insert total time to database
        + calculate the total price
        + check debtor
        + close the order, write the product to the bill
        + display the bill
        + check if there is no product in the order then remove the order

        """

        self.end_time()
        # insert total time to database
        self.insert_total_time(self.order_id)
        # calculate total time
        self.calculate_total_price(self.order_id)
        # get the file path where the bill is created and show to the label
        self.path_file = self.bill_control.complete_bill(window, self.order_id, self.bill_name, self.date,
                                                         self.origin_time_price, self.total_price, self.total_time,
                                                         self.Storage.add_dot(int(self.time_price)))
        # check if the bill's total price is > 0
        total = self.order_control.get_price(self.order_id)
        # or self.Storage.remove_dot_to_number(total) == 0
        if total == "None" or total == "0" :
            self.order_control.delete(self.order_id)

    def clear_tree_view(self, treeview):
        # product_id = self.order_detail_control.select_detail_order(self.order_id)
        # for i in product_id:
        #     self.tree_view_control(treeview, i[0])
        # def delete_trv(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def In_bill(self, debtor_window, treeview, bill_window):
        """
        get debtor from the debtor window
        clear treeview and all display labels

        """
        # get debtor and clear debtor widget
        self.get_debt(debtor_window)
        self.set_debt(debtor_window)
        # print hard copy of the bill
        self.bill_control.in_Bill(self.path_file)
        # clear treeview && bill lable
        self.clear_tree_view(treeview)
        self.clear_bill(bill_window)
        # update the file path into database
        self.order_control.update_file(self.path_file, self.order_id)

        # set all variables to the initial
        self.bill_created = False
        self.order_id = None
        self.time_price = 0
        self.bill_name = ""
        self.product_id = None
        self.date = ""
        self.total_price = 0
        self.total_time = 0
        self.Order_name = ""
        self.path_file = ""
        self.origin_time_price = 0

    def time_start(self):
        """
        + get the current time
        + if the bill is not created => create the bill and change value to True
        :return:
        """
        # get time currently
        starting_time = self.time_control.get_current_time()
        # check bill status
        if self.bill_created == False:
            # get date, time => create the bill name = room + date + time
            self.date = self.time_control.get_current_time('date')  # get day
            date = self.convert_date_format(self.date)
            h, m = self.time_control.get_current_time().split(":")
            # same as add product function
            self.Order_name = self.bill_name = self.room_name + "_" + date + "-%s_%s" % (h, m)
            self.order_id = self.order_control.insert(self.Order_name, None, self.date, None, None, None, None, None,
                                                      "orders")
            self.bill_created = True


        self.order_control.update_start(starting_time, self.order_id)

    def end_time(self):
        # get the current ending time and update to database
        ending_time = self.time_control.get_current_time()
        self.order_control.update_end(ending_time, self.order_id)

    def insert_total_time(self, Order_id):
        # get the starting and ending time and estimate the time interval and calculate the price
        try:
            # get start and ending time
            start, end, total = self.order_control.get_time(Order_id)

            # estimate the total time interval & calculate the time price and update to database
            self.total_time, self.time_price = self.calculate_time_price(start, end)
            self.order_control.update_total_time(self.total_time, Order_id)


        except:
            # if they are not use the karaoke room but order products => set time price and total time == 0
            self.time_price = 0
            self.total_time = "0:00"

    def calculate_total_price(self, Order_ID):
        """
        calculate price belong to the order id
        """
        # get and calculate all price from all items of the order
        result = self.order_detail_control.get_all_price_of_order(Order_ID)

        # calculate all price
        total_product_price = 0
        for price in result:
            price = self.Storage.remove_dot_to_number(price)
            total_product_price += price

        #calculate total and add dot to the int and update to database
        self.total_price = self.time_price + total_product_price
        self.total_price = self.Storage.add_dot(int(self.total_price))
        self.order_control.update_price(self.total_price, Order_ID)

    def calculate_time_price(self, starting_time, ending_time):
        """
        estimate time price every 10 minutes
        :param starting_time:
        :param ending_time:
        :return:
        """
        time = self.time_control.time_estimate(starting_time, ending_time)
        sec = self.time_control.get_sec(time)
        total_time = sec / 60 / 10
        even_time = np.floor(total_time)

        # get directly time id in product_data
        origin_price = self.origin_time_price = self.product_control.get_price_by_name("thời gian")
        origin_price = self.Storage.remove_dot_to_number(origin_price)
        origin_price /= 6
        result = origin_price * even_time

        if (total_time - even_time) != 0:
            result += origin_price
        return time, result

    def clear_bill(self, window):
        window.delete('1.0', 'end')
