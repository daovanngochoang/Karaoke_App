import functools
from tkinter import ttk
from tkinter import *
from Data_manager.src.product_manager import product_manager
from Data_manager.src.bill_manager import bill_manager
from Data_manager.Controller import Controler
# from Data_manager.src.Order_detail_manager import Order_detail_manager
from Data_manager.src.time_control import time_control
from PIL import Image, ImageTk

class tab:
    def __init__(self, root, tab_parent, name, room_class = 'normal'):
        self.root = root
        self.tab_parent =tab_parent
        self.room_name = 1
        self.product_frame = False

        self.millisec = 00
        self.sec = 00
        self.min = 00
        self.time = 0

        self.room_class = 'normal'
        if room_class == 'VIP':
            self.room_class = 'VIP'


        self.product_manager1 = product_manager()
        self.bill_manage1 = bill_manager()
        self.control = Controler(name)
        self.time_control = time_control()


        self.tab1 = Frame(self.tab_parent)
        self.tab_parent.add(self.tab1, tex=name)
        self.tab_parent.pack(expand=1, fill="both")

        self.canvas = Canvas(self.tab1, width=1920, height=1080, bg="white", bd=0, highlightthickness=0, relief='ridge')
        self.canvas.grid()

        ## digital clock
        clock_label1 = Label(self.tab1, bg="white", fg="black", font=("Times", 40, 'bold'), borderwidth="2",
                             relief="groove")
        clock_label1.place(x=1170, y=5)




        # frame stopwatch
        # clock_frame1 = Label(self.tab1, text="0:0:0", bg="WHITE", fg='#C0B57D', font=("default", 40, "bold"))
        # clock_frame1.place()

        self.timer = Label(self.tab1, font=("times new roman", 40), fg="blue",
                      bg="white")
        self.timer.place(x=670, y=61, width=200, height=60)
        self.timer.config(text=f'{self.min}:{self.sec}:{self.millisec}')

        self.time_control.update_label1(clock_label1)

        # main label
        Frame(self.tab1, width=1010, height=610, bg="#505863").place(x=24, y=140)
        Display_main = Frame(self.tab1, width=1000, height=600, bg="white").place(x=29, y=145)

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
        self.order_show.heading("2", text="tên sản phẩm")
        self.order_show.heading("3", text="giá gốc")
        self.order_show.heading("4", text="số lượng ")
        self.order_show.heading("5", text="giá tiền ")



        # show frame bill
        Display = Frame(self.tab1, bg="#505863")
        self.canvas.create_window(1070, 160, anchor=NW, window=Display, width=420, height=530, )

        display_bill = Text(self.tab1, font=('Calibri', 13), bg="white", )
        self.canvas.create_window(1075, 165, anchor=NW, window=display_bill, width=400, height=520)

        scrollb = Scrollbar(Display, orient="vertical", command=display_bill.yview)
        scrollb.pack(side=RIGHT, fill=Y)
        display_bill['yscrollcommand'] = scrollb.set

        # button
        button_them = Button(self.tab1, text="Thêm ", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82", relief=FLAT,
                        command=self.add)
        self.canvas.create_window(20, 70, anchor=NW, window=button_them, width=130, height=52)

        # Display = Label(self.tab1, text="Phòng 1", font=('Time New Roman', 40), bg="white").place(x=680, y=3)
        self.room = Label(self.tab1, text=name, bg="white",  font=('Time New Roman', 40))
        self.room.place(x=670, y=0)

        button_xoa = Button(self.tab1, text="Xóa", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82", relief=FLAT,
                        command=lambda: self.control.delete_trv(self.order_show))
        self.canvas.create_window(160, 70, anchor=NW, window=button_xoa, width=130, height=52)

        debtor = Entry(self.tab1, bd=5, font=('Time New Roman', 16), bg="white", fg="black", justify='center')
        self.canvas.create_window(1110, 117, anchor=NW, window=debtor, width=350, height=40)

        Display_debtor = Label(self.tab1, text="tên người nợ ", font=('Time New Roman', 18), bg="white")
        self.canvas.create_window(1200, 83, anchor=NW, window=Display_debtor)

        button_batdau = Button(self.tab1, text="Bắt Đầu ", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82",
                        relief=FLAT,
                        command=lambda: [self.Start(), self.control.time_start()])
        self.canvas.create_window(20, 12, anchor=NW, window=button_batdau, width=130, height=52)



        button_ketthuc = Button(self.tab1, text="Tạm dừng", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82",
                        relief=FLAT,
                        command=lambda: self.Stop())


        self.canvas.create_window(160, 12, anchor=NW, window=button_ketthuc, width=130, height=52)
        button_xong = Button(self.tab1, text="xong", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82", relief=FLAT,
                        command=lambda: [self.Reset(),
                                         display_bill.delete("1.0", "end"),self.control.order_closing(display_bill, self.room_class)])
        self.canvas.create_window(300, 12, anchor=NW, window=button_xong, width=130, height=52)

        button_in_bill = Button(self.tab1, text="In Bill", font=('Time New Roman', 19), bg="#505863", fg="#FFDC82", relief=FLAT,
                        command=lambda: self.control.In_bill(debtor, self.order_show, display_bill))
        self.canvas.create_window(1250, 700, anchor=NW, window=button_in_bill, width=100, height=50)

    def Start(self):

        self.millisec += 1
        if self.millisec == 60:
            self.millisec = 0
            self.sec = self.sec + 1
        if self.sec == 60:
            self.sec = 0
            self.min = self.min + 1
        self.timer.config(text=f'{self.min}:{self.sec}:{self.millisec}')
        self.time = self.timer.after(1000, self.Start)

    def Stop(self):
        global time
        self.timer.after_cancel(self.time)

    def Reset(self):
        try:

            self.millisec = 00
            self.sec = 00
            self.min = 00
            self.timer.config(text=f'{self.min}:{self.sec}:{self.millisec}')
            self.timer.after_cancel(self.time)
        except:
            pass

    def add(self):
        # if self.product_frame == False:
            newWindow = Toplevel(self.root)
            newWindow.geometry("900x700")
            newWindow.maxsize(width=900, height=700)
            newWindow.title("sản phẩm")
            newWindow.configure(bg="white")

            # p1 = PhotoImage(file='../GUI/Main_image/logo.png')
            # # Icon set for program windowX
            # newWindow.iconphoto(False, p1)

            Label(newWindow, text="tên sản phẩm : ", font=('Time New Roman', 18), bg="white").place(
                x=20, y=2)

            Label(newWindow, text="số lượng : ", font=('Time New Roman', 18), bg="white").place(
                x=440, y=2)

            self.text_variable = IntVar()

            Spinbox(newWindow, font=('Time New Roman', 17), borderwidth="2", relief="groove", from_=1, to=100.0,
                    increment=1.0,
                    textvariable=self.text_variable).place(x=570, y=1, width=100, height=40)
            Button(newWindow, text="OK", font=('Time New Roman', 17), bg="#505863", fg="#FFDC82",
                   command=lambda: [self.control.add_product(self.text_variable, self.order_show), self.control.set_quantity(self.text_variable, 1),
                                    self.control.reset_text(frame_show_name)], relief=FLAT).place(x=700, y=5, width=80,
                                                                                                  height=30)

            # Create a Label
            Label(newWindow, text="chọn sản phẩm ", font=('Aerial 20 bold'), bg="white").place(x=300, y=60)

            # frame show name san pham
            frame_show_name = Label(newWindow, bg="white", borderwidth="2", relief="groove")
            frame_show_name.place(x=200, y=2, width=220, height=40)

            frame_container = Frame(newWindow)
            canvas_container = Canvas(frame_container, width=885, height=600, bg="#505863", bd=0, highlightthickness=0,
                                      relief='ridge')
            frame2 = Frame(canvas_container, bg="#505863")

            my_scrollbar = Scrollbar(frame_container, orient="vertical",
                                     command=canvas_container.yview)  # will be visible if the frame2 is to to big for
            # the canvas
            canvas_container.create_window((0, 0), window=frame2, anchor='nw')

            mylist = []
            for i in self.product_manager1.select_all():
                if i[1] != "thời gian" and i[1] != "thời gian(VIP)":
                    mylist.append((i[0], i[1], i[3]))
            col = 0
            row = 1

            dict = {}

            for item in mylist:
                if col == 7:
                    row += 1
                    col = 0
                # print(col)
                path = item[2]

                # Creating a photoimage object to use image
                image = Image.open(r"%s" % path)
                image = image.resize((110, 110), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image)
                dict[item[0]] = (img, item[1])

                button = Button(frame2, text=item[0], image=dict[item[0]][0],
                                command = functools.partial(self.control.get_product_id, item[0], frame_show_name, item[1]))
                button.grid(row=row, column=col, padx=5, pady=5)
                col += 1

            frame2.update()
            canvas_container.configure(yscrollcommand=my_scrollbar.set,
                                       scrollregion="0 0 0 %s" % frame2.winfo_height())
            canvas_container.pack(side=LEFT, fill=BOTH)
            my_scrollbar.pack(side=RIGHT, fill=Y)

            # This is windows code for scrolling the Frame
            def _on_mousewheel(event):
                canvas_container.yview_scroll(int(-1 * (event.delta / 120)), "units")

            def _bind_to_mousewheel(event):
                canvas_container.bind_all("<MouseWheel>", _on_mousewheel)

            def _unbind_from_mousewheel(event):
                canvas_container.unbind_all("<MouseWheel>", )

            frame_container.place(y=100)
            canvas_container.bind_all("<MouseWheel>", _on_mousewheel)
            canvas_container.bind('<Enter>', _bind_to_mousewheel)
            canvas_container.bind('<Leave>', _unbind_from_mousewheel)

            self.product_frame = True
            newWindow.mainloop()

