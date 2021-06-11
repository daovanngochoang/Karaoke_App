import uuid  # module for generating Unique ids
import mysql.connector  # My sql connector python lib


class Storage:
    def __init__(self):

        self.cur = None
        self.db = None
        self.__time = 10

        # sql command to create table with its columns
        self.__create_product_table_command = "CREATE TABLE IF NOT EXISTS {} (product_id varchar(60) NOT NULL PRIMARY KEY , product_name VARCHAR(100),product_price varchar (100), image varchar(150), Stt int)"
        self.__create_Order_table_command = "CREATE TABLE IF NOT EXISTS {} (Order_ID varchar(60) NOT NULL PRIMARY KEY , Order_name VARCHAR(100), debtor VARCHAR(100),  Order_day varchar(20), Order_starting_time varchar(20), Order_ending_time varchar(20), total_time varchar(20), total_price varchar(100), bill_file varchar(500))"
        self.__create_order_product_table_command = "CREATE TABLE IF NOT EXISTS {} (Order_ID varchar(60) , Product_ID VARCHAR(60), quantity int,  total_price varchar(100))"

    # function to connect to mysql
    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="karaoke_admin",
                password="karaoke_admin@123",
                database="karaoke_data")

            self.cur = self.db.cursor()

        except mysql.connector.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

    def Create_table(self, option, table_name):
        """
        option include "product" which tell the function to create a table for product,
        "order_product" is the option to tell the function to 
        create the table of order products and "order" option to create orders table.
        """
        # connect to database and execute command
        self.connect()
        if (option == "product"):
            self.cur.execute(self.__create_product_table_command.format(table_name))

        elif (option == "order_product"):
            self.cur.execute(self.__create_order_product_table_command.format(table_name))

        else:
            self.cur.execute(self.__create_Order_table_command.format(table_name))

        self.db.commit()
        self.db.close()

    # to show all tables in database
    def show_table(self):
        sql = "show tables"
        self.connect()
        self.cur.execute(sql)
        result = []
        for i in self.cur:
            result.append(i)

        self.db.commit()
        self.db.close()
        return result

    def drop_table(self, table):
        self.connect()
        try:
            self.cur.execute("DROP TABLE {}".format(table))
            print("successfully drop table %s" % (table))
        except:
            print("table not exist")
        self.db.commit()
        self.db.close()

    def Select_all(self, table, ordered_col=None):
        self.connect()
        command = "SELECT * FROM {}".format(table)
        if ordered_col != None:
            command = "SELECT * FROM %s order by %s " % (table, ordered_col)
        self.cur.execute(command)
        all_in = []

        for i in self.cur:
            all_in.append(i)

        self.db.commit()
        self.db.close()

        return all_in

    # check if item is exist in the table
    def check_exist(self, key, value, table):
        """
        key: field to check
        value : the value of the field to check
        example : the key is product_id and the value is the id that we want to check
        """
        self.connect()

        Command = "SELECT * FROM %s WHERE %s = '%s'" % (table, key, value)

        self.cur.execute(Command)
        result = []

        # add items in the cur in to the list
        for i in self.cur:
            result.append(i)

        self.db.commit()
        self.db.close()

        if len(result) > 0:  # check the list len, if > 0 that mean the item is exist
            return True

        return False

    def ID_generating(self, table, option):  # generating ID by the method of uuid.

        id = ''
        exist = True
        while (exist == True):
            id = str(uuid.uuid4()) # use the uuid4 method
            exist = self.check_exist(option, id, table)  # check if the id is unique

        if (self.__time == 0):
            self.__time = 10

        finalid = id[10 - self.__time:len(id) - self.__time]   # cut the id

        user_id = ""

        # remove the '-' outside of the id
        if finalid[0] != "-" and finalid[- 1] != "-":
            user_id = finalid
        elif finalid[0] == "-" and finalid[- 1] != "-":
            user_id += finalid[1:]
        elif finalid[-1] == "-" and finalid[0] != "-":
            user_id += finalid[:-1]
        else:
            user_id += finalid[1:-1]

        self.__time -= 1
        return user_id

    def Storage_update(self, option, option_value, field, newval, db):
        """

        :param option: this is the filed that we use to find the item
        :param option_value: the value of the field
        :param field: this is the one that we want to update
        :param newval: this is the new value
        :param db: this is the table
        :return:
        """
        self.connect()
        command = "UPDATE %s SET %s = '%s' WHERE %s= '%s'"
        val = (db, field, newval, option, option_value)
        sql = command % (val)

        self.cur.execute(sql)
        self.db.commit()
        self.db.close()
        return

    def Storage_search(self, option, value, table):

        """
        option: which field to search.
        value: value of the desired searching field.
        table: table to search.

        """
        self.connect()
        out_put = []
        count = 0

        try:
            sql = "SELECT * FROM %s WHERE %s = '%s'" % (table, option, value)
            self.cur.execute(sql)

        except:
            pass

        for i in self.cur:
            out_put.append(i)
            count += 1
        self.db.commit()
        self.db.close()
        # print(out_put)
        return out_put

    def Storage_delete(self, option, option_value, table):
        """
        option is the field that you want to delete
        and option value is the target that you want to select for removing
        :param option:
        :param option_value:
        :param table:
        :return:
        """

        sql = "SELECT * FROM %s  WHERE %s = '%s'" % (table, option, option_value)
        command = "DELETE FROM %s  WHERE %s = '%s'" % (table, option, option_value)

        a = self.check_exist(option, option_value, table)

        if not a:
            print("%s not exist !" % (option_value))

        else:
            self.connect()
            self.cur.execute(sql)

            status = "successfully deleted %s: " % (option_value)

            self.connect()
            self.cur.execute(command)
            self.db.commit()
            self.db.close()
            print(status)

    def back_up(self, data):

        return

    def delete_all(self, table):
        self.connect()
        self.cur.execute("DELETE * FROM %s")
        self.db.commit()
        self.db.close()

    def execute_query(self, query):
        self.connect()
        self.cur.execute(query)
        self.db.commit()
        self.db.close()

    def select_by_query(self, query):
        result = []
        self.connect()
        try:
            self.cur.execute(query)
            for i in self.cur:
                result.append(i)
            print("Sucessfully execute comand !")

        except:
            print("command does not work !")

        self.db.close()

        return result

    def remove_dot_to_number(self, string_number):
        string = ''
        for i in string_number:
            if i.isnumeric():
                string += i
        return int(string)

    # add dot to the number
    def add_dot(self, number):
        to_str = str(number)
        dot_added = ''
        count = 0
        lenn = len(to_str)
        for i in range(1, lenn + 1):
            if count == 3:
                dot_added += ","
                count = 0
            dot_added += to_str[-i]
            count += 1

        dot_added = dot_added[::-1]
        return dot_added


