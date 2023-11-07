import sounddevice as sd
import soundfile as sf
import queue
import threading

class AudioRecorder:
    def __init__(self, filename, device=None, samplerate=16000, channels=1, subtype=None):
        self.filename = filename
        self.device = device
        self.samplerate = samplerate
        self.channels = channels
        self.subtype = subtype
        self.recording = threading.Event()
        self.recording.set()
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def record(self):
        self.recording.set()
        # Set device_info and samplerate if not set
        if self.samplerate is None:
            device_info = sd.query_devices(self.device, 'input')
            self.samplerate = int(device_info['default_samplerate'])

        with sf.SoundFile(self.filename, mode='x', samplerate=self.samplerate,
                          channels=self.channels, subtype=self.subtype) as file:
            with sd.InputStream(samplerate=self.samplerate, device=self.device,
                                channels=self.channels, callback=self.callback):
                print('Recording...')
                while self.recording.is_set():
                    try:
                        file.write(self.q.get(timeout=0.5))
                    except queue.Empty:
                        pass
                print('Recording stopped.')

    def stop(self):
        self.recording.clear()
