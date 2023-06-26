
import tkinter as tk
from tkinter import ttk
import re


class LogViewer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.treeview = ttk.Treeview(self, columns=("time", "level", "message"), show="headings")
        self.treeview.heading("time", text="Time")
        self.treeview.heading("level", text="Level")
        self.treeview.heading("message", text="Message")
        self.treeview.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        self.filter_entry = ttk.Entry(self)
        self.filter_entry.pack(side="top", fill="x")
        self.filter_entry.bind("<KeyRelease>", self.filter_logs)

        self.logs = []

    def load_logs(self, filename):
        with open(filename, "r") as f:
            logs = f.readlines()

        for log in logs:

            match = re.match(r"^\[(.*)\] \[(.*)\] (.*)$", log)

            if match:
                time = match.group(1)
                level = match.group(2)
                message = match.group(3)
                self.logs.append((time, level, message))

        self.update_treeview()

    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())

        for log in self.logs:
            self.treeview.insert("", "end", values=log)


    def filter_logs(self, event=None):
        filter_text = self.filter_entry.get().lower()
        filtered_logs = []

        for log in self.logs:
            if filter_text in log[2].lower():
                filtered_logs.append(log)

        self.treeview.delete(*self.treeview.get_children())

        for log in filtered_logs:
            self.treeview.insert("", "end", values=log)

root = tk.Tk()
log_viewer = LogViewer(root)
log_viewer.pack(fill="both", expand=True)
log_viewer.load_logs("access_logs.log")
root.mainloop()