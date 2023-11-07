import os
import wave
import time
import threading
import customtkinter as ctk
import pyaudio
import notes_generate

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AudioRecorder:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Welcome to Scraibe")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

         #welcome message
        self.welcome_label = ctk.CTkLabel(self.root, text="Welcome to Scraibe", font=("Arial", 24, "bold"))
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
        self.frames = []
        self.audio = None
        self.stream = None
        self.root.mainloop()


    def button_click(self):
        if self.recording:
            self.recording = False
            self.button.configure(text="Record")
            threading.Thread(target=self.save_audio_and_generate_notes).start()
        else:
            self.recording = True
            self.button.configure(text="Stop")
            threading.Thread(target=self.record).start()

    def record(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format = pyaudio.paInt16, channels = 1, rate = 44100,
                            input = True, frames_per_buffer = 1024)
        
        self.frames = []
        start_time = time.time()

        while self.recording:
            data = self.stream.read(1024)
            self.frames.append(data)

            passed = time.time() - start_time
            seconds = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.configure(text=f"{int(hours):02d}:{int(mins):02d}:{int(seconds):02d}")

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def save_audio_and_generate_notes(self):
        filename = f"recorded_audio_{time.strftime('%Y%m%d%H%M%S')}.wav"

        recorded_file = wave.open(filename, "wb")
        recorded_file.setnchannels(1)
        recorded_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        recorded_file.setframerate(44100)  # Sample rate
        recorded_file.writeframes(b''.join(self.frames))
        recorded_file.close()
        print(f"Audio saved as {recorded_file}")
        
        audio_file= open(filename, "rb")
        output_directory = "audio_chunks"
        chunk_length_ms = 5 * 60 * 1000  # 10 minutes in milliseconds
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        notes_generate.split_audio(audio_file, output_directory, chunk_length_ms)

        transcription = notes_generate.transcribe_directory(output_directory)
        print(transcription)

        #delete audio file once we are done with it
        audio_file.close()
        try:
            audio_file.close()
            # Attempt to delete the file
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f"Error deleting the file: {e}")

        notes_generate.generate_notes('gpt-3.5', transcription)

AudioRecorder()