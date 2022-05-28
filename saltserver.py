import os
import string
import time
from random import choices, choice

raspis = [
    'raspi-e4:5f:01:56:d9:a2',
    'raspi-e4:5f:01:72:9e:28',
    'raspi-e4:5f:01:75:6b:35',
    'raspi-e4:5f:01:56:d9:a3',
    'raspi-e4:5f:01:56:d8:fc',
    'raspi-e4:5f:01:75:6b:2c',
    'raspi-e4:5f:01:72:89:99',
    'raspi-e4:5f:01:75:ae:8d',
]

videos = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=WglgwAwaW1g',
    'https://www.youtube.com/watch?v=f_WqZjy8T5M',
    'https://www.youtube.com/watch?v=0w6kXdHXxAA',
    'https://www.youtube.com/watch?v=tmNXKqeUtJM',
]

DURATION = 120
SLEEP_INTERVAL = 1200

iteration = 0
while True:
    print('Iteration: {}'.format(iteration))
    for device in raspis:
        os.system(f"salt '{device}' cmd.run 'killall Xvfb'")
        video = choice(videos)
        folder = ''.join(choices(string.ascii_lowercase, k=10))
        cmd = f"salt '{device}' cmd.run 'cd kell/pinot_minion_tasks && xvfb-run python3 example.py {video} {DURATION} {folder}' --async"
        os.system(cmd)
        time.sleep(1)
    print('Sleeping for {} seconds'.format(SLEEP_INTERVAL))
    time.sleep(SLEEP_INTERVAL)
