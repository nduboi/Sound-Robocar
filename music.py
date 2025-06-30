import sys
import os
import subprocess
import uuid
import wave
import pyaudio
import yt_dlp

def download_audio(url, output_path):
    temp_file = output_path + ".webm"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': temp_file,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading audio from: {url}")
        ydl.download([url])

    # Convert to WAV
    wav_file = output_path + ".wav"
    print("Converting to WAV...")
    subprocess.run(['ffmpeg', '-y', '-i', temp_file, wav_file],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(temp_file)
    return wav_file

def play_audio(wav_path):
    import pyaudio
    import wave

    chunk = 1024
    wf = wave.open(wav_path, 'rb')
    p = pyaudio.PyAudio()

    # Trouver l'index de la carte son USB (nom contient "USB")
    device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if "USB" in dev['name'] and dev['maxOutputChannels'] > 0:
            device_index = i
            print(f"Using output device {dev['name']} at index {i}")
            break

    if device_index is None:
        print("No USB audio output device found, using default output")
        device_index = None  # Laisser par défaut

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
    temp_name = f"/tmp/{uuid.uuid4()}"
    
    try:
        wav_path = download_audio(url, temp_name)
        play_audio(wav_path)
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)
