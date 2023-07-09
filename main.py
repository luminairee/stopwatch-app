import tkinter as tk
from tkinter import *
from tkinter import messagebox
import func


class Stopwatch:
    def __init__(self, master):
        self.master = master
        self.seconds = 0
        self.time_string = 0
        self.process_name = ''
        self.is_running = True
        self.time_label = tk.Label(master, text='', font=('Arial', 26))
        self.time_label.pack()
        self.frame = tk.Frame()
        self.scrollbar = tk.Scrollbar(self.frame, orient=VERTICAL)
        self.listbox = tk.Listbox(self.frame, width=100, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.frame.pack()
        self.listbox.pack(pady=15)
        self.btn_frame = tk.Frame(self.master)
        self.btn = tk.Button(self.btn_frame, text='Choose', command=self.select_item)
        self.btn.pack(side=TOP, padx=5, pady=5, fill=BOTH)
        self.btn_exit = tk.Button(self.btn_frame, text='Stop', command=self.save_Time)
        self.btn_exit.pack(side=TOP, padx=5, pady=5, fill=BOTH)
        self.btn_refresh = tk.Button(self.btn_frame, text='Refresh', command=self.fill_listbox)
        self.btn_refresh.pack(side=TOP, padx=5, pady=5, fill=BOTH)
        self.btn_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
        self.fill_listbox()

    def fill_listbox(self):
        for item in func.getProcessList():
            self.listbox.insert(END, item)

        if not self.process_name:
            self.btn_exit.config(state=DISABLED)

    def save_Time(self):
        if not self.process_name:
            self.time_label.config(text='Choose process.')
            return
        
        self.is_running = False
        try:
            with open(f'{self.process_name}.txt', 'a') as file:
                file.write(f'{self.time_string}\n')
        except FileNotFoundError:
            with open(f'{self.process_name}.txt', 'x') as file:
                file.write(f'{self.time_string}\n')

        self.sum_times()
        self.master.destroy()

    def get_total_time(self):
        total_time = 0
        try:
            with open(f'{self.process_name}.txt', 'r') as file:
                for line in file:
                    total_time += int(line.strip())
        except FileNotFoundError:
            pass
        return total_time

    def sum_times(self):
        total_seconds = 0
        with open(f'{self.process_name}.txt', 'r') as file:
            for line in file:
                time_string = line.strip()  
                time_parts = time_string.split(':')  
                hours = int(time_parts[0])
                minutes = int(time_parts[1])
                seconds = int(time_parts[2])
                total_seconds += hours * 3600 + minutes * 60 + seconds

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_time_string = f'{hours:02d}:{minutes:02d}:{seconds:02d}'

        messagebox.showinfo('Stopwatch', f'All the time spent in {self.process_name} is: {total_time_string}')
        
    def update_time(self):
        if self.is_running:
            self.seconds += 1
            hours = self.seconds // 3600
            remaining_seconds = self.seconds % 3600
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            self.time_string = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            self.time_label.config(text=self.time_string)
            self.master.update()
            self.master.after(1000, self.update_time)
            if minutes == 0 and seconds == 0:
                self.seconds = hours * 3600  

    

    def select_item(self):
        if len(self.listbox.curselection()) == 0:
            self.time_label.config(text='Choose process.')
            return
        else:
            self.btn_exit.config(state=NORMAL)

        for i in self.listbox.curselection():
            if self.listbox.get(i) in func.getProcessList():
                self.process_name = self.listbox.get(i)
                self.update_time()
                self.btn.config(state=DISABLED)
                self.btn_refresh.config(state=DISABLED)
                return


root = tk.Tk()
root.title('Stoper')
root.resizable(False, False)
root.iconbitmap('icon.ico')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry('260x370+{}+{}'.format(screen_width // 2-100, screen_height // 2 - 185))
stoper = Stopwatch(root)
root.mainloop()