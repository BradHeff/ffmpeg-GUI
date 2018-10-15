# ffmpeg python Gtk GUI 

![screenshot](https://github.com/BradHeff/ffmpeg-GUI/blob/master/image.png)

![screenshot](https://github.com/BradHeff/ffmpeg-GUI/blob/master/image2.png)

This is a GUI i made to encode video files with ease, to use this just do the following.

NOTE:
----

Tested solely on URxvt. options for other terminals have been taken from online man pages and not tested. all execution commands use the option _-e_. 

Any feedback is appreciated.

Dependencies
----
* python3
* GTK+ 3
* [PyGObject](https://pygobject.readthedocs.io/en/latest/)


Installation:
---

1. open terminal and clone repository

	```bash

	> git clone https://github.com/BradHeff/ffmpeg-GUI.git && cd ffmpeg-GUI

	```

2. then run the ffmpegGUI.py

	```bash

	> python3 ffmpegGUI.py

	```


Alternative Installation
------

1. open terminal and clone repository

	```bash

	> git clone https://github.com/BradHeff/ffmpeg-GUI.git && cd ffmpeg-GUI

	```

2. make the script executable

	```bash 

	> chmod +x ffmpegGUI.py

	```


3. now you can run the script from within its directory with the following

	```bash
	
	> ./ffmpegGUI.py
	
	```
	

Optional:
---

symlink it to your **_/usr/bin_** or **_/usr/local/bin_**

1. symlink the script

	* replace **_USER_** with your username

	* replace **_DIR_** with the directory were you cloned your ffmpeg-GUI repository

	```bash

	> sudo ln -s /home/_USER_/_DIR_/ffmpeg-GUI/ffmpegGUI.py /usr/bin/ffmpegGUI

	```

2. now you can execute the script with the following from rofi, dmenu or anywere in terminal.

	```bash

	> ffmpegGUI

	```

