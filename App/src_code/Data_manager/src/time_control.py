
from time import strftime

from  datetime import datetime


class time_control:
    def __init__(self):
        self.time1_elapsed1 = 0
        self.time1_elapsed2 = 0
        self.time1_elapsed3 = 0
        self.i1 = 0
        self.j1 = 0
        self.time1 = 0


    def update_label1(self, window):
        current_time = strftime('%H: %M: %S')
        window.configure(text=current_time)
        window.after(80, self.update_label1, window)


    def get_sec(self, time_str):
        """Get Seconds from time."""
        h, m = time_str.split(':')
        return int(h) * 3600 + int(m) * 60

    def time_estimate(self, starting_time, ending_time):
        """
        :param starting_time: start time
        :param ending_time: end time
        :return: the time interval between start and ending time
        """
        FMT = '%H:%M' # time format
        time_delta = datetime.strptime(ending_time, FMT) - datetime.strptime(starting_time, FMT)
        new_time_del = ''
        count = 0
        for i in str(time_delta): # get h:m remove sec
            if i == ":":
                count += 1
            if count == 2:
                break
            new_time_del += i

        len_time = len(new_time_del)
        final_time = ""
        if len_time > 5:  # for example 1 day 0:59 => get 0:59
            for i in range(1, 6):
                final_time += new_time_del[len_time - i]

            final_time = final_time[::-1]

            return final_time
        return new_time_del

    def get_current_time(self, option="time"):
        time_format = ""
        import datetime
        if option == "time":
            time_format = "%H:%M"

        if option == "date":
            time_format = '%x'

        time = datetime.datetime.now().strftime(time_format)
        return str(time)