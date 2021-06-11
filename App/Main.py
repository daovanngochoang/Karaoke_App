from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook

from GUI.tab import tab
from Data_manager.src.orders_manager import Order_manager


class UI_window_fullHD:
    def __init__(self, master):
        self.id = None
        self.product_id = None
        self.room_name = 1

        self.master = master
        self. master.geometry("1530x900")
        self.master.maxsize(1530, 900)
        self.master.title("Karaoke App")
        self.order_manager = Order_manager()

        self.order_manager.delete_empty_bills()


        # p1 = PhotoImage(file='GUI/Main_image/logo.png')
        # # Icon set for program windowX
        # master.iconphoto(False, p1)
        # create control TAB
        self.customed_style = ttk.Style()
        self.customed_style.configure('.', padding=[2, 0], font=('Helvetica', 15))


        self.tab_paren = Notebook(master)
        tab(self.master, self.tab_paren, "Phòng 1")
        tab(self.master, self.tab_paren, "Phòng 2")
        tab(self.master, self.tab_paren, "Phòng 3")
        tab(self.master, self.tab_paren, "Phòng 4")
        tab(self.master, self.tab_paren, "Phòng 5")
        tab(self.master, self.tab_paren, "Phòng 6(VIP)", room_class="VIP")
        tab(self.master, self.tab_paren, "Phòng 7(VIP)", room_class="VIP")
        tab(self.master, self.tab_paren, "Phòng 8(VIP)", room_class="VIP")
        tab(self.master, self.tab_paren, "Phòng 9(VIP)", room_class="VIP")
        tab(self.master, self.tab_paren, "Phòng 10(VIP)", room_class="VIP")


root = Tk()
app = UI_window_fullHD(root)
root.mainloop()





