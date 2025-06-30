import sys
import os
import subprocess
import uuid
import pyaudio

def play_audio(wav_path):
    import wave
    import pyaudio

    chunk = 1024
    wf = wave.open(wav_path, 'rb')
    p = pyaudio.PyAudio()

    device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if "USB" in dev['name'] and dev['maxOutputChannels'] > 0:
            device_index = i
            print(f"Using output device {dev['name']} at index {i}")
            break

    if device_index is None:
        print("No USB audio output device found, using default output")
        device_index = None

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=device_index)

    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 music.py <youtube-url>")
        sys.exit(1)

    url = sys.argv[1]
    play_audio(url)
