# record_audio.py
import argparse
import tempfile
import queue
import sys
import sounddevice as sd
import soundfile as sf
import numpy
assert numpy

is_recording = True

def record_audio(filename=None, device=None, samplerate=None, channels=1, subtype=None):
    global is_recording
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    if samplerate is None:
        device_info = sd.query_devices(device, 'input')
        samplerate = int(device_info['default_samplerate'])
    if filename is None:
        filename = tempfile.mktemp(prefix='delme_rec_unlimited_', suffix='.wav', dir='')

    with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                        channels=channels, subtype=subtype) as file:
        with sd.InputStream(samplerate=samplerate, device=device,
                            channels=channels, callback=callback):
            print('#' * 80)
            print('Recording')
            print('#' * 80)
            while is_recording:
                try:
                    file.write(q.get())
                except queue.Empty:
                    pass

def stop_recording():
    global is_recording
    is_recording = False
    print('\nRecording stopped')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a recording with arbitrary duration.")
    parser.add_argument('filename', nargs='?', metavar='FILENAME', help='audio file to store recording to')
    parser.add_argument('-d', '--device', type=int, help='input device (numeric ID)')
    parser.add_argument('-r', '--samplerate', type=int, help='sampling rate')
    parser.add_argument('-c', '--channels', type=int, default=1, help='number of input channels')
    parser.add_argument('-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
    args = parser.parse_args()

    try:
        record_audio(args.filename, args.device, args.samplerate, args.channels, args.subtype)
    except KeyboardInterrupt:
        stop_recording()
        print('\nRecording stopped')