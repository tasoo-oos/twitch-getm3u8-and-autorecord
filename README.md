# no more maintenance
# 유지보수 안함



# twitch-getm3u8-and-autorecord
This program will give you m3u8 adress of vods or record the stream if adress is not available. 

Do not attempt to harm the streamer with this program or use it for illegal purposes.

### for the people having trouble using this program

download following files


getstreamerinfo.exe

stream.exe

streamers.txt

settings.txt 


and put those in single folder.

## how to get m3u8 adress with getstreaminfo

To make this program work properly, you must have at least one file called streamers.txt.
You can use the streamers.txt file I uploaded, but if you want to make or modify one yourself, please read this description below.

![Alt text](https://i.imgur.com/j1i1ZEg.png)

1. enter the id of the streamer you want to get the m3u8,
2. enter colon(:)
3. Depending on whether you want to auto-record the streamer's broadcast, enter True or False ( if there is no True in file, autorecord feature is disabled )
4. press enter once

However, you must not press enter like below if you don't have a streamer to write more, or program will crash.

![Alt text](https://i.imgur.com/mImLmwh.png)

m3u8 link will be saved in yyyy-mm \ streamerid.txt
and log.txt will appear to save last stream status and to prevent overlapping m3u8 address in file

you can edit streamers.txt while program is running.
The program receives a list of streamers from the file and checks each broadcast every 5 minutes.

## how to automatically record streams with stream

if you want to use this feature, you need to download https://streamlink.github.io/ with latest version.

and you also need to get settings.txt

you need to enter quality settings in first row, and directory you want to save recorded vods in second row.
third row should not exist or else program will crash.
also modifying settings.txt during stream.exe or stream.py is running is not recommended ( not tested ).

available quality options(not always) : audio_only, 160p (worst), 360p, 480p, 720p, 720p60, 1080p60 (best)

sometimes there are streams which has much narrow video quality settings.
if stream does not support quality option you want to record, stream will be recorded with best quality.

multi-recording did go well in my case.

When the program detects that the broadcast is started, the program creates an m3u8 address and uses the requests module to verify that the server has a video file corresponding to the m3u8 address.

if communicaion did not go well ( status code is not 200 ( usually 403 )), record starts

you can manually stop recording 


this program has only tested in windows.


## reference

This program was referenced by the following link.

https://github.com/siddhantdubey/getdeletedtwitchvods

https://www.godo.dev/tutorials/python-record-twitch/
