import os
import wave
import time
import threading
import customtkinter as ctk
import pyaudio
import notes_generate
import record_audio

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AudioRecorder:
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
        self.root.mainloop()

    #button click event
    def button_click(self):
        if self.recording:
            self.recording = False
            self.button.configure(text="Record")
            record_audio.stop_recording()
            self.save_audio_and_generate_notes()
        else:
            self.recording = True
            self.button.configure(text="Stop")
            self.start_time = time.time()
            threading.Thread(target=self.record).start()
            self.update_timer(self.start_time)


    #update timer
    def update_timer(self, start_time):
        if self.recording:
            passed = time.time() - start_time
            seconds = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.configure(text=f"{int(hours):02d}:{int(mins):02d}:{int(seconds):02d}")
            self.root.after(1000, self.update_timer, start_time)


    #record audio
    def record(self):
        self.filename = "speech.wav"
        if os.path.exists(self.filename):
            os.remove(self.filename)

        device_index = notes_generate.find_microphone()
    
        record_audio.record_audio(filename=self.filename, device=device_index, samplerate=16000, channels=1, subtype='PCM_24')
        start_time = time.time()
        self.update_timer(start_time)

        
    #save audio and generate notes
    def save_audio_and_generate_notes(self):
        audio_file= open(self.filename, "rb")
        output_directory = "audio_chunks"
        chunk_length_ms = 5 * 60 * 1000  # 10 minutes in milliseconds
        
        #create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        notes_generate.split_audio(audio_file, output_directory, chunk_length_ms)

        transcription = notes_generate.transcribe_directory(output_directory)
        print(transcription)

        #delete audio file once we are done with it
        audio_file.close()
        try:
            audio_file.close()
            #attempt to delete the file
            if os.path.exists(self.filename):
                os.remove(self.filename)
        except Exception as e:
            print(f"Error deleting the file: {e}")

        notes_generate.generate_notes('gpt-3.5', transcription)

AudioRecorder()