from tkinter import *
from tkinter import ttk
import time


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Progress Bar")
        self.minsize(640, 400)
        self.wm_iconbitmap('icon.ico')

        self.buttonFrame = ttk.LabelFrame(self, text="Progress Bar")
        self.buttonFrame.grid(column=0, row=0)

        self.progressBar()

    def progressBar(self):
        self.button1 = ttk.Button(self.buttonFrame, text="Start Progress Bar", command = self.start_progress)
        self.button1.grid(column=0, row=0)

        self.button2 = ttk.Button(self.buttonFrame, text="Stop Progress Bar", command = self.stop_progress)
        self.button2.grid(column=0, row=1)

        self.progress_bar = ttk.Progressbar(self, orient=HORIZONTAL, length=286, mode='determinate')
        self.progress_bar.grid(column=0, row=2, pady=10)

    def run_progressBar(self):
        self.progress_bar['maximum'] = 100

        for i in range(101):
            time.sleep(0.05)
            self.progress_bar["value"] = i
            self.progress_bar.update()

        self.progress_bar["value"] = 0

    def start_progress(self):
        self.progress_bar.start()

    def stop_progress(self):
        self.progress_bar.stop()


root = Root()
root.mainloop()
