import requests
import hashlib
import datetime
import time
import os
import requests
import ast
import subprocess

# pyinstaller --onefile getstreaminfo.py
# pyinstaller --onefile --noconole getstreaminfo.py


def check_vod_id(username):
    client_id = "jzkbprff40iqj646a697cyrvl0zt2m6"  # don't change this
    url = 'https://api.twitch.tv/kraken/channels/' + username
    info = None

    try:
        h = {"Client-ID": client_id, "Accept": "application/vnd.twitchtv.v5+json"}
        r = requests.get(f"https://api.twitch.tv/kraken/users?login={username}", headers=h)
        user_id = r.json().get("users", [{}])[0].get("_id", "")

        r = requests.get(f"https://api.twitch.tv/kraken/streams/{user_id}", headers=h, timeout=15)
        r.raise_for_status()

        r_dict = r.json()
        if r_dict["stream"]:
            info = [r_dict["stream"]['_id'], r_dict["stream"]['created_at'], username]

        else:
            info = []
    # except requests.exceptions.RequestException as e:
    except (KeyboardInterrupt, SystemExit):  # temporary workaround for all kinds of possible exceptions, notably JSONDecodeError
        raise

    return info


def makem3u8(info):

    year = int(info[1][:4])
    month = int(info[1][5:7])
    day = int(info[1][8:10])
    # 날짜 입력한거 분해하기

    hour = int(info[1][11:13])
    minute = int(info[1][14:16])
    seconds = int(info[1][17:19])
    # 시간 입력한거 분해하기

    td = datetime.datetime(year, month, day, hour, minute, seconds)
    converted_timestamp = totimestamp(td)  # 시간부분 번역

    formattedstring = info[2] + "_" + str(info[0]) + "_" + str(int(converted_timestamp))  # 해쉬구하기용 합치기

    hash = str(hashlib.sha1(formattedstring.encode('utf-8')).hexdigest())
    requiredhash = hash[:20]  # 해쉬구하기

    finalformattedstring = requiredhash + '_' + formattedstring  # 해쉬까지 합치기

    url = f"https://vod-secure.twitch.tv/{finalformattedstring}/chunked/index-dvr.m3u8"  # m3u8 주소에 끼워넣기

    return url


def tofile(info, url):
    createFolder(info[1][:7])
    file = open(f'{info[1][:7]}\\{info[2]}.txt', 'at')
    file.write(url)
    file.write('\n\n')
    file.close()


def filedate(timestamp, streamer):
    createFolder(timestamp[:7])
    for username in streamer:
        file = open(f'{timestamp[:7]}\\{username}.txt', 'at')
        file.write('\n\n')
        file.write(timestamp[:10])
        file.write('\n\n')
        file.close()


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        return -1
        # print('Error: Creating directory. ' + directory)


def totimestamp(dt, epoch=datetime.datetime(1970, 1, 1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6


def getstream():
    f = open('streamers.txt', 'rt')
    inp = f.read()
    f.close()
    inp = inp.split('\n')
    streamer = []
    record = {}

    for i in inp:
        streamer.append(i.split(":")[0])
        record[i.split(":")[0]] = bool(i.split(":")[1])

    return streamer, record


def main():
    streamer, record = getstream()

    prev = {}

    try:
        t = open("log.txt", 'rt')
        prev = ast.literal_eval(t.read())
        t.close()
    except (FileNotFoundError, EOFError):
        for i in streamer:
            prev[i] = []
        filedate(datetime.date.isoformat(datetime.date.today()), streamer)
        prev['time'] = datetime.date.isoformat(datetime.date.today())

    while True:
        now = time.time()
        print()
        print(time.strftime('%x %X', time.localtime(time.time())))

        for i in streamer:
            if streamer == '':
                continue

            print(i, end=' : ')
            info = check_vod_id(i)
            print(info)
            if info != prev[i] and info:
                prev[i] = info
                url = makem3u8(info)
                tofile(info, url)

                response = requests.get(url)
                print(response.status_code)
                print(response.reason)
                if response.status_code != 200 and record[i]:
                    with open('record.txt', 'wt') as f:
                        f.write(i)
                    os.startfile('stream.exe')

        if prev['time'] != datetime.date.isoformat(datetime.date.today()):
            print("자정")
            filedate(datetime.date.isoformat(datetime.date.today()), streamer)

        prev['time'] = datetime.date.isoformat(datetime.date.today())

        t = open("log.txt", 'wt')
        t.write(str(prev))
        t.close()

        streamer, record = getstream()

        try:
            time.sleep(600 + now - time.time())
        except ValueError:
            pass


if __name__ == "__main__":
    main()

