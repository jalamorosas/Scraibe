import os
import time
import threading
import shutil
import customtkinter as ctk
from tkinter.constants import *
from tkinter import filedialog
import async_notes_generate
import asyncio
import record_audio_class

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ScribeGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # window configuration
        self.title("Scribe - AI Notetaking")
        self.geometry("575x450")
        self.resizable(False, False)

        # grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # create sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row = 0, column=0, rowspan=5, sticky="nsew")
        self.welcome_label = ctk.CTkLabel(self.sidebar_frame, text="Scribe  📝", font=("Arial", 30, "bold"))
        self.welcome_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # sidebar buttons
        self.model_label = ctk.CTkLabel(self.sidebar_frame, text="Model:", anchor="w", font=("Arial", 14))
        self.model_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        self.model_menu = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["gpt-3.5", "gpt-4", "davinci"])
        self.model_menu.grid(row=2, column=0, padx=20, pady=10)
        self.file_type_label = ctk.CTkLabel(self.sidebar_frame, text="File Type:", anchor="w", font=("Arial", 14))
        self.file_type_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        self.file_type_menu = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["Markdown file", "Text file"])
        self.file_type_menu.grid(row=4, column=0, padx=20, pady=10)

        # record frame
        self.record_frame = ctk.CTkFrame(self)
        self.record_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.record_frame.grid_columnconfigure(0, weight=1)
       

        self.record_label = ctk.CTkLabel(self.record_frame, text="Record", font=("Arial", 20, "bold"))
        self.record_label.grid(row=0, column=0, padx=0, pady=10, sticky="")

        # second: record button
        self.record_button = ctk.CTkButton(self.record_frame, text="Start", state=NORMAL, font=("Arial", 15, "bold"),
                                command=self.button_click)
        self.record_button.grid(row=1, column=0, padx=(0, 0), pady=(30, 0)) 

        # third: timer
        self.label = ctk.CTkLabel(self.record_frame, text="00:00:00", font=("Arial", 20))
        self.label.grid(row=2, column=0, padx=(0, 0), pady=(10, 0), sticky="nsew")
        
        # upload frame
        self.upload_frame = ctk.CTkFrame(self)
        self.upload_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.upload_frame.columnconfigure(0, weight=1)

        self.upload_label = ctk.CTkLabel(self.upload_frame, text="Upload", font=("Arial", 20, "bold"))
        self.upload_label.grid(row=0, column=0, padx=0, pady=10, sticky="")

        # upload button
        self.upload_button = ctk.CTkButton(self.upload_frame, text="Browse", state=NORMAL, font=("Arial", 15, "bold"),
                                command=self.upload_click)
        self.upload_button.grid(row=1, column=0, padx=(0, 0), pady=(30, 0))

        # progress bar
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.set(0)
        self.progressbar.grid(row=2, column=1, padx=(20, 20), pady=(10, 0), sticky="nsew")
        
        # status messages
        self.status_label = ctk.CTkLabel(self, text="Record or upload a file", font=("Arial", 12))
        self.status_label.grid(row=3, column=1, padx=(0, 0), pady=(0, 2), sticky="")

        # recording setup
        self.recording = False
        self.filename = None

        # set up recorder class
        self.recorder = record_audio_class.AudioRecorder(filename='my_recording.wav', channels=1, subtype='PCM_24')
        self.recording_thread = None

    # update status message
    def set_status(self, message):
        self.status_label.configure(text=message)
        self.status_label.update()

    # record button event
    def button_click(self):
        if self.recording:
            # disable record button while processing
            self.record_button.configure(state=DISABLED)
            self.set_status("Stopping recording, please wait...")
            self.recording = False
            self.record_button.configure(text="Record")
            self.recorder.stop()  # Stop the recording
            print("button: waiting for recording thread to finish")
            self.recording_thread.join()  # Wait for the recording thread to finish
            print("button: recording thread finished")
            self.recording_thread = None  # Clear the thread
            self.progressbar.set(0)
            self.progressbar.start()
            self.set_status("Processing... Please wait.")
            self.filename = 'my_recording.wav'
            threading.Thread(target=self.between_callback).start() 

        else:
            # disable upload button while recording
            self.upload_button.configure(state=DISABLED)
            self.set_status("Recording...")
            self.recording = True
            self.record_button.configure(text="Stop")
            self.start_time = time.time()
            self.recording_thread = threading.Thread(target=self.recorder.record)
            self.recording_thread.start()
            self.update_timer(self.start_time)
    
    #upload button event
    def upload_click(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")])

        if file_path:
            # disable both buttons while processing
            self.record_button.configure(state=DISABLED)
            self.upload_button.configure(state=DISABLED)
            self.progressbar.set(0)
            self.progressbar.start()
            self.set_status("Processing... Please wait.")
            self.filename = os.path.basename(file_path)

            # make a copy of the file in the current directory
            new_file_path = os.path.join(os.getcwd(), self.filename)
            shutil.copy(file_path, new_file_path)
            self.filename = self.filename
            threading.Thread(target=self.between_callback).start()

    # update timer
    def update_timer(self, start_time):
        if self.recording:
            passed = time.time() - start_time
            seconds = passed % 60
            mins = (passed // 60) % 60
            hours = (passed // 60) // 60
            self.label.configure(text=f"{int(hours):02d}:{int(mins):02d}:{int(seconds):02d}")
            self.after(1000, self.update_timer, start_time)

    # async processing
    def between_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.save_audio_and_generate_notes())
        # enable both buttons after processing is done
        self.record_button.configure(state=NORMAL)
        self.upload_button.configure(state=NORMAL)
        print("Async loop completed")
        self.progressbar.set(100)
        self.progressbar.stop()
        self.set_status("Processing Finished")
        loop.close()
        return

    # save audio and generate notes
    async def save_audio_and_generate_notes(self): 
        # prepare audio for chunking before passing to whisper for transcription
        audio_file= open(self.filename, "rb")
        output_directory = "audio_chunks"
        chunk_length_ms = 5 * 60 * 1000  # 10 minutes in milliseconds
        
        # create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, async_notes_generate.split_audio, self.filename, output_directory, chunk_length_ms)

        transcription = await async_notes_generate.transcribe_directory(output_directory)
        print(transcription)

        # delete audio file once we are done with it
        try:
            audio_file.close()
            # attempt to delete the file
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except Exception as e:
            print(f"Error deleting the file: {e}")
        
        model_selected = self.model_menu.get()
        file_type_selected = self.file_type_menu.get()
        if file_type_selected == "Markdown file":
            note_type = "md"
        else:
            note_type = "txt"
        await async_notes_generate.generate_notes(model_selected, note_type, transcription)
        return
        
if __name__ == "__main__":
    app = ScribeGUI()
    app.mainloop()