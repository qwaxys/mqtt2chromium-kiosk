# mqtt2chromium-kiosk

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



