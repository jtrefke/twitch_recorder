# twitch_recorder
Project for recording twitch.tv streams

This project was created in order to streamline the recording of Twitch.tv streams.
To do so I have added the following features.

 * Raw recordings can be divided into hour-long segments via `split_files.sh`
 * The entire project can be run on a standalone Vagrant box.
 * Vagrant will install an isolated server with the required libraries. From there all you have to do is run the recorder. (directions below)

# Configuration

* Usernames: Place the twitch usernames for the streams you wish to record in `usernames.txt`. Each username belongs on a separate line.
* Client ID: Create a twitch ClientID.
 * Follow these directions https://blog.twitch.tv/client-id-required-for-kraken-api-calls-afbb8e95f843
 * Modify `record.py` line #95 `clientId` by replacing `xxxxxxxxxxx...` with your Client ID
* OAuth Token: You will also need an OAuth token.
 * A token can be retrieved from http://www.twitchapps.com/tmi/ .
 * Modify `record.py` line #96 `oauthToken` by replacing `xxxxxxxxxxx...` with the key (do not include the oauth part).

# Running the scripts
Recording streams: In order to record streams simply execute the following bash command from the project folder `/bin/bash record_twitch.sh`
Splitting long recordings: To divide long recordings into hour-long segments run the following bash command from the project folder `/bin/bash split_files.sh`

# Vagrant
https://www.vagrantup.com/docs/getting-started/

The entire project can be run from a standalone vagrant server. The purpose of this was for portability and ease of use. Vagrant allows anyone to run this code regardless of operating system or existing system configurations. Furthermore since this can be run from any machine with vagrant installed, users can create and destroy twitch-recorder instances as they see fit.

1. Install Vagrant
2. From the project directory run the following command `vagrant up`. This will build a Centos7 server with the required python and livestreamer libraries
3. Log into the Vagrant machine. Run `vagrant ssh`
4. Navigate to the project within the vagrant machine. `cd /vagrant`
5. From this point you may now run either of the scripts mentioned above. ( `record_twitch.sh` and `split_files.sh` )

# Planned updates
1. Move Client ID, and OAuth Token into a configuration file.
2. Optimize Vagrant deployment.

# Handling the problem with O-Auth
if you get an error that pervents you from accessing streams. Try this (it worked for me)... 

 * Step 1. (in terminal/cli) Type `livestreamer --twitch-oauth-authenticate`.
 * Step 2 copy the response url into Chrome will open and ask you to login to twitch. It will give you a "page does not exist" error. FeelsBadMan
 * Step 3. Check the url. It has a section that says `access_token=xxxxxxxxxxxxxxxxxxxxxxxx`. Copy this string.
 * Step 4: use this as your oauthToken in record.py

Source: https://www.reddit.com/r/Twitch/comments/52sye3/livestreamer_help_please_help/d7n0j36/?st=iyz5xqc2&sh=0f192548

# Credits and thanks
The initial stream recording code came from Avernus on Pastebin http://pastebin.com/2w1wT18d

Script was made possible again by /u/TheOnlyLeo's & /u/DallasNChains' input.

S/O to JEGGOTT for the original pastebin at http://pastebin.com/BwzP6ayG.

# License
This is free software, and is released under the terms of the **GNU General Public License** version 3.
See: LICENSE
