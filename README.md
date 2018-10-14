# ffmpeg python Gtk GUI 

This is a GUI i made to encode video files with ease, to use this just do the following.

1. open terminal and clone repository

	```bash

	git clone https://github.com/BradHeff/ffmpeg-GUI.git && cd ffmpeg-GUI

	```

2. then run the ffmpegGUI.py

	```bash

	python3 ffmpegGUI.py

	```

ALTERNATIVELY
------

you can make the script executable and symlink it to your **_/usr/bin_** or **_/usr/local/bin_**.

1. make the script executable

	```bash 
	
	chmod +x ffmpegGUI.py
	
	```

2. symlink the script

	* replace **_USER_** with your username

	* replace **_DIR_** with the directory were you cloned your ffmpeg-GUI repository

	```bash

	sudo ln -s /home/_USER_/_DIR_/ffmpeg-GUI/ffmpegGUI.py /usr/bin/ffmpegGUI

	```

3. now you can execute the script with the following

	```bash

	ffmpegGUI.py

	```

