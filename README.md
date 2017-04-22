# twitch_recorder
Project for recording twitch.tv streams

This project was created in order to streamline the recording of Twitch.tv streams.
To do so I have added the following features.

 * Raw recordings can be divided into configurable-length (hour-long by default) segments via `split_twitch_videos`
 * The entire project can be run on a standalone vagrant box.
 * Vagrant will install an isolated server with the required libraries. From there all you have to do is run the recorder. (directions below)

# Configuration

* Twitch recorder will run in its own _workspace directory_, which is by default `${HOME}/twitch_recorder`/a `twitch_recorder` directory in this directory, if you're running it through vagrant
* **Usernames**: Place the twitch usernames for the streams you wish to record in the _workspace directory_ in a file `twitch_usernames.txt`. Each username belongs on a separate line.
* The setup configuration file is `twitch_recorder.conf`, feel free to experiment/update the settings according to your needs. However, there are a few required settings (see below) you have to set.
* Client ID: Create a twitch ClientID.
 * Follow these directions https://blog.twitch.tv/client-id-required-for-kraken-api-calls-afbb8e95f843
 * Modify `twitch_recorder.conf`, in the line starting with `CLIENT_ID=` replace `your_client_id_here` with your Client ID
* OAuth Token: You will also need an OAuth token.
 * A token can be retrieved from http://www.twitchapps.com/tmi/ .
 * Modify  `twitch_recorder.conf`, in the line starting with `OAUTH_TOKEN` replace `your_oauth_token_here` with the key (do not include the oauth part).


# Running the scripts

## Recording streams
In order to record streams simply execute the following bash script from the project folder `./bin/record_twitch` (or anywhere if installed/running through vagrant)

## Splitting long recordings
To divide long recordings into hour-long segments run the following bash script from the project folder `./bin/split_twitch_videos` (or anywhere if installed/running through vagrant)

# Vagrant
https://www.vagrantup.com/docs/getting-started/

The entire project can be run from a standalone vagrant virtual box server. The purpose of this was for portability and ease of use. Vagrant allows anyone to run this code regardless of operating system or existing system configurations. Furthermore since this can be run from any machine with vagrant and VirtualBox installed, users can create and destroy twitch-recorder instances as they see fit.

1. Install VirtualBox
1. Install Vagrant
2. From the project directory run the following command `vagrant up`. This will build a CentOS 7 server with the required python and livestreamer libraries
3. Log into the Vagrant machine. Run `vagrant ssh`
4. Navigate to the project within the vagrant machine. `cd /vagrant`
5. From this point you may now run either of the scripts mentioned above. ( `record_twitch` and `split_twitch_videos` )

Alternatively, you can just run:
- `vagrant provision --provision-with record` - To start recording in the background
- `vagrant provision --provision-with split` - To start splitting in the background

# Installation on your computer (optional/experimental)

If you want to install the application on your computer, just run `install.sh`.
If you install twitch recorder as a regular user it will be installed to `${HOME}/twitch_recorder`.
If you install twitch recorder as root, it will be installed to `/opt/twitch_recorder`
However, you'll need to manually install `Python` (3.4), `pip`, and `ffmpeg` to make the twitch recorder work.

# Planned updates
1. Optimize Vagrant deployment.

# Handling the problem with O-Auth
if you get an error that prevents you from accessing streams. Try this (it worked for me)...

 * Step 1. (in terminal/cli) Type `livestreamer --twitch-oauth-authenticate`.
 * Step 2. Copy the response url into Chrome. It will open and ask you to login to twitch. It will give you a "page does not exist" error. FeelsBadMan
 * Step 3. Check the url. It has a section that says `access_token=xxxxxxxxxxxxxxxxxxxxxxxx`. Copy this string.
 * Step 4. Use this as your `OAUTH_TOKEN` in `twitch_recorder.conf`

Source: https://www.reddit.com/r/Twitch/comments/52sye3/livestreamer_help_please_help/d7n0j36/?st=iyz5xqc2&sh=0f192548

# Credits and thanks
The initial stream recording code came from Avernus on Pastebin http://pastebin.com/2w1wT18d

Script was made possible again by /u/TheOnlyLeo's & /u/DallasNChains' input.

S/O to JEGGOTT for the original pastebin at http://pastebin.com/BwzP6ayG.

# License
This is free software, and is released under the terms of the **GNU General Public License** version 3.
See: LICENSE
