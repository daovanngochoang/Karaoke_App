from tkinter import filedialog

from  Data_manager.src.orders_manager import Order_manager
from Data_manager.src.product_manager import product_manager
from Data_manager.src.bill_manager import bill_manager
from Data_manager.src.Order_detail_manager import Order_detail_manager
from Data_manager.Controller import Controler
class user_manager_controller:
    def __init__(self):
        self.order_control=Order_manager()
        self.product_control=product_manager()
        self.bill_control=bill_manager()
        self.controller = Controler("")
        self.order_detail_control = Order_detail_manager()

        self.info = None
        self.deb_bills = None
        self.location = None
        self.status = ""
    def tong_bill(self, trv):

        self.delete_trv(trv)
        quantity, self.info, total = self.order_control.show_bill_infor_and_calculate_total()
        self.controller.insert_treview(trv, self.info)
        total_and_quantity = [ ("1"," "," ","số lượng bill", quantity), ("2"," "," ","Tổng Tiền", total),]
        self.controller.insert_treview(trv, total_and_quantity)
        self.status = "all"



    def delete_trv(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)



    def no(self, trv):
        self.delete_trv(trv)
        quantity, total, self.deb_bills = self.order_control.get_debtor_bills()
        total_and_quantity = [("1", " ", " ", "số lượng bill", quantity), ("2", " ", " ", "Tổng Tiền", total), ]
        self.controller.insert_treview(trv, self.deb_bills)
        self.controller.insert_treview(trv, total_and_quantity)

        self.status = "no"


    def delete_individual(self, trv):
        id = trv.selection()
        for i in id:
            try:
                trv.delete(i)
                self.order_control.delete(i)
                self.order_detail_control.delete_product_from_order(i)
            except:
                pass

    def delete_all(self, trv):
        trv.delete("1")
        trv.delete("2")
        if self.status == "all":
            for i in self.info:
                trv.delete(i[0])
                self.order_control.delete(i[0])
                self.order_detail_control.delete_product_from_order(i[0])
        elif self.status == "no":
            for i in self.deb_bills:
                trv.delete(i[0])
                self.order_control.delete(i[0])
                self.order_detail_control.delete_product_from_order(i[0])




    def xem_bill(self, trv, show_bill_widget):
        try:
            self.controller.clear_bill(show_bill_widget)
        except:
            pass
        id = trv.selection()[0]
        self.location = self.order_control.get_location(id)
        self.bill_control.show_bill_to_label(show_bill_widget, self.location)

    def print_bill(self):
        self.bill_control.in_Bill(self.location)


    def them_san_pham(self):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Text files",
                                                          "*.xlsx*"),
                                                         ("all files",
                                                          "*.*")))

        self.product_control.read_file_and_insert_product(filename, option2="")
        return

