# ffmpeg-GUI
ffmpeg python Gtk GUI 
------

This is a GUI i made to encode x264 video files with ease, to use this just run the following.

1. open terminal in .py directory

2. the run the .py file with python

```bash

python3 ffmpegGUI.py

```

Alt-ALTERNATIVLY
------

you can make the script executable.

1. open terminal in .py directory and execute the following

	```bash 
	
	chmod +x ffmpegGUI.py
	
	```

2. now you can execute the script with the following

```bash

./ffmpegGUI.py

```

now you can symlink the script to run from termimal anywhere or rofi

1. replace **_USER_** with your username

2. replace **_DIR_** with the directoy(s) were you cloned your ffmpeg-GUI repository

```bash

sudo ln -s /home/_USER_/_DIR_/ffmpeg-GUI/ffmpegGUI.py /usr/bin/ffmpegGUI

```
