import subprocess
import os
import time

def convert_video(video_input, video_output):
    cmds = ['ffmpeg', '-i', video_input, video_output]
    subprocess.Popen(cmds)

a = os.listdir('state_videos/fry/')
b = [f for f in a if f.endswith('avi')]

for v in b:
    video_in = 'state_videos/fry/' + v
    video_out = 'state_videos/fry/' + v[:-4] + '.mp4'
    if os.path.exists(video_out)：
    	continue
    convert_video(video_in, video_out)
    time.sleep(5)