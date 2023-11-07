import os
import wave
import time
import threading
import customtkinter as ctk
import pyaudio
import async_notes_generate
import asyncio
import record_audio_class

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ScribeGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Welcome to Scribe")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

         #welcome message
        self.welcome_label = ctk.CTkLabel(self.root, text="Welcome to Scribe", font=("Arial", 24, "bold"))
        self.welcome_label.pack(pady=10)

         #instructions
        self.instructions_label = ctk.CTkLabel(self.root,
                                           text="Click 'Record' to start recording your lecture.\n"
                                                "Click 'Stop' to end the recording and automatically\n"
                                                "download a notes file of the recording.",
                                           font=("Arial", 14), justify=ctk.LEFT)
        self.instructions_label.pack(pady=20) 

        #record button
        self.button = ctk.CTkButton(self.root, text="Record", font=("Arial", 15, "bold"),
                                command=self.button_click)
        self.button.pack(pady=10)

        #timer
        self.label = ctk.CTkLabel(self.root, text="00:00:00", font=("Arial", 20))
        self.label.pack(pady=10)

        self.recording = False
        self.filename = None
        self.processing_thread = None
        # Add a label for status messages
        self.status_label = ctk.CTkLabel(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.filename = 'my_recording.wav'
        self.recorder = record_audio_class.AudioRecorder(filename=self.filename, channels=1, subtype='PCM_24')
        self.recording_thread = None

        self.root.mainloop()


    def set_status(self, message):
        """Updates the status label with a given message."""
        self.status_label.configure(text=message)
        self.status_label.update()

    def button_click(self):
        if self.recording:
            self.set_status("Stopping recording, please wait...")
            self.recording = False
            self.button.configure(text="Record")
            self.recorder.stop()  # Stop the recording
            print("button: waiting for recording thread to finish")
            self.recording_thread.join()  # Wait for the recording thread to finish
            print("button: recording thread finished")
            self.recording_thread = None  # Clear the thread
            self.set_status("Processing... Please wait.")
            threading.Thread(target=self.between_callback).start() 

        else:
            self.set_status("Recording...")
            self.recording = True
            self.button.configure(text="Stop")
            self.start_time = time.time()
            self.recording_thread = threading.Thread(target=self.recorder.record)
            self.recording_thread.start()
            self.update_timer(self.start_time)

    #update timer
    def update_timer(self, start_time):
        if self.recording:
            passed = time.time() - start_time
            seconds = passed % 60
            mins = (passed // 60) % 60
            hours = (passed // 60) // 60
            self.label.configure(text=f"{int(hours):02d}:{int(mins):02d}:{int(seconds):02d}")
            self.root.after(1000, self.update_timer, start_time)

    def between_callback(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.save_audio_and_generate_notes())
        print("Async loop completed")
        self.set_status("Processing Finished")
        loop.close()
        return

    async def save_audio_and_generate_notes(self): 
        audio_file= open(self.filename, "rb")
        output_directory = "audio_chunks"
        chunk_length_ms = 5 * 60 * 1000  # 10 minutes in milliseconds
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, async_notes_generate.split_audio, self.filename, output_directory, chunk_length_ms)

        transcription = await async_notes_generate.transcribe_directory(output_directory)
        print(transcription)

        #delete audio file once we are done with it
        audio_file.close()
        try:
            audio_file.close()
            # Attempt to delete the file
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except Exception as e:
            print(f"Error deleting the file: {e}")

        notes = await async_notes_generate.generate_notes('gpt-3.5', transcription)
        print("save audio and notes generation completed")
        return
        
if __name__ == "__main__":
    ScribeGUI()