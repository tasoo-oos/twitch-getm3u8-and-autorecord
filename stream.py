# This code is based on tutorial by slicktechies modified as needed to use oauth token from Twitch.
# You can read more details at: https://www.junian.net/2017/01/how-to-record-twitch-streams.html
# original code is from https://slicktechies.com/how-to-watchrecord-twitch-streams-using-livestreamer/

# Only works for Streamlink version >= 1.3.0
# Please get the newest version using methods described in https://streamlink.github.io/install.html

# pyinstaller --onefile stream.py

import os
import subprocess
import datetime


class TwitchRecorder:
    def __init__(self):
        # global configuration
        self.client_id = "jzkbprff40iqj646a697cyrvl0zt2m6"  # don't change this

        self.ffmpeg_path = 'ffmpeg'
        self.processed_path = "C:\\Users\\tasoo\\PycharmProjects\\study"

        # user configuration
        self.username = "chick_0318"
        self.quality = "480p"

    def run(self):
        # create directory for recordedPath and processedPath if not exist
        if (os.path.isdir(self.processed_path) is False):  # 만약 설정한 디렉토리가 없으면
            os.makedirs(self.processed_path)               # 만들기

        self.loopcheck()

    def loopcheck(self):
        filename = self.username + " - " + datetime.datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss") + ".mp4"  # 파일이름 생성

        # 불필요한 문자 제거
        filename = "".join(x for x in filename if x.isalnum() or x in [" ", "-", "_", "."])

        recorded_filename = os.path.join(self.processed_path, filename)  # C:\ 등으로 시작하는 절대주소 생성

        # 스팀링크(녹화) 시작
        subprocess.call(
            ["streamlink", "--twitch-disable-hosting", "--twitch-disable-ads", "twitch.tv/" + self.username,
             self.quality, "-o", recorded_filename])

        print("Recording stream is done.")


def main():
    twitch_recorder = TwitchRecorder()

    with open("settings.txt", 'rt') as f:
        twitch_recorder.quality = f.readline()
        twitch_recorder.processed_path = f.readline()
    with open("record.txt", 'rt') as f:
        twitch_recorder.username = f.readline()
    # 여러 정보 파일로부터 입력받음

    print(twitch_recorder.quality)
    print(twitch_recorder.processed_path)
    print(twitch_recorder.username)

    twitch_recorder.run()


if __name__ == "__main__":
    main()
