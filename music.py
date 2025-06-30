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

    return temp_file

def play_audio(wav_path):
    import pyaudio
    import wave

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

def convert_to_wav(input_path, output_path):
    print("Converting to WAV...")
    subprocess.run(['ffmpeg', '-y', '-i', input_path, output_path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 music.py <youtube-url>")
        sys.exit(1)

    url = sys.argv[1]
    temp_name = f"/tmp/{uuid.uuid4()}"
    isYoutube: bool = False;

    try:
        if (url.startswith("http://") or
            url.startswith("https://")):
            filePath = download_audio(url, temp_name)
            isYoutube = True
        else:
            filePath = url
        if not filePath.endswith('.wav'):
            wavPath = os.path.splitext(filePath)[0] + ".wav"
            convert_to_wav(filePath, wavPath)
        play_audio(wavPath)
    finally:
        if os.path.exists(wavPath) and isYoutube:
            webmPath = os.path.splitext(filePath)[0] + ".webm"
            os.remove(wavPath)
            os.remove(webmPath)
