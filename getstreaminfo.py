import hashlib
import datetime
import time
import os
import requests
import ast

# pyinstaller --onefile getstreaminfo.py
# pyinstaller --onefile --noconole getstreaminfo.py


def check_vod_id(username):
    client_id = "jzkbprff40iqj646a697cyrvl0zt2m6"  # don't change this

    try:
        h = {"Client-ID": client_id, "Accept": "application/vnd.twitchtv.v5+json"}
        r = requests.get(f"https://api.twitch.tv/kraken/users?login={username}", headers=h)  # 트위치 api와 통신하여 유저id받기
        user_id = r.json().get("users", [{}])[0].get("_id", "")

        r = requests.get(f"https://api.twitch.tv/kraken/streams/{user_id}", headers=h, timeout=15)  # 트위치 api와 통신하여 방송정보 받기
        r.raise_for_status()

        r_dict = r.json()
        if r_dict["stream"]:  # 방송중이면
            info = [r_dict["stream"]['_id'], r_dict["stream"]['created_at'], username]  # [vod 고유번호, 방송시작시간, 스트리머id]

        else:  # 방송중이 아니면
            info = []  # 정보없음
    except (KeyboardInterrupt, SystemExit):  # 키보드나 시스템이 프로그램 작동을 막으면
        raise                                # 튕김

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


def tofile(info, txt):
    createFolder(info[1][:7])  # YYYY-MM 이름의 파일 생성
    file = open(f'{info[1][:7]}\\{info[2]}.txt', 'at')  # 파일 내에 (스트리머id).txt 생성
    file.write(txt)  # 받은 문자열 입력
    file.write('\n\n')
    file.close()


def filedate(timestamp, streamer):
    createFolder(timestamp[:7])  # YYYY-MM 이름의 파일 생성
    for username in streamer:    # 각 스트리머 항목마다 이하 작업 수행
        file = open(f'{timestamp[:7]}\\{username}.txt', 'at')  # 파일 내에 (스트리머id).txt 생성
        file.write('\n\n')
        file.write(timestamp[:10])  # 오늘날짜 입력
        file.write('\n\n')
        file.close()  # 파일닫기


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
    f = open('streamers.txt', 'rt')  # 스트리머 목록 입력
    inp = f.read()
    f.close()
    inp = inp.split('\n')  # 엔터 단위로 나눔
    streamer = []
    record = {}

    for i in inp:
        streamer.append(i.split(":")[0])  # : 이전에 있는 스트리머 id만 저장
        record[i.split(":")[0]] = bool(i.split(":")[1])  # : 전후로 나눠서 각 스트리머마다 녹화를 해야하는지 여부 저장

    return streamer, record


def main():
    streamer, record = getstream()  # 스트리머 목록 정보 받음

    prev = {}  # 이전 탐색 결과 저장용
    try:
        t = open("log.txt", 'rt')
        prev = ast.literal_eval(t.read())  # 과거에 탐색을 한 결과가 있으면 가져오기
        t.close()
    except (FileNotFoundError, EOFError):  # 과거에 탐색을 한 결과가 없으면
        for i in streamer:
            prev[i] = []
        filedate(datetime.date.isoformat(datetime.date.today()), streamer)
        prev['time'] = datetime.date.isoformat(datetime.date.today())      # 스트리머별 탐색결과는 없다치고 날짜는 오늘날짜로
    else:  # 과거에 탐색을 한 결과가 있어서 try 부분에서 오류가 없었으면
        for i in streamer:
            if i not in prev:  # 스트리머 목록중에 이전 탐색 결과에 없는 항목이 있으면
                prev[i] = []   # 이전 탐색 결과에 항목 추가

    while True:
        now = time.time()  # 프로세스 시작시간 기록
        print()            # 엔터
        print(time.strftime('%x %X', time.localtime(time.time())))  # 프로세스 시작시간 출력(예 : 02/04/21 09:54:49)

        if prev['time'] != datetime.date.isoformat(datetime.date.today()):  # 마지막으로 저장된 날짜와 현재날짜가 다르면
            print("자정")
            filedate(datetime.date.isoformat(datetime.date.today()), streamer)  # 모든 파일에 날짜 입력

        for i in streamer:  # 각 항목당 한번씩 이하 작업 수행
            print('{:<25}'.format(i), end=' : ')
            info = check_vod_id(i)  # m3u8 제작에 필요한 정보 받아오기
            print(info)
            if info != prev[i] and info:  # 스트리머가 방송을 켰으면 (만약 이전 탐색 결과와 현재 참색 결과가 다르고 현재 탐색 결과에 뭐가 있으면)
                prev[i] = info            # 이전 탐색결과에 현재 탐색결과 복붙
                url = makem3u8(info)      # m3u8 링크 제작
                tofile(info, url)         # 파일에 저장

                response = requests.get(url, timeout=10)  # 만들어진 주소를 기반으로 서버와 통신
                print(response.status_code)
                if response.status_code != 200:  # 통신이 정상적이지 않았으면
                    if record[i]:  # 사용자가 녹화를 허용했으면
                        with open('record.txt', 'wt') as f:
                            f.write(i)  # stream.exe 에 전해주기 위해 녹화할 스트리머 이름 파일에 쓰기
                        os.startfile('stream.exe')  # stream.exe 실행

        prev['time'] = datetime.date.isoformat(datetime.date.today())  # 이전 탐사 결과 목록에 탐사한 시간 추가

        t = open("log.txt", 'wt')
        t.write(str(prev))  # 나중에 프로그램이 꺼졌을 경우에 대비해 이전 탐사 목록 저장
        t.close()

        streamer, record = getstream()  # 파일 변경에 대응해기 위해 스트리머 항목 다시 불러오기

        for i in streamer:
            if i not in prev:  # 파일이 바뀌었으면
                prev[i] = []   # 항목 추가

        try:
            time.sleep(300 + now - time.time())  # 프로세스 시작시간을 기준으로 5분후까지 프로그램 멈추기
        except ValueError:                       # 만약 시간이 너무 오래 걸렸으면
            pass                                 # 넘기고 바로 다시 시작

        tofile(info, '이 m3u8 주소는 작동하지 않을 수 있습니다. 오류코드 : ' + str(response.status_code))  # 파일 입력


if __name__ == "__main__":
    main()

