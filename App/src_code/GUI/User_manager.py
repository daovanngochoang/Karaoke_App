from tkinter import *
from tkinter import ttk
from Data_manager.User_manager_controller import user_manager_controller
from Data_manager.src.orders_manager import Order_manager


class UI_USER:
    def __init__(self, window):

        self.window = window
        self. window.geometry("1530x900")
        self.window.maxsize(1530, 900)
        self.window.title("App Payment")

        self.controller=user_manager_controller()
        self.order_manager = Order_manager()

        self.order_manager.delete_empty_bills()

        self.canvas = Canvas(self.window, width=1920, height=1080, bg="white", bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid()

        Frame(self.window, width=1010, height=610, bg="#505863").place(x=24, y=140)
        Display_main = Frame(self.window, width=1000, height=600, bg="white").place(x=29, y=145)

        self.order_show = ttk.Treeview(Display_main)
        self.canvas.create_window(29, 145, anchor=NW, window=self.order_show, width=1000, height=600)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 15))
        style.configure("Treeview", highlightthickness=0, bd=0, rowheight=50, font=('Calibri', 16))
        vsb = ttk.Scrollbar(self.order_show, orient="vertical", command=self.order_show.yview)
        vsb.pack(fill=Y, side=RIGHT)

        self.order_show.configure(yscrollcommand=vsb.set)
        self.order_show["columns"] = ("1", "2", "3", "4", "5")
        self.order_show['show'] = 'headings'

        self.order_show.column("1", width=5, anchor='c')
        self.order_show.column("2", width=200, anchor='c')
        self.order_show.column("3", width=200, anchor='c')
        self.order_show.column("4", width=200, anchor='c')
        self.order_show.column("5", width=200, anchor='c')

        self.order_show.heading("1", text="ID")
        self.order_show.heading("2", text="Tên phòng")
        self.order_show.heading("3", text="Người nợ")
        self.order_show.heading("4", text="Ngày" )
        self.order_show.heading("5", text="Tổng tiền")


        # button connect

        button_danh_thu = Button(self.window, text="Tổng bills ", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82",relief=FLAT, command = lambda : [self.order_manager.delete_empty_bills(), self.controller.tong_bill(self.order_show)])
        self.canvas.create_window(10, 70, anchor=NW, window=button_danh_thu, width=165, height=52)

        button_debtor = Button(self.window, text="Nợ ", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82",relief=FLAT, command = lambda : self.controller.no(self.order_show))
        self.canvas.create_window(200, 70, anchor=NW, window=button_debtor, width=165, height=52)

        button_total_bill = Button(self.window, text="thêm sản phẩm ", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82",relief=FLAT,command=self.controller.them_san_pham)
        self.canvas.create_window(400, 70, anchor=NW, window=button_total_bill, width=165, height=52)

        button_delete_data = Button(self.window, text="xóa", font=('Time New Roman', 17), bg="#505863",
                                   fg="#FFDC82", relief=FLAT, command = lambda : self.controller.delete_individual(self.order_show))
        self.canvas.create_window(600, 70, anchor=NW, window=button_delete_data, width=165, height=52)

        button_check_bill = Button(self.window, text="xem bill", font=('Time New Roman', 17), bg="#505863",
                                   fg="#FFDC82", relief=FLAT, command = lambda : self.controller.xem_bill(self.order_show, self.display_bill_user ))
        self.canvas.create_window(800, 70, anchor=NW, window=button_check_bill, width=165, height=52)

        button_clear_data = Button(self.window, text="xoá hết", font=('Time New Roman', 17), bg="#505863",fg="#FFDC82", relief=FLAT, command = lambda  : self.controller.delete_all(self.order_show))
        self.canvas.create_window(1000, 70, anchor=NW, window=button_clear_data, width=165, height=52)

        button_In_bill= Button(self.window, text="In Bill", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82",
                                   relief=FLAT, command = self.controller.print_bill)
        self.canvas.create_window(1230, 700, anchor=NW, window=button_In_bill, width=165, height=52)

        # frame show in user_manager
        Display_user = Frame(self.window, bg="#505863")
        self.canvas.create_window(1070, 160, anchor=NW, window=Display_user, width=420, height=530, )

        self.display_bill_user = Text(self.window, font=('Calibri', 13), bg="white", )
        self.canvas.create_window(1075, 165, anchor=NW, window=self.display_bill_user, width=400, height=520)

        scrollb = Scrollbar(Display_user, orient="vertical", command=self.display_bill_user.yview)
        scrollb.pack(side=RIGHT, fill=Y)
        self.display_bill_user['yscrollcommand'] = scrollb.set



root = Tk()
app = UI_USER(root)
root.mainloop()


