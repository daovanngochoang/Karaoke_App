import csv

from Data_manager.src.Storage_data import Storage


class product_manager:
    def __init__(self):
        self.storage = Storage()

    def insert(self, name, price, image, Stt, table="product_data"):
        # generate id
        id = self.storage.ID_generating(table, 'product_id')
        remake_path = "GUI/Main_image/" + image
        dot_price = self.storage.add_dot(price)

        if not self.storage.check_exist("product_name", name, table):

            query =  "INSERT INTO %s (product_id, product_name, product_price, image, Stt) VALUE ('%s','%s','%s','%s','%s')"%(table, id, name, dot_price, remake_path, Stt)
            self.storage.execute_query(query)
            print("Successfully insert product!: %s price :%s" % (name, dot_price))


    @staticmethod
    def read_product_format_xlsx(xlsx_file):
        import openpyxl

        wb = openpyxl.load_workbook(xlsx_file)
        sheet = wb.active
        result = []
        # read all info from the file and insert
        for col in sheet.iter_cols():
            for row_value_num in range(2, len(col) + 5):
                if sheet["A" + str(row_value_num)].value is not None:
                    result.append((sheet["A" + str(row_value_num)].value, sheet["B" + str(row_value_num)].value, sheet["C" + str(row_value_num)].value, sheet["D" + str(row_value_num)].value))
            break

        return result

    def read_file_and_insert_product(self, file_name, option2= "default",option='xlsx'):
        if option2 == "default":
            data_dir = "../Data_manager/Data/"
        else:
            data_dir = ""

        file_path = data_dir+file_name
        if option == "xlsx":
            data = self.read_product_format_xlsx(file_path)
            for element in data:
                self.insert(element[0], element[1], element[2], element[3])

        elif option == "csv":
            with open(file_path, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    print(f'\t{row["Tên"]} and {row["giá"]} ')
                    self.insert(row["Tên"], row["giá"], row["ảnh"], row["Stt"])
                    line_count += 1
                print(f'Processed {line_count} lines.')

        return id

    def delete(self, product_id, table="product_data"):
        self.storage.Storage_delete("product_id", product_id, table)

    def search_full_info(self, product_id):
        """
        full information by id
        :return:
        """
        result = self.storage.Storage_search("product_id", product_id, table="product_data")
        return result

    def select_all(self):
        cur = self.storage.Select_all("product_data", ordered_col= "Stt")
        return cur

    def get_name(self, product_id):
        result = self.storage.Storage_search("product_id", product_id, table="product_data")
        return result[0][1]

    def get_price(self, product_id):
        result = self.storage.Storage_search("product_id", product_id, table="product_data")
        return result[0][2]

    def update_name(self, new_name, id):
        self.storage.Storage_update("product_name", new_name, "product_id", id)

    def update_price(self, new_price, id):
        self.storage.Storage_update("product_price", new_price, "product_id", id)

    def update_image(self, new_img, id):
        self.storage.Storage_update("product_image", new_img, "product_id", id)

    def create_table(self):
        self.storage.Create_table("product", "product_data")

    def clear_table(self):
        self.storage.delete_all("product_data")

    def drop(self):
        self.storage.drop_table("product_data")

    def get_price_by_name(self, name):
        result = self.storage.Storage_search("product_name", name, table="product_data")
        return result[0][2]


