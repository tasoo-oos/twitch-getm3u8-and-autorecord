# This code is based on tutorial by slicktechies modified as needed to use oauth token from Twitch.
# You can read more details at: https://www.junian.net/2017/01/how-to-record-twitch-streams.html
# original code is from https://slicktechies.com/how-to-watchrecord-twitch-streams-using-livestreamer/

# Only works for Streamlink version >= 1.3.0
# Please get the newest version using methods described in https://streamlink.github.io/install.html

# pyinstaller --onefile stream.py

import requests
import os
import time
import json
import sys
import subprocess
import datetime
import getopt


class TwitchRecorder:
    def __init__(self):
        # global configuration
        self.client_id = "jzkbprff40iqj646a697cyrvl0zt2m6"  # don't change this

        self.ffmpeg_path = 'ffmpeg'
        self.refresh = 1.0  # don't go too low like 0.5 sec! In fact 1.0 might still cause some troubles
        self.root_path = "C:\\Users\\tasoo\\PycharmProjects\\study"

        # user configuration
        self.username = "danz_59"
        self.quality = "best"

    def run(self):
        # path to finished video, errors removed
        self.processed_path = self.root_path

        # create directory for recordedPath and processedPath if not exist
        if (os.path.isdir(self.processed_path) is False):
            os.makedirs(self.processed_path)

        print("Checking for", self.username, "every", self.refresh, "seconds. Record with", self.quality, "quality.")
        self.loopcheck()


    def loopcheck(self):
        # while True:
        # status, info = self.check_user()
        #            if status == 2:
        #                print("Username not found or server error")
        #                time.sleep(self.refresh)
        # if status == 1:
        #     print(self.username, "is currently offline, checking again in", self.refresh, "seconds.")
        #     time.sleep(self.refresh)
        # else:  # even if the API query is errored (condition code 2), the recording must continue
        print(self.username, "online. Stream recording in session.")
        filename = self.username + " - " + datetime.datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss") + ".mp4"

        # clean filename from unecessary characters
        filename = "".join(x for x in filename if x.isalnum() or x in [" ", "-", "_", "."])

        recorded_filename = os.path.join(self.processed_path, filename)

        # start streamlink process
        subprocess.call(
            ["streamlink", "--twitch-disable-hosting", "--twitch-disable-ads", "twitch.tv/" + self.username,
             self.quality, "-o", recorded_filename])

        print("Recording stream is done. Going back to checking..")


def main(argv):
    twitch_recorder = TwitchRecorder()

    with open("settings.txt", 'rt') as f:
        twitch_recorder.quality = f.readline()
        twitch_recorder.root_path = f.readline()
    with open("record.txt", 'rt') as f:
        twitch_recorder.username = f.readline()

    print(twitch_recorder.quality, twitch_recorder.root_path, twitch_recorder.username)

    twitch_recorder.run()


if __name__ == "__main__":
    main(sys.argv[1:])
