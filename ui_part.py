import time
import tkinter as tk
from random import choice
from tkinter import ttk

from multiprocessing import Process, get_context
from threading import Thread
import asyncio

from request_functionality import Requests
from auth_page import Authorization
from database import Database
from email_part import Email


class MyApp:
    def __init__(self, master):
        self.tracking_process = None
        self.periodical_proc = None
        self.rows = []

        self.frame = tk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.section1 = tk.Frame(self.frame, height=100, borderwidth=1, relief=tk.SUNKEN)

        self.section1.pack(fill=tk.BOTH, expand=True)
        self.create_section_1()

    def create_section_1(self):
        self.insert_user_section = tk.Frame(self.section1, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.insert_user_section.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.username_label = tk.Label(self.insert_user_section, text="Username", fg="black")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_field = tk.Entry(self.insert_user_section)
        self.username_field.grid(row=1, column=0, padx=10, pady=10)

        self.password_label = tk.Label(self.insert_user_section, text="Password", fg="black")
        self.password_label.grid(row=0, column=1, padx=10, pady=10)
        self.password_field = tk.Entry(self.insert_user_section)
        self.password_field.grid(row=1, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self.insert_user_section, text='Submit',
                                       command=self.submit_button_functionality)
        self.submit_button.grid(row=1, column=2, padx=10, pady=10)

        self.tracking_with_telegram_section = tk.Frame(self.section1, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.tracking_with_telegram_section.grid(row=0, column=1, padx=10, pady=10, sticky="nw")
        self.sender_email_label = tk.Label(self.tracking_with_telegram_section, text="Sender Email", fg="black")
        self.sender_email_label.grid(row=0, column=0, padx=10, pady=10)

        self.sender_email_field = tk.Entry(self.tracking_with_telegram_section)
        self.sender_email_field.grid(row=1, column=0, padx=10, pady=10)

        self.sender_email_password_label = tk.Label(self.tracking_with_telegram_section, text="Sender Email Password",
                                                    fg="black")
        self.sender_email_password_label.grid(row=0, column=1, padx=10, pady=10)

        self.sender_email_password_field = tk.Entry(self.tracking_with_telegram_section)
        self.sender_email_password_field.grid(row=1, column=1, padx=10, pady=10)

        self.recever_email_label = tk.Label(self.tracking_with_telegram_section, text="Recipient Email", fg="black")
        self.recever_email_label.grid(row=2, column=0, padx=10, pady=10)

        self.recever_email_field = tk.Entry(self.tracking_with_telegram_section)
        self.recever_email_field.grid(row=3, column=0, padx=10, pady=10)

        self.start_tracking_button = tk.Button(self.tracking_with_telegram_section, text='Start',
                                               command=self.start_tracking_functionality)
        self.start_tracking_button.grid(row=3, column=1, padx=10, pady=10)

        self.stop_tracking_button = tk.Button(self.tracking_with_telegram_section, text='Stop',
                                              command=self.stop_tracking_functionality)
        self.stop_tracking_button.grid(row=3, column=2, padx=10, pady=10)

        # self.save_email_and_password_button = tk.Button(self.tracking_with_telegram_section, text='Save',
        #                                                 command=self.save_email_and_password_functionality)
        # self.save_email_and_password_button.grid(row=1, column=2, padx=10, pady=10)

        self.periodical_requests_section = tk.Frame(self.section1, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.periodical_requests_section.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        self.periodical_requests_delay_label = tk.Label(self.periodical_requests_section,
                                                        text="Requests Delay Value/40 Seconds",
                                                        fg="black")
        self.periodical_requests_delay_label.grid(row=4, column=0, padx=10, pady=10)

        self.periodical_requests_delay__field = tk.Entry(self.periodical_requests_section)
        self.periodical_requests_delay__field.grid(row=5, column=0, padx=10, pady=10)

        self.periodical_requests_duration_label = tk.Label(self.periodical_requests_section,
                                                           text="Requests Duration Seconds",
                                                           fg="black")
        self.periodical_requests_duration_label.grid(row=6, column=0, padx=10, pady=10)
        self.periodical_requests_duration__field = tk.Entry(self.periodical_requests_section)
        self.periodical_requests_duration__field.grid(row=7, column=0, padx=10, pady=10)

        self.periodical_requests_start_button = tk.Button(self.periodical_requests_section, text='Start',
                                                          command=self.periodical_requests_start_functionality)
        self.periodical_requests_start_button.grid(row=5, column=1, padx=10, pady=10)

        self.periodical_requests_stop_button = tk.Button(self.periodical_requests_section, text='Stop',
                                                         command=self.periodical_requests_stop_functionality)
        self.periodical_requests_stop_button.grid(row=5, column=2, padx=10, pady=10)

        self.fast_request_section = tk.Frame(self.section1, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.fast_request_section.grid(row=2, column=1, padx=10, pady=10, sticky="nw")
        self.fast_requests_count_label = tk.Label(self.fast_request_section, text="Fast Requests Count",
                                                  fg="black")
        self.fast_requests_count_label.grid(row=6, column=0, padx=10, pady=10)

        self.fast_requests_count_field = tk.Entry(self.fast_request_section)
        self.fast_requests_count_field.grid(row=7, column=0, padx=10, pady=10)

        self.fast_requests_start_button = tk.Button(self.fast_request_section, text='Start',
                                                    command=lambda: self.fast_requests_start_functionality())
        self.fast_requests_start_button.grid(row=7, column=1, padx=10, pady=10)

        self.log_window_section = tk.Frame(self.section1, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.log_window_section.grid(row=0, column=3, columnspan=5, rowspan=10, padx=20, pady=1, sticky="nw")
        self.log_window = tk.Text(self.log_window_section, width=40, height=30)
        self.log_window.grid(row=0, column=0)
        self.set_free_rows()
        self.user_table_section = tk.Frame(self.section1, bd=2, relief=tk.GROOVE, padx=10, pady=10)
        self.user_table_section.grid(row=1, column=0, rowspan=20, padx=10, pady=10, sticky="nw")
        self.canvas = tk.Canvas(self.user_table_section)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.user_table_section, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.user_table_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.user_table_frame, anchor="nw")
        self.user_table_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.config(width=450, height=400)

        self.create_by_users()
        self.sync_db_button = tk.Button(self.section1, text='Sync User Chances',
                                        command=self.sync_db_functionality)
        self.sync_db_button.grid(row=3, column=1, padx=10, pady=10, sticky="nw")

    def log_to_log_window(self, log):
        pass

    def set_free_rows(self):
        self.row1 = tk.Label(self.section1, text="")
        self.row1.grid(row=0, column=20, padx=10, pady=10)
        self.row2 = tk.Label(self.section1, text="")
        self.row2.grid(row=1, column=20, padx=10, pady=10)
        self.row3 = tk.Label(self.section1, text="")
        self.row3.grid(row=2, column=20, padx=10, pady=10)
        self.row4 = tk.Label(self.section1, text="")
        self.row4.grid(row=3, column=20, padx=10, pady=10)
        self.row5 = tk.Label(self.section1, text="")
        self.row5.grid(row=4, column=20, padx=10, pady=10)
        self.row6 = tk.Label(self.section1, text="")
        self.row6.grid(row=5, column=20, padx=10, pady=10)
        self.row7 = tk.Label(self.section1, text="")
        self.row7.grid(row=6, column=20, padx=10, pady=10)
        self.row8 = tk.Label(self.section1, text="")
        self.row8.grid(row=7, column=20, padx=10, pady=10)
        self.row9 = tk.Label(self.section1, text="")
        self.row9.grid(row=8, column=20, padx=10, pady=10)
        self.row10 = tk.Label(self.section1, text="")
        self.row10.grid(row=9, column=20, padx=10, pady=10)
        self.row11 = tk.Label(self.section1, text="")
        self.row11.grid(row=10, column=20, padx=10, pady=10)
        self.row12 = tk.Label(self.section1, text="")
        self.row12.grid(row=11, column=20, padx=10, pady=10)
        self.row13 = tk.Label(self.section1, text="")
        self.row13.grid(row=12, column=20, padx=10, pady=10)
        self.row14 = tk.Label(self.section1, text="")
        self.row14.grid(row=13, column=20, padx=10, pady=10)
        self.row15 = tk.Label(self.section1, text="")
        self.row15.grid(row=14, column=20, padx=10, pady=10)
        self.row16 = tk.Label(self.section1, text="")
        self.row16.grid(row=15, column=20, padx=10, pady=10)
        self.row17 = tk.Label(self.section1, text="")
        self.row17.grid(row=16, column=20, padx=10, pady=10)
        self.row18 = tk.Label(self.section1, text="")
        self.row18.grid(row=1, column=2, padx=10, pady=10)

    def create_by_users(self):
        db = Database()
        user_list = db.get_all_users_from_db()
        start_row = 0
        self.create_table(start_row, user_list)

    def start_tracking_functionality(self):
        if self.tracking_process:
            self.log_window.insert(tk.END, 'Tracking for changes is already started!...\n')
        else:
            self.tracking_process = Process(target=self.tracking)
            self.log_window.insert(tk.END, 'Tracking for changes started!...\n')
            self.tracking_process.start()

    def stop_tracking_functionality(self):
        if self.tracking_process:
            self.tracking_process.terminate()
            self.log_window.insert(tk.END, 'Tracking for changes stopped!...\n')
            self.tracking_process = None

    def tracking(self):
        while True:
            rec = Requests()
            period = 2
            if len(self.rows) > 0:
                user_id = choice(self.rows)[2].cget('text')
                start_json = rec.get_prize_chance_count(user_id=user_id)
                self.log_window.insert(tk.END, 'Waiting 30 seconds!...\n')
                result = rec.tracking_request(period=period, user_id=user_id, start_json=start_json)
                mail = Email()

                mail.send_mail(self.sender_email_field.get(), self.sender_email_password_field.get(),
                               self.recever_email_field.get(), result)

    def periodical_requests_start_functionality(self):
        if self.periodical_proc:
            self.log_window.insert(tk.END, 'Periodical requests is already started!...\n')
        else:
            self.periodical_proc = Process(target=self.periodical)
            self.periodical_proc.start()
            self.log_window.insert(tk.END, 'Periodical requests is started!...\n')

    def periodical(self):
        value = self.periodical_requests_delay__field.get()
        self.log_window.insert(tk.END, f'Periodical requests delay is {value}!...\n')
        duration = self.periodical_requests_duration__field.get()
        self.log_window.insert(tk.END, f'Periodical requests duration is {duration}!...\n')
        true_rows = self.get_checkbox_values()
        if value.isnumeric():
            period = float(value)
            if duration.isnumeric():
                int_duration = int(duration)
                if true_rows:
                    user = choice(true_rows)
                    asyncio.run(Requests().request_periodical(user=user, user_list=true_rows, period=period,
                                                              duration=int_duration))

        else:
            self.log_window.insert(tk.END, 'period should be a number!...\n')

    def periodical_requests_stop_functionality(self):
        if self.periodical_proc:
            self.periodical_proc.terminate()
            self.log_window.insert(tk.END, f'Periodical requests process is stopped!...\n')
            self.periodical_proc = None

    def fast_requests_start_functionality(self):
        user_list = self.get_checkbox_values()
        user = choice(user_list)
        count = self.fast_requests_count_field.get()
        if count.isdigit():
            rec = Requests()
            asyncio.run(rec.request(count=int(count), user=user, user_list=user_list))

    def sync_db_functionality(self):
        req = Requests()
        for var, checkbox, user_id_header, username_header, chance_count_header, delete_button in self.rows:
            data = req.get_prize_chance_count(user_id=user_id_header.cget('text'))
            spinids = data.get("SpinIds")
            if spinids:
                chance_count = spinids.get('avialable_try')
                db = Database()
                db.update_value_in_table(chance_count=chance_count,
                                         user_id=user_id_header.cget('text'))
                chance_count_header.config(text=chance_count)
        self.log_window.insert(tk.END, 'Users chances is synced!...\n')

    def submit_button_functionality(self):
        self.submit_proc = Thread(target=self.submit)
        self.submit_proc.start()

    def submit(self):
        start_column = 0
        chance_count = 0
        auth = Authorization()
        username = self.username_field.get()
        password = self.password_field.get()
        self.log_window.insert(tk.END, f'Authorization is started for {username} please wait several seconds....\n')
        auth.authorization(username, password)
        message, user_id = auth.write_user_in_db()
        self.log_window.insert(tk.END, f'Status of adding user {username} is {message}....\n')
        if user_id:
            row = len(self.rows)
            var, checkbox, user_id_header, username_header, chance_count_header, delete_button = self.create_row(row,
                                                                                                                 username,
                                                                                                                 user_id,
                                                                                                                 chance_count,
                                                                                                                 start_column)
            self.rows.append([var, checkbox, user_id_header, username_header, chance_count_header, delete_button])

    def get_checkbox_values(self):
        self.true_row_list = []
        for row in self.rows:
            if row[0].get():
                self.true_row_list.append(row)
        return self.true_row_list

    def create_table(self, start_column, user_list):
        self.rows = []
        row = 0
        for id, username, password, user_id, chance_count in user_list:
            var, checkbox, user_id_header, username_header, chance_count_header, delete_button = self.create_row(row,
                                                                                                                 username,
                                                                                                                 user_id,
                                                                                                                 chance_count,
                                                                                                                 start_column)
            self.rows.append([var, checkbox, user_id_header, username_header, chance_count_header, delete_button])
            row += 1

    def create_row(self, row, username, user_id, chance_count, start_column):
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(self.user_table_frame, text='', variable=var)
        checkbox.grid(row=row, column=start_column, padx=10, pady=10)
        user_id_header = tk.Label(self.user_table_frame, text=f"{user_id}", fg="black")
        user_id_header.grid(row=row, column=start_column + 1, padx=10, pady=10)
        username_header = tk.Label(self.user_table_frame, text=f"{username}", fg="black")
        username_header.grid(row=row, column=start_column + 2, padx=10, pady=10)
        chance_count_header = tk.Label(self.user_table_frame, text=f"{chance_count}", fg="black")
        chance_count_header.grid(row=row, column=start_column + 3, padx=10, pady=10)

        delete_button = tk.Button(self.user_table_frame, text='Delete',
                                  command=lambda row=row: self.delete_functionality(row))
        delete_button.grid(row=row, column=start_column + 4, padx=10, pady=10)
        return var, checkbox, user_id_header, username_header, chance_count_header, delete_button

    def add_functionality(self):
        pass

    def delete_functionality(self, row):
        db = Database()
        db.delete_user_from_table(id=self.rows[row][2].cget('text'), username=self.rows[row][3].cget('text'))

        for widget in self.rows[row][1:]:
            widget.grid_remove()


if __name__ == '__main__':
    try:
        root = tk.Tk()
        # root.attributes('-zoomed', True)
        app = MyApp(root)
        root.mainloop()
    except Exception as e:
        print(e)
