from pytube import YouTube
import subprocess
import os
import re

# Get the video link and preferred resolution from user
link = input("Video link: ")
res = input("Preferred video resolution: ")

# Download the video file
yt = YouTube(link)
video_files = yt.streams
d_file = video_files.filter(resolution=res).order_by('resolution')[-1]
title = d_file.title
title = re.sub('\W+', ' ', title)
d_file.download(output_path='temp', filename='temp_v')

# Download the audio file
audio_files = yt.streams.filter(only_audio=True)
audio_files = audio_files.order_by('abr')
audio_files[-1].download(output_path='temp', filename='temp_a')

# Merge the files
files = os.listdir('temp')
for f in files:
    if 'temp_v' in f:
        vid = 'temp\\' + f
        ext = f[6:]
    if 'temp_a' in f:
        aud = 'temp\\' + f
cmd = 'ffmpeg -i ' + vid + ' -i ' + aud + \
    ' -c:v copy -c:a copy "' + title + ext + '"'
subprocess.call(cmd, shell=True)

# Delete temporary files
for f in files:
    os.remove('temp\\' + f)
