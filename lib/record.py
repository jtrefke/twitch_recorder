#This script checks if a user on twitch is currently streaming and then records the stream via livestreamer

from urllib.request import urlopen
from urllib.error import URLError
from threading import Timer
import time
import json
import sys
import subprocess
import datetime
from datetime import datetime

def check_user(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    global info
    url = 'https://api.twitch.tv/kraken/streams/' + user + '?client_id=' + clientId
    print (url)
    try:
        info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))
        print ('running: ')
        if info['stream'] == None:
            status = 1
        else:
            status = 0
    except URLError as e:
        if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
            status = 2
        else:
            status = 3
    return status

def format_filename(fname):
# Removes invalid characters from filename
    fname = fname.replace("/","")
    fname = fname.replace("?","")
    fname = fname.replace(":","-")
    fname = fname.replace("\\","")
    fname = fname.replace("<","")
    fname = fname.replace(">","")
    fname = fname.replace("*","")
    fname = fname.replace("\"","")
    fname = fname.replace("|","")
    return fname

def update_timestamp(timestamp, duration):
# takes a timestamp and a duration (seconds), returns new timestamp once duration is passed
# used to set length of files
  if(time.time() > timestamp + duration):
    return time.time()
  else:
    return timestamp

def format_timestamp(unixtime, format):
  return (datetime.fromtimestamp(int(unixtime)).strftime(format))

def loopcheck():
    timestamp = time.time()
    while True:
        status = check_user(user)
        if status == 2:
            print("username not found. invalid username?")
        elif status == 3:
            print(datetime.now().strftime("%Hh%Mm%Ss")," ","unexpected error. will try again in 5 minutes.")
            time.sleep(300)
        elif status == 1:
            print(user,"currently offline, checking again in",refresh,"seconds")
            time.sleep(refresh)
        elif status == 0:
            print(user,"online. stop.")
            timestamp = update_timestamp(timestamp, duration)
            formatted_timestamp = format_timestamp(timestamp, "%m_%d_%Y_%H_%M_%S")
            filename = user+" - "+ formatted_timestamp +" - "+(info['stream']).get("channel").get("status")+".mp4"
            filename = format_filename(filename)
            subprocess.call(["livestreamer", "--twitch-oauth-token="+oauthToken, "twitch.tv/"+user,quality,"-o",directory+filename])
            print("Stream is done. Going back to checking..")
            time.sleep(15)

def main(argRefresh, argUsername, argQuality, argDirectory, argClientId, argOauthToken):
    global refresh
    global user
    global quality
    global directory
    global duration
    global clientId
    global oauthToken

    refresh = float(argRefresh) # time in s
    user = argUsername
    quality = argQuality # best, high, medium, low, mobile
    directory = argDirectory
    duration = 240 # length of movie. seconds to minutes. 3600 = 60 minutes, 3000 = 50,  2700 = 45
    clientId = argClientId # unique to this app ( https://blog.twitch.tv/client-id-required-for-kraken-api-calls-afbb8e95f843 )
    oauthToken = argOauthToken # twitch token needs to be retrieved from http://www.twitchapps.com/tmi/ . Copy only the key and not the oauth part, and replace the xxxxxxxxx portion above.

    print("refresh=",refresh,", user=",user,", quality=",quality,", directory=",directory,", duration=",duration,", clientId=",clientId,", oauthToken=",oauthToken)
    sys.exit(13)

    if(refresh<15):
        print("Check refresh interval should not be lower than 15 seconds")
        refresh=15

    print("Checking for",user,"every",refresh,"seconds. Record with",quality,"quality.")
    loopcheck()


if __name__ == "__main__":
    # execute only if run as a script
    if len(sys.argv[1:]) != 6:
        print("Invalid arguments: ", ' '.join(sys.argv[1:]),"\n")
        print("Usage: record.py [refresh] [username] [quality] [directory] [clientid] [oauthtoken]")
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
