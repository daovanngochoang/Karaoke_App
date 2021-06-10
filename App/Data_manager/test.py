from Data_manager.src.product_manager import product_manager
from Data_manager.src.bill_manager import bill_manager
from Data_manager.src.Order_detail_manager import Order_detail_manager
from Data_manager.src.orders_manager import Order_manager
from Data_manager.src.time_control import time_control
from Data_manager.Controller import Controler



order = Order_manager()
order_manage = Order_detail_manager()
product = product_manager()
control = Controler(None)
time_control1 = time_control()
print(order_manage.select_all())
product.drop()
product.create_table()
# product.read_file_and_insert_product("data.xlsx")
#
order_manage.drop()
order_manage.create()
order.drop()
order.create_table()
# #
# order.delete('6e04ba57-298e-4856-8cef-f0')
print(order.select_all())
print(order_manage.select_all())




# print(product.select_all())
#
# bill = bill_manager()
# total = "\t\t\tTổng : 10,000,000"
# date = "\n\t\t\tNgày : 23/06/2001"
# control.add_product('0a3-3aea-43bd-8e20-488ea6b', 5)
# control.add_product('0a3-3aea-43bd-8e20-488ea6b', 7)
# control.add_product('0fa4-4b3f-af20-a98076a24d7', 5)
# control.add_product('0a3-3aea-43bd-8e20-488ea6b', 5)
# control.add_product('1495edf-8c4e-4adf-a904-823', 5)
# control.add_product('290fa-6c84-4e9a-b162-e5b1c', 5)
# control.add_product('5377d-8038-4e20-ad53-6242c', 5)
#
# info = order_manage.select_detail_order(control.order_id)
#
#
# bill.insert_row_and_value("../Data_manager/bill_form/Form_bill.docx" ,'../Data_manager/testmotherfuker.docx', info )

# bill.add_infor("../Data_manager/bill_form/Form_bill.docx", control.bill_name, None, font_size=9, text= total+date)
# bill.add_infor("../Data_manager/bill_form/Form_bill.docx", control.bill_name, None, font_size=9, text= total+date)


# start = time_control1.get_current_time()
# print(start)
# end = '00:00'
# time = time_control1.time_estimate(start, end)
# time_control1.get_sec(time)
# print(type (time_control1.time_estimate(start, end)))