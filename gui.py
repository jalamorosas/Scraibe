import os
import wave
import time
import threading
import tkinter as tk
import pyaudio


class AudioRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x300")
        self.root.resizable(False, False)
        self.button = tk.Button(text="record", font=("Arial", 15, "bold"),
                                command=self.button_click)
        self.button.pack()
        self.label = tk.Label(text="00:00:00", font=("Arial", 20))
        self.label.pack()
        self.root.mainloop()


    def button_click(self):
        pass


AudioRecorder()