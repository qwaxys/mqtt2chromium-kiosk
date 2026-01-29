# mqtt2chromium-kiosk

## Why?
This project is made to reduce ewaste: it's aim is to reuse the stack of old Banana Pi M1's that FOSDEM donated to Hackerspace Brussels. It *should* also just work on Rasberry Pi's and other armbian/raspbian/debian like systems. (to be tested)

One service is responsible for (re)starting chromium fullscreen in kiosk mode with the remote debugging enabled.

The other service is resposible for (re)starting a python script.

The python script will use MQTT to take URL(s) and open them in chromium via the remote debugging protocol.

## How to use

Either send a single **URL**:
```
{"url":"https://hackerspace.gent"}
```
Or send multiple with a **delay** in seconds between rotation and indicate if you want it to keep **loop**ing.
```
{"url":["https://bytenight.brussels/", "https://hsbxl.be/events/byteweek/2026/bytenight/", "https://we.voidwarranties.be/DOS"], "delay": 20, "loop":1}
```


Note that the Pi's aren't as powerfull as you hope so stick to simpler webpages without video.

## Todo

remove any hard links.
Use virtual enviroment or package pychrome. (paho-mqtt already exists as a package)
Make an install script or package this mess.

## How to install

Write [Armbian_23.08.0-trunk_Bananapi_bookworm_current_6.1.37_xfce_desktop.img](https://drive.google.com/file/d/1jjDfkKM7ALygaZ1p4toLcjfzhQf-jSZS/view?usp=drive_link) to SD card (link via [official docs](https://docs.banana-pi.org/en/BPI-M1/BananaPi_BPI-M1))

Go through setup

I used en_IE.UTF-8 and Timezone Europe/Brussels

You should now be logged into the desktop.

Go to Applications -> Settings -> Power Manager

On the tab Display, set everything to Never.
```
sudo nano /etc/lightdm/lightdm.conf
```
Find 
```
#autologin-user=
#autologin-user-timeout=0
```
Uncomment both and set it to your username.
```
sudo apt update
sudo apt install chromium python3-pip netcat-traditional

sudo pip install pychrome  --break-system-packages
sudo pip install paho-mqtt --break-system-packages

```

Get this project in your home directory with git clone / wget or any other way.




