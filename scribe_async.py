import os
import time
import threading
import shutil
import customtkinter as ctk
from tkinter.constants import DISABLED, NORMAL 
from tkinter import filedialog
import async_notes_generate
import asyncio
import record_audio_class

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ScribeGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Welcome to Scribe")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        # welcome message
        self.welcome_label = ctk.CTkLabel(self.root, text="Scribe", font=("Arial", 24, "bold"))
        self.welcome_label.pack(pady=10)

        # record instructions
        self.instructions_label = ctk.CTkLabel(self.root,
                                           text="Click 'Record' to start recording your lecture.\n"
                                                "Click 'Stop' to end the recording and automatically\n"
                                                "download a notes file of the recording.",
                                           font=("Arial", 14), justify=ctk.LEFT)
        self.instructions_label.pack(pady=10) 

        # record button
        self.button = ctk.CTkButton(self.root, text="Record", state=NORMAL, font=("Arial", 15, "bold"),
                                command=self.button_click)
        self.button.pack(pady=1)

        # timer
        self.label = ctk.CTkLabel(self.root, text="00:00:00", font=("Arial", 20))
        self.label.pack(pady=20)

        # progress bar
        self.progressbar = ctk.CTkProgressBar(self.root, orientation="horizontal")
        self.progressbar.set(0)
        self.progressbar.pack(pady=20)

        # status messages
        self.status_label = ctk.CTkLabel(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=20)

        # upload instructions
        self.upload_label = ctk.CTkLabel(self.root,
                                           text="Or upload a .wav or .mp3 file to automatically\n"
                                                " download a notes file of the recording.",
                                           font=("Arial", 14), justify=ctk.LEFT)
        self.upload_label.pack(pady=10)

        # upload button
        self.upload = ctk.CTkButton(self.root, text="Upload", state=NORMAL, font=("Arial", 15, "bold"),
                                command=self.upload_click)
        self.upload.pack(pady=10)

        self.recording = False
        self.filename = None
        self.processing_thread = None

        # set up recorder class
        self.recorder = record_audio_class.AudioRecorder(filename='my_recording.wav', channels=1, subtype='PCM_24')
        self.recording_thread = None

        self.root.mainloop()

    # update status message
    def set_status(self, message):
        self.status_label.configure(text=message)
        self.status_label.update()

    # record button event
    def button_click(self):
        if self.recording:
            # disable record button while processing
            self.button.configure(state=DISABLED)
            self.set_status("Stopping recording, please wait...")
            self.recording = False
            self.button.configure(text="Record")
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
            self.upload.configure(state=DISABLED)
            self.set_status("Recording...")
            self.recording = True
            self.button.configure(text="Stop")
            self.start_time = time.time()
            self.recording_thread = threading.Thread(target=self.recorder.record)
            self.recording_thread.start()
            self.update_timer(self.start_time)
    
    #upload button event
    def upload_click(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3")])

        if file_path:
            # disable both buttons while processing
            self.button.configure(state=DISABLED)
            self.upload.configure(state=DISABLED)
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
            self.root.after(1000, self.update_timer, start_time)

    # async processing
    def between_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.save_audio_and_generate_notes())
        # enable both buttons after processing is done
        self.button.configure(state=NORMAL)
        self.upload.configure(state=NORMAL)
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

        await async_notes_generate.generate_notes('gpt-3.5', transcription)
        print("save audio and notes generation completed")
        return
        
if __name__ == "__main__":
    ScribeGUI()